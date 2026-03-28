# Token Saver

[![GitHub stars](https://img.shields.io/github/stars/Windymonkeys/token-saver?style=social)](https://github.com/Windymonkeys/token-saver/stargazers)
[![GitHub license](https://img.shields.io/github/license/Windymonkeys/token-saver)](https://github.com/Windymonkeys/token-saver/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/Windymonkeys/token-saver)](https://github.com/Windymonkeys/token-saver/issues)
[![GitHub forks](https://img.shields.io/github/forks/Windymonkeys/token-saver?style=social)](https://github.com/Windymonkeys/token-saver/network/members)

> 🚀 全方位 Token 节省解决方案 - 让你的 AI 对话更高效！

**支持平台**: WorkBuddy | Cursor | Claude | ChatGPT | Poe | Coze | Dify

---

## 📸 效果展示

### 文言文压缩

```
输入: 今天我在使用这个功能的时候发现了一个问题，就是当我点击提交按钮之后，页面没有任何反应
输出: 提交按钮无响应，需排查
节省: 79%
```

### 智能压缩

```
输入: I think that we should probably consider the fact that the system was created by the development team
输出: The system was created by the development team
节省: 43%
```

### 批量处理

```bash
$ token-saver --batch ./docs/

✓ report.md: 节省 42 字 (35%)
✓ api.md: 节省 28 字 (28%)
✓ tutorial.md: 节省 56 字 (51%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
处理完成: 3 个文件，总共节省: 126 字
```

---

## ✨ 核心功能

| 功能 | 说明 | 节省率 |
|------|------|--------|
| 📜 文言文压缩 | 现代汉语 → 简洁文言 | 20-40% |
| 🧠 智能压缩 | 语义权重分析 | 25-80% |
| 🌐 英语压缩 | 去除填充词 | 15-30% |
| 💰 Token 计算 | 多模型成本估算 | - |
| 📦 批量处理 | 文件夹一键压缩 | - |
| 🎨 Prompt 模板 | 30+ 预定义模板 | - |

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/Windymonkeys/token-saver.git

# 安装命令行工具
cd token-saver
bash scripts/install.sh
```

### 使用

```bash
# 压缩文本（自动推荐最佳方式）
token-saver "你的文本"

# 全局开关
token-saver --enable      # 开启节省模式（默认已开启）
token-saver --disable     # 关闭节省模式
token-saver --status      # 查看状态

# 批量处理
token-saver --batch ./docs/

# 查看历史
token-saver --history
```

---

## 🌍 多平台支持

### WorkBuddy

```bash
# 安装到 WorkBuddy
git clone https://github.com/Windymonkeys/token-saver.git
mv token-saver ~/.workbuddy/skills/
```

### Cursor

```bash
# 复制配置文件到项目根目录
cp token-saver/.cursorrules ./
```

### Claude

复制 `claude_prompt.md` 内容到 Claude 设置 > 自定义指令

### ChatGPT

复制 `chatgpt_instructions.md` 内容到 ChatGPT 设置 > 自定义指令

### 其他平台

| 平台 | 使用方式 |
|------|----------|
| **Poe** | 创建 Bot，粘贴 SKILL.md 内容 |
| **Coze** | 创建插件，导入配置 |
| **Dify** | 创建应用，添加技能 |
| **FastGPT** | 导入知识库 |

---

## 📊 效果对比

| 场景 | 原文长度 | 压缩后 | 节省率 |
|------|---------|--------|--------|
| 需求描述 | 62 字 | 45 字 | 27% |
| 问题反馈 | 58 字 | 38 字 | 34% |
| 代码解释 | 46 字 | 28 字 | 39% |
| 英文文档 | 120 词 | 85 词 | 29% |

---

## 📁 项目结构

```
token-saver/
├── scripts/                     # 核心脚本
│   ├── token-saver.py          # 统一入口 ⭐
│   ├── install.sh              # 安装脚本
│   ├── translate.py            # 文言文转换
│   ├── smart_compress.py       # 智能压缩
│   ├── english_compressor.py   # 英语压缩
│   ├── token_counter.py        # Token 计算
│   └── ...
├── references/                  # 资源文件
│   ├── wenyan_mapping.json     # 文言文词库（450+）
│   ├── struct_templates.md     # 结构化模板
│   └── prompt_templates.md     # Prompt 模板
├── .cursorrules                 # Cursor 兼容
├── claude_prompt.md            # Claude 专用
├── chatgpt_instructions.md     # ChatGPT 专用
├── SKILL.md                    # WorkBuddy 技能
└── README.md                   # 本文件
```

---

## 🛠️ 高级配置

配置文件位置：`~/.token-saver/config.json`

```json
{
  "enabled": true,
  "default_mode": "auto",
  "default_level": "medium",
  "default_model": "gpt-4",
  "show_stats": true,
  "auto_cache": true,
  "max_history": 100
}
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发指南

```bash
# 克隆仓库
git clone https://github.com/Windymonkeys/token-saver.git
cd token-saver

# 运行测试
python scripts/token-saver.py --test

# 提交代码
git checkout -b feature/your-feature
git commit -m "Add your feature"
git push origin feature/your-feature
```

---

## 📄 License

[MIT License](LICENSE)

---

## 🙏 致谢

感谢所有贡献者和用户的支持！

---

## 📮 联系方式

- **GitHub Issues**: [提交问题](https://github.com/Windymonkeys/token-saver/issues)
- **GitHub Discussions**: [参与讨论](https://github.com/Windymonkeys/token-saver/discussions)

---

⭐ 如果这个项目对你有帮助，请给一个 Star 支持一下！

[![Star History Chart](https://api.star-history.com/svg?repos=Windymonkeys/token-saver&type=Date)](https://star-history.com/#Windymonkeys/token-saver&Date)
