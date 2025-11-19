import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import json
import os
import threading
import schedule
import time
from datetime import datetime
import asyncio
import shutil
import subprocess

class BiliUploaderApp(ctk.CTk):
    CONFIG_FILE = "config.json"
    BILIUP_COOKIE_FILE = os.path.expanduser("~/cookies.json")

    def __init__(self):
        super().__init__()

        self.scheduler_running = False
        self.scheduler_thread = None

        self.title("B站定时上传工具 (内核: biliup-rs)")
        self.geometry("800x700")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        self.config_frame = ctk.CTkFrame(self)
        self.config_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.config_frame.grid_columnconfigure(1, weight=1)

        self.info_label = ctk.CTkLabel(self.config_frame, text="请先在终端手动运行 'biliup login' 完成登录", text_color="yellow")
        self.info_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.video_path_label = ctk.CTkLabel(self.config_frame, text="待上传文件夹:")
        self.video_path_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.video_path_entry = ctk.CTkEntry(self.config_frame, placeholder_text="选择包含视频文件的文件夹")
        self.video_path_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.video_path_button = ctk.CTkButton(self.config_frame, text="选择", width=60, command=lambda: self.select_folder(self.video_path_entry))
        self.video_path_button.grid(row=1, column=2, padx=10, pady=5)

        self.uploaded_path_label = ctk.CTkLabel(self.config_frame, text="已上传文件夹:")
        self.uploaded_path_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.uploaded_path_entry = ctk.CTkEntry(self.config_frame, placeholder_text="选择用于存放已上传视频的文件夹")
        self.uploaded_path_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.uploaded_path_button = ctk.CTkButton(self.config_frame, text="选择", width=60, command=lambda: self.select_folder(self.uploaded_path_entry))
        self.uploaded_path_button.grid(row=2, column=2, padx=10, pady=5)
        
        self.copyright_label = ctk.CTkLabel(self.config_frame, text="稿件类型:")
        self.copyright_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.copyright_var = tk.StringVar(value="转载")
        self.copyright_menu = ctk.CTkOptionMenu(self.config_frame, values=["自制", "转载"], variable=self.copyright_var)
        self.copyright_menu.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        self.source_label = ctk.CTkLabel(self.config_frame, text="转载来源:")
        self.source_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.source_entry = ctk.CTkEntry(self.config_frame, placeholder_text="如果稿件为转载，请填写来源")
        self.source_entry.grid(row=4, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        self.interval_label = ctk.CTkLabel(self.config_frame, text="上传间隔(小时):")
        self.interval_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.interval_entry = ctk.CTkEntry(self.config_frame)
        self.interval_entry.grid(row=5, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        
        self.save_button = ctk.CTkButton(self.config_frame, text="保存配置", command=self.save_config)
        self.save_button.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")
        self.control_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.manual_upload_button = ctk.CTkButton(self.control_frame, text="立即上传一个视频", command=self.trigger_manual_upload)
        self.manual_upload_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.auto_upload_start_button = ctk.CTkButton(self.control_frame, text="开始自动上传", fg_color="green", command=self.start_auto_upload)
        self.auto_upload_start_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.auto_upload_stop_button = ctk.CTkButton(self.control_frame, text="停止自动上传", fg_color="red", command=self.stop_auto_upload, state="disabled")
        self.auto_upload_stop_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.log_frame.grid_columnconfigure(0, weight=1)
        self.log_frame.grid_rowconfigure(0, weight=1)

        self.log_textbox = ctk.CTkTextbox(self.log_frame, state="disabled")
        self.log_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.load_config()
        self.log("程序已启动。内核已切换为 biliup-rs。")
        self.log(f"将使用 {self.BILIUP_COOKIE_FILE} 作为登录凭证。")

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"[{timestamp}] {message}\n"
        def _update_textbox():
            self.log_textbox.configure(state="normal")
            self.log_textbox.insert("end", full_message)
            self.log_textbox.configure(state="disabled")
            self.log_textbox.see("end")
        self.after(0, _update_textbox)

    def select_folder(self, entry_widget):
        folder_path = filedialog.askdirectory()
        if folder_path:
            entry_widget.delete(0, "end")
            entry_widget.insert(0, folder_path)
            self.log(f"已选择文件夹: {folder_path}")

    def save_config(self):
        config_data = {
            "video_path": self.video_path_entry.get(),
            "uploaded_path": self.uploaded_path_entry.get(),
            "interval": self.interval_entry.get(),
            "copyright": self.copyright_var.get(),
            "source": self.source_entry.get(),
        }
        try:
            with open(self.CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=4)
            self.log("配置已成功保存到 " + self.CONFIG_FILE)
        except Exception as e:
            self.log(f"错误：保存配置失败！ {e}")

    def load_config(self):
        try:
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
                    config_data = json.load(f)
                self.video_path_entry.insert(0, config_data.get("video_path", ""))
                self.uploaded_path_entry.insert(0, config_data.get("uploaded_path", ""))
                self.interval_entry.insert(0, config_data.get("interval", "4"))
                self.copyright_var.set(config_data.get("copyright", "转载"))
                self.source_entry.insert(0, config_data.get("source", ""))
                self.log("已成功加载本地配置。")
        except Exception as e:
            self.log(f"错误：加载配置失败！可能是配置文件损坏。 {e}")

    def trigger_manual_upload(self):
        self.log("手动上传任务已触发...")
        upload_thread = threading.Thread(target=self._upload_task_with_biliup)
        upload_thread.daemon = True
        upload_thread.start()

    def _upload_task_with_biliup(self):
        try:
            video_path = self.video_path_entry.get()
            uploaded_path = self.uploaded_path_entry.get()

            if not all([video_path, uploaded_path]):
                self.log("错误：配置不完整！请填写文件夹路径。")
                return
            
            if not os.path.exists(self.BILIUP_COOKIE_FILE):
                self.log(f"错误：未找到 biliup-rs 的 Cookie 文件: {self.BILIUP_COOKIE_FILE}")
                self.log("请先在终端手动运行 'biliup login' 完成一次登录。")
                return

            video_to_upload = None
            for filename in sorted(os.listdir(video_path)):
                if filename.lower().endswith(('.mp4', '.flv', '.avi', '.mkv', '.mov')):
                    video_to_upload = os.path.join(video_path, filename)
                    break
            
            if not video_to_upload:
                self.log("在待上传文件夹中没有找到视频文件。")
                return

            self.log(f"找到视频文件，准备使用 biliup-rs 上传: {os.path.basename(video_to_upload)}")

            title = os.path.splitext(os.path.basename(video_to_upload))[0]
            copyright_val = "1" if self.copyright_var.get() == "自制" else "2"
            source_val = self.source_entry.get()

            if copyright_val == "2" and not source_val:
                self.log("错误：稿件类型为转载时，必须填写转载来源！")
                return

            biliup_path = os.path.expanduser("~/bin/biliup")
            command = [
                biliup_path, "upload",
                "--submit", "app",
                "--copyright", copyright_val,
                "--source", source_val,
                "--tid", "171",
                "--title", title,
                "--desc", f"{title} - by biliup-rs uploader",
                video_to_upload
            ]

            self.log(f"执行命令: {' '.join(command)}")

            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', cwd=os.path.expanduser("~"))

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.log(output.strip())

            if process.returncode == 0:
                self.log("biliup-rs 内核报告上传成功！")
                shutil.move(video_to_upload, os.path.join(uploaded_path, os.path.basename(video_to_upload)))
                self.log("文件移动成功。本次上传任务完成！")
            else:
                self.log(f"biliup-rs 内核报告上传失败！退出码: {process.returncode}")

        except Exception as e:
            self.log(f"上传失败！发生严重错误: {e}")

    def _scheduler_loop(self):
        self.log("后台调度器已启动。")
        while self.scheduler_running:
            schedule.run_pending()
            time.sleep(1)
        self.log("后台调度器已停止。")

    def start_auto_upload(self):
        if self.scheduler_running:
            self.log("自动上传任务已在运行中。")
            return
        
        try:
            interval = float(self.interval_entry.get())
            if interval <= 0:
                raise ValueError("Interval must be positive")
        except ValueError:
            self.log("错误：上传间隔必须是一个有效的小时数（如 4, 0.5）。")
            return

        self.scheduler_running = True
        schedule.clear()
        schedule.every(interval).hours.do(self.trigger_manual_upload)
        
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()

        self.auto_upload_start_button.configure(state="disabled")
        self.auto_upload_stop_button.configure(state="normal")
        self.log(f"自动上传任务已启动，每 {interval} 小时执行一次。")

    def stop_auto_upload(self):
        if not self.scheduler_running:
            self.log("自动上传任务尚未运行。")
            return
        
        self.scheduler_running = False
        schedule.clear()
        self.auto_upload_start_button.configure(state="normal")
        self.auto_upload_stop_button.configure(state="disabled")
        self.log("自动上传任务已停止。")

    def on_closing(self):
        self.log("正在关闭程序...")
        self.stop_auto_upload()
        self.destroy()

if __name__ == "__main__":
    app = BiliUploaderApp()
    app.mainloop()
