#!/usr/bin/env bash
# KB Workbench 部署脚本：git archive HEAD → 传服务器 → 服务器侧 docker build → 重启
# 服务器无 git/registry 直连，故采用「源码上下文传输 + 服务器构建」（基座镜像已缓存，
# pip 走清华镜像）。用法: ./deploy/deploy.sh [tag]（默认 git sha + 日期）
# 前置: SSH key 默认 repo 根 key_20261027.pem，可用 KEY/SERVER 覆盖
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SERVER="${SERVER:-root@81.68.192.59}"
KEY="${KEY:-$REPO_ROOT/key_20261027.pem}"
REMOTE_DIR="/opt/kb-workbench"
DATA_DIR="/data/kb-workbench"
TAG="${1:-$(git -C "$REPO_ROOT" rev-parse --short HEAD)-$(date +%Y%m%d)}"
IMAGE="kb-workbench:$TAG"

echo "==> [1/5] 归档 HEAD 源码上下文并传输到 $SERVER:$REMOTE_DIR/build"
ssh -i "$KEY" -o BatchMode=yes "$SERVER" "mkdir -p $REMOTE_DIR/build $DATA_DIR/staging"
git -C "$REPO_ROOT" archive HEAD | ssh -i "$KEY" -o BatchMode=yes "$SERVER" \
  "tar -x -C $REMOTE_DIR/build"

echo "==> [2/5] 服务器侧构建 $IMAGE（python:3.12-slim 已缓存，pip 走 tuna）"
ssh -i "$KEY" -o BatchMode=yes "$SERVER" \
  "cd $REMOTE_DIR/build && docker build -t $IMAGE ."

echo "==> [3/5] compose 配置与启动"
scp -i "$KEY" -o BatchMode=yes "$REPO_ROOT/deploy/compose.yml" "$SERVER:$REMOTE_DIR/compose.yml"
ssh -i "$KEY" -o BatchMode=yes "$SERVER" \
  "cd $REMOTE_DIR && KB_TAG=$TAG docker compose up -d"

echo "==> [4/5] 健康检查"
sleep 3
ssh -i "$KEY" -o BatchMode=yes "$SERVER" \
  "curl -sf http://127.0.0.1:8010/api/health && echo && docker ps --filter name=kb-workbench --format '{{.Status}}'"

echo "==> [5/5] 完成。公网入口: https://ad.sagegogo.com"
echo "    （nginx conf: deploy/nginx-ad.sagegogo.com.conf；首次需装 conf + certbot 签发）"
echo "    回滚: ssh $SERVER 'cd $REMOTE_DIR && KB_TAG=<旧tag> docker compose up -d'"
