"""FastAPI 工作台：GET-only 只读 API + 静态 SPA。

启动：python -m kb_ops.web [--port 8000]
或：  uvicorn 'kb_ops.web.app:create_app()' --factory
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles

from ..paths import kb_root as default_kb_root
from . import service

STATIC_DIR = Path(__file__).resolve().parents[1] / "static"


def create_app(kb_root: str | Path | None = None) -> FastAPI:
    root = Path(kb_root) if kb_root else default_kb_root()
    app = FastAPI(title="ad-agent-qa KB Workbench", version="0.1.0")
    app.state.kb_root = root

    @app.get("/api/stats")
    def api_stats() -> dict:
        return service.stats(root)

    @app.get("/api/cards")
    def api_cards(cluster: str | None = None) -> dict:
        cards = service.list_cards(root)
        if cluster:
            cards = [c for c in cards if c["cluster"] == cluster]
        return {"cards": cards}

    @app.get("/api/cards/{cluster}/{name}")
    def api_card(cluster: str, name: str) -> dict:
        try:
            return service.get_card(root, cluster, name)
        except (FileNotFoundError, ValueError):
            raise HTTPException(404, "card not found")

    @app.get("/api/qa")
    def api_qa() -> dict:
        return {"files": service.list_qa(root)}

    @app.get("/api/qa/{cluster}")
    def api_qa_cluster(cluster: str) -> dict:
        try:
            return service.get_qa(root, cluster)
        except (FileNotFoundError, ValueError):
            raise HTTPException(404, "qa file not found")

    @app.get("/api/graph")
    def api_graph(rebuild: bool = False) -> dict:
        try:
            return service.get_graph(root, rebuild=rebuild)
        except FileNotFoundError:
            raise HTTPException(503, "graph not built")

    @app.get("/api/search")
    def api_search(q: str = Query(min_length=1, max_length=500),
                   k: int = Query(default=8, ge=1, le=50)) -> dict:
        return {"query": q, "results": service.search(root, q, k)}

    @app.get("/api/health")
    def api_health(refresh: bool = False) -> dict:
        return service.health(root, refresh=refresh)

    @app.get("/api/doc/{name}")
    def api_doc(name: str) -> dict:
        try:
            return {"name": name, "markdown": service.get_doc(root, name)}
        except FileNotFoundError:
            raise HTTPException(404, "doc not found")

    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
    return app
