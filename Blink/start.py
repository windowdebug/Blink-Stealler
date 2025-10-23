import os 
from colorama import *
init()
os.system("title by @novaglitter")
os.system("cls")
r = Fore.LIGHTBLACK_EX + Style.BRIGHT
b = Fore.LIGHTBLUE_EX + Style.BRIGHT
w = Fore.LIGHTWHITE_EX + Style.BRIGHT

banner=rf'''
           {Fore.LIGHTWHITE_EX}                        ▄▄▄▄▄▄▄██▄▄▄▄▄▄▄
                              ▄▄██████▀▀▀▀▀▀▀▀▀▀██████▄▄
                            █████▀▀░░░░░░░░░░░░░░░░░░▀▀███   {b} ___  _     ___  _  _  _  __{Fore.RESET}
                            ███░░░▄▄▄▄▄░░░░░░░░▄▄▄▄▄░░░███   {b}| _ )| |   |_ _|| \| || |/ /{Fore.RESET}
                            ███░▄▀░░░▀██▄░░░░▄██▀░░░▀▄░███   {b}| _ \| |__  | | | .  ||   < {Fore.RESET}
                            ███░░░░░░░░▀█▀░░▀█▀░░░░░░░░███   {b}|___/|____||___||_|\_||_|\_\{Fore.RESET}
                            ███░░░{r}▓▓▓▓▓{Fore.RESET}░░░░░░░░{r}▓▓▓▓▓{Fore.RESET}░░░███     
                            ███░░░░░░░░░░░░░░░░░░░░░░░░███   {b}< {Fore.RESET}BLINK STEALER v-2.0 {b}>{Fore.RESET}
                            ███░░░░░░░░░░░░░░░░░░░░░░░░███
                            ███░░░░░░░░░░░░░░░░░░░░░░░░███   {b}<{Fore.RESET} Система защиты логов {b}>{Fore.RESET}
                            ███░░░█▄░░░░░▄██▄░░░░░▄█░░░███   {b}<{Fore.RESET} Двухканальная зашифровка {b}>{Fore.RESET}
                            ▀██▄░░░▀█▄▄▄██████▄▄▄█▀░░░▄██▀    
                             ▀██▄░░░▀████▀▀▀▀████▀░░░▄██▀    {b}<{Fore.RESET} Синхронизация Telegram и Discord {b}>{Fore.RESET}
                               ███▄░░░░░░░░░░░░░░░░▄███▀     {b}<{Fore.RESET} Соль и разделение хэша  {b}>{Fore.RESET}
                                ▀███▄░░░░░██░░░░░▄███▀       {b}<{Fore.RESET} Анти-реверсинг {b}>{Fore.RESET}
                                   ▀███▄░░██░░▄▄███▀ 
                                     ▀▀█████████▀            {b}<{Fore.RESET} Поддержка нескольких хостов файла-обмена {b}>{Fore.RESET}
                                          ▀▀▀                {b}<{Fore.RESET} @novaglitter {b}>{Fore.RESET}

'''

def main():
    print(banner)
    input(f"{b}< {w}BLINK {b}> {w}Ожидаю нажатия Enter...")

    try:
        from blink.main import build
        build()
    except Exception as e:
        print(f"{b}< {w}BLINK {b}> {w}Ошибка: {e}")
        input(f"{b}< {w}BLINK {b}> {w}Нажми Enter чтобы выйти.")

if __name__ == "__main__":
    main()