# **Pomodoro Pro 🍅**

**Pomodoro Pro** is a powerful desktop productivity tool that combines a **Pomodoro Timer** with **Automatic Activity Tracking**.

It helps you stay focused while silently recording where your time goes in the background—whether you're coding in an IDE, writing documents in Word, or browsing specific websites like GitHub or Bilibili.

## **✨ Key Features**

### **1\. Focus Timer**

* 🍅 **Standard Modes**: Preset for 25m Focus / 5m Short Break / 15m Long Break.  
* ⏱️ **Custom Duration**: Input any minute value to start a countdown.  
* 🎵 **Background Music**: Load local audio files (.mp3/.wav) that loop during focus and stop automatically when time is up.

### **2\. Smart Tracking**

* 🖥️ **Desktop App Tracking**: Automatically records the active window (e.g., PyCharm, Word, Photoshop).  
* 🌐 **Web Tracking**: Works with a lightweight, auto-generated browser extension to record specific domains (e.g., github.com instead of just "Google Chrome").  
* 🔒 **Privacy**: All data is stored locally in a SQLite database (pomodoro\_data.db). **No data is ever uploaded to the cloud.**

### **3\. Statistics Center**

* 📊 **Multi-view Reports**: Visualize time distribution for Today, This Week, and This Month.  
* 🗂️ **Smart Grouping**: Web activities are automatically grouped under "🌐 Browser (Total)". Click to expand and see detailed site usage.  
* 📜 **Session History**: A detailed log of every completed Pomodoro session, including start time and duration.

### **4\. Enhanced User Experience**

* 🌍 **Multi-language**: One-click switch between **简体中文** and **English**.  
* 👻 **Boss Key (Global Hotkey)**: Default Alt+H to instantly hide/show the window (customizable).  
* 📥 **System Tray**: Minimizes to the system tray on close; right-click the tray icon to exit.  
* 🚀 **Auto-start**: Option to launch automatically with Windows.

## **🛠️ Installation & Running**

### **Option 1: Run from Source**

1. **Clone/Download** the repository.  
2. **Install Dependencies**:  
   pip install pygame keyboard pystray Pillow

3. **Run the App**:  
   python pomodoro.py

### **Option 2: Build EXE (Recommended)**

To generate a standalone executable file:

pip install pyinstaller  
pyinstaller \--onefile \--windowed \--name="PomodoroPro" pomodoro.py

*Note: If you have an icon file, add \--icon="tomato.ico" to the command.*

## **🧩 Browser Extension Guide**

To track specific websites, the app relies on a minimal browser extension. **The app generates this for you automatically.**

1. Run Pomodoro Pro.  
2. If you see **"🔴 Plugin Missing"** (or red text) on the interface, click it.  
3. The app will open the generated Pomodoro\_Extension folder and copy the extensions URL to your clipboard.  
4. **Manual Installation Steps**:  
   * Open Chrome or Edge.  
   * Paste chrome://extensions into the address bar and hit Enter.  
   * Toggle **Developer mode** on (top right).  
   * **Drag and drop** the Pomodoro\_Extension folder directly into the browser window.  
5. The app status should turn to **"🟢 Plugin Connected"**.

## **📖 How to Use**

* **Start Focus**: Click preset buttons or enter a custom time.  
* **Hide Window**:  
  * Click the X button (minimizes to tray).  
  * Press the global hotkey (Default Alt+H).  
* **View Stats**: Click "📊 Statistics" at the bottom to see your time usage.  
* **Settings**:  
  * Toggle "Always Top" or "Auto Start" at the top right.  
  * Click the "Hotkey" button to customize your hide/show shortcut.

## **📂 Project Structure**

Pomodoro-Pro/  
├── pomodoro.py            \# Main application source code  
├── pomodoro\_data.db       \# \[Auto-generated\] Local database  
├── Pomodoro\_Extension/    \# \[Auto-generated\] Browser extension folder  
│   ├── manifest.json  
│   └── background.js  
└── README.md              \# Documentation

## **⚠️ Notes**

1. **Antivirus False Positives**: Since the app uses keyboard for global hotkeys, some antivirus software might flag it. Please add it to the exclusion/whitelist.  
2. **Port Usage**: The app starts a minimal local HTTP server on 127.0.0.1:5000 to receive data from the browser extension. Ensure this port is free.

## **📝 License**

This project is open-source under the MIT License. Feel free to modify and distribute.

**Enjoy your focus time\! 🍅**
