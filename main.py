import tkinter as tk
from tkinter import messagebox, filedialog, ttk, simpledialog
from datetime import datetime, timedelta
import pygame
import sqlite3
import threading
import time
import ctypes
from urllib.parse import urlparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import keyboard
import pystray
from PIL import Image, ImageDraw, ImageTk
import os
import sys
import subprocess

# --- 全局变量 ---
LATEST_BROWSER_DATA = {"url": "", "title": "", "ts": 0}

# ==========================================
# 0. 多语言配置 (新增历史记录相关文案)
# ==========================================
TRANSLATIONS = {
    "zh_CN": {
        "app_title": "番茄钟 Pro",
        "btn_lang": "English",
        "topmost": "窗口置顶",
        "hotkey_fmt": "显/隐快捷键: {}",
        "set_hk": "设置显/隐快捷键",
        "input_hk": "请输入新的快捷键 (例如 f10, alt+z)：\n(按下此键可快速隐藏或显示窗口)",
        "current_time": "当前时间",
        "ready": "准备就绪",
        "focus": "专注",
        "short_break": "短休",
        "long_break": "长休",
        "custom": "自定义:",
        "start": "开始",
        "music_def": "🎵 默认提示音",
        "music_sel": "📂 换音乐",
        "stats": "📊 统计面板",
        "reset": "⏹ 重置计时",
        "plugin_ok": "🟢 浏览器插件已连接",
        "plugin_fail": "🔴 未检测到插件 (点击修复)",
        "wait_monitor": "等待监测...",
        "monitor_prefix": "正在使用: ",
        "install_title": "插件安装引导",
        "install_msg": "【安装引导】\n\n1. 插件文件夹已为您打开。\n2. 扩展管理页地址已复制。\n\n请操作：\n👉 浏览器地址栏粘贴并回车 (Ctrl+V)。\n👉 开启右上角【开发者模式】。\n👉 将文件夹拖入浏览器。",
        "done_title": "完成",
        "done_msg": "时间到了！已记录本次番茄钟。",
        "stats_title": "统计中心",
        "tab_today": "今日",
        "tab_week": "本周",
        "tab_month": "本月",
        "tab_history": "📜 历史记录",  # 新增
        "col_name": "名称",
        "col_time": "时长",
        "col_pct": "占比",
        "col_start_at": "开始时间",  # 新增
        "col_type": "类型",  # 新增
        "col_duration_min": "时长 (分钟)",  # 新增
        "browser_total": "🌐 浏览器 (总计)",
        "tray_show": "显示窗口",
        "tray_exit": "退出程序",
        "err_hk": "快捷键无效"
    },
    "en_US": {
        "app_title": "Pomodoro Pro",
        "btn_lang": "中文",
        "topmost": "Always Top",
        "hotkey_fmt": "Show/Hide Key: {}",
        "set_hk": "Set Toggle Hotkey",
        "input_hk": "Enter new hotkey (e.g., f10, alt+z):\n(Press to toggle window visibility)",
        "current_time": "Current Time",
        "ready": "Ready",
        "focus": "Focus",
        "short_break": "Short",
        "long_break": "Long",
        "custom": "Custom:",
        "start": "Start",
        "music_def": "🎵 Default Sound",
        "music_sel": "📂 Music",
        "stats": "📊 Statistics",
        "reset": "⏹ Reset",
        "plugin_ok": "🟢 Plugin Connected",
        "plugin_fail": "🔴 Plugin Missing (Fix)",
        "wait_monitor": "Waiting...",
        "monitor_prefix": "Active: ",
        "install_title": "Install Guide",
        "install_msg": "[Guide]\n\n1. Folder opened.\n2. URL copied.\n\nAction:\n👉 Paste in browser address bar (Ctrl+V).\n👉 Enable 'Developer mode'.\n👉 Drag folder into browser.",
        "done_title": "Finished",
        "done_msg": "Time is up! Session recorded.",
        "stats_title": "Statistics",
        "tab_today": "Today",
        "tab_week": "Week",
        "tab_month": "Month",
        "tab_history": "📜 History",  # New
        "col_name": "Name",
        "col_time": "Time",
        "col_pct": "%",
        "col_start_at": "Start At",  # New
        "col_type": "Type",  # New
        "col_duration_min": "Duration (m)",  # New
        "browser_total": "🌐 Browser (Total)",
        "tray_show": "Show",
        "tray_exit": "Exit",
        "err_hk": "Invalid Key"
    }
}


# ==========================================
# 1. 浏览器扩展生成
# ==========================================
def generate_extension_files():
    base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    ext_dir = os.path.join(base_path, "Pomodoro_Extension")
    if not os.path.exists(ext_dir): os.makedirs(ext_dir)

    manifest = {
        "name": "Pomodoro Link Sync", "version": "2.0", "manifest_version": 3,
        "permissions": ["tabs"], "host_permissions": ["http://127.0.0.1:5000/*"],
        "background": {"service_worker": "background.js"}
    }
    js = """
    const SERVER='http://127.0.0.1:5000/update_url';
    async function s(){try{const t=await chrome.tabs.query({active:true,currentWindow:true});
    if(t&&t[0]&&t[0].url&&!t[0].url.startsWith('chrome')&&!t[0].url.startsWith('edge')){
    await fetch(SERVER,{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({url:t[0].url,title:t[0].title})});}}catch(e){}}
    chrome.tabs.onActivated.addListener(s);chrome.tabs.onUpdated.addListener((i,c,t)=>{if(c.status==='complete')s()});
    setInterval(s,3000);
    """
    with open(os.path.join(ext_dir, "manifest.json"), "w", encoding="utf-8") as f: json.dump(manifest, f)
    with open(os.path.join(ext_dir, "background.js"), "w", encoding="utf-8") as f: f.write(js)
    return ext_dir


# ==========================================
# 2. HTTP 服务器
# ==========================================
class SilentHandler(BaseHTTPRequestHandler):
    def log_message(self, f, *a):
        pass

    def do_OPTIONS(self):
        self.send_response(200);
        self.send_header('Access-Control-Allow-Origin', '*');
        self.send_header('Access-Control-Allow-Headers', 'Content-Type');
        self.end_headers()

    def do_POST(self):
        if self.path == '/update_url':
            try:
                l = int(self.headers.get('Content-Length', 0))
                if l > 0:
                    d = json.loads(self.rfile.read(l))
                    global LATEST_BROWSER_DATA
                    LATEST_BROWSER_DATA['url'] = d.get('url', '');
                    LATEST_BROWSER_DATA['ts'] = time.time()
                self.send_response(200);
                self.send_header('Access-Control-Allow-Origin', '*');
                self.end_headers();
                self.wfile.write(b'ok')
            except:
                pass
        else:
            self.send_response(404); self.end_headers()


def run_server():
    try:
        HTTPServer(('127.0.0.1', 5000), SilentHandler).serve_forever()
    except:
        pass


# ==========================================
# 3. 窗口解析与数据库
# ==========================================
user32 = ctypes.windll.user32


def get_active_window_title():
    h = user32.GetForegroundWindow()
    if not h: return ""
    l = user32.GetWindowTextLengthW(h)
    b = ctypes.create_unicode_buffer(l + 1);
    user32.GetWindowTextW(h, b, l + 1)
    return b.value


def extract_clean_domain(url):
    try:
        d = urlparse(url).netloc;
        if not d: return ""
        if ':' in d: d = d.split(':')[0]
        p = d.split('.');
        if len(p) == 1: return p[0].title()
        cp = {'com.cn', 'edu.cn', 'gov.cn', 'net.cn', 'co.jp', 'co.uk'}
        m = p[-3] if len(p) >= 3 and f"{p[-2]}.{p[-1]}" in cp else p[-2]
        if m == 'www' and len(p) > 2: m = p[-3]
        return m.title()
    except:
        return "Web"


def parse_activity(t):
    if not t: return "Unknown"
    tl = t.lower();
    bs = ['chrome', 'edge', 'firefox', 'brave', 'opera']
    if any(b in tl for b in bs):
        if time.time() - LATEST_BROWSER_DATA['ts'] < 10:
            u = LATEST_BROWSER_DATA['url']
            if u:
                c = extract_clean_domain(u)
                if c: return f"🌐 {c}"
        p = t.split(" - ");
        if len(p) >= 2: return f"🌐 {p[-2]}"
        return "🌐 Browser"
    else:
        return f"🖥️ {t.split(' - ')[-1][:15]}"


class DatabaseManager:
    def __init__(self, db="pomodoro_data.db"):
        self.conn = sqlite3.connect(db, check_same_thread=False);
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()
        # 表1：记录每秒的应用使用详情
        c.execute(
            'CREATE TABLE IF NOT EXISTS focus_log (id INTEGER PRIMARY KEY, log_date TEXT, app_name TEXT, duration_seconds INTEGER)')
        # 表2：设置
        c.execute('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)')
        # 表3：(新增) 记录番茄钟完成历史
        c.execute(
            'CREATE TABLE IF NOT EXISTS sessions (id INTEGER PRIMARY KEY, start_time TEXT, duration_minutes INTEGER, session_type TEXT)')
        self.conn.commit()

    def add_log(self, n, d):
        t = datetime.now().strftime("%Y-%m-%d")
        self.conn.cursor().execute("INSERT INTO focus_log (log_date,app_name,duration_seconds) VALUES (?,?,?)",
                                   (t, n, d));
        self.conn.commit()

    # 新增：记录一个完成的番茄钟
    def add_session_record(self, start_time, duration, s_type):
        self.conn.cursor().execute("INSERT INTO sessions (start_time, duration_minutes, session_type) VALUES (?,?,?)",
                                   (start_time, duration, s_type))
        self.conn.commit()

    # 新增：获取番茄钟历史
    def get_session_history(self, limit=50):
        c = self.conn.cursor()
        c.execute("SELECT start_time, session_type, duration_minutes FROM sessions ORDER BY id DESC LIMIT ?", (limit,))
        return c.fetchall()

    def get_stats(self, s, e):
        c = self.conn.cursor();
        c.execute(
            'SELECT app_name,SUM(duration_seconds) FROM focus_log WHERE log_date BETWEEN ? AND ? GROUP BY app_name ORDER BY SUM(duration_seconds) DESC',
            (s, e))
        return c.fetchall()

    def get_conf(self, k, d):
        c = self.conn.cursor();
        c.execute("SELECT value FROM settings WHERE key=?", (k,));
        r = c.fetchone()
        return r[0] if r else d

    def set_conf(self, k, v):
        self.conn.cursor().execute("REPLACE INTO settings (key,value) VALUES (?,?)", (k, v));
        self.conn.commit()


# ==========================================
# 4. 主程序
# ==========================================
class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x700")
        self.root.resizable(False, False)
        self.root.protocol('WM_DELETE_WINDOW', self.minimize_to_tray)

        # 图标设置
        icon_img = self.create_tray_image()
        self.tk_icon = ImageTk.PhotoImage(icon_img)
        self.root.wm_iconphoto(True, self.tk_icon)

        self.ext_path = generate_extension_files()
        threading.Thread(target=run_server, daemon=True).start()

        pygame.mixer.init()
        self.db = DatabaseManager()
        self.bg_color = "#f0f0f0"
        self.root.configure(bg=self.bg_color)

        self.font_clock = ("Helvetica", 36, "bold")
        self.font_timer = ("Helvetica", 48, "bold")
        self.music_file = None

        # 计时相关变量
        self.timer_running = False
        self.remaining_seconds = 0
        self.timer_id = None
        self.session_data = {}
        self.last_activity_name = ""
        self.var_monitor = tk.StringVar()
        self.is_topmost = tk.BooleanVar(value=False)

        # 本次番茄钟的记录信息
        self.current_session_start_time = ""
        self.current_session_duration = 0
        self.current_session_type = ""

        self.hotkey_str = self.db.get_conf("hotkey", "alt+h")
        self.update_hotkey_binding(self.hotkey_str)

        self.lang_code = self.db.get_conf("lang", "zh_CN")
        self.txt = TRANSLATIONS[self.lang_code]

        self.plugin_status_var = tk.StringVar()
        self.plugin_connected = False

        self.create_widgets()
        self.update_texts()
        self.update_current_time()
        self.setup_tray_icon()
        self.check_plugin_heartbeat()

    def toggle_language(self):
        self.lang_code = "en_US" if self.lang_code == "zh_CN" else "zh_CN"
        self.txt = TRANSLATIONS[self.lang_code]
        self.db.set_conf("lang", self.lang_code)
        self.update_texts()
        self.update_tray_menu()

    def update_texts(self):
        self.root.title(self.txt["app_title"])
        self.btn_lang.config(text=f"🌐 {self.txt['btn_lang']}")
        self.btn_hk.config(text=self.txt["hotkey_fmt"].format(self.hotkey_str))
        self.chk_top.config(text=self.txt["topmost"])
        self.lbl_time_title.config(text=self.txt["current_time"])

        if not self.timer_running:
            self.lbl_status.config(text=self.txt["ready"])
            self.var_monitor.set(self.txt["wait_monitor"])

        self.btn_focus.config(text=f"{self.txt['focus']} (25m)")
        self.btn_short.config(text=f"{self.txt['short_break']} (5m)")
        self.btn_long.config(text=f"{self.txt['long_break']} (15m)")
        self.lbl_custom.config(text=self.txt["custom"])
        self.btn_custom_start.config(text=self.txt["start"])
        self.lbl_music_name.config(
            text=self.txt["music_def"] if not self.music_file else self.music_file.split("/")[-1][:10] + "...")
        self.btn_music_sel.config(text=self.txt["music_sel"])
        self.btn_stats.config(text=self.txt["stats"])
        self.btn_reset.config(text=self.txt["reset"])

        self.check_plugin_heartbeat(force_update=True)

    def check_plugin_heartbeat(self, force_update=False):
        is_active = time.time() - LATEST_BROWSER_DATA['ts'] < 10 and LATEST_BROWSER_DATA['ts'] != 0
        if is_active != self.plugin_connected or force_update:
            self.plugin_connected = is_active
            if is_active:
                self.plugin_status_var.set(self.txt["plugin_ok"])
                self.lbl_plugin_status.config(fg="green", cursor="")
            else:
                self.plugin_status_var.set(self.txt["plugin_fail"])
                self.lbl_plugin_status.config(fg="red", cursor="hand2")
        if not force_update: self.root.after(2000, self.check_plugin_heartbeat)

    def show_install_guide(self, event=None):
        if self.plugin_connected: return
        try:
            self.root.clipboard_clear(); self.root.clipboard_append("chrome://extensions"); self.root.update()
        except:
            pass
        if messagebox.askokcancel(self.txt["install_title"], self.txt["install_msg"]):
            try:
                folder_path = os.path.abspath(self.ext_path)
                subprocess.Popen(f'explorer /select,"{folder_path}"')
            except:
                pass

    def create_tray_image(self):
        img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        dc = ImageDraw.Draw(img)
        dc.ellipse((4, 12, 60, 58), fill='#FF4500', outline='#DC143C')
        dc.polygon([(32, 2), (24, 14), (40, 14)], fill='#228B22')
        dc.polygon([(24, 14), (10, 18), (28, 24)], fill='#228B22')
        dc.polygon([(40, 14), (54, 18), (36, 24)], fill='#228B22')
        return img

    def setup_tray_icon(self):
        self.update_tray_menu()
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def update_tray_menu(self):
        if hasattr(self, 'tray_icon') and self.tray_icon: pass
        if not hasattr(self, 'tray_icon'):
            menu = (pystray.MenuItem(lambda text: self.txt["tray_show"], self.restore_from_tray, default=True),
                    pystray.MenuItem(lambda text: self.txt["tray_exit"], self.quit_app))
            self.tray_icon = pystray.Icon("pomodoro", self.create_tray_image(), "Pomodoro", menu)

    def minimize_to_tray(self):
        self.root.withdraw()

    def restore_from_tray(self, i=None, item=None):
        self.root.after(0, self._restore)

    def _restore(self):
        self.root.deiconify();
        self.root.attributes('-topmost', True)
        if not self.is_topmost.get(): self.root.after(100, lambda: self.root.attributes('-topmost', False))

    def quit_app(self, i=None, it=None):
        if hasattr(self, 'tray_icon'): self.tray_icon.stop()
        self.root.quit();
        os._exit(0)

    def create_widgets(self):
        top_frame = tk.Frame(self.root, bg=self.bg_color)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        self.btn_lang = tk.Button(top_frame, text="🌐", command=self.toggle_language, bg="#eee", font=("Arial", 8))
        self.btn_lang.pack(side=tk.LEFT, padx=(0, 5))
        self.btn_hk = tk.Button(top_frame, text="", command=self.ask_hk, bg="#ddd", relief="groove", font=("Arial", 8))
        self.btn_hk.pack(side=tk.LEFT)
        self.chk_top = tk.Checkbutton(top_frame, text="", var=self.is_topmost, command=self.toggle_topmost,
                                      bg=self.bg_color)
        self.chk_top.pack(side=tk.RIGHT)

        self.lbl_plugin_status = tk.Label(self.root, textvariable=self.plugin_status_var, bg=self.bg_color,
                                          font=("Arial", 9, "bold"))
        self.lbl_plugin_status.pack(fill=tk.X, pady=2)
        self.lbl_plugin_status.bind("<Button-1>", self.show_install_guide)

        self.lbl_time_title = tk.Label(self.root, text="", bg=self.bg_color, fg="#777")
        self.lbl_time_title.pack(pady=(5, 0))
        self.lbl_clock = tk.Label(self.root, text="00:00:00", font=self.font_clock, bg=self.bg_color, fg="#333")
        self.lbl_clock.pack(pady=5)

        tk.Label(self.root, textvariable=self.var_monitor, bg="#d5f5e3", fg="#196f3d", font=("Arial", 10), pady=5).pack(
            fill=tk.X, padx=20, pady=5)
        tk.Frame(self.root, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=20, pady=10)

        self.lbl_status = tk.Label(self.root, text="", font=("Arial", 12), bg=self.bg_color, fg="blue")
        self.lbl_status.pack(pady=(5, 0))
        self.lbl_timer = tk.Label(self.root, text="25:00", font=self.font_timer, bg=self.bg_color, fg="#e74c3c")
        self.lbl_timer.pack(pady=5)

        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=10)
        self.btn_focus = tk.Button(btn_frame, width=10, command=lambda: self.start(25, self.txt["focus"]))
        self.btn_focus.grid(row=0, column=0, padx=5)
        self.btn_short = tk.Button(btn_frame, width=10, command=lambda: self.start(5, self.txt["short_break"], True))
        self.btn_short.grid(row=0, column=1, padx=5)
        self.btn_long = tk.Button(btn_frame, width=10, command=lambda: self.start(15, self.txt["long_break"], True))
        self.btn_long.grid(row=0, column=2, padx=5)

        custom_frame = tk.Frame(self.root, bg=self.bg_color)
        custom_frame.pack(pady=5)
        self.lbl_custom = tk.Label(custom_frame, bg=self.bg_color)
        self.lbl_custom.pack(side=tk.LEFT)
        self.entry_custom = tk.Entry(custom_frame, width=5, justify="center")
        self.entry_custom.insert(0, "45")
        self.entry_custom.pack(side=tk.LEFT, padx=5)
        self.btn_custom_start = tk.Button(custom_frame, bg="#aed6f1", command=self.start_custom)
        self.btn_custom_start.pack(side=tk.LEFT)

        music_frame = tk.Frame(self.root, bg=self.bg_color)
        music_frame.pack(pady=10, fill=tk.X, padx=20)
        self.lbl_music_name = tk.Label(music_frame, bg=self.bg_color, fg="#555", width=20, anchor="w")
        self.lbl_music_name.pack(side=tk.LEFT, padx=5)
        self.btn_music_sel = tk.Button(music_frame, command=self.select_music, font=("Arial", 8))
        self.btn_music_sel.pack(side=tk.RIGHT)

        btm_frame = tk.Frame(self.root, bg=self.bg_color)
        btm_frame.pack(pady=15)
        self.btn_stats = tk.Button(btm_frame, command=self.show_stats_window, bg="#f9e79f", width=15)
        self.btn_stats.pack(side=tk.LEFT, padx=10)
        self.btn_reset = tk.Button(btm_frame, command=self.reset, bg="#bdc3c7", width=15)
        self.btn_reset.pack(side=tk.LEFT, padx=10)

    # --- 统计窗口 (升级版) ---
    def show_stats_window(self):
        win = tk.Toplevel(self.root)
        win.title(self.txt["stats_title"])
        win.wm_iconphoto(True, self.tk_icon)
        win.geometry("600x500")
        nb = ttk.Notebook(win)

        t2, t3, t4 = ttk.Frame(nb), ttk.Frame(nb), ttk.Frame(nb)
        # 新增：历史记录 Tab
        t_hist = ttk.Frame(nb)

        nb.add(t2, text=self.txt["tab_today"]);
        nb.add(t3, text=self.txt["tab_week"]);
        nb.add(t4, text=self.txt["tab_month"])
        nb.add(t_hist, text=self.txt["tab_history"])  # 添加历史记录标签

        nb.pack(expand=1, fill='both', padx=5, pady=5)

        today = datetime.now().strftime("%Y-%m-%d")
        self.build_treeview(t2, self.db.get_stats(today, today))
        self.build_treeview(t3, self.db.get_stats((datetime.now() - timedelta(6)).strftime("%Y-%m-%d"), today))
        self.build_treeview(t4, self.db.get_stats((datetime.now() - timedelta(29)).strftime("%Y-%m-%d"), today))

        # 构建历史记录列表
        self.build_history_treeview(t_hist)

    # 构建应用统计树 (原有逻辑)
    def build_treeview(self, parent, raw):
        tree = ttk.Treeview(parent, columns=('d', 'p'))
        tree.heading('#0', text=self.txt["col_name"], anchor='w');
        tree.heading('d', text=self.txt["col_time"], anchor='center');
        tree.heading('p', text=self.txt["col_pct"], anchor='center')
        tree.column('#0', width=300);
        tree.column('d', width=120, anchor='center');
        tree.column('p', width=80, anchor='center')
        sb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview);
        tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y");
        tree.pack(side="left", fill="both", expand=1)
        if not raw: tree.insert("", "end", text=self.txt["no_data"], values=("-", "-")); return
        total = sum(i[1] for i in raw)
        apps, webs, w_sum = [], [], 0
        for n, d in raw:
            if n.startswith("🌐"):
                webs.append((n, d)); w_sum += d
            else:
                apps.append((n, d))
        items = []
        for n, d in apps: items.append((n, d, False))
        if w_sum: items.append((self.txt["browser_total"], w_sum, True))
        items.sort(key=lambda x: x[1], reverse=True)

        def ft(s):
            m, s = divmod(s, 60); h, m = divmod(m, 60); return f"{h}h {m}m" if h else f"{m}m {s}s"

        def fp(s):
            return f"{s / total * 100:.1f}%" if total else "0%"

        for n, d, isg in items:
            if isg:
                node = tree.insert("", "end", text=n, values=(ft(d), fp(d)), open=True)
                webs.sort(key=lambda x: x[1], reverse=True)
                for wn, wd in webs: tree.insert(node, "end", text=wn.replace("🌐 ", ""), values=(ft(wd), fp(wd)))
            else:
                tree.insert("", "end", text=n, values=(ft(d), fp(d)))

    # 新增：构建番茄钟历史列表
    def build_history_treeview(self, parent):
        # 列: 开始时间, 类型, 时长
        cols = ('start', 'type', 'duration')
        tree = ttk.Treeview(parent, columns=cols, show='headings')

        tree.heading('start', text=self.txt["col_start_at"], anchor='center')
        tree.heading('type', text=self.txt["col_type"], anchor='center')
        tree.heading('duration', text=self.txt["col_duration_min"], anchor='center')

        tree.column('start', width=200, anchor='center')
        tree.column('type', width=100, anchor='center')
        tree.column('duration', width=100, anchor='center')

        sb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview);
        tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y");
        tree.pack(side="left", fill="both", expand=1)

        history = self.db.get_session_history()
        if not history:
            tree.insert("", "end", values=(self.txt["no_data"], "-", "-"))
        else:
            for start_t, s_type, dur in history:
                # 如果类型是翻译key (例如 "Focus"), 尝试翻译，如果是 "Custom" 等可能直接显示
                # 简单处理: 如果是英文Focus，显示翻译后的
                disp_type = s_type
                if s_type == "Focus" and "focus" in self.txt:
                    disp_type = self.txt["focus"]
                elif s_type == "Short Break" and "short_break" in self.txt:
                    disp_type = self.txt["short_break"]
                elif s_type == "Long Break" and "long_break" in self.txt:
                    disp_type = self.txt["long_break"]

                tree.insert("", "end", values=(start_t, disp_type, f"{dur} m"))

    def update_current_time(self):
        self.lbl_clock.config(text=datetime.now().strftime("%H:%M:%S"))
        self.root.after(1000, self.update_current_time)

    def toggle_topmost(self):
        self.root.attributes('-topmost', self.is_topmost.get())

    def select_music(self):
        p = filedialog.askopenfilename(filetypes=[("Audio", "*.mp3 *.wav")])
        if p: self.music_file = p; self.lbl_music_name.config(text=p.split("/")[-1][:10] + "...", fg="green")

    def start_custom(self):
        try:
            m = int(self.entry_custom.get()); self.start(m, f"{self.txt['custom']} {m}m", False,
                                                         True) if m > 0 else None
        except:
            pass

    def monitor(self):
        while self.timer_running and not getattr(self, 'is_break', False):
            try:
                t = get_active_window_title();
                n = parse_activity(t)
                if n != self.last_activity_name: self.root.after(0, lambda x=n: self.var_monitor.set(
                    f"{self.txt['monitor_prefix']}{x}")); self.last_activity_name = n
                self.session_data[n] = self.session_data.get(n, 0) + 2
                time.sleep(2)
            except:
                break

    # 修改 start 方法，记录开始状态
    def start(self, mins, st, is_break=False, is_custom=False):
        self.reset()
        self.timer_running = True
        self.is_break = is_break
        self.remaining_seconds = mins * 60

        # 记录本次番茄钟元数据
        self.current_session_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.current_session_duration = mins
        # 确定类型名称 (用于存入数据库，建议存通用英文key，展示时翻译)
        if is_custom:
            self.current_session_type = "Custom"
        elif is_break:
            self.current_session_type = "Break"  # 简略，或者根据 mins 判断
        else:
            self.current_session_type = "Focus"

        # 如果是预设按钮，这里修正一下类型名以更精确
        if st == self.txt["short_break"]: self.current_session_type = "Short Break"
        if st == self.txt["long_break"]: self.current_session_type = "Long Break"

        self.lbl_status.config(text=st, fg="green" if not is_break else "#e67e22")
        if not is_break: self.session_data = {}; threading.Thread(target=self.monitor, daemon=True).start()
        self.countdown()

    def countdown(self):
        if self.timer_running and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            m, s = divmod(self.remaining_seconds, 60)
            self.lbl_timer.config(text=f"{m:02d}:{s:02d}")
            self.timer_id = self.root.after(1000, self.countdown)
        elif self.timer_running:
            self.finish()

    def finish(self):
        # 保存应用统计
        if not getattr(self, 'is_break', False): self.save_data()

        # 新增：保存番茄钟记录
        if self.timer_running:
            self.db.add_session_record(self.current_session_start_time, self.current_session_duration,
                                       self.current_session_type)

        self.timer_running = False
        if self.music_file:
            try:
                pygame.mixer.music.load(self.music_file); pygame.mixer.music.play(-1)
            except:
                pass
        else:
            for _ in range(3): self.root.bell(); time.sleep(0.5)
        self._restore();
        messagebox.showinfo(self.txt["done_title"], self.txt["done_msg"])
        if pygame.mixer.music.get_busy(): pygame.mixer.music.stop()
        self.reset()

    def save_data(self):
        for k, v in self.session_data.items():
            if v > 0: self.db.add_log(k, v)
        self.session_data = {}

    def reset(self):
        if self.timer_running and not getattr(self, 'is_break', False): self.save_data()
        self.timer_running = False
        if self.timer_id: self.root.after_cancel(self.timer_id); self.timer_id = None
        if pygame.mixer.music.get_busy(): pygame.mixer.music.stop()
        self.lbl_timer.config(text="00:00");
        self.lbl_status.config(text=self.txt["ready"], fg="blue");
        self.var_monitor.set(self.txt["wait_monitor"])

    def ask_hk(self):
        k = simpledialog.askstring(self.txt["set_hk"], self.txt["input_hk"], parent=self.root,
                                   initialvalue=self.hotkey_str)
        if k: self.update_hotkey_binding(k.lower().strip())

    def update_hotkey_binding(self, nk):
        try:
            try:
                keyboard.unhook_all_hotkeys()
            except:
                pass
            keyboard.add_hotkey(nk, lambda: self.root.after(0, self.toggle_vis))
            self.hotkey_str = nk;
            self.db.set_conf("hotkey", nk)
            if hasattr(self, 'btn_hk'): self.btn_hk.config(text=self.txt["hotkey_fmt"].format(nk))
            return True
        except:
            messagebox.showerror("Error", self.txt["err_hk"]); return False

    def toggle_vis(self):
        if self.root.state() == 'normal':
            self.minimize_to_tray()
        else:
            self._restore()


if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()