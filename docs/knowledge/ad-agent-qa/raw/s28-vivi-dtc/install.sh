#!/usr/bin/env bash
# 把 AI 跨境地圖診斷 Skill 安裝到 Codex 或 Claude Code。
#
# 用法：
#   bash install.sh          # 自動偵測已安裝的工具，裝進去
#   bash install.sh codex    # 只裝 Codex
#   bash install.sh claude   # 只裝 Claude Code
#
# 這個腳本只複製檔案到你自己的家目錄，不會連外、不會改動其他設定。

set -euo pipefail

SKILL_NAME="goaskvivi-dtc-diagnostic"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

CODEX_DIR="${CODEX_HOME:-$HOME/.codex}/skills/$SKILL_NAME"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/$SKILL_NAME"

target="${1:-auto}"
case "$target" in
  auto|codex|claude) ;;
  *)
    # 變數一律用 ${} 包起來：後面接全形標點時，bash 3.2（macOS 內建）會把
    # 全形字的位元組當成變數名的一部分，$target（ 會被讀成變數「target（」→ unbound。
    echo "✗ 不認得的參數：${target}（可用：codex、claude，或不帶參數自動偵測）" >&2
    exit 1
    ;;
esac

# 先確認來源完整，再動任何目的地檔案。
# 順序很重要：安裝是「先刪舊版再複製」，來源缺一份就中止的話，
# 使用者原本能用的舊版已經被刪掉了。所以檢查一律放在最前面。
[ -f "$SRC/SKILL.md" ] || { echo "✗ 來源不完整，缺少 SKILL.md。請在技能包資料夾裡執行。" >&2; exit 1; }
for required in references references-zh-tw; do
  [ -d "$SRC/$required" ] || { echo "✗ 來源不完整，缺少 $required/ 目錄。請在技能包資料夾裡執行。" >&2; exit 1; }
done

install_to() {
  local label="$1" dest="$2"

  # 這個函式會 rm -rf，所以動手前先確認 dest 真的是我們要裝的技能目錄，
  # 不是空字串或被環境變數改成別的路徑（例如 CODEX_HOME 設錯）。
  case "$dest" in
    */"$SKILL_NAME") ;;
    *)
      echo "✗ 安裝路徑不合法，已中止：$dest" >&2
      return 1
      ;;
  esac

  # 來源與目的地是同一個資料夾時直接跳過，否則會把來源本身刪掉。
  # 使用者手動把整包複製進 skills/ 之後再跑這個腳本，就會走到這條。
  # 用 -ef 比對 inode，符號連結或結尾多一條斜線都能正確判斷（字串比對不行）。
  if [ -d "$dest" ] && [ "$dest" -ef "$SRC" ]; then
    echo "→ $label 已經就是這個資料夾，略過複製：$dest"
    echo "  ✓ 完成"
    return 0
  fi

  echo "→ 安裝到 ${label}：${dest}"

  # 先把完整的一份組在暫存資料夾，成功了才換掉舊版。
  # 這樣即使中途失敗，使用者原本的舊版仍然完好，不會留下裝到一半的殘骸。
  local stage="${dest}.tmp.$$"
  rm -rf "$stage"
  # 用單引號延後展開：trap 在函式返回時才跑，那時 $stage 這個 local 仍在作用域內。
  # （若改成現在展開，路徑含單引號會讓 trap 內容變成語法錯誤。）
  trap 'rm -rf "$stage"' RETURN

  mkdir -p "$stage"
  cp "$SRC/SKILL.md" "$stage/"
  cp -R "$SRC/references" "$SRC/references-zh-tw" "$stage/"
  if [ -d "$SRC/assets" ]; then
    cp -R "$SRC/assets" "$stage/"
  fi

  mkdir -p "$(dirname "$dest")"
  rm -rf "$dest"
  mv "$stage" "$dest"
  echo "  ✓ 完成"
}

installed=0

# 自動模式只裝「家目錄看得到設定資料夾」的工具；
# 明確指定 codex/claude 時一律安裝，不做偵測。
if [ "$target" = "codex" ] || { [ "$target" = "auto" ] && [ -d "${CODEX_HOME:-$HOME/.codex}" ]; }; then
  install_to "Codex" "$CODEX_DIR"
  installed=$((installed + 1))
fi

if [ "$target" = "claude" ] || { [ "$target" = "auto" ] && [ -d "${CLAUDE_CONFIG_DIR:-$HOME/.claude}" ]; }; then
  install_to "Claude Code" "$CLAUDE_DIR"
  installed=$((installed + 1))
fi

if [ "$installed" -eq 0 ]; then
  cat >&2 <<'EOF'
✗ 沒有偵測到 Codex 或 Claude Code。

如果你確定有裝，請直接指定：
  bash install.sh codex
  bash install.sh claude

如果你用的是 ChatGPT / Claude 網頁版，不需要安裝——
請看 README.md 的「方法 2」或「方法 3」。
EOF
  exit 1
fi

cat <<'EOF'

安裝完成。請重開你的 AI 工具，然後輸入這句話：

  幫我做跨境出海診斷

它會反問你品牌資料，然後產出診斷報告。
EOF
