#!/bin/bash
# Token Saver 安装脚本

SKILL_DIR="$HOME/.workbuddy/skills/token-saver"
SCRIPT_PATH="$SKILL_DIR/scripts/token-saver.py"
BIN_PATH="/usr/local/bin/token-saver"

echo "🚀 安装 Token Saver..."

# 检查 Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python 3，请先安装"
    exit 1
fi

# 创建符号链接
echo "📦 创建命令链接..."
sudo ln -sf "$SCRIPT_PATH" "$BIN_PATH"
sudo chmod +x "$BIN_PATH"

# 创建配置目录
mkdir -p "$HOME/.token-saver"

# 测试
echo "✅ 安装完成！"
echo ""
echo "使用方法:"
echo "  token-saver \"你的文本\"        # 压缩文本"
echo "  token-saver --enable           # 开启节省模式"
echo "  token-saver --disable          # 关闭节省模式"
echo "  token-saver --status           # 查看状态"
echo "  token-saver --history          # 查看历史"
echo ""
echo "立即测试:"
token-saver --status
