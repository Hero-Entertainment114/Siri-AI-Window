import asyncio
import glob
import json
import math
import os
import platform
import re
import subprocess
import sys
import threading
import time
import webbrowser

import google.genai as genai
from google.genai import types
import psutil
import pyautogui
import pygame
from PyQt5.QtCore import QPoint, QRectF, QThread, QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QLinearGradient, QPainter, QRadialGradient
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
import speech_recognition as sr
from edge_tts import Communicate

CONFIG_FILE = "siri_config.json"

DEFAULT_GEMINI_KEY = ""

DEFAULT_VOICES_BY_LANG = {
    "vi-VN": "vi-VN-HoaiMyNeural",
    "en-US": "en-US-AvaMultilingualNeural",
    "ja-JP": "ja-JP-NanamiNeural",
    "zh-CN": "zh-CN-XiaoxiaoNeural",
    "ko-KR": "ko-KR-SunHiNeural",
    "fr-FR": "fr-FR-DeniseNeural",
    "de-DE": "de-DE-KatjaNeural",
    "es-ES": "es-ES-ElviraNeural",
    "auto": "en-US-AvaMultilingualNeural",
}


def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "api_key": "",
        "model": "gemini-3.6-flash",
        "tts_speed": 15,
        "input_mode": "voice",
        "voice_gender": "en-US-AvaMultilingualNeural",
        "language": "en-US",
    }


def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)


# =========================================================
# 📜 STARTUP DISCLAIMER & LICENSE DIALOG (ENGLISH)
# =========================================================
class StartupDisclaimerDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📜 Terms of Use & AI Disclaimer")
        self.resize(540, 480)
        self.setStyleSheet("""
            QDialog { background-color: #121212; color: #FFFFFF; font-family: 'Segoe UI', sans-serif; }
            QTextEdit { 
                background-color: #1E1E2E; 
                border: 1px solid #333344; 
                border-radius: 8px; 
                padding: 12px; 
                color: #E0E0E0; 
                font-size: 13px;
            }
            QPushButton#btn_accept { 
                background-color: #198754; 
                color: white; 
                border-radius: 8px; 
                padding: 10px 20px; 
                font-weight: bold; 
            }
            QPushButton#btn_accept:hover { background-color: #157347; }
            QPushButton#btn_decline { 
                background-color: #DC3545; 
                color: white; 
                border-radius: 8px; 
                padding: 10px 20px; 
                font-weight: bold; 
            }
            QPushButton#btn_decline:hover { background-color: #BB2D3B; }
        """)

        layout = QVBoxLayout(self)

        lbl_title = QLabel("📜 COPYRIGHT TERMS & AI DISCLAIMER")
        lbl_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #0D6EFD; margin-bottom: 5px;")
        layout.addWidget(lbl_title, alignment=Qt.AlignCenter)

        self.txt_content = QTextEdit()
        self.txt_content.setReadOnly(True)
        self.txt_content.setHtml("""
            <h4 style='color: #0D6EFD; margin-bottom: 4px;'>1. License & Commercial Usage</h4>
            <p>• This software is <b>Open Source</b>. You are free to copy, modify, and distribute it for personal or educational purposes.</p>
            <p>• <b>Mandatory Requirement:</b> If you integrate or use this source code or application in any <b>commercial project</b>, you <u>must give proper credit and include the Author's name</u> in the project's Credits/Acknowledgements section.</p>

            <h4 style='color: #FFC107; margin-bottom: 4px;'>2. Disclaimer of Liability</h4>
            <p>• The software is provided <b>"AS IS"</b>, without warranty of any kind, express or implied.</p>
            <p>• The author shall not be held liable for any damages, system errors, data loss, or unexpected system behavior arising directly or indirectly from operating this software.</p>

            <h4 style='color: #20C997; margin-bottom: 4px;'>3. Important AI Usage Guidelines</h4>
            <p>• <b>Accuracy & Reliability:</b> AI responses and automated tasks are provided for reference only. AI models may hallucinate or execute commands incorrectly.</p>

            <p>• <b>Data Privacy:</b> Never disclose <b>sensitive personal details</b> (e.g., passwords, banking information, confidential records) during interactions.</p>
            <p>• <b>API Key Security:</b> You are solely responsible for securing your Gemini API Key. Keep your keys private to avoid quota abuse or unauthorized access.</p>
        """)
        layout.addWidget(self.txt_content)

        btn_box = QHBoxLayout()
        self.btn_decline = QPushButton("Decline and Exit")
        self.btn_decline.setObjectName("btn_decline")
        self.btn_decline.clicked.connect(self.reject)

        self.btn_accept = QPushButton("I Agree and Continue")
        self.btn_accept.setObjectName("btn_accept")
        self.btn_accept.clicked.connect(self.accept)

        btn_box.addWidget(self.btn_decline)
        btn_box.addWidget(self.btn_accept)
        layout.addLayout(btn_box)


# =========================================================
# 🛠️ SYSTEM CONTROLLER MODULE
# =========================================================
class SystemController:

    @staticmethod
    def search_and_open(target_name):
        target_name = target_name.strip()
        if not target_name:
            return "Invalid file or app name."

        if os.path.exists(target_name):
            try:
                os.startfile(target_name)
                return f"Opened directly: {target_name}"
            except Exception as e:
                return f"Error opening path: {str(e)}"

        drives = [
            f"{d}:\\"
            for d in "CDEFGHIJKLMNOPQRSTUVWXYZ"
            if os.path.exists(f"{d}:\\")
        ]
        user_profile = os.environ.get("USERPROFILE", "")

        priority_paths = [
            os.path.join(user_profile, "Desktop"),
            os.path.join(user_profile, "Downloads"),
            os.path.join(user_profile, "Documents"),
            os.path.join(user_profile, "Pictures"),
            os.path.join(user_profile, "Videos"),
            r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
            os.path.join(
                user_profile,
                r"AppData\Roaming\Microsoft\Windows\Start Menu\Programs",
            ),
        ]

        for d in drives:
            if d.upper() != "C:\\" and d not in priority_paths:
                priority_paths.append(d)

        for base_path in priority_paths:
            if os.path.exists(base_path):
                for root, dirs, files in os.walk(base_path):
                    if (
                        "$Recycle.Bin" in root
                        or "System Volume Information" in root
                    ):
                        continue

                    depth = root.count(os.sep) - base_path.count(os.sep)
                    if depth > 5:
                        continue

                    for item in dirs + files:
                        if target_name.lower() in item.lower():
                            full_path = os.path.join(root, item)
                            try:
                                os.startfile(full_path)
                                return f"Found and opened: {item} at ({full_path})"
                            except Exception:
                                pass

        try:
            res = subprocess.run(
                ["where", target_name], capture_output=True, text=True
            )
            if res.returncode == 0:
                exe_path = res.stdout.splitlines()[0]
                os.startfile(exe_path)
                return f"Opened system app: {target_name}"
        except Exception:
            pass

        return f"File, folder, or application '{target_name}' not found."

    @staticmethod
    def stop_application(app_name):
        app_name = app_name.strip()
        if not app_name:
            return "Invalid application name."

        if not app_name.endswith('.exe'):
            app_name += '.exe'
            
        closed = False
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() == app_name.lower():
                    proc.kill()
                    closed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        if closed:
            return f"Closed application: {app_name}"
        return f"Application '{app_name}' is not running."

    @staticmethod
    def execute_cmd_in_new_window(command):
        try:
            subprocess.Popen(f'start cmd /k "{command}"', shell=True)
            return f"Opened CMD and executed command: {command}"
        except Exception as e:
            return f"Error executing command: {str(e)}"

    @staticmethod
    def get_full_sys_info():
        uname = platform.uname()
        cpu_usage = psutil.cpu_percent(interval=0.3)
        ram = psutil.virtual_memory()
        disk = (
            psutil.disk_usage("C:\\")
            if os.path.exists("C:\\")
            else psutil.disk_usage("/")
        )

        return (
            f"System Specifications:\n"
            f"- OS: {uname.system} {uname.release} ({uname.machine})\n"
            f"- CPU: {uname.processor or uname.machine} (Usage: {cpu_usage}%)\n"
            f"- RAM: Total {ram.total // (1024**3)} GB (Usage: {ram.percent}%)\n"
            f"- Drive (C:): Total {disk.total // (1024**3)} GB, Free {disk.free // (1024**3)} GB."
        )


# =========================================================
# 🌌 SIRI GLOWING ORB OVERLAY
# =========================================================
class SiriOverlayWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(200, 200)

        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = screen.height() - self.height() - 20
        self.move(x, y)

        self.phase = 0
        self.state = "idle"

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)

    def set_state(self, state):
        self.state = state
        self.update()

    def update_animation(self):
        self.phase += 0.05
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center = QPoint(self.width() // 2, self.height() // 2)
        base_radius = 50

        if self.state == "listening":
            pulse = math.sin(self.phase * 3) * 8
            c1, c2 = QColor(0, 180, 255, 200), QColor(140, 0, 255, 180)
        elif self.state == "thinking":
            pulse = math.sin(self.phase * 6) * 4
            c1, c2 = QColor(255, 0, 150, 200), QColor(0, 255, 200, 180)
        elif self.state == "speaking":
            pulse = abs(math.sin(self.phase * 5)) * 14
            c1, c2 = QColor(0, 255, 120, 220), QColor(0, 120, 255, 200)
        else:
            pulse = math.sin(self.phase) * 3
            c1, c2 = QColor(100, 100, 255, 120), QColor(50, 0, 150, 100)

        radius = base_radius + pulse
        grad = QRadialGradient(center, radius * 1.4)
        grad.setColorAt(0.0, c1)
        grad.setColorAt(0.5, c2)
        grad.setColorAt(1.0, QColor(0, 0, 0, 0))

        painter.setBrush(grad)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center, int(radius * 1.3), int(radius * 1.3))


# =========================================================
# 💬 CHAT WINDOW
# =========================================================
class ChatWindow(QWidget):
    sig_send_msg = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Siri Chat - Text Mode")
        self.resize(480, 580)
        self.setStyleSheet("""
            QWidget { background-color: #121212; color: #FFFFFF; font-family: 'Segoe UI'; }
            QTextEdit { background-color: #1E1E2E; border: 1px solid #333344; border-radius: 8px; padding: 10px; font-size: 14px; color: #FFFFFF; }
            QLineEdit { background-color: #1E1E2E; border: 1px solid #333344; border-radius: 8px; padding: 8px; color: #FFFFFF; font-size: 14px; }
            QPushButton { background-color: #0D6EFD; color: white; border-radius: 8px; padding: 8px 16px; font-weight: bold; }
            QPushButton:hover { background-color: #0B5ED7; }
        """)

        layout = QVBoxLayout(self)

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        layout.addWidget(self.chat_history)

        input_box = QHBoxLayout()
        self.txt_input = QLineEdit()
        self.txt_input.setPlaceholderText("Type a question or command for Siri...")
        self.txt_input.returnPressed.connect(self.send_message)

        self.btn_send = QPushButton("Send")
        self.btn_send.clicked.connect(self.send_message)

        input_box.addWidget(self.txt_input)
        input_box.addWidget(self.btn_send)
        layout.addLayout(input_box)

    def send_message(self):
        text = self.txt_input.text().strip()
        if text:
            self.txt_input.clear()
            self.sig_send_msg.emit(text)

    def append_log(self, sender, message):
        color = "#0D6EFD" if sender == "User" else "#198754"
        if sender == "System":
            color = "#FFC107"
        self.chat_history.append(
            f"<b style='color: {color};'>{sender}:</b> {message}<br>"
        )


# =========================================================
# 🎙️ WORKER THREAD
# =========================================================
class SiriWorker(QThread):
    sig_status = pyqtSignal(str)
    sig_log = pyqtSignal(str, str)
    sig_error = pyqtSignal(str)
    sig_open_settings = pyqtSignal()
    sig_toggle_overlay = pyqtSignal(bool)

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.is_running = True

        self.api_keys = []
        self.current_key_idx = 0
        self.client = None
        self.chat_session = None
        self.current_model_name = ""

        self.parse_api_keys()

        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.6
        self.recognizer.dynamic_energy_threshold = True

        try:
            pygame.mixer.init()
        except Exception as e:
            self.sig_error.emit(f"Pygame audio init error: {str(e)}")

    def parse_api_keys(self):
        raw_keys = self.config.get("api_key", "").strip()
        if not raw_keys:
            raw_keys = DEFAULT_GEMINI_KEY

        keys = [k.strip() for k in re.split(r"[,;]", raw_keys) if k.strip()]
        self.api_keys = keys if keys else []
        self.current_key_idx = 0
        self.client = None
        self.chat_session = None

    def update_config(self, new_config):
        self.config = new_config
        self.parse_api_keys()

    def get_client(self):
        if not self.api_keys:
            self.sig_error.emit("API Key is not configured!")
            return None

        key = self.api_keys[self.current_key_idx]
        try:
            self.client = genai.Client(api_key=key)
            return self.client
        except Exception as e:
            self.sig_error.emit(f"Error creating API Key client: {str(e)}")
            return None

    def rotate_key(self):
        if len(self.api_keys) > 1:
            self.current_key_idx = (self.current_key_idx + 1) % len(self.api_keys)
            self.sig_log.emit("System", f"🔄 Switched to Key {self.current_key_idx + 1}/{len(self.api_keys)}")
            self.client = None
            self.chat_session = None
        else:
            self.sig_error.emit("API Key error or quota exceeded!")

    def init_ai_memory(self):
        model_name = self.config.get("model", "gemini-3.6-flash")
        lang_mode = self.config.get("language", "en-US")

        if lang_mode == "vi-VN":
            lang_instruction = "Respond strictly in Vietnamese (concise, under 5 sentences)."
        elif lang_mode == "en-US":
            lang_instruction = "Respond strictly in English (concise, under 5 sentences)."
        elif lang_mode == "ja-JP":
            lang_instruction = "Respond strictly in Japanese (concise, under 5 sentences)."
        elif lang_mode == "zh-CN":
            lang_instruction = "Respond strictly in Simplified Chinese (concise, under 5 sentences)."
        elif lang_mode == "ko-KR":
            lang_instruction = "Respond strictly in Korean (concise, under 5 sentences)."
        elif lang_mode == "fr-FR":
            lang_instruction = "Respond strictly in French (concise, under 5 sentences)."
        elif lang_mode == "de-DE":
            lang_instruction = "Respond strictly in German (concise, under 5 sentences)."
        elif lang_mode == "es-ES":
            lang_instruction = "Respond strictly in Spanish (concise, under 5 sentences)."
        else:
            lang_instruction = "Always reply in the EXACT SAME language as the user's input message."

        if not self.chat_session or self.current_model_name != model_name:
            sys_instruct = f"You are Siri, an intelligent desktop assistant. {lang_instruction}"
            client = self.get_client()
            if client:
                try:
                    self.chat_session = client.chats.create(
                        model=model_name,
                        config=types.GenerateContentConfig(system_instruction=sys_instruct),
                    )
                    self.current_model_name = model_name
                except Exception as e:
                    self.sig_error.emit(f"AI Init Error ({model_name}): {str(e)}")

    def get_effective_voice(self):
        configured_voice = self.config.get("voice_gender", "")
        lang_code = self.config.get("language", "en-US")

        if configured_voice.endswith("MultilingualNeural"):
            return configured_voice

        if lang_code in DEFAULT_VOICES_BY_LANG:
            expected_prefix = lang_code.split("-")[0]
            if not configured_voice.startswith(expected_prefix):
                return DEFAULT_VOICES_BY_LANG[lang_code]

        return configured_voice or "en-US-AvaMultilingualNeural"

    def speak(self, text):
        if not text or not text.strip():
            return

        self.sig_status.emit("speaking")
        speed_val = self.config.get("tts_speed", 15)
        speed_str = f"{'+' if speed_val >= 0 else ''}{speed_val}%"
        voice = self.get_effective_voice()
        output_file = "temp_siri.mp3"

        async def _gen():
            try:
                comm = Communicate(text, voice, rate=speed_str)
                await comm.save(output_file)
            except Exception as e:
                self.sig_error.emit(f"Edge-TTS Error ({voice}): {str(e)}")

        try:
            asyncio.run(_gen())

            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()

                pygame.mixer.music.load(output_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(20)

                pygame.mixer.music.unload()
                try:
                    os.remove(output_file)
                except Exception:
                    pass
        except Exception as e:
            self.sig_error.emit(f"TTS Playback Error: {str(e)}")

        self.sig_status.emit("idle")

    def parse_user_intents(self, user_prompt):
        model_name = self.config.get("model", "gemini-3.6-flash")
        lang_code = self.config.get("language", "en-US")

        prompt = f"""
        You are an intent parser for Siri AI assistant.
        Analyze the user input and extract JSON actions.
        
        CRITICAL RULE FOR "chat" type:
        The "message" field MUST be written in the target language configured ({lang_code}) or in the exact same language as the user prompt!

        Return ONLY a JSON array, no markdown formatting:
        [
          {{"type": "open", "target": "app_file_or_folder_name"}},
          {{"type": "close", "target": "app_name_or_process"}},
          {{"type": "cmd", "command": "cmd_command_to_run"}},
          {{"type": "mouse_move", "x": 500, "y": 300}},
          {{"type": "sys_info"}},
          {{"type": "open_settings"}},
          {{"type": "search_web", "query": "search_keyword"}},
          {{"type": "chat", "message": "direct_response_in_user_language"}}
        ]

        User Input: "{user_prompt}"
        """

        for _ in range(max(1, len(self.api_keys))):
            try:
                client = self.get_client()
                if not client:
                    break
                response = client.models.generate_content(
                    model=model_name, contents=prompt
                )
                clean_json = (
                    response.text.replace("```json", "")
                    .replace("```", "")
                    .strip()
                )
                return json.loads(clean_json)
            except Exception:
                self.rotate_key()

        return [{"type": "chat_fallback", "query": user_prompt}]

    def send_chat_message_with_fallback(self, query):
        for _ in range(max(1, len(self.api_keys))):
            try:
                self.init_ai_memory()
                if self.chat_session:
                    response = self.chat_session.send_message(query)
                    return response.text.strip()
            except Exception:
                self.rotate_key()
        return None

    def process_query(self, query):
        if not query:
            return

        query_clean = query.strip().lower()

        if any(cmd in query_clean for cmd in ["open settings", "mở cài đặt", "mở cài đặt ai"]):
            self.sig_open_settings.emit()
            res = "Opened settings window." if self.config.get("language") != "vi-VN" else "Đã mở giao diện cài đặt."
            self.sig_log.emit("Siri", res)
            self.speak(res)
            return

        self.sig_log.emit("User", query)
        self.sig_status.emit("thinking")

        actions = self.parse_user_intents(query)

        for act in actions:
            act_type = act.get("type")

            if act_type == "open":
                target = act.get("target", "")
                res = SystemController.search_and_open(target)
                self.sig_log.emit("Siri", res)
                self.speak(res)

            elif act_type == "close":
                target = act.get("target", "")
                res = SystemController.stop_application(target)
                self.sig_log.emit("Siri", res)
                self.speak(res)

            elif act_type == "cmd":
                cmd = act.get("command", "")
                res = SystemController.execute_cmd_in_new_window(cmd)
                self.sig_log.emit("Siri", res)
                self.speak(res)

            elif act_type == "mouse_move":
                x = act.get("x", 0)
                y = act.get("y", 0)
                try:
                    pyautogui.moveTo(int(x), int(y), duration=0.2)
                    res = (
                        f"Moved mouse to coordinates ({x}, {y})."
                        if self.config.get("language") != "vi-VN"
                        else f"Đã di chuyển chuột đến tọa độ ({x}, {y})."
                    )
                except Exception as e:
                    res = f"Error moving mouse: {str(e)}"
                self.sig_log.emit("Siri", res)
                self.speak(res)

            elif act_type == "sys_info":
                res = SystemController.get_full_sys_info()
                self.sig_log.emit("Siri", res)
                self.speak("System details checked.")

            elif act_type == "open_settings":
                self.sig_open_settings.emit()
                res = "Opened settings window." if self.config.get("language") != "vi-VN" else "Đã mở giao diện cài đặt."
                self.sig_log.emit("Siri", res)
                self.speak(res)

            elif act_type == "search_web":
                kw = act.get("query", "")
                webbrowser.open(f"https://www.google.com/search?q={kw}")
                res = f"Searched for: {kw}"
                self.sig_log.emit("Siri", res)
                self.speak(res)

            elif act_type == "chat":
                msg = act.get("message", "")
                self.sig_log.emit("Siri", msg)
                self.speak(msg)

            elif act_type == "chat_fallback":
                q_text = act.get("query", query)
                reply = self.send_chat_message_with_fallback(q_text)
                if reply:
                    self.sig_log.emit("Siri", reply)
                    self.speak(reply)
                else:
                    err_msg = "API Key Error or Quota Exceeded!"
                    self.sig_error.emit(err_msg)
                    self.sig_log.emit("Siri", err_msg)
                    self.speak(err_msg)

        self.sig_status.emit("idle")

    def recognize_audio(self, audio, lang_code):
        """Automatically prioritizes the selected language with dynamic speech fallback"""
        candidates = []
        if lang_code and lang_code != "auto":
            candidates.append(lang_code)

        supported_langs = ["en-US", "vi-VN", "ja-JP", "zh-CN", "ko-KR", "fr-FR", "de-DE", "es-ES"]
        for l in supported_langs:
            if l not in candidates:
                candidates.append(l)

        for lang in candidates[:3]:
            try:
                text = self.recognizer.recognize_google(audio, language=lang)
                if text and text.strip():
                    return text.strip()
            except (sr.UnknownValueError, sr.RequestError):
                continue
            except Exception:
                continue
        return ""

    def run(self):
        wake_words = [
            "xin chào", "hello", "hi siri", "siri", "chào siri",
            "こんにちは", "コンニチハ", "こんにちは siri",
            "ni hao", "你好", "안녕", "안녕하세요"
        ]

        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                self.recognizer.dynamic_energy_threshold = True

                while self.is_running:
                    if self.config.get("input_mode") == "voice":
                        try:
                            lang_code = self.config.get("language", "en-US")

                            self.recognizer.pause_threshold = 0.6
                            audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=4)

                            text = self.recognize_audio(audio, lang_code).lower()

                            if any(kw in text for kw in wake_words):
                                self.sig_toggle_overlay.emit(True)
                                self.sig_status.emit("listening")

                                greeting = "Hi! How can I help you?"
                                if lang_code == "vi-VN":
                                    greeting = "Chào bạn! Tôi có thể giúp gì cho bạn?"
                                elif lang_code == "ja-JP":
                                    greeting = "こんにちは！何かお手伝いできますか？"
                                elif lang_code == "zh-CN":
                                    greeting = "你好！有什么我可以帮您的吗？"
                                elif lang_code == "ko-KR":
                                    greeting = "안녕하세요! 무엇을 도와드릴까요？"
                                elif lang_code == "fr-FR":
                                    greeting = "Bonjour! Comment puis-je vous aider?"
                                elif lang_code == "de-DE":
                                    greeting = "Hallo! Wie kann ich Ihnen helfen?"
                                elif lang_code == "es-ES":
                                    greeting = "¡Hola! ¿En qué puedo ayudarte?"

                                self.speak(greeting)

                                try:
                                    self.sig_status.emit("listening")
                                    self.recognizer.pause_threshold = 0.8
                                    cmd_audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=15)

                                    self.sig_status.emit("thinking")
                                    cmd_text = self.recognize_audio(cmd_audio, lang_code)
                                    if cmd_text:
                                        self.process_query(cmd_text)
                                except Exception:
                                    self.sig_status.emit("idle")

                                self.sig_toggle_overlay.emit(False)

                        except sr.UnknownValueError:
                            pass
                        except sr.WaitTimeoutError:
                            pass
                        except Exception:
                            time.sleep(0.2)
                    else:
                        time.sleep(0.3)
        except Exception as e:
            self.sig_error.emit(f"Unable to access the Microphone: {str(e)}")


# =========================================================
# ⚙️ MAIN SETTINGS WINDOW (ENGLISH INTERFACE)
# =========================================================
class SiriSettingsWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.config = load_config()

        self.overlay_window = SiriOverlayWindow()
        self.chat_window = ChatWindow()
        self.chat_window.sig_send_msg.connect(self.handle_text_query)

        self.initUI()
        self.start_worker()

    def start_worker(self):
        self.worker = SiriWorker(self.config)
        self.worker.sig_status.connect(self.overlay_window.set_state)
        self.worker.sig_log.connect(self.chat_window.append_log)
        self.worker.sig_error.connect(self.show_error_dialog)
        self.worker.sig_open_settings.connect(self.show_settings_window)
        self.worker.sig_toggle_overlay.connect(self.toggle_overlay)
        self.worker.start()

    def toggle_overlay(self, show):
        if show:
            self.overlay_window.show()
        else:
            self.overlay_window.hide()

    def show_settings_window(self):
        self.show()
        self.activateWindow()

    def show_error_dialog(self, error_msg):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Siri System Error")
        msg_box.setText(error_msg)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setStyleSheet("""
            QMessageBox { background-color: #1E1E2E; }
            QLabel { color: #FFFFFF; font-size: 13px; }
            QPushButton { background-color: #0D6EFD; color: #FFFFFF; border-radius: 6px; padding: 6px 14px; font-weight: bold; min-width: 70px; }
            QPushButton:hover { background-color: #0B5ED7; }
        """)
        msg_box.exec_()

    def handle_text_query(self, text):
        if hasattr(self, "worker"):
            threading.Thread(
                target=self.worker.process_query, args=(text,)
            ).start()

    def initUI(self):
        self.setWindowTitle("Siri AI - System Settings")
        self.resize(460, 640)

        self.setStyleSheet("""
            QMainWindow { background-color: #121212; }
            QWidget { color: #FFFFFF; font-family: 'Segoe UI', sans-serif; }
            QLineEdit { background-color: #1E1E2E; border: 1px solid #333344; border-radius: 8px; padding: 8px; color: #FFFFFF; }
            
            QComboBox { 
                background-color: #1E1E2E; 
                color: #FFFFFF; 
                border: 1px solid #333344; 
                border-radius: 8px; 
                padding: 6px 10px; 
                font-weight: bold; 
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView { 
                background-color: #1E1E2E; 
                color: #FFFFFF; 
                selection-background-color: #0D6EFD; 
                selection-color: #FFFFFF;
                border: 1px solid #333344;
                outline: none;
            }
            
            QPushButton { background-color: #198754; color: white; border-radius: 8px; padding: 10px; font-weight: bold; }
            QPushButton:hover { background-color: #157347; }
            QSlider::groove:horizontal { height: 6px; background: #333344; border-radius: 3px; }
            QSlider::handle:horizontal { background: #0D6EFD; width: 16px; margin: -5px 0; border-radius: 8px; }
            
            QMessageBox { background-color: #1E1E2E; }
            QMessageBox QLabel { color: #FFFFFF; font-size: 13px; }
            QMessageBox QPushButton { background-color: #0D6EFD; color: #FFFFFF; border-radius: 6px; padding: 6px 14px; font-weight: bold; min-width: 80px; }
            QMessageBox QPushButton:hover { background-color: #0B5ED7; }
        """)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        lbl_title = QLabel("⚙️ SIRI AI SETTINGS")
        lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(lbl_title, alignment=Qt.AlignCenter)

        layout.addWidget(QLabel("Gemini API Keys (separated by commas):"))
        self.txt_api_key = QLineEdit()
        self.txt_api_key.setEchoMode(QLineEdit.Password)
        self.txt_api_key.setPlaceholderText("AQ.Ab8RN6..., AQ.Ab8RN7...")
        self.txt_api_key.setText(self.config.get("api_key", ""))
        layout.addWidget(self.txt_api_key)

        layout.addWidget(QLabel("AI Model:"))
        self.cbo_model = QComboBox()
        self.cbo_model.addItems(["gemini-3.6-flash", "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"])
        self.cbo_model.setCurrentText(self.config.get("model", "gemini-3.6-flash"))
        layout.addWidget(self.cbo_model)

        layout.addWidget(QLabel("Communication Language:"))
        self.cbo_language = QComboBox()
        self.cbo_language.addItem("English (US)", "en-US")
        self.cbo_language.addItem("Vietnamese (vi-VN)", "vi-VN")
        self.cbo_language.addItem("Japanese (ja-JP)", "ja-JP")
        self.cbo_language.addItem("Chinese (zh-CN)", "zh-CN")
        self.cbo_language.addItem("Korean (ko-KR)", "ko-KR")
        self.cbo_language.addItem("French (fr-FR)", "fr-FR")
        self.cbo_language.addItem("German (de-DE)", "de-DE")
        self.cbo_language.addItem("Spanish (es-ES)", "es-ES")
        self.cbo_language.addItem("Auto / Multilingual", "auto")
        
        current_lang = self.config.get("language", "en-US")
        idx = self.cbo_language.findData(current_lang)
        if idx >= 0:
            self.cbo_language.setCurrentIndex(idx)
        layout.addWidget(self.cbo_language)

        self.lbl_speed = QLabel(f"Voice Speed: +{self.config.get('tts_speed', 15)}%")
        layout.addWidget(self.lbl_speed)
        self.slider_speed = QSlider(Qt.Horizontal)
        self.slider_speed.setRange(-20, 60)
        self.slider_speed.setValue(self.config.get("tts_speed", 15))
        self.slider_speed.valueChanged.connect(
            lambda v: self.lbl_speed.setText(f"Voice Speed: {'+' if v >= 0 else ''}{v}%")
        )
        layout.addWidget(self.slider_speed)

        layout.addWidget(QLabel("Operation Mode:"))
        self.rad_voice = QRadioButton("Voice Mode (Say 'hello' in your language to activate.)")
        self.rad_text = QRadioButton("Text Mode (Show Chat Window)")

        if self.config.get("input_mode") == "voice":
            self.rad_voice.setChecked(True)
        else:
            self.rad_text.setChecked(True)

        layout.addWidget(self.rad_voice)
        layout.addWidget(self.rad_text)

        layout.addWidget(QLabel("Default TTS Voice:"))
        self.cbo_voice = QComboBox()
        self.cbo_voice.addItem("🌐 Female Multilingual (Ava)", "en-US-AvaMultilingualNeural")
        self.cbo_voice.addItem("🌐 Male Multilingual (Andrew)", "en-US-AndrewMultilingualNeural")
        self.cbo_voice.addItem("🇺🇸 Female English (Jenny)", "en-US-JennyNeural")
        self.cbo_voice.addItem("🇺🇸 Male English (Guy)", "en-US-GuyNeural")
        self.cbo_voice.addItem("🇻🇳 Female Vietnamese (Hoai My)", "vi-VN-HoaiMyNeural")
        self.cbo_voice.addItem("🇻🇳 Male Vietnamese (Nam Minh)", "vi-VN-NamMinhNeural")
        self.cbo_voice.addItem("🇯🇵 Female Japanese (Nanami)", "ja-JP-NanamiNeural")
        self.cbo_voice.addItem("🇯🇵 Male Japanese (Keita)", "ja-JP-KeitaNeural")
        self.cbo_voice.addItem("🇨🇳 Female Chinese (Xiaoxiao)", "zh-CN-XiaoxiaoNeural")
        self.cbo_voice.addItem("🇰🇷 Female Korean (Sun-Hi)", "ko-KR-SunHiNeural")
        self.cbo_voice.addItem("🇫🇷 Female French (Denise)", "fr-FR-DeniseNeural")
        self.cbo_voice.addItem("🇩🇪 Female German (Katja)", "de-DE-KatjaNeural")
        self.cbo_voice.addItem("🇪🇸 Female Spanish (Elvira)", "es-ES-ElviraNeural")

        curr_voice = self.config.get("voice_gender", "en-US-AvaMultilingualNeural")
        v_idx = self.cbo_voice.findData(curr_voice)
        if v_idx >= 0:
            self.cbo_voice.setCurrentIndex(v_idx)
        layout.addWidget(self.cbo_voice)

        btn_save = QPushButton("💾 Save Settings & Activate")
        btn_save.clicked.connect(self.apply_settings)
        layout.addWidget(btn_save)

        self.setCentralWidget(central_widget)

    def apply_settings(self):
        api_key_text = self.txt_api_key.text().strip()

        self.config["api_key"] = api_key_text
        self.config["model"] = self.cbo_model.currentText()
        self.config["language"] = self.cbo_language.currentData()
        self.config["tts_speed"] = self.slider_speed.value()
        self.config["input_mode"] = "voice" if self.rad_voice.isChecked() else "text"
        self.config["voice_gender"] = self.cbo_voice.currentData()

        save_config(self.config)

        if hasattr(self, "worker"):
            self.worker.update_config(self.config)

        if self.rad_voice.isChecked():
            self.chat_window.hide()
            self.overlay_window.hide()
        else:
            self.overlay_window.hide()
            self.chat_window.show()

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Notification")
        msg_box.setText("Settings saved successfully! Siri is ready.")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()

    def closeEvent(self, event):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Exit Options")
        msg_box.setText("Do you want to keep Siri running in the background or exit completely?")
        msg_box.setIcon(QMessageBox.Question)
        
        btn_background = msg_box.addButton("Run in Background", QMessageBox.AcceptRole)
        btn_exit = msg_box.addButton("Exit Completely", QMessageBox.RejectRole)
        btn_cancel = msg_box.addButton("Cancel", QMessageBox.DestructiveRole)

        msg_box.exec_()

        if msg_box.clickedButton() == btn_background:
            event.ignore()
            self.hide()
            if not self.rad_voice.isChecked():
                self.chat_window.show()
        elif msg_box.clickedButton() == btn_exit:
            if hasattr(self, "worker"):
                self.worker.is_running = False
                self.worker.quit()
            self.overlay_window.close()
            self.chat_window.close()
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Launch disclaimer dialog on application startup
    disclaimer_dialog = StartupDisclaimerDialog()
    if disclaimer_dialog.exec_() == QDialog.Accepted:
        window = SiriSettingsWindow()
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)