<div align="center">

  <br />
  <h1 align="center">ShopFlow - Print Automation For Businesses</h1>

  <p align="center">
    <br>
    Monitor folders, trigger prints via Telegram, and control settings (Copies, Duplex, Color) remotely.
    <br />
    <br />
  </p>

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Telegram-Bot_API-2CA5E0.svg?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
    <img src="https://img.shields.io/badge/Platform-Windows-0078D6.svg?style=for-the-badge&logo=windows&logoColor=white" alt="Windows">
    <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License">
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

## ✨ Features

| Feature | Description |
| :--- | :--- |
| **📂 Folder Watchdog** | Instantly detects `.pdf`, `.docx`, `.jpg`, `.png` files dropped into the target folder. |
| **🎮 Remote Control** | Interactive Telegram buttons to control the printer from anywhere in the shop. |
| **⚙️ Advanced Settings** | Toggle **2-Sided (Duplex)**, **Black & White**, or adjust **Page Copies** via Telegram. |
| **🧠 Smart Queue** | Handles multiple files without crashing; safety "Yes/No" confirmation before printing. |
| **⚡ Silent Engine** | Uses **SumatraPDF** for high-speed, driver-less printing in the background. |
| **📡 Real-time Notifications** | Get instant Telegram alerts when new files are ready for printing. |

---

## 🛠️ Tech Stack

| Component | Details |
| :--- | :--- |
| **Language** | [Python 3.10+](https://www.python.org/) |
| **File Monitoring** | [watchdog](https://github.com/gorakhargosh/watchdog) |
| **Telegram Integration** | [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) |
| **Environment Config** | [python-dotenv](https://github.com/theskumar/python-dotenv) |
| **Print Engine** | [SumatraPDF Portable](https://www.sumatrapdfreader.org/download-free-pdf-viewer) |
| **OS Support** | Windows 10/11 |

---

## 📦 Installation

### Prerequisites
- Windows 10 or Windows 11
- Python 3.10 or higher
- Telegram Bot (create one via [@BotFather](https://t.me/botfather))
- Your Telegram Chat ID

### Step 1: Clone the Repository
```powershell
git clone https://github.com/ez-vivek/ShopFlow.git
cd ShopFlow
```

### Step 2: Set up Virtual Environment
Create a virtual environment to keep dependencies organized:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Python Dependencies
```powershell
pip install watchdog pyTelegramBotAPI python-dotenv pywin32
```

### Step 4: Configure Environment Variables
Create a `.env` file in the project root:
```env
BOT_TOKEN=your_telegram_bot_token_here
YOUR_CHAT_ID=your_telegram_chat_id_here
```

### Step 5: Create Incoming Files Folder
Ensure the `Incoming Files` folder exists in the project directory:
```powershell
New-Item -ItemType Directory -Force -Path "Incoming Files"
```

-----

## 🔧 Configuration

### Environment Variables (.env)
The application reads configuration from a `.env` file in the project root:

```env
BOT_TOKEN=your_telegram_bot_token_here
YOUR_CHAT_ID=your_telegram_chat_id_here
```

### How to Get Your Credentials

1. **BOT_TOKEN:**
   - Chat with [@BotFather](https://t.me/botfather) on Telegram
   - Use command `/newbot`
   - Follow the instructions and copy the token

2. **YOUR_CHAT_ID:**
   - Chat with [@userinfobot](https://t.me/userinfobot) on Telegram
   - The bot will show your Chat ID

### Supported File Types
The following file formats are automatically detected and can be printed:
- `.pdf` - PDF Documents
- `.docx` - Microsoft Word Documents
- `.jpg`, `.jpeg` - JPEG Images
- `.png` - PNG Images

> **⚠️ Important:** Ensure the `Incoming Files` folder exists before running the application. The script will monitor this folder for new files.

-----

## 🎯 Usage Workflow

### Starting the Application
1. Activate your virtual environment (if not already active):
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. Run the bot:
   ```powershell
   python autoprint.py
   ```
   You should see a confirmation message indicating the bot has started successfully.

### Printing a File
1. **Save a file** to the `Incoming Files` folder (e.g., `resume.pdf`)
2. **Wait for notification** - Your phone will receive an instant Telegram message with print options
3. **Configure settings** using the interactive buttons:
   - `➕` - Increase number of copies
   - `➖` - Decrease number of copies
   - `🔄` - Toggle 2-Sided (Duplex) printing
   - `🎨` - Toggle Color/Black & White
   - `✅ PRINT NOW` - Confirm and print
   - `❌ CANCEL` - Cancel the print job
4. **Confirmation** - Once you tap `✅ PRINT NOW`, the document prints automatically to your default printer

### Tips
- Keep the bot running in the background while working
- You can manage multiple print jobs simultaneously
- Each file gets its own Telegram control panel
- The bot logs all activity to the console


## ❓ Troubleshooting

| Issue | Solution |
| :--- | :--- |
| **Bot not responding** | Check that `BOT_TOKEN` and `YOUR_CHAT_ID` are correctly set in `.env` file. Restart the application. |
| **Files not detected** | Ensure the `Incoming Files` folder exists. Check file extensions are supported (`.pdf`, `.docx`, `.jpg`, `.png`). |
| **`ModuleNotFoundError`** | Install all dependencies: `pip install -r requirements.txt` |
| **Telegram errors** | Verify bot is still active in BotFather. Check internet connection. |

## 📋 Requirements File

For easier setup, all dependencies are listed in `requirements.txt`:
```
watchdog>=3.0.0
pyTelegramBotAPI>=4.10.0
python-dotenv>=1.0.0
pywin32>=305
```

Install all at once:
```powershell
pip install -r requirements.txt
```

## 📄 Project Structure

```
ShopFlow/
├── autoprint.py           # Main application file
├── test.py               # Testing file
├── .env                  # Environment variables (create this)
├── requirements.txt      # Python dependencies
├── Readme.md            # This file
├── SumatraPDF.exe       # Printer engine (download separately)
└── Incoming Files/      # Folder for files to print
```

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

### How to Contribute
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.


## 📞 Support

For issues, questions, or suggestions, please [open an issue](https://github.com/ez-vivek/ShopFlow/issues) on GitHub.

---

<div align="center">
  <p>
    Made with ❤️ for Businesses
  </p>
</div>