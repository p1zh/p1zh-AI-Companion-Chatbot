\# AI智能伴侣项目

一个基于 DeepSeek API 的流式对话聊天机器人，支持人设配置与会话记忆。



\## ✨ 功能特点

\- 🧠 \*\*流式对话\*\*：实时输出回复，模拟真人聊天体验

\- 🎭 \*\*人设配置\*\*：可自定义AI角色的性格、语气和背景设定

\- 💾 \*\*会话记忆\*\*：自动保存聊天记录，下次打开可继续对话

\- 🖼️ \*\*图片支持\*\*：内置头像和背景资源，界面更友好



\## 🛠️ 使用方法

1\.  安装依赖：

&nbsp;   ```bash

&nbsp;   pip install streamlit requests

&nbsp;   ```

2\.  配置 API 密钥：

&nbsp;   在 `ai\_partner.py` 中填入你的 DeepSeek API Key

3\.  启动项目：

&nbsp;   ```bash

&nbsp;   streamlit run ai\_partner.py

&nbsp;   ```



\## 📂 项目结构

\- `ai\_partner.py`：主程序文件，包含对话逻辑与界面代码

\- `resources/`：存放头像、背景等图片资源

\- `session/`：自动生成的聊天记录文件，按日期保存



\## 📝 开发说明

\- 基于 Python + Streamlit 开发

\- 使用 DeepSeek API 实现大语言模型对话能力

\- 会话记录以 JSON 格式本地存储，方便后续扩展

