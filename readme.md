# **Pomodoro Pro 🍅**

**Pomodoro Pro** 是一款功能强大的桌面生产力工具，结合了 **番茄工作法计时器** 与 **全自动应用/网页活动追踪** 功能。它不仅能帮助你保持专注，还能在后台默默记录你的时间都去哪了。

**Pomodoro Pro** is a powerful desktop productivity tool that combines a **Pomodoro Timer** with **Automatic Activity Tracking**. It helps you stay focused while silently recording where your time goes in the background.

## **✨ 主要功能 / Key Features**

### **1\. 专注计时 (Focus Timer)**

* 🍅 **标准番茄钟 / Standard Modes** 预设 25分钟专注 / 5分钟短休 / 15分钟长休。  
  Preset for 25m Focus / 5m Short Break / 15m Long Break.  
* ⏱️ **自定义时长 / Custom Duration** 支持输入任意分钟数进行倒计时。  
  Input any minute value to start a countdown.  
* 🎵 **白噪音/背景音 / Background Music** 支持加载本地音频文件（.mp3/.wav），专注时循环播放，结束自动停止。  
  Load local audio files (.mp3/.wav) that loop during focus and stop automatically when time is up.

### **2\. 智能追踪 (Smart Tracking)**

* 🖥️ **桌面应用追踪 / Desktop App Tracking** 自动记录当前正在使用的窗口（如 PyCharm, Word, Photoshop）。  
  Automatically records the active window (e.g., PyCharm, Word, Photoshop).  
* 🌐 **网页级追踪 / Web Tracking** 配合内置浏览器插件，精确记录当前浏览的网站域名（如 github.com），而非笼统的“谷歌浏览器”。  
  Works with a lightweight, auto-generated browser extension to record specific domains (e.g., github.com instead of just "Google Chrome").  
* 🔒 **隐私安全 / Privacy** 所有数据仅存储在本地 SQLite 数据库中，**绝不上传云端**。  
  All data is stored locally in a SQLite database (pomodoro\_data.db). **No data is ever uploaded to the cloud.**

### **3\. 数据统计 (Statistics Center)**

* 📊 **多维度报表 / Multi-view Reports** 查看今日、本周、本月的专注时长分布。  
  Visualize time distribution for Today, This Week, and This Month.  
* 🗂️ **分组展示 / Smart Grouping** 网页访问记录会自动归纳到“🌐 浏览器 (总计)”下，支持展开/折叠，像任务管理器一样清晰。  
  Web activities are automatically grouped under "🌐 Browser (Total)". Click to expand and see detailed site usage.  
* 📜 **历史记录 / Session History** 详细记录每一个完成的番茄钟开始时间和类型。  
  A detailed log of every completed Pomodoro session, including start time and duration.

### **4\. 贴心交互 (Enhanced User Experience)**

* 🌍 **多语言支持 / Multi-language** 一键切换 **简体中文 / English**。  
  One-click switch between **简体中文** and **English**.  
* 👻 **老板键 / Boss Key (Global Hotkey)** 默认 Alt+H 一键隐藏/呼出窗口（支持自定义快捷键）。  
  Default Alt+H to instantly hide/show the window (customizable).  
* 📥 **系统托盘 / System Tray** 点击关闭按钮自动最小化到托盘，右键菜单控制退出。  
  Minimizes to the system tray on close; right-click the tray icon to exit.  
* 🚀 **开机自启 / Auto-start** 支持设置随 Windows 启动自动运行。  
  Option to launch automatically with Windows.

## **🛠️ 安装与运行 / Installation & Running**

### **方式一：直接运行源码 (Run from Source)**

1. **克隆/下载代码** (Clone/Download the repository).  
2. **安装依赖库** (Install Dependencies):  
   pip install pygame keyboard pystray Pillow

3. **运行程序** (Run the App):  
   python pomodoro.py

### **方式二：打包为 EXE (Build EXE \- Recommended)**

如果您想生成独立的 .exe 文件分享给朋友：

To generate a standalone executable file:

pip install pyinstaller  
pyinstaller \--onefile \--windowed \--name="PomodoroPro" pomodoro.py

*注：如果准备了图标，请加上 \--icon="tomato.ico" 参数。* *Note: If you have an icon file, add \--icon="tomato.ico" to the command.*

## **🧩 浏览器插件安装指南 / Browser Extension Guide**

为了精确统计网页浏览时长，软件依赖一个轻量级浏览器插件。**请放心，软件会自动为您生成插件文件。** To track specific websites, the app relies on a minimal browser extension. **The app generates this for you automatically.**

1. 运行 Pomodoro Pro 软件 (Run Pomodoro Pro).  
2. 如果界面显示红色 **“🔴 未检测到插件”**，请点击该文字 (If you see **"🔴 Plugin Missing"**, click it).  
3. 软件会自动打开生成的 Pomodoro\_Extension 文件夹，并尝试复制扩展管理页地址 (The app will open the generated folder and copy the extensions URL).  
4. **手动操作步骤 (Manual Steps)**：  
   * 打开 Chrome 或 Edge 浏览器 (Open Chrome or Edge).  
   * 地址栏输入 chrome://extensions 并回车 (Paste chrome://extensions and hit Enter).  
   * 打开右上角的 **【开发者模式 (Developer mode)】** 开关 (Toggle **Developer mode** on).  
   * 将 Pomodoro\_Extension 文件夹**直接拖入**浏览器窗口即可 (Drag and drop the folder into the browser).  
5. 回到软件，状态应变为绿色 **“🟢 浏览器插件已连接”** (The app status should turn green).

## **📖 使用说明 / Usage**

* **开始专注 (Start Focus)**: 点击“专注”按钮或输入自定义时间开始 (Click preset buttons or enter a custom time).  
* **隐藏窗口 (Hide Window)**:  
  * 点击右上角 X 按钮（最小化到托盘） (Click X button to minimize to tray).  
  * 按下快捷键（默认 Alt+H） (Press global hotkey, default Alt+H).  
* **查看统计 (View Stats)**: 点击底部的“📊 统计面板” (Click "📊 Statistics").  
* **设置 (Settings)**:  
  * 顶部开关：窗口置顶、开机自启 (Toggle "Always Top" or "Auto Start").  
  * 左上角：设置快捷键 (Click "Hotkey" button to customize).

## **📂 项目结构 / Project Structure**

Pomodoro-Pro/  
├── pomodoro.py            \# 主程序源码 (Main source code)  
├── pomodoro\_data.db       \# \[自动生成\] 本地数据库 (Auto-generated database)  
├── Pomodoro\_Extension/    \# \[自动生成\] 浏览器插件 (Auto-generated extension)  
│   ├── manifest.json  
│   └── background.js  
└── README.md              \# 说明文档 (Documentation)

## **⚠️ 注意事项 / Notes**

1. **杀毒软件误报 (Antivirus False Positives)**:  
   由于软件包含“全局快捷键监听”功能（使用了 keyboard 库），某些杀毒软件可能会误报。请将其添加到信任白名单。  
   Since the app uses keyboard for global hotkeys, some antivirus software might flag it. Please add it to the exclusion/whitelist.  
2. **端口占用 (Port Usage)**:  
   软件会在本地启动一个极简的 HTTP 服务器监听 127.0.0.1:5000 用于接收浏览器数据。请确保该端口未被其他程序占用。  
   The app starts a minimal local HTTP server on 127.0.0.1:5000 to receive data. Ensure this port is free.

## **📝 License**

此项目开源，遵循 MIT License。您可以随意修改和分发。

This project is open-source under the MIT License. Feel free to modify and distribute.

**Enjoy your focus time\! 🍅**