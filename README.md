<div align="center">

# 🎙️ Siri AI Desktop Assistant

### Trợ lý ảo AI đa ngôn ngữ dành cho Windows

<p>
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/GUI-PyQt5-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt5">
  <img src="https://img.shields.io/badge/AI-Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white" alt="Google Gemini">
  <img src="https://img.shields.io/badge/Voice-Edge--TTS-0078D4?style=for-the-badge&logo=microsoftedge&logoColor=white" alt="Edge-TTS">
  <img src="https://img.shields.io/badge/License-MIT-2EA44F?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="MIT">
</p>

<p>
  Trợ lý ảo desktop kết hợp <b>Google Gemini AI</b>, nhận diện giọng nói,
  tổng hợp giọng nói và khả năng tự động hóa Windows trong một giao diện hiện đại.
</p>

<p>
  <a href="#-tính-năng">Tính năng</a> •
  <a href="#-cài-đặt">Cài đặt</a> •
  <a href="#-api-key">API Key</a> •
  <a href="#-bản-quyền-license">Bản quyền</a> •
  <a href="#️-miễn-trừ-trách-nhiệm">Disclaimer</a>
</p>

</div>

---

## 📌 Giới thiệu

**Siri AI Desktop Assistant** là trợ lý ảo mã nguồn mở dành cho Windows, tập trung vào ba khả năng chính:

| 🧠 Hiểu lệnh | ⚙️ Hành động | 🔊 Phản hồi |
|---|---|---|
| Gemini phân tích yêu cầu bằng ngôn ngữ tự nhiên | Thực hiện thao tác trên Windows | Edge-TTS trả lời bằng giọng nói |
| Voice / Text Input | App, file, CMD, chuột, phần cứng | Nhiều ngôn ngữ & nhiều giọng đọc |

> **Ý tưởng cốt lõi:** người dùng nói điều cần làm, AI phân tích ý định, ứng dụng thực hiện hành động tương ứng.

---

## ✨ Tính năng

### 🎙️ Voice Assistant
- Kích hoạt bằng các từ khóa như `hello`, `siri`, `xin chào`, ...
- Nhận diện giọng nói qua **Google Speech Recognition**.
- Cho phép chuyển sang nhập lệnh bằng văn bản.

### 🧠 Gemini Intent Parsing
Gemini được dùng để hiểu câu lệnh và xác định hành động cần thực hiện.

| Ví dụ lệnh | Hành động |
|---|---|
| `mở Chrome` | Tìm và khởi chạy ứng dụng |
| `đóng Discord` | Đóng tiến trình tương ứng |
| `kiểm tra RAM` | Đọc thông tin phần cứng |
| `chạy ipconfig` | Mở CMD và thực thi lệnh |
| `di chuyển chuột tới 500 300` | Điều khiển con trỏ |

### 🖥️ Windows Automation

| Chức năng | Công nghệ |
|---|---|
| 🚀 Mở app / file / folder | Windows / Python |
| 🛑 Đóng tiến trình | `psutil` |
| 💻 Chạy lệnh CMD | Windows CMD |
| 🖱️ Điều khiển chuột | `pyautogui` |
| 📊 Kiểm tra CPU / RAM / ổ C: | System information |

### 🌍 Multi-language TTS

| Ngôn ngữ | Ví dụ giọng đọc |
|---|---|
| 🇻🇳 Tiếng Việt | Hoài Mỹ, Nam Minh |
| 🇺🇸 Tiếng Anh | Ava, Jenny, Guy |
| 🇯🇵 Tiếng Nhật | Nanami, Keita |
| 🇨🇳 Tiếng Trung | Nhiều voice |
| 🇰🇷 Tiếng Hàn | Nhiều voice |

### 🌌 UI

- 🔮 **Visual Orb**: thay đổi trạng thái giữa `Listening`, `Thinking`, `Speaking`.
- 💬 **Chat Window**: nhập và xem lệnh bằng văn bản.
- ⚙️ **Settings**: cấu hình API Key, voice, model và các tùy chọn liên quan.

---

## 🧱 Công nghệ

```text
Python 3.9+
├── PyQt5              → Giao diện
├── Google Gemini API  → AI / Intent Parsing
├── Speech Recognition → Nhận diện giọng nói
├── Edge-TTS           → Tổng hợp giọng nói
├── psutil             → Quản lý tiến trình & phần cứng
└── pyautogui          → Điều khiển chuột
```

---

## 📁 Cấu trúc dự án

```text
Siri-AI-Window/
├── siri.py
├── siri_config.json
├── requirements.txt
├── .gitignore
└── README.md
```

| File | Vai trò |
|---|---|
| `siri.py` | Mã nguồn chính |
| `siri_config.json` | API Key, voice, model và cấu hình cá nhân |
| `requirements.txt` | Danh sách dependency |
| `.gitignore` | File / thư mục loại khỏi Git |
| `README.md` | Tài liệu dự án |

> 🔐 **Không commit `siri_config.json` lên GitHub nếu file đang chứa API Key thật.**

---

## 🚀 Cài đặt

### 📦 Phương án A · Bản đóng gói

**Không cần cài Python.**

**1.** Mở mục **[Releases](../../releases)** của repository.

**2.** Tải:

```text
Siri-AI-v1.0-Trial.zip
```

**3.** Giải nén → chạy:

```text
siri.exe
```

**4.** Vào **Settings** → nhập Gemini API Key → **Save Settings & Activate**.

---

### 🐍 Phương án B · Chạy từ source

#### 1. Clone

```bash
git clone https://github.com/Hero-Entertainment114/Siri-AI-Window.git
cd Siri-AI-Window
```

#### 2. Tạo môi trường ảo

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

#### 3. Cài dependency

```bash
pip install -r requirements.txt
```

#### 4. Chạy

```bash
python siri.py
```

> **Yêu cầu:** Python **3.9+** và môi trường Windows phù hợp với các thư viện được liệt kê trong `requirements.txt`.

---

## 🔑 API Key

### BYOK · Bring Your Own Key

Ứng dụng sử dụng mô hình **BYOK**, tức người dùng tự cung cấp Gemini API Key.

Key được lưu trong:

```text
siri_config.json
```

### 🔄 Nhiều API Key

Có thể nhập nhiều key và phân tách bằng dấu phẩy:

```text
API_KEY_1,API_KEY_2,API_KEY_3
```

Ứng dụng hỗ trợ cơ chế xoay vòng key (`rotate_key`) để chuyển sang key khác khi key hiện tại gặp giới hạn sử dụng.

### 🔗 Tạo Gemini API Key

**Google AI Studio**  
https://aistudio.google.com/

> ⚠️ **API Key là thông tin bí mật. Không đăng công khai, không commit vào repository và không gửi cho người khác.**

---

## 🔒 Bảo mật & Quyền riêng tư

| Vấn đề | Chính sách |
|---|---|
| 🔑 API Key | Lưu cục bộ trong `siri_config.json` |
| 🎙️ Microphone | Dùng cho phiên nhận diện giọng nói |
| 💾 Audio | Dự án không chủ động lưu âm thanh thành file lâu dài |
| 🌐 API | Request có thể được gửi tới dịch vụ bên thứ ba cần thiết cho chức năng, đặc biệt là dịch vụ Google |
| 👀 Source Code | Có thể kiểm tra trực tiếp từ repository |

### ⚠️ Quan trọng

Khẳng định an toàn tuyệt đối là không phù hợp với bất kỳ phần mềm nào. Người dùng nên **tự kiểm tra source code, dependency và quyền truy cập** trước khi chạy trên máy quan trọng.

---

## ⚠️ Miễn trừ trách nhiệm

> ### ❗ SỬ DỤNG CÓ RỦI RO
>
> **Siri AI Desktop Assistant được cung cấp theo nguyên tắc `AS IS`, không có bất kỳ bảo đảm nào về tính chính xác, ổn định hoặc phù hợp cho một mục đích cụ thể.**
>
> Do ứng dụng có khả năng để AI thực hiện thao tác trên hệ điều hành, **người dùng tự chịu trách nhiệm đối với mọi câu lệnh đã cung cấp và mọi hậu quả phát sinh từ việc sử dụng phần mềm**.

Tác giả không chịu trách nhiệm đối với:

- Mất dữ liệu hoặc thay đổi dữ liệu ngoài ý muốn.
- Đóng, mở hoặc điều khiển nhầm ứng dụng / tiến trình.
- Lệnh hệ thống gây lỗi, mất cấu hình hoặc ảnh hưởng Windows.
- Thiệt hại phát sinh từ lỗi AI, lỗi thư viện hoặc dịch vụ bên thứ ba.
- Giới hạn, thay đổi API, chính sách hoặc hành vi của Google / Microsoft / nhà cung cấp khác.
- Bất kỳ thiệt hại trực tiếp, gián tiếp, ngẫu nhiên hoặc hậu quả nào phát sinh từ việc sử dụng phần mềm.

> 🛑 **Không giao cho AI các tác vụ có thể gây mất dữ liệu hoặc ảnh hưởng hệ thống nếu bạn chưa hiểu rõ tác động.**

---

## ©️ Bản quyền & License

### MIT License

Dự án được phát hành theo **MIT License**.

Điều đó cho phép bạn, theo các điều khoản của MIT License:

```text
✓ Sử dụng
✓ Sao chép
✓ Chỉnh sửa
✓ Phân phối
✓ Sử dụng trong dự án cá nhân
✓ Sử dụng trong dự án thương mại
```

### 📌 Điều kiện quan trọng

Nếu bạn sao chép, tái sử dụng hoặc phân phối mã nguồn của dự án, **vui lòng giữ lại thông báo bản quyền và giấy phép MIT**.

Thông tin tác giả gốc:

```text
Author:
Hero-Entertainment114

Repository:
https://github.com/Hero-Entertainment114/Siri-AI-Window
```

> **Không được trình bày mã nguồn gốc như sản phẩm do bạn tự viết hoàn toàn.**
>
> **Việc sử dụng mã nguồn theo MIT License không đồng nghĩa với việc chuyển giao quyền tác giả hay thương hiệu của tác giả gốc.**

### 📚 License đầy đủ

Bạn có thể thêm file `LICENSE` vào repository với nội dung chuẩn của **MIT License**, trong đó ghi tên chủ sở hữu bản quyền của dự án.

---

## 🤝 Đóng góp

Pull Request và Issue được hoan nghênh.

### Báo lỗi

Khi mở Issue, nên kèm:

```text
OS:
Python:
Version:
Error:
Steps to reproduce:
Log / Traceback:
```

### Pull Request

```bash
git checkout -b feature/my-feature
git add .
git commit -m "Add: my feature"
git push origin feature/my-feature
```

Sau đó mở **Pull Request** trên GitHub.

---

## 🗺️ Roadmap

```text
[✓] Voice Assistant
[✓] Gemini AI Integration
[✓] Windows Automation
[✓] Multi-language TTS
[✓] Chat UI
[✓] Settings UI

[ ] Wake-word detection nâng cao
[ ] Plugin / Extension System
[ ] More system actions
[ ] Custom personality
[ ] Conversation history
[ ] Tray mode
```

> Roadmap có thể thay đổi trong quá trình phát triển.

---

<div align="center">

## 👤 Author

### Hero-Entertainment114

**Siri AI Desktop Assistant for Windows**

[![GitHub](https://img.shields.io/badge/GitHub-Hero--Entertainment114-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Hero-Entertainment114)

<br>

Made with 🧠 AI, 🐍 Python & ☕

---

### ⭐ Nếu dự án hữu ích, hãy để lại một Star trên GitHub!

</div>
