# token-saver

> 🤖 WorkBuddy 技能 - 节省 Token 的利器

用文言文压缩 + 结构化输出，让你的 AI 对话更高效！

## 功能

### 1️⃣ 文言文压缩
将冗长的现代汉语转换为简洁的文言表达，节省 Token 用量。

| 现代汉语 | 文言文 |
|---------|--------|
| 你知道这个方法吗？ | 汝知此法乎？ |
| 我认为这个结果很好 | 吾以为此果甚善 |
| 因为他很努力，所以成功了 | 彼甚勤，故成 |

### 2️⃣ 结构化输出
提供预定义的模板（JSON Schema、Markdown 表格、代码注释等），减少重复描述。

## 安装

### 方法一：克隆到本地
```bash
git clone https://github.com/Windymonkeys/token-saver.git
mv token-saver ~/.workbuddy/skills/
```

### 方法二：下载 ZIP
1. 点击右上角 **Code** → **Download ZIP**
2. 解压到 `~/.workbuddy/skills/` 目录

## 使用

在 WorkBuddy 中，当需要节省 Token 时：

1. **文言文模式**：输入"用文言文说..."或"翻译成文言"
2. **结构化模式**：输入"用 JSON 格式"或"给我一个模板"

## 文件结构

```
token-saver/
├── SKILL.md                      # 技能说明
└── references/
    ├── wenyan_mapping.json      # 文言文词库（300+词条）
    └── struct_templates.md       # 结构化输出模板
```

## 词库预览

支持的词汇类型：
- 常见代词（我、你、他 → 吾、汝、彼）
- 常用动词（知道、认为 → 知、以为）
- 常见形容词（好的、重要 → 善、重）
- 连接词（但是、如果、因为 → 然、若、因）
- 现代网络语（点赞、内卷、躺平...）

## License

MIT

---

⭐ 如果对你有帮助，点个 Star 支持一下！
