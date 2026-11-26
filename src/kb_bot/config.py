"""环境变量配置。所有密钥只从环境读取，不落盘。"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_KB_ROOT = REPO_ROOT / "docs" / "knowledge" / "ad-agent-qa"


@dataclass(frozen=True)
class Settings:
    lark_app_id: str
    lark_app_secret: str
    llm_base_url: str
    llm_api_key: str
    llm_model: str
    kb_root: Path
    retrieve_top_k: int = 5
    llm_timeout: float = 60.0
    max_answer_chars: int = 1200


def load_settings(require_lark: bool = True) -> Settings:
    required = ["LLM_API_KEY"] + (["LARK_APP_ID", "LARK_APP_SECRET"] if require_lark else [])
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise SystemExit(f"缺少环境变量: {', '.join(missing)}（见 .env.example）")
    return Settings(
        lark_app_id=os.environ.get("LARK_APP_ID", ""),
        lark_app_secret=os.environ.get("LARK_APP_SECRET", ""),
        llm_base_url=os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/"),
        llm_api_key=os.environ["LLM_API_KEY"],
        llm_model=os.environ.get("LLM_MODEL", "gpt-4o-mini"),
        kb_root=Path(os.environ.get("KB_ROOT", str(DEFAULT_KB_ROOT))),
        retrieve_top_k=int(os.environ.get("RETRIEVE_TOP_K", "5")),
        llm_timeout=float(os.environ.get("LLM_TIMEOUT", "60")),
        max_answer_chars=int(os.environ.get("MAX_ANSWER_CHARS", "1200")),
    )
