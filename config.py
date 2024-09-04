#    ____  ____  _      ____  ____  _     _____
#   /   _\/  _ \/ \  /|/ ___\/  _ \/ \   /  __/
#   |  /  | / \|| |\ |||    \| / \|| |   |  \  
#   |  \__| \_/|| | \||\___ || \_/|| |_/\|  /_ 
#   \____/\____/\_/  \|\____/\____/\____/\____\
                                          
# Специально для тех кто копается в файлах моего лаунчера(его создателя), не ебите мозги владельцам
# сервер, то что он частично на английском, а частично на русском - этот лаунчер полностью принадлежит ESphagnum,то есть мне.
# Я изначально делал его для гит хаб, поэтому добавил поддержку английского и кастомного языке.
# В том числе я писал подсказки ввезде на мировом языке, то есть на Английском.

# Мои Аккаунты
# Discord: id: xydownik_  ник: ESphagnum
# Minecraft: ESphagnumOff, McFukker


# Language selection: custom, ru, eng
lang = "ru"

with open('_internal/data/ram.data', 'r') as file:
    ozu = int(file.read())

# Colors
from colorama import Fore, Back, Style
color = Fore.CYAN
color_one = Back.RED
color_two = Fore.GREEN

color_cls = Style.RESET_ALL

# Standart: launch_files = "BeeLauncher"
#           launch_name = "Launcher"
#           info_prefix = "[console] "
#           prefix = "Bee_"
launch_files = "VWPLLauncher"
launch_version = "Launcher 1.0C Login Support"
launch_name = "Launcher"
console_name = "CONSOLE"
info_name = "INFO"
console_prefix = f" [{color}{console_name}{color_cls}] " #Prefix In The Console
info_prefix = f" [{color_two}{info_name}{color_cls}] "
prefix = "ES_" #Prefix In The NickName

# Standart: display = "800x500"
display = "800x500"

# MessageBox
# Standart: mesbox = True
#
# True/False
mesbox = True
# Standart: meswarn = True
meswarn = True

def txt_info():
    print(color, """
        8 8888 b.             8 8 8888888888       ,o888888o.     
        8 8888 888o.          8 8 8888          . 8888     `88.   
        8 8888 Y88888o.       8 8 8888         ,8 8888       `8b  
        8 8888 .`Y888888o.    8 8 8888         88 8888        `8b 
        8 8888 8o. `Y888888o. 8 8 888888888888 88 8888         88 
        8 8888 8`Y8o. `Y88888o8 8 8888         88 8888         88 
        8 8888 8   `Y8o. `Y8888 8 8888         88 8888        ,8P 
        8 8888 8      `Y8o. `Y8 8 8888         `8 8888       ,8P  
        8 8888 8         `Y8o.` 8 8888          ` 8888     ,88'   
        8 8888 8            `Yo 8 8888             `8888888P'     \n""", color_cls)
    

