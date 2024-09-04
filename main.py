#     _      ____  _  _        _____ _  _     _____
#    / \__/|/  _ \/ \/ \  /|  /    // \/ \   /  __/
#    | |\/||| / \|| || |\ ||  |  __\| || |   |  \  
#    | |  ||| |-||| || | \||  | |   | || |_/\|  /_ 
#    \_/  \|\_/ \|\_/\_/  \|  \_/   \_/\____/\____\



# --- Imports ---

# lang
from lang import messagebox_name, messagebox_text, messagebox_warn_text, app_is_closed_text, assets_loaded, lang_loaded, imports_loaded, cfg_loaded, cfg_settings, ram_txt, mb, new_name, news_1, news_2, news_version, db_cfg_loaded
print(lang_loaded)

# Import's
import tkinter, customtkinter, minecraft_launcher_lib, subprocess, asyncio, threading, os, shutil, mysql.connector, bcrypt, requests, platform, zipfile, urllib.request
import nbtlib
from nbtlib import Compound, String, List, File
import mysql.connector.plugins.mysql_native_password
from mysql.connector.plugins import caching_sha2_password
from tkinter import messagebox as msg
from PIL import Image, ImageTk
import uuid
from tkinter import *
from customtkinter import *
print(imports_loaded)

# cfg
from config import launch_files, launch_name, display, mesbox, meswarn, info_prefix, console_prefix, ozu, prefix, launch_version
print(cfg_loaded)

# assets
from assets import image_icon, pastlife_play, vinewood_play, pastlife_frame, vinewood_frame, background_img, settings_button
print(assets_loaded)


# --- Settings For DataBase ---
db_config = {
    'user': 'u215915_XncKbz2EO5',
    'password': '=Sc0cjDk!rr.b!^eh8tMS8CE',
    'host': 'mysql3.joinserver.xyz',  # Или ваш хост
    'port': '3306',
    'database': 's215915_mcAuth'
}
print(db_cfg_loaded)

cfg_settings()

# --- CTk Main Settings ---
root_tk = tkinter.Tk()
root_tk.geometry(display)
root_tk.title(launch_name)
root_tk.resizable(width=False, height=False)
customtkinter.deactivate_automatic_dpi_awareness()

# Icon
icon = ImageTk.PhotoImage(image_icon)
root_tk.iconphoto(False, icon)

with open('_internal/data/prefix.data', 'r') as file:
    prefix_name = file.read()
    file.close()
    
switch_var = customtkinter.StringVar(value=prefix_name)

# --- Func's ---

def get_minecraft_motd(server_ip):
    url = f"https://api.mcsrvstat.us/2/{server_ip}"
    response = requests.get(url)
    data = response.json()
    motd = data.get('motd', {}).get('clean', ["No MOTD found"])
    return "\n".join(motd)

def add_server_to_servers_dat(server_name, server_ip, servers_dat_path):
    # Проверка наличия файла servers.dat
    if os.path.exists(servers_dat_path):
        # Загрузка файла servers.dat
        servers_dat = nbtlib.load(servers_dat_path)
    else:
        # Если файла нет, создаем новый
        servers_dat = File({'servers': List[Compound]()})
    
    # Очистка списка серверов
    servers_dat['servers'].clear()

    # Создание новой записи сервера
    new_server = Compound({
        'name': String(server_name),
        'ip': String(server_ip)
    })

    # Добавление новой записи в список серверов
    servers_dat['servers'].append(new_server)

    # Сохранение файла servers.dat
    servers_dat.save(servers_dat_path)

# Создание начального изображения
initial_image = ImageTk.PhotoImage(background_img)
background_label = Label(root_tk, image=initial_image)
background_label.place(relwidth=1, relheight=1)

# Check profile
def check_credentials(username, password):
    connection = None
    try:
        # Connection to DataBase
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Database Query
        query = "SELECT password_hash FROM mc_auth_accounts WHERE player_name = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result and bcrypt.checkpw(password.encode('utf-8'), result['password_hash'].encode('utf-8')):
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

async def pastlife_button_event():
    username = entry.get()
    password = entry_password.get()

    print(username, password)

    if check_credentials(username, password):
        label_pastlife_news.configure(text="Аунтификачия прошла успешно!", foreground="green", borderwidth=0)
        global ozu
        global prefix
        if switch_var.get() == "on":
            get_user_name = prefix + entry.get()
        elif switch_var.get() == "off":
            get_user_name = entry.get()

        # Minecraft settings (backend)
        options = {
            'username': get_user_name,
            'uuid': str(uuid.uuid1()),
            'token': '',
            "jvmArguments": [f"-Xmx{ozu}M", "-XX:+UnlockExperimentalVMOptions", "-XX:+UseG1GC",
                             "-XX:G1NewSizePercent=20", "-XX:G1ReservePercent=20",
                             "-XX:MaxGCPauseMillis=50", "-XX:G1HeapRegionSize=32M"]
        }

        # Путь к Java
        java_path = os.path.join("_internal", "java1.20.4", "bin", "javaw.exe")

        # Убедитесь, что Java существует
        if not os.path.exists(java_path):
            print(f"{console_prefix}Error: Java не найдена по пути: {java_path}")
            return

        # Nickname saving
        save_ok = True
        print(f"{console_prefix}Saving")
        with open('_internal/data/user.data', 'w') as file:
            file.write(entry.get())
            print(f"{console_prefix}Saved")
        if not save_ok:
            print(f"{info_prefix}Error: {entry.get()} - не успешно")
        else:
            print(f"{console_prefix}{entry.get()} - успешно")

        # Files bar - funcs
        current_max = 0

        def set_status(status: str):
            print(status)

        def set_progress(progress: int):
            if current_max != 0:
                print(f"{progress}/{current_max}")

        def set_max(new_max: int):
            nonlocal current_max
            current_max = new_max

        # Minecraft folder
        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace('minecraft', launch_files)

        callback = {
            "setStatus": set_status,
            "setProgress": set_progress,
            "setMax": set_max
        }

        # Other folders for Minecraft
        mods_directory = f"{minecraft_directory}/mods"
        resourcepacks_directory = f"{minecraft_directory}/resourcepacks"
        shaderpacks_directory = f"{minecraft_directory}/shaderpacks"
        config_directory = f"{minecraft_directory}/config"
        emotes_directory = f"{minecraft_directory}/emotes"

        # Installing
        if os.path.exists(f"{minecraft_directory}/fabric-loader-0.16.2-1.20.4"):
            print(info_prefix + "Directory:", minecraft_directory)
            await compare_and_copy_folders("_internal/pastlife_mods", mods_directory)
            await compare_and_copy_folders("_internal/resourcepacks", resourcepacks_directory)
            await compare_and_copy_folders("_internal/config", config_directory)
            print(f"{console_prefix}1.20.4 - Загружен")
            add_server_to_servers_dat(server_ip="herbobra.cringe.team", server_name="Выживание", servers_dat_path=f"{minecraft_directory}/servers.dat")
        else:
            print(f"{console_prefix}1.20.4 - Не Установлен")
            minecraft_launcher_lib.install.install_minecraft_version("1.20.4", minecraft_directory, callback=callback)
            minecraft_launcher_lib.fabric.install_fabric("1.20.4", minecraft_directory, callback=callback, java=java_path)
            print(info_prefix + "Directory:", minecraft_directory)
            await compare_and_copy_folders("_internal/pastlife_mods", mods_directory)
            await compare_and_copy_folders("_internal/resourcepacks", resourcepacks_directory)
            await compare_and_copy_folders("_internal/shaderpacks", shaderpacks_directory)
            await compare_and_copy_folders("_internal/emotes", emotes_directory)
            os.rmdir(f"{minecraft_directory}/config")
            os.mkdir(f"{minecraft_directory}/config")
            await compare_and_copy_folders("_internal/config", config_directory)
            loader_version = "fabric-loader-0.16.2-1.20.4"
            add_server_to_servers_dat(server_ip="herbobra.cringe.team", server_name="Выживание", servers_dat_path=f"{minecraft_directory}/servers.dat")
            copy_file("_internal/data/options.txt", minecraft_directory)

        print(console_prefix + "Все Установленные Версии: ", minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory))

        # Start the game
        if os.path.exists(java_path):
            command = minecraft_launcher_lib.command.get_minecraft_command(loader_version, minecraft_directory, options)
            
            # Заменяем стандартный путь к Java на пользовательский
            command[0] = java_path
            
            await asyncio.get_event_loop().run_in_executor(None, subprocess.call, command)
        else:
            print(f"{console_prefix}Error: Java не найдена по пути: {java_path}")

    else:
        label_pastlife_news.configure(text="Неверный Пароль или Никнейм.", foreground="red", borderwidth=0)

# Использование в основном коде
async def vinewood_button_event():
    username = entry.get()
    password = entry_password.get()

    print(username, password)

    if check_credentials(username, password):
        label_vinewood_news.configure(text="Аунтификачия прошла успешно!", foreground="green", borderwidth=0)
        global ozu
        global prefix
        if switch_var.get() == "on":
            get_user_name = prefix + entry.get()
        elif switch_var.get() == "off":
            get_user_name = entry.get()

        # Minecraft settings (backend)
        options = {
            'username': get_user_name,
            'uuid': str(uuid.uuid1()),
            'token': '',
            "jvmArguments": [f"-Xmx{ozu}M", "-XX:+UnlockExperimentalVMOptions", "-XX:+UseG1GC",
                             "-XX:G1NewSizePercent=20", "-XX:G1ReservePercent=20",
                             "-XX:MaxGCPauseMillis=50", "-XX:G1HeapRegionSize=32M"]
        }

        # Путь к Java
        java_path = os.path.join("_internal", "java1.16.5", "bin", "javaw.exe")

        # Убедитесь, что Java существует
        if not os.path.exists(java_path):
            print(f"{console_prefix}Error: Java не найдена по пути: {java_path}")
            return

        # Nickname saving
        save_ok = True
        print(f"{console_prefix}Сохранение Данных")
        with open('_internal/data/user.data', 'w') as file:
            file.write(entry.get())
        if not save_ok:
            print(f"{info_prefix}Error: {entry.get()} - не успешно")
        else:
            print(f"{console_prefix}{entry.get()} - успешно")

        # Files bar - funcs
        current_max = 0

        def set_status(status: str):
            print(status)

        def set_progress(progress: int):
            if current_max != 0:
                print(f"{progress}/{current_max}")

        def set_max(new_max: int):
            nonlocal current_max
            current_max = new_max

        # Minecraft folder
        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace('minecraft', launch_files)

        callback = {
            "setStatus": set_status,
            "setProgress": set_progress,
            "setMax": set_max
        }

        mods_directory = f"{minecraft_directory}/mods"
        resourcepacks_directory = f"{minecraft_directory}/resourcepacks"
        loader_version = None  # Initialize loader_version safely

        # Установка и запуск Minecraft с использованием указанной Java
        if os.path.exists(f"{minecraft_directory}/1.16.5-36.2.34"):
            print(info_prefix + "Папка:", minecraft_directory)
            await compare_and_copy_folders("_internal/vinewood_mods", mods_directory)
            await compare_and_copy_folders("_internal/vinewood_resourcepacks", resourcepacks_directory)
            print(f"{console_prefix}1.16.5 - Загружен")
            add_server_to_servers_dat(server_ip="vinewood.gomc.fun", server_name="Role Play", servers_dat_path=f"{minecraft_directory}/servers.dat")
        else:
            print(f"{console_prefix}1.16.5 - Не Установлен")
            minecraft_launcher_lib.install.install_minecraft_version("1.16.5", minecraft_directory, callback=callback)
            minecraft_launcher_lib.forge.install_forge_version("1.16.5-36.2.34", minecraft_directory, callback=callback)
            print(info_prefix + "Папка:", minecraft_directory)
            await compare_and_copy_folders("_internal/vinewood_mods", mods_directory)
            await compare_and_copy_folders("_internal/vinewood_resourcepacks", resourcepacks_directory)
            loader_version = "1.16.5-forge-36.2.34"
            if loader_version is None:
                print(f"{console_prefix}Error: Не найдена версия Forge {loader_version} для Minecraft 1.16.5.")
                return  # or handle the error as necessary

            add_server_to_servers_dat(server_ip="vinewood.gomc.fun", server_name="Role Play", servers_dat_path=f"{minecraft_directory}/servers.dat")

        print(console_prefix + "Все Установленные Версии: ", minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory))

        # Start the game with specified Java path
        if loader_version:
            command = minecraft_launcher_lib.command.get_minecraft_command(loader_version, minecraft_directory, options)
            
            # Заменяем стандартный путь к Java на пользовательский
            command[0] = java_path
            
            await asyncio.get_event_loop().run_in_executor(None, subprocess.call, command)
        else:
            print(f"{console_prefix}Error: Minecraft не может стартовать, {loader_version} не загружен.")

    else:
        label_vinewood_news.configure(text="Неверный Пароль или Никнейм.", foreground="red", borderwidth=0)




async def compare_and_copy_folders(source_folder, destination_folder):
    # Список файлов в папке folder1
    source_files = os.listdir(source_folder)
    
    # Проверка на существование папки
    if not os.path.exists(destination_folder):
        # Создание папки, если она отсутствует
        os.makedirs(destination_folder)
        print(f"{destination_folder}Создана папка")
    
    # Список файлов в папке folder2
    destination_files = os.listdir(destination_folder)
    
    # Сравнивание файлов в обеих папках
    if set(source_files) == set(destination_files):
        print("OK")
    else:
        # copy files from the source folder to the folder2
        for file in source_files:
            source_path = os.path.join(source_folder, file)
            destination_path = os.path.join(destination_folder, file)
            shutil.copy2(source_path, destination_path)

            # excluding copying of the _internal folder
            if file != "_internal":
                shutil.copy2(source_path, destination_path)

        print(f"{source_folder}, {destination_folder} успешное копирование")

def copy_file(source_file_path, destination_folder_path):
    # Проверка, существует ли исходный файл
    if not os.path.isfile(source_file_path):
        print(f"Файл {source_file_path} не существует.")
        return
    
    # Проверка, существует ли целевая папка, если нет - создаем
    if not os.path.exists(destination_folder_path):
        os.makedirs(destination_folder_path)
        print(f"Папка {destination_folder_path} была создана.")
    
    # Получаем имя файла из полного пути
    file_name = os.path.basename(source_file_path)
    
    # Формируем путь для копирования файла
    destination_file_path = os.path.join(destination_folder_path, file_name)
    
    # Копируем файл
    shutil.copy2(source_file_path, destination_file_path)
    
    print(f"Файл {source_file_path} успешно скопирован в {destination_file_path}.")

# pastlife Async Func
def pastlife_button_event_async():
    asyncio.run(pastlife_button_event())

# pastlife Thread Func
def pastlife_button_event_thread():
    threading.Thread(target=pastlife_button_event_async).start()

# vinewood Async Func
def vinewood_button_event_async():
    asyncio.run(vinewood_button_event())

# vinewood Thread Func
def vinewood_button_event_thread():
    threading.Thread(target=vinewood_button_event_async).start()

# txt func
def closed():
    print(app_is_closed_text)
    root_tk.destroy()
    

# messBox closing func
def on_closing():
    if msg.askokcancel(messagebox_name, messagebox_text):
        closed()

# --- Visual ---

# Создание полупрозрачного фрейма
class TransparentFrame(customtkinter.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color=("white", "gray20", "gray70", 0))  # Цвет с альфа-каналом для полупрозрачности

#frame
#global_frame = customtkinter.CTkFrame(root_tk, width=1920, height=1080, fg_color=("black"), bg_color=("#181818"))
#global_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

#frame = customtkinter.CTkCanvas(root_tk, bg="gray20", highlightthickness=0)
#frame.place(relx=0.5, rely=0.95, anchor=tkinter.CENTER, width=800, height=78)


#label

motd_server_ip = "185.9.145.176:25635"  # Замените на IP вашего сервера
motd_text = get_minecraft_motd(motd_server_ip)
lines = motd_text.split('\n')

vw_motd_server_ip = "185.9.145.176:25635"  # Замените на IP вашего сервера
vw_motd_text = get_minecraft_motd(vw_motd_server_ip)
vw_lines = motd_text.split('\n')

# Для каждой линии создаем новый label
for line in lines:
    font = tkinter.PhotoImage(file="_internal/assets/pastlife_fon.png") 
    label_pastlife_news = tkinter.Label(root_tk, image=font, text=line, compound=tkinter.CENTER, fg="white", justify="right") 
    label_pastlife_news.place(x=517, y=146, width=256, height=277)

for line2 in vw_lines:
    font_2 = tkinter.PhotoImage(file="_internal/assets/vinewood_fon.png") 
    label_vinewood_news = tkinter.Label(root_tk, image=font_2, text=line2, compound=tkinter.CENTER, fg="white", justify="right") 
    label_vinewood_news.place(x=32, y=146, width=256, height=277)

label_pastlife_login = tkinter.Label(root_tk, text=line, compound=tkinter.CENTER, fg="white", justify="right") 
#label_pastlife_login.place(x=517, y=146, width=256, height=277)

#entry
def on_entry_click(event):
    if entry.get() == "Nickname":
        entry.delete(0, 50)

def on_focusout(event):
    with open('_internal/data/user.data', 'r') as file:
        user_name = file.read()
    if entry.get() == '':
        entry.insert(0, f"{user_name}")
        entry.configure(fg_color=("#34d450"))
    file.close()

entry = tkinter.Entry(master=root_tk,
                                foreground=("#008000"),
                                fg=("#fffdfe"),
                                background=("#181818"),
                                borderwidth=0
                                )
with open('_internal/data/user.data', 'r') as file:
    user_name = file.read()
    file.close()
entry.insert(0, f"{user_name}")
entry.bind('<FocusIn>', on_entry_click)
entry.bind('<FocusOut>', on_focusout)
entry.place(relx=0.25, rely=0.9, width=190, height=25)

entry_password = tkinter.Entry(master=root_tk,
                                        foreground=("#008000"),
                                        fg=("#fffdfe"),
                                        background=("#181818"),
                                        show="*",
                                        borderwidth=0
                                        )
entry_password.place(relx=0.5, rely=0.9, width=190, height=25)

#button
button_image = ImageTk.PhotoImage(pastlife_play)
button = tkinter.Button(master=root_tk,
                                 command=pastlife_button_event_thread,
                                 width=150,
                                 height=49,
                                 image=button_image,
                                 text="",
                                 borderwidth=0
                                 )
button.place(x=633, y=440)

#button
button_image2 = ImageTk.PhotoImage(vinewood_play)
button2 = tkinter.Button(master=root_tk,
                                 command=vinewood_button_event_thread,
                                 width=150,
                                 height=49,
                                 image=button_image2,
                                 text="",
                                 borderwidth=0
                                 )
button2.place(x=20, y=440)

#button
def settings_button_func():
    settings = Toplevel(root_tk)
    settings.title("Настройки")
    settings.geometry("250x200")
    settings.resizable(width=False, height=False)

    global_frame = customtkinter.CTkFrame(settings, width=300, height=250, fg_color=("#181818"), bg_color=("#181818"))
    global_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    # slider
    def slider_event(value):
        global ozu
        ozu = int(value)
        print(ozu)
        label_slider.configure(text=f"{ram_txt}: {ozu}{mb}")
        with open('_internal/data/ram.data', 'w') as file:
            file.write(str(ozu))
            file.close()

    slider = customtkinter.CTkSlider(settings, from_=1000, to=12000, command=slider_event, bg_color=("#181818"), button_color=("#007300"), button_hover_color=("#006800"))
    slider.set(int(ozu))
    slider.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

    label_slider = customtkinter.CTkLabel(settings, width=100, height=10, text=f"{ram_txt}: {ozu}{mb}", bg_color=("#181818"))
    label_slider.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    # switch
    def switch_event():
        global prefix
        if switch_var.get() == "on":
            with open('_internal/data/prefix.data', 'w') as file:
                file.write(switch_var.get())
                file.close()
            print("Prefix On")
            from config import prefix
        elif switch_var.get() == "off":
            with open('_internal/data/prefix.data', 'w') as file:
                file.write(switch_var.get())
                file.close()
            print("Prefix Off")
            prefix = ""

    switch = customtkinter.CTkSwitch(settings, text="Prefix", command=switch_event, variable=switch_var, onvalue="on", offvalue="off", progress_color=("#aab0b5"), bg_color=("#181818"), button_color=("#007300"), button_hover_color=("#006800"))
    switch.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)


settings_image = ImageTk.PhotoImage(settings_button)
button4 = tkinter.Button(master=root_tk,
                                command=settings_button_func,
                                width=70,
                                height=70,
                                image=settings_image,
                                text="",
                                borderwidth=0
                                )
button4.place(x=730, y=0)

# --- Other cfg ---
if mesbox:
    root_tk.protocol("WM_DELETE_WINDOW", on_closing)
else:
    root_tk.protocol("WM_DELETE_WINDOW", closed)
    if meswarn:
        print(messagebox_warn_text)
# --- Loop ---
root_tk.mainloop()
