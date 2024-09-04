#    _     ____  _      _____
#   / \   /  _ \/ \  /|/  __/
#   | |   | / \|| |\ ||| |  _
#   | |_/\| |-||| | \||| |_//
#   \____/\_/ \|\_/  \|\____\



# Import's
from config import lang, launch_name, console_prefix, color_two, color_one, color_cls, mesbox, meswarn, display, prefix, color, info_prefix, txt_info, launch_version

# Custom Lang
if lang == "custom":

    # MessageBox
    # Default:  Num1 - messagebox_name = launch_name
    #           Num2 - messagebox_name = "Your_txt"
    messagebox_text = "."
    messagebox_name = launch_name
    messagebox_warn_text = f"{console_prefix}." # console

    ram_txt = "."
    mb = "."

    app_is_closed_text = f"{console_prefix}. - {color_one}.{color_cls}" # console

    txt_info()

    imports_loaded = f"{console_prefix}. - {color_two}.{color_cls}" # console
    assets_loaded = f"{console_prefix}. - {color_two}.{color_cls}"  # console
    lang_loaded = f"{console_prefix}. - {color_two}.{color_cls}"    # console
    cfg_loaded = f"{console_prefix}. - {color_two}.{color_cls}"     # console
    db_cfg_loaded = f"{console_prefix}. - {color_two}.{color_cls}"  # console

    def cfg_settings():   # console
        print(info_prefix + ".: ", launch_version) #version                         
        print(info_prefix + ".: ", lang) #lang
        print(info_prefix + ".: ", launch_name) #launcher name
        print(info_prefix + ".: " + display) #display
        print(info_prefix + ".: " + prefix) #prefix in game
        print(info_prefix + ".:" + color, "123", color_cls) #Main color
        print(info_prefix + ".:" + color_one, "Text", color_cls) #color1
        print(info_prefix + ".:" + color_two, "Текст", color_cls, "\n") #color2
        print(info_prefix + f"mesbox = {mesbox}") #don't touch, pls
        print(info_prefix + f"meswarn = {meswarn}") #it's too
    
    new_name = "------------ News ------------"
    news_version = launch_version
    news_1 = "."
    news_2 = "."

# Ru Lang
elif lang == "eng":

    # MessageBox
    # Default:  Num1 - messagebox_name = launch_name
    #           Num2 - messagebox_name = "Your_txt"
    messagebox_text = "Are you sure you want to go out?"
    messagebox_name = launch_name
    messagebox_warn_text = f"{console_prefix}MessageBox is disabled. This is message can be turned off in the config.py . P.S. The variable of this message is meswarn" # console

    ram_txt = "RAM"
    mb = "mb"

    app_is_closed_text = f"{console_prefix}App - {color_one}OFF{color_cls}" # console

    txt_info()

    imports_loaded = f"{console_prefix}Libs - {color_two}Loaded{color_cls}"            # console
    assets_loaded = f"{console_prefix}Assets - {color_two}Loaded{color_cls}"           # console
    lang_loaded = f"{console_prefix}Lang - {color_two}Loaded{color_cls}"               # console
    cfg_loaded = f"{console_prefix}Config - {color_two}Loaded{color_cls}"              # console
    db_cfg_loaded = f"{console_prefix}Data Base Config - {color_two}Loaded{color_cls}" # console

    def cfg_settings():   # console
        print(info_prefix + "Version: ", launch_version)                           
        print(info_prefix + "Lang: ", lang)
        print(info_prefix + "Launcher Name: ", launch_name)
        print(info_prefix + "Display: " + display)
        print(info_prefix + "Prefix: " + prefix)
        print(info_prefix + "Main Color:" + color, "123", color_cls)
        print(info_prefix + "Color 1:" + color_one, "Text", color_cls)
        print(info_prefix + "Color 2:" + color_two, "Текст", color_cls, "\n")
        print(info_prefix + f"mesbox = {mesbox}")
        print(info_prefix + f"meswarn = {meswarn}")
    
    new_name = "------------ News ------------"
    news_version = launch_version
    news_1 = "Bug's fix"
    news_2 = "Fabric will a loading with speed x2, lol"

# Ru Lang
elif lang == "ru":

    # MessageBox
    # Стандарт: Num1 - messagebox_name = launch_name
    #           Num2 - messagebox_name = "Your_txt"
    messagebox_text = "Вы точно хотите выйти?"
    messagebox_name = launch_name
    messagebox_warn_text = f"{console_prefix}MessageBox выключен. Это сообщение можно выключить в config.py" # console

    ram_txt = "ОЗУ"
    mb = "мб"

    app_is_closed_text = f"{console_prefix}Программа - {color_one}OFF{color_cls}" # console

    txt_info()

    imports_loaded = f"{console_prefix}Библиотеки - {color_two}Загружены{color_cls}"       # console
    assets_loaded = f"{console_prefix}Ассеты - {color_two}Загружены{color_cls}"            # console
    lang_loaded = f"{console_prefix}Язык - {color_two}Загружен{color_cls}"                 # console
    cfg_loaded = f"{console_prefix}Конфиг - {color_two}Загружен{color_cls}"                # console
    db_cfg_loaded = f"{console_prefix}Конфиг Базы Данных - {color_two}Загружен{color_cls}" # console

    def cfg_settings():   # console    
        print(info_prefix + "Версия: ", launch_version)                      
        print(info_prefix + "Язык: ", lang)
        print(info_prefix + "Название: ", launch_name)
        print(info_prefix + "Разрешение: " + display)
        print(info_prefix + "Prefix: " + prefix)
        print(info_prefix + "Основной цвет:" + color, "123", color_cls)
        print(info_prefix + "Цвет 1:" + color_one, "Text", color_cls)
        print(info_prefix + "Цвет 2:" + color_two, "Текст", color_cls, "\n")
        print(info_prefix + f"mesbox = {mesbox}")
        print(info_prefix + f"meswarn = {meswarn}")
    
    new_name = "------------ News ------------"
    news_version = launch_version
    news_1 = "Исправлено множество багов"
    news_2 = "Ускорен запуск Minecraft Fabric"

        


#error: Language not found 
else:
    print(f'{info_prefix}{color_one}ENG Err: Language not found{color_cls}') # console
    print(f'{info_prefix}{color_one}RU Err: Язык не найден{color_cls}')      # console