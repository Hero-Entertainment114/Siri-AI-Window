<div align="center">

# Siri AI Desktop Assistant

### A multilingual AI virtual assistant for Windows

<p>
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/GUI-PyQt5-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt5">
  <img src="https://img.shields.io/badge/AI-Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white" alt="Google Gemini">
  <img src="https://img.shields.io/badge/Voice-Edge--TTS-0078D4?style=for-the-badge&logo=microsoftedge&logoColor=white" alt="Edge-TTS">
  <img src="https://img.shields.io/badge/License-MIT-2EA44F?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="MIT">
</p>

<p>
  A desktop virtual assistant that combines <b>Google Gemini AI</b>, speech recognition,
  speech synthesis, and Windows automation in a modern interface.
</p>

<p>
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#api-key">API Key</a> •
  <a href="#license">License</a> •
  <a href="#disclaimer">Disclaimer</a>
</p>

</div>

---

## Introduction

**Siri AI Desktop Assistant** is an open-source virtual assistant for Windows, built around three core capabilities:

| Understand commands | Take action | Respond |
|---|---|---|
| Gemini interprets natural-language requests | Performs the corresponding action on Windows | Edge-TTS replies with voice output |
| Voice / text input | Apps, files, CMD, mouse, hardware | Multiple languages and voices |

> **Core idea:** the user says what they need done, the AI parses the intent, and the app carries out the matching action.

---

## Features

### Voice Assistant
- Activated by wake words such as `hello`, `siri`, `xin chào`, etc.
- Speech recognition powered by **Google Speech Recognition**.
- Can switch to text-based command input.

### Gemini Intent Parsing
Gemini is used to understand commands and determine the action to take.

| Example command | Action |
|---|---|
| `open Chrome` | Finds and launches the application |
| `close Discord` | Terminates the corresponding process |
| `check RAM` | Reads hardware information |
| `run ipconfig` | Opens CMD and executes the command |
| `move mouse to 500 300` | Controls the cursor |

### Windows Automation

| Function | Technology |
|---|---|
| Open app / file / folder | Windows / Python |
| Terminate process | `psutil` |
| Run CMD commands | Windows CMD |
| Control the mouse | `pyautogui` |
| Check CPU / RAM / C: drive | System information |

### Multi-language TTS

| Language | Example voices |
|---|---|
| Vietnamese | Hoai My, Nam Minh |
| English | Ava, Jenny, Guy |
| Japanese | Nanami, Keita |
| Chinese | Multiple voices |
| Korean | Multiple voices |
| And more | — |

### UI

- **Visual Orb**: shifts between `Listening`, `Thinking`, and `Speaking` states.
- **Chat Window**: type and view commands as text.
- **Settings**: configure API Key, voice, model, and related options.

---

## Tech Stack

```text
Python 3.9+
├── PyQt5              → User interface
├── Google Gemini API  → AI / intent parsing
├── Speech Recognition → Voice recognition
├── Edge-TTS           → Speech synthesis
├── psutil             → Process & hardware management
└── pyautogui          → Mouse control
```

---

## Project Structure

```text
Siri-AI-Window/
├── siri.py
├── siri_config.json
├── requirements.txt
├── .gitignore
└── README.md
```

| File | Role |
|---|---|
| `siri.py` | Main source code |
| `siri_config.json` | API key, voice, model, and personal configuration |
| `requirements.txt` | Dependency list |
| `.gitignore` | Files/folders excluded from Git |
| `README.md` | Project documentation |

> **Do not commit `siri_config.json` to GitHub if it contains a real API key.**

---

## Installation

### Option A · Packaged build

**No Python installation required.**

1. Open the **[Releases](../../releases)** section of the repository.
2. Download:

```text
Siri-AI-v1.0-Trial.zip
```

3. Extract, then run:

```text
siri.exe
```

4. Go to **Settings** → enter your Gemini API Key → **Save Settings & Activate**.

---

### Option B · Run from source

#### 1. Clone

```bash
git clone https://github.com/Hero-Entertainment114/Siri-AI-Window.git
cd Siri-AI-Window
```

#### 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Run

```bash
python siri.py
```

> **Requirements:** Python **3.9+** and a Windows environment compatible with the libraries listed in `requirements.txt`.

---

## API Key

### BYOK · Bring Your Own Key

The application uses a **BYOK** model, meaning users supply their own Gemini API Key.

The key is stored in:

```text
siri_config.json
```

### Multiple API Keys

You can enter multiple keys separated by commas:

```text
API_KEY_1,API_KEY_2,API_KEY_3
```

The app supports a key-rotation mechanism (`rotate_key`) to switch to another key when the current one hits a usage limit.

### Creating a Gemini API Key

**Google AI Studio**
https://aistudio.google.com/

> **Your API key is sensitive information. Do not post it publicly, commit it to a repository, or share it with others.**

---

## Security & Privacy

| Topic | Policy |
|---|---|
| API Key | Stored locally in `siri_config.json` |
| Microphone | Used during speech-recognition sessions |
| Audio | The project does not deliberately store audio as permanent files |
| API | Requests may be sent to necessary third-party services, particularly Google's |
| Source Code | Can be reviewed directly from the repository |

### Important

No software can guarantee absolute safety. Users should **review the source code, dependencies, and permissions themselves** before running it on an important machine.

---

## Disclaimer

> ### USE AT YOUR OWN RISK
>
> **Siri AI Desktop Assistant is provided "AS IS", without any warranty of accuracy, stability, or fitness for a particular purpose.**
>
> Because the application allows AI to perform actions on the operating system, **users are solely responsible for every command they provide and for any consequences arising from use of the software**.

The author is not responsible for:

- Data loss or unintended data changes.
- Applications/processes being closed, opened, or controlled by mistake.
- System commands that cause errors, loss of configuration, or affect Windows.
- Damage arising from AI errors, library bugs, or third-party services.
- Limitations, changes to APIs, policies, or behavior from Google, Microsoft, or other providers.
- Any direct, indirect, incidental, or consequential damages arising from use of the software.

> **Do not assign the AI tasks that could cause data loss or affect your system if you do not fully understand the impact.**

---

## License

### MIT License

This project is released under the **MIT License**.

Under the terms of the MIT License, you are permitted to:

```text
✓ Use
✓ Copy
✓ Modify
✓ Distribute
✓ Use in personal projects
✓ Use in commercial projects
```

### Important condition

If you copy, reuse, or redistribute this project's source code, **please retain the copyright notice and MIT license**.

Original author information:

```text
Author:
Hero-Entertainment114

Repository:
https://github.com/Hero-Entertainment114/Siri-AI-Window
```

> **Do not present the original source code as something you wrote entirely by yourself.**
>
> **Using the source code under the MIT License does not transfer the original author's copyright or brand.**

### Full license

You may add a `LICENSE` file to the repository with the standard MIT License text, naming the copyright holder of the project.

---

## Contributing

Pull requests and issues are welcome.

### Reporting bugs

When opening an issue, please include:

```text
OS:
Python:
Version:
Error:
Steps to reproduce:
Log / Traceback:
```

### Pull requests

```bash
git checkout -b feature/my-feature
git add .
git commit -m "Add: my feature"
git push origin feature/my-feature
```

Then open a **Pull Request** on GitHub.

---

## Roadmap

```text
[x] Voice Assistant
[x] Gemini AI Integration
[x] Windows Automation
[x] Multi-language TTS
[x] Chat UI
[x] Settings UI

[ ] Advanced wake-word detection
[ ] Plugin / extension system
[ ] More system actions
[ ] Custom personality
[ ] Conversation history
[ ] Tray mode
```

> The roadmap is subject to change as development continues.

---

<div align="center">

## Author

### Hero-Entertainment114

**Siri AI Desktop Assistant for Windows**

[![GitHub](https://img.shields.io/badge/GitHub-Hero--Entertainment114-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Hero-Entertainment114)

---

### If this project is useful, please leave a Star on GitHub!

</div>
