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
    print("   Please make sure you created the .env file correctly.")
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
                print(f"📂 New File: {os.path.basename(filename)}")
                time.sleep(2) 
                self.send_control_panel(filename)

    def send_control_panel(self, filepath):
        file_name = os.path.basename(filepath)
        default_settings = {'filepath': filepath, 'copies': 1, 'sides': 'simplex', 'color': 'color'}
        markup = generate_markup(default_settings)
        
        try:
            msg = bot.send_message(YOUR_CHAT_ID, f"🎛️ **CUSTOM PRINT ENGINE**\nFile: `{file_name}`", parse_mode="Markdown", reply_markup=markup)
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
        types.InlineKeyboardButton("✅ PRINT NOW", callback_data="print_now"),
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
        execute_printing(settings, call)
        update = False
    elif call.data == "cancel_job":
        bot.delete_message(call.message.chat.id, msg_id)
        del job_registry[msg_id]
        update = False
    elif call.data == "ignore": update = False

    if update:
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=msg_id, reply_markup=generate_markup(settings))
        bot.answer_callback_query(call.id)

# ================= THIS IS THE CUSTOM ENGINE =================
def execute_printing(settings, call):
    filepath = settings['filepath']
    
    try:
        printer_name = win32print.GetDefaultPrinter()
        print(f"🖨️ Using Driver: {printer_name}")
        
        # 1. Get Printer Handle
        hPrinter = win32print.OpenPrinter(printer_name)
        
        # 2. Get Current Configuration (DevMode)
        printer_info = win32print.GetPrinter(hPrinter, 2)
        devmode = printer_info["pDevMode"]
        
        # 3. MODIFY THE CONFIGURATION
        devmode.Copies = settings['copies']
        devmode.Color = 1 if settings['color'] == "monochrome" else 2
        devmode.Duplex = 2 if settings['sides'] == "duplex" else 1
        
        # 4. UPDATE PRINTER SETTINGS
        win32print.SetPrinter(hPrinter, 2, printer_info, 0)
        
        # 5. EXECUTE PRINT
        win32api.ShellExecute(0, "print", filepath, None, ".", 0)
        
        # 6. SUCCESS MSG
        bot.edit_message_text(
            f"✅ **PRINTING VIA WINDOWS API**\nSent to: {printer_name}\nSettings: {settings['copies']}x | {settings['sides']} | {settings['color']}",
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )

        win32print.ClosePrinter(hPrinter)
        del job_registry[call.message.message_id]
        
    except Exception as e:
        bot.send_message(call.message.chat.id, f"⚠️ Windows API Error: {e}")
# =============================================================

def start_system():
    if not os.path.exists(WATCH_FOLDER):
        print(f"❌ ERROR: Folder {WATCH_FOLDER} not found")
        return

    event_handler = PrintHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()
    
    print("--- CUSTOM ENGINE STARTED (SECURE MODE) ---")
    try: 
        bot.send_message(YOUR_CHAT_ID, "⚡ **Custom Print Engine Online**")
    except Exception as e: 
        print(f"Startup Message Failed: {e}")

    try: 
        bot.infinity_polling()
    except: 
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_system()