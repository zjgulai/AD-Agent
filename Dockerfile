# KB Workbench — ad-agent-qa 知识工作台
# 构建: docker build --platform linux/amd64 -t kb-workbench:TAG .
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src \
    KB_ROOT=/app/docs/knowledge/ad-agent-qa \
    STAGING_DIR=/data/staging \
    PORT=8000

WORKDIR /app

# 处理器依赖均为纯 Python wheel，slim 基础镜像足够；不装 curl（healthcheck 用 python）
# 服务器在国内，pypi.org 不可达 → 默认清华镜像，可用 --build-arg 覆盖
ARG PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
COPY requirements.txt .
RUN pip install --no-cache-dir -i "$PIP_INDEX_URL" -r requirements.txt

COPY src/ ./src/
COPY docs/knowledge/ad-agent-qa/ ./docs/knowledge/ad-agent-qa/

# graph/dist 是 gitignored 产物，镜像构建期生成（networkx Louvain 社区检测）
RUN python -m kb_ops graph-export

RUN useradd -r -u 10001 -m kb \
    && mkdir -p /data/staging \
    && chown -R kb:kb /data /app
USER kb

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request,sys;sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/api/health',timeout=4).status==200 else 1)"

CMD ["python", "-m", "kb_ops.web", "--host", "0.0.0.0", "--port", "8000"]
