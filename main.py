import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime
import pygame # 需要 pip install pygame

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("番茄钟 & 桌面时钟")
        # 高度再次微调以容纳音乐选择区
        self.root.geometry("400x520")  
        self.root.resizable(False, False)

        # --- 初始化音频模块 ---
        pygame.mixer.init()
        self.music_file = None # 存储用户选择的音乐路径

        # --- 配置颜色和字体 ---
        self.bg_color = "#f0f0f0"
        self.root.configure(bg=self.bg_color)
        self.font_clock = ("Helvetica", 36, "bold")
        self.font_timer = ("Helvetica", 48, "bold")

        # --- 状态变量 ---
        self.timer_running = False
        self.remaining_seconds = 0
        self.timer_id = None

        # --- 界面布局 ---
        self.create_widgets()

        # --- 启动实时时钟 ---
        self.update_current_time()

    def create_widgets(self):
        # 1. 顶部控制栏 (置顶开关)
        top_frame = tk.Frame(self.root, bg=self.bg_color)
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        self.is_topmost = tk.BooleanVar()
        chk_top = tk.Checkbutton(top_frame, text="窗口置顶", var=self.is_topmost,
                                 command=self.toggle_topmost, bg=self.bg_color)
        chk_top.pack(side=tk.RIGHT)

        # 2. 当前时间显示区域
        self.lbl_current_time_msg = tk.Label(self.root, text="当前时间", bg=self.bg_color, fg="#555")
        self.lbl_current_time_msg.pack(pady=(5, 0))

        self.lbl_clock = tk.Label(self.root, text="00:00:00", font=self.font_clock, bg=self.bg_color, fg="#333")
        self.lbl_clock.pack(pady=5)

        # 分割线
        tk.Frame(self.root, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=20, pady=10)

        # 3. 番茄钟状态标签
        self.lbl_status = tk.Label(self.root, text="准备就绪", font=("Arial", 12), bg=self.bg_color, fg="blue")
        self.lbl_status.pack(pady=(5, 0))

        # 4. 倒计时显示区域
        self.lbl_timer = tk.Label(self.root, text="25:00", font=self.font_timer, bg=self.bg_color, fg="#e74c3c")
        self.lbl_timer.pack(pady=5)

        # 5. 预设按钮区域
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="标准专注\n(25分)", width=10,
                  command=lambda: self.start_timer(25, "专注中...")).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="短休息\n(5分)", width=10,
                  command=lambda: self.start_timer(5, "休息中...")).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="长休息\n(15分)", width=10,
                  command=lambda: self.start_timer(15, "长休息中...")).grid(row=0, column=2, padx=5)

        # 6. 自定义时长区域
        custom_frame = tk.Frame(self.root, bg=self.bg_color)
        custom_frame.pack(pady=5)

        tk.Label(custom_frame, text="自定义:", bg=self.bg_color).pack(side=tk.LEFT)
        self.entry_custom = tk.Entry(custom_frame, width=5, justify="center")
        self.entry_custom.pack(side=tk.LEFT, padx=5)
        self.entry_custom.insert(0, "45")
        tk.Label(custom_frame, text="分钟", bg=self.bg_color).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(custom_frame, text="开始", bg="#aed6f1", command=self.start_custom_timer).pack(side=tk.LEFT)

        # 7. [新增] 音乐选择区域
        music_frame = tk.Frame(self.root, bg=self.bg_color)
        music_frame.pack(pady=10, fill=tk.X, padx=20)

        tk.Label(music_frame, text="提示音:", bg=self.bg_color, fg="#555").pack(side=tk.LEFT)
        
        # 显示当前音乐文件名的标签（初始显示“默认提示音”）
        self.lbl_music_name = tk.Label(music_frame, text="默认提示音 (系统)", bg=self.bg_color, fg="#333", width=20, anchor="w")
        self.lbl_music_name.pack(side=tk.LEFT, padx=5)

        btn_select_music = tk.Button(music_frame, text="📂 选择文件", command=self.select_music_file, font=("Arial", 8))
        btn_select_music.pack(side=tk.RIGHT)

        # 8. 重置按钮
        btn_reset = tk.Button(self.root, text="重置 / 停止", width=34, bg="#bdc3c7", command=self.reset_timer)
        btn_reset.pack(pady=(5, 15))

    def toggle_topmost(self):
        self.root.attributes('-topmost', self.is_topmost.get())

    def update_current_time(self):
        now_str = datetime.now().strftime("%H:%M:%S")
        self.lbl_clock.config(text=now_str)
        self.root.after(1000, self.update_current_time)

    # --- 音乐选择逻辑 ---
    def select_music_file(self):
        """打开文件选择对话框"""
        file_path = filedialog.askopenfilename(
            title="选择提示音音乐",
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")]
        )
        if file_path:
            self.music_file = file_path
            # 获取文件名显示在界面上
            file_name = file_path.split("/")[-1]
            if len(file_name) > 15: file_name = file_name[:12] + "..." # 截断长文件名
            self.lbl_music_name.config(text=file_name, fg="green")
        else:
            # 如果用户取消选择，保持原状或重置
            pass

    def play_alarm(self):
        """播放音乐或系统音"""
        if self.music_file:
            try:
                pygame.mixer.music.load(self.music_file)
                pygame.mixer.music.play(loops=-1) # -1 表示循环播放
            except Exception as e:
                messagebox.showerror("播放错误", f"无法播放该音频文件:\n{e}")
                self.root.bell()
        else:
            # 如果没选文件，响铃3次
            for _ in range(3):
                self.root.bell()
                self.root.after(500)

    def stop_alarm(self):
        """停止音乐"""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

    # --- 计时逻辑 ---
    def start_custom_timer(self):
        user_input = self.entry_custom.get()
        try:
            minutes = int(user_input)
            if minutes <= 0:
                messagebox.showwarning("输入错误", "请输入大于0的整数！")
                return
            self.start_timer(minutes, f"自定义 ({minutes}分)")
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字！")

    def start_timer(self, minutes, status_text):
        self.reset_timer()
        self.timer_running = True
        self.remaining_seconds = minutes * 60
        self.lbl_status.config(text=status_text, fg="green")
        self.update_timer_display()
        self.countdown()

    def countdown(self):
        if self.timer_running and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_timer_display()
            self.timer_id = self.root.after(1000, self.countdown)
            
        elif self.timer_running and self.remaining_seconds == 0:
            self.timer_running = False
            self.lbl_status.config(text="计时结束！", fg="red")
            
            # 1. 播放音乐
            self.play_alarm()

            # 2. 窗口操作
            original_topmost = self.root.attributes('-topmost')
            self.root.attributes('-topmost', True)
            
            # 3. 弹出提示框 (此时程序会暂停在这里等待用户点击确定)
            messagebox.showinfo("番茄钟提示", "时间到了！请休息或开始下一段专注。")
            
            # 4. 用户点击确定后，停止音乐并恢复窗口状态
            self.stop_alarm()
            self.root.attributes('-topmost', original_topmost)
            self.reset_timer()

    def update_timer_display(self):
        mins, secs = divmod(self.remaining_seconds, 60)
        self.lbl_timer.config(text="{:02d}:{:02d}".format(mins, secs))

    def reset_timer(self):
        self.timer_running = False
        self.stop_alarm() # 确保按下重置也能停止音乐
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.lbl_timer.config(text="00:00")
        self.lbl_status.config(text="准备就绪", fg="blue")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
