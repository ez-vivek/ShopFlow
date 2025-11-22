import time
import os
import telebot
from telebot import types
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import win32print
import win32api
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
YOUR_CHAT_ID = os.getenv("YOUR_CHAT_ID")

if not BOT_TOKEN or not YOUR_CHAT_ID:
    print("❌ ERROR: Could not find BOT_TOKEN or YOUR_CHAT_ID in .env file.")
    exit()

WATCH_FOLDER = r"C:\Users\vivek\Desktop\ShopFlow\Incoming Files"
ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.jpg', '.png', '.jpeg']

bot = telebot.TeleBot(BOT_TOKEN)
job_registry = {} 

class PrintHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            filename = event.src_path
            ext = os.path.splitext(filename)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                print(f"📂 File Detected: {os.path.basename(filename)}")
                time.sleep(2) 
                self.send_control_panel(filename)

    def send_control_panel(self, filepath):
        file_name = os.path.basename(filepath)
        default_settings = {'filepath': filepath, 'copies': 1, 'sides': 'simplex', 'color': 'color'}
        markup = generate_markup(default_settings)
        
        try:
            # Use the diagnostic message format
            msg = bot.send_message(YOUR_CHAT_ID, f"🧪 **DIAGNOSTIC TEST**\nFile: `{file_name}`", parse_mode="Markdown", reply_markup=markup)
            job_registry[msg.message_id] = default_settings
        except Exception as e:
            print(f"Telegram Error: {e}")

def generate_markup(settings):
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("➖", callback_data="dec_copy"),
        types.InlineKeyboardButton(f"📄 Copies: {settings['copies']}", callback_data="ignore"),
        types.InlineKeyboardButton("➕", callback_data="inc_copy")
    )
    markup.row(
        types.InlineKeyboardButton("📄 1-Sided" if settings['sides'] == "simplex" else "🔄 2-Sided", callback_data="toggle_sides"),
        types.InlineKeyboardButton("🎨 Color" if settings['color'] == "color" else "⚫ B/W", callback_data="toggle_color")
    )
    markup.row(
        types.InlineKeyboardButton("✅ TEST DRIVER", callback_data="print_now"),
        types.InlineKeyboardButton("❌ DELETE", callback_data="cancel_job")
    )
    return markup

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    msg_id = call.message.message_id
    if msg_id not in job_registry: return

    settings = job_registry[msg_id]
    update = True
    
    if call.data == "inc_copy": settings['copies'] += 1
    elif call.data == "dec_copy": 
        if settings['copies'] > 1: settings['copies'] -= 1
    elif call.data == "toggle_sides": settings['sides'] = "duplex" if settings['sides'] == "simplex" else "simplex"
    elif call.data == "toggle_color": settings['color'] = "monochrome" if settings['color'] == "color" else "color"
    elif call.data == "print_now": 
        run_diagnostic(settings, call) # CALLING DIAGNOSTIC FUNCTION
        update = False
    elif call.data == "cancel_job":
        bot.delete_message(call.message.chat.id, msg_id)
        del job_registry[msg_id]
        update = False
    elif call.data == "ignore": update = False

    if update:
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=msg_id, reply_markup=generate_markup(settings))
        bot.answer_callback_query(call.id)

# ================= THIS IS THE DIAGNOSTIC ENGINE =================
def run_diagnostic(settings, call):
    print("\n--- 🔍 STARTING DRIVER DIAGNOSTIC ---")
    
    try:
        # 1. CHECK PRINTER CONNECTION
        printer_name = win32print.GetDefaultPrinter()
        print(f"✅ STEP 1: Found Default Printer -> [{printer_name}]")
        
        hPrinter = win32print.OpenPrinter(printer_name)
        print(f"✅ STEP 2: Connection Open Successfully")
        
        # 2. READ CURRENT SETTINGS (DEVMODE)
        printer_info = win32print.GetPrinter(hPrinter, 2)
        devmode = printer_info["pDevMode"]
        print(f"✅ STEP 3: Read Driver Settings Successfully")
        
        print(f"\n--- 📊 CONFIGURATION CHECK ---")
        print(f"   Existing Driver Copies: {devmode.Copies}")
        print(f"   Existing Driver Color Mode: {devmode.Color} (1=Mono, 2=Color)")
        
        # 3. CALCULATE CHANGES
        print(f"\n--- 🔄 APPLYING REQUESTED CHANGES ---")
        
        print(f"   [Copies]  Changing to -> {settings['copies']}")
        devmode.Copies = settings['copies']
        
        target_color = 1 if settings['color'] == "monochrome" else 2
        print(f"   [Color]   Changing to -> {target_color} ({settings['color']})")
        devmode.Color = target_color

        target_duplex = 2 if settings['sides'] == "duplex" else 1
        print(f"   [Duplex]  Changing to -> {target_duplex} ({settings['sides']})")
        devmode.Duplex = target_duplex
        
        # 4. SIMULATE UPDATE
        print(f"\n✅ STEP 4: Virtual Configuration Update Passed")
        print("   (Skipping 'SetPrinter' to avoid changing your real defaults)")
        
        print(f"✅ STEP 5: Ready to fire 'ShellExecute' for file:")
        print(f"   {os.path.basename(settings['filepath'])}")
        
        # 5. SUCCESS MSG
        bot.edit_message_text(
            f"✅ **TEST PASSED**\n\n🔌 Printer: `{printer_name}`\n🧠 Driver Logic: OK\n\n(No paper was wasted)",
            chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown"
        )
        
        win32print.ClosePrinter(hPrinter)
        del job_registry[call.message.message_id]
        print("\n--- ✅ DIAGNOSTIC COMPLETE ---\n")
        
    except Exception as e:
        error_msg = f"❌ **TEST FAILED**\n\nError: `{e}`\n\nMake sure you installed: pip install pywin32"
        bot.edit_message_text(error_msg, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown")
        print(f"❌ ERROR: {e}")
# =============================================================

def start_system():
    if not os.path.exists(WATCH_FOLDER):
        print(f"❌ ERROR: Folder {WATCH_FOLDER} not found")
        return

    event_handler = PrintHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()
    
    print("--- 🧪 DIAGNOSTIC TOOL RUNNING ---")
    print(f"Watching: {WATCH_FOLDER}")
    print("Waiting for files to test driver connection...")

    try: bot.infinity_polling()
    except: observer.stop()
    observer.join()

if __name__ == "__main__":
    start_system()