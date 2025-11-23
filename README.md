Pomodoro Pro 🍅Pomodoro Pro 是一款功能强大的桌面生产力工具，结合了 番茄工作法计时器 与 全自动应用/网页活动追踪 功能。它不仅能帮助你保持专注，还能在后台默默记录你的时间都去哪了——无论是写代码、写文档，还是在 Bilibili 上摸鱼，都能被精确统计（支持精确到具体的网站域名）。✨ 主要功能 (Key Features)1. 专注计时 (Focus Timer)🍅 标准番茄钟：预设 25分钟专注 / 5分钟短休 / 15分钟长休。⏱️ 自定义时长：支持输入任意分钟数进行倒计时。🎵 白噪音/背景音：支持加载本地音频文件（.mp3/.wav），专注时循环播放，结束自动停止。2. 智能追踪 (Smart Tracking)🖥️ 桌面应用追踪：自动记录当前正在使用的窗口（如 PyCharm, Word, Photoshop）。🌐 网页级追踪：配合内置浏览器插件，精确记录当前浏览的网站域名（如 github.com, bilibili.com），而非笼统的“谷歌浏览器”。🔒 隐私安全：所有数据仅存储在本地 SQLite 数据库中，绝不上传云端。3. 数据统计 (Statistics Center)📊 多维度报表：查看今日、本周、本月的专注时长分布。🗂️ 分组展示：网页访问记录会自动归纳到“🌐 浏览器 (总计)”下，支持展开/折叠，像任务管理器一样清晰。📜 历史记录：详细记录每一个完成的番茄钟开始时间和类型。4. 贴心交互 (User Experience)🌍 多语言支持：一键切换 简体中文 / English。👻 老板键 (Global Hotkey)：默认 Alt+H 一键隐藏/呼出窗口（支持自定义快捷键）。📥 系统托盘：点击关闭按钮自动最小化到托盘，右键菜单控制退出。🚀 开机自启：支持设置随 Windows 启动自动运行。🛠️ 安装与运行 (Installation)方式一：直接运行源码克隆/下载代码安装依赖库：pip install pygame keyboard pystray Pillow
运行程序：python pomodoro.py
方式二：打包为 EXE (推荐)如果您想生成独立的 .exe 文件分享给朋友：pip install pyinstaller
pyinstaller --onefile --windowed --name="PomodoroPro" pomodoro.py
注：如果准备了图标，请加上 --icon="tomato.ico" 参数。🧩 浏览器插件安装指南 (Browser Extension)为了精确统计网页浏览时长，软件依赖一个轻量级浏览器插件。请放心，软件会自动为您生成插件文件。运行 Pomodoro Pro 软件。如果界面显示红色 “🔴 未检测到插件”，请点击该文字。软件会自动打开生成的 Pomodoro_Extension 文件夹，并尝试复制扩展管理页地址。手动操作步骤：打开 Chrome 或 Edge 浏览器。地址栏输入 chrome://extensions 并回车。打开右上角的 【开发者模式 (Developer mode)】 开关。将 Pomodoro_Extension 文件夹直接拖入浏览器窗口即可。回到软件，状态应变为绿色 “🟢 浏览器插件已连接”。📖 使用说明 (Usage)开始专注：点击“专注”按钮或输入自定义时间开始。隐藏窗口：点击右上角 X 按钮（最小化到托盘）。按下快捷键（默认 Alt+H）。查看统计：点击底部的“📊 统计面板”，查看您的时间分布。设置快捷键：点击左上角的快捷键按钮，输入新的组合键（如 F10, Ctrl+Q）。📂 项目结构 (Project Structure)Pomodoro-Pro/
├── pomodoro.py            # 主程序源码
├── pomodoro_data.db       # [自动生成] 本地数据库 (存储统计数据)
├── Pomodoro_Extension/    # [自动生成] 浏览器插件文件夹
│   ├── manifest.json
│   └── background.js
└── README.md              # 说明文档
⚠️ 注意事项杀毒软件误报：由于软件包含“全局快捷键监听”功能（使用了 keyboard 库），某些杀毒软件可能会误报。请将其添加到信任白名单。端口占用：软件会在本地启动一个极简的 HTTP 服务器监听 127.0.0.1:5000 用于接收浏览器数据。请确保该端口未被其他程序占用。📝 License此项目开源，遵循 MIT License。您可以随意修改和分发。Enjoy your focus time! 🍅
