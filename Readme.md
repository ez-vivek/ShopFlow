<div align="center">

  <br />
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDN5MGhtZXpmNWVremV0eWs1cnlmOGhxZGZvaGxwYXl3dzZiZW1mbyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/lXiRLb0xFzmreM8k8/giphy.gif" alt="Printer Animation" width="200">
  
  <h1 align="center">ShopFlow: Telegram Print Automation</h1>

  <p align="center">
    <strong>Turn your Print Shop into a Smart Office.</strong><br>
    Monitor folders, trigger prints via Telegram, and control settings (Copies, Duplex, Color) remotely.
    <br />
    <br />
    <a href="#-demo">View Demo</a>
    ·
    <a href="#-installation">Installation</a>
    ·
    <a href="#-configuration">Configuration</a>
  </p>

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Telegram-Bot_API-2CA5E0.svg?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
    <img src="https://img.shields.io/badge/Platform-Windows-0078D6.svg?style=for-the-badge&logo=windows&logoColor=white" alt="Windows">
    <img src="https://img.shields.io/badge/Engine-SumatraPDF-FFD700.svg?style=for-the-badge" alt="SumatraPDF">
  </p>
</div>

---

## 🚀 The Problem & Solution

**The Problem:** In a busy print shop, customers send files via WhatsApp. You have to walk to the PC, open the file, hit print, select settings, and wait. It wastes time.

**The Solution:** A "Folder Watcher" bot.
1. Customer sends file -> You save it to a specific folder.
2. Python detects the file.
3. **You get a Telegram notification on your phone.**
4. You select **Copies**, **Color**, or **Duplex** directly from the chat.
5. The PC prints it automatically in the background.

---

## 📱 Features

| Feature | Description |
| :--- | :--- |
| **📂 Folder Watchdog** | Instantly detects `.pdf`, `.docx`, `.jpg` dropped into the target folder. |
| **🎮 Remote Control** | Interactive Telegram buttons to control the printer from anywhere in the shop. |
| **⚙️ Advanced Settings** | Toggle **2-Sided (Duplex)**, **Black & White**, or **Page Copies** via Telegram. |
| **🧠 Smart Queue** | Handles multiple files without crashing; safety "Yes/No" check before printing. |
| **⚡ Silent Engine** | Uses **SumatraPDF** for high-speed, driver-less printing in the background. |

---

## 🛠️ Tech Stack

* **Language:** [Python](https://www.python.org/)
* **Libraries:**
    * `watchdog` (File System Monitoring)
    * `pyTelegramBotAPI` (Telegram Integration)
* **External Engine:** [SumatraPDF Portable](https://www.sumatrapdfreader.org/download-free-pdf-viewer) (CLI Printing)

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/shopflow-automation.git](https://github.com/yourusername/shopflow-automation.git)
cd shopflow-automation
````

### 2\. Set up Virtual Environment

It is recommended to use a virtual environment to keep dependencies clean.

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3\. Install Dependencies

```bash
pip install watchdog pyTelegramBotAPI
```

### 4\. Install SumatraPDF Engine

1.  Download **SumatraPDF Portable** (zip version).
2.  Extract `SumatraPDF.exe`.
3.  Place the `.exe` file inside your project root folder (same place as `autoprint.py`).

-----

## 🔧 Configuration

Open `autoprint.py` and edit the **Configuration Section** at the top:

```python
# ==================== CONFIGURATION ====================
BOT_TOKEN = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"  # Get from @BotFather
YOUR_CHAT_ID = 123456789                                  # Get from @userinfobot
WATCH_FOLDER = r"C:\Users\ShopAdmin\Desktop\Incoming_Files"
SUMATRA_PATH = r"C:\Users\ShopAdmin\Desktop\SumatraPDF.exe"
# =======================================================
```

> **Note:** Ensure `WATCH_FOLDER` exists. The script will error out if the folder is missing.

-----

## 🕹️ Usage Workflow

1.  **Start the Bot:**

    ```bash
    python autoprint.py
    ```

    *You will see: "--- ADVANCED PRINT BOT STARTED ---"*

2.  **Trigger a Print:**

      * Save a customer's file (e.g., `resume.pdf`) into the `Incoming_Files` folder.

3.  **Control via Telegram:**

      * Your phone vibrates.
      * **Tap** `➕` to increase copies.
      * **Tap** `🔄` to switch to 2-sided.
      * **Tap** `✅ PRINT NOW`.

4.  **Done\!** The printer starts automatically.


## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request