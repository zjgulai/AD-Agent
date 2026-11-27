"""kb_ops.ingest 摄入管道测试：多格式提取 + staging 全流程 + API 端点。"""

import io
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from kb_ops import ingest
from kb_ops.processors import process_file, supported_ext
from kb_ops.web.app import create_app


@pytest.fixture()
def staging(tmp_path, monkeypatch):
    d = tmp_path / "staging"
    monkeypatch.setenv("STAGING_DIR", str(d))
    return d


def _docx_bytes() -> bytes:
    from docx import Document
    doc = Document()
    doc.add_paragraph("Momcozy 投放复盘")
    doc.add_paragraph("Meta ROAS 环比下降 20%")
    t = doc.add_table(rows=2, cols=2)
    t.rows[0].cells[0].text = "渠道"
    t.rows[0].cells[1].text = "ROAS"
    t.rows[1].cells[0].text = "Meta"
    t.rows[1].cells[1].text = "2.1"
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


def _xlsx_bytes() -> bytes:
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "日报"
    ws.append(["日期", "消耗", "GMV"])
    ws.append(["2026-11-01", 1200, 5400])
    ws2 = wb.create_sheet("周报")
    ws2.append(["指标", "值"])
    ws2.append(["ROAS", 4.5])
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


class TestSupported:
    @pytest.mark.parametrize("ext", [".txt", ".md", ".csv", ".pdf", ".docx",
                                     ".xlsx", ".pptx", ".html", ".png"])
    def test_supported(self, ext):
        assert supported_ext(ext)

    @pytest.mark.parametrize("ext", [".zip", ".doc", ".mp4", ""])
    def test_unsupported(self, ext):
        assert not supported_ext(ext)


class TestProcessors:
    def test_txt(self, tmp_path):
        p = tmp_path / "a.txt"
        p.write_text("第一行\n第二行", encoding="utf-8")
        doc = process_file(p)
        assert "第一行" in doc.content and doc.metadata["type"] == "txt"
        assert not doc.errors

    def test_csv_to_markdown(self, tmp_path):
        p = tmp_path / "data.csv"
        p.write_text("name,roas\nMeta,2.1\nTikTok,3.0\n", encoding="utf-8")
        doc = process_file(p)
        assert "| name | roas |" in doc.content
        assert "| --- | --- |" in doc.content or "|---|" in doc.content.replace(" ", "")

    def test_docx(self, tmp_path):
        p = tmp_path / "report.docx"
        p.write_bytes(_docx_bytes())
        doc = process_file(p)
        assert "投放复盘" in doc.content
        assert "| 渠道 | ROAS |" in doc.content
        assert doc.metadata["type"] == "docx"

    def test_xlsx(self, tmp_path):
        p = tmp_path / "stats.xlsx"
        p.write_bytes(_xlsx_bytes())
        doc = process_file(p)
        assert "工作表: 日报" in doc.content and "工作表: 周报" in doc.content
        assert "消耗" in doc.content
        assert doc.metadata["sheets"] == 2

    def test_html(self, tmp_path):
        p = tmp_path / "page.html"
        p.write_text(
            "<html><head><title>广告诊断手册</title><style>x{}</style></head>"
            "<body><h1>诊断流程</h1><p>先查 L0 再查 L4。</p>"
            "<table><tr><th>层级</th><th>检查</th></tr>"
            "<tr><td>L0</td><td>EQ/频次</td></tr></table></body></html>",
            encoding="utf-8")
        doc = process_file(p)
        assert "诊断流程" in doc.content
        assert "L0" in doc.content and "| 层级 | 检查 |" in doc.content
        assert doc.metadata["title"] == "广告诊断手册"
        assert "style" not in doc.content

    def test_image_stub(self, tmp_path):
        p = tmp_path / "shot.png"
        p.write_bytes(b"\x89PNG\r\n\x1a\n" + b"0" * 100)
        doc = process_file(p)
        assert doc.content == ""
        assert any("OCR" in e or "ocr" in e.lower() for e in doc.errors)

    def test_garbage_pdf_no_crash(self, tmp_path):
        p = tmp_path / "bad.pdf"
        p.write_bytes(b"not a pdf at all")
        doc = process_file(p)
        assert doc.errors  # 提取异常被兜底成 errors


class TestIngest:
    def test_txt_flow(self, staging):
        item = ingest.ingest_bytes("notes.txt", "Meta ROAS 口径说明".encode())
        assert item["status"] == "extracted"
        assert item["content_chars"] > 0
        assert (staging / "inbox" / f"{item['id']}.txt").is_file()
        assert (staging / "extracted" / f"{item['id']}.md").is_file()
        assert (staging / "extracted" / f"{item['id']}.json").is_file()

    def test_chinese_filename(self, staging):
        item = ingest.ingest_bytes("投放复盘-11月.txt", "内容".encode())
        assert item["id"].startswith("20")  # date prefix
        assert ingest.get_item(item["id"])["filename"] == "投放复盘-11月.txt"

    def test_duplicate_name_gets_suffix(self, staging):
        a = ingest.ingest_bytes("same.txt", b"one")
        b = ingest.ingest_bytes("same.txt", b"two")
        assert a["id"] != b["id"] and b["id"].endswith("-2")

    def test_reject_unsupported_and_empty(self, staging):
        with pytest.raises(ValueError):
            ingest.ingest_bytes("a.zip", b"x")
        with pytest.raises(ValueError):
            ingest.ingest_bytes("a.txt", b"")

    def test_list_get_content(self, staging):
        item = ingest.ingest_bytes("a.md", "# 标题\n正文".encode())
        items = ingest.list_items()
        assert [i["id"] for i in items] == [item["id"]]
        detail = ingest.get_item(item["id"])
        assert detail["has_brief"] is False
        assert "标题" in detail["extracted_preview"]
        md = ingest.get_content(item["id"])
        assert md.startswith("---") and "ingest_id" in md

    def test_status_flow_and_validation(self, staging):
        item = ingest.ingest_bytes("a.txt", b"x")
        with pytest.raises(ValueError):
            ingest.set_status(item["id"], "bogus")
        it = ingest.set_status(item["id"], "distilled")
        assert it["status"] == "distilled"
        assert ingest.get_item(item["id"])["status"] == "distilled"

    def test_invalid_id(self, staging):
        with pytest.raises((ValueError, FileNotFoundError)):
            ingest.get_item("../escape")
        with pytest.raises((ValueError, FileNotFoundError)):
            ingest.get_content("no-such-id")

    def test_generate_brief(self, staging, kb_root):
        item = ingest.ingest_bytes(
            "meta-ads-report.txt",
            "Momcozy Meta 广告 ROAS 下降，CTR 与 CPM 分层分析，归因窗口 7 天点击".encode())
        brief = ingest.generate_brief(item["id"])
        assert "蒸馏简报" in brief and "meta-ads-report.txt" in brief
        assert "BM25" in brief
        it = ingest.get_item(item["id"])
        assert it["status"] == "briefed" and it["has_brief"] is True
        assert "raw/sXX" in ingest.get_brief(item["id"]) or "raw/" in ingest.get_brief(item["id"])

    def test_generate_brief_missing(self, staging):
        with pytest.raises(FileNotFoundError):
            ingest.generate_brief("nonexistent-id-xyz")


class TestIngestAPI:
    @pytest.fixture()
    def client(self, kb_root, staging):
        return TestClient(create_app(kb_root))

    def test_upload_list_detail_content(self, client):
        r = client.post("/api/ingest/upload",
                        files={"file": ("guide.txt", "归因三角测量说明".encode(), "text/plain")})
        assert r.status_code == 200, r.text
        item = r.json()
        assert item["status"] == "extracted"

        r = client.get("/api/ingest")
        assert [i["id"] for i in r.json()["items"]] == [item["id"]]

        r = client.get(f"/api/ingest/{item['id']}")
        assert r.status_code == 200 and "归因" in r.json()["extracted_preview"]

        r = client.get(f"/api/ingest/{item['id']}/content")
        assert "ingest_id" in r.json()["markdown"]

    def test_upload_bad_ext_400(self, client):
        r = client.post("/api/ingest/upload",
                        files={"file": ("x.zip", b"PK", "application/zip")})
        assert r.status_code == 400

    def test_item_404(self, client):
        assert client.get("/api/ingest/nope-404").status_code == 404
        assert client.get("/api/ingest/nope-404/content").status_code == 404
        assert client.get("/api/ingest/nope-404/brief").status_code == 404

    def test_brief_and_status_via_api(self, client):
        r = client.post("/api/ingest/upload",
                        files={"file": ("tiktok-ads.txt", "TikTok 广告 GMV Max 出价策略".encode(), "text/plain")})
        iid = r.json()["id"]
        r = client.post(f"/api/ingest/{iid}/brief")
        assert r.status_code == 200 and "蒸馏简报" in r.json()["brief"]
        r = client.get(f"/api/ingest/{iid}/brief")
        assert "TikTok" in r.json()["brief"]
        r = client.post(f"/api/ingest/{iid}/status", json={"status": "distilled"})
        assert r.json()["status"] == "distilled"
        r = client.post(f"/api/ingest/{iid}/status", json={"status": "bad"})
        assert r.status_code == 400
