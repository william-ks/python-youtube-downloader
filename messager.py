from colorama import init, Fore

init(autoreset=True)


class Messager():
    def green_line(self):
        print(f"{Fore.GREEN}{'-'*50}")

    def red_line(self):
        print(f"{Fore.RED}{'-'*50}")

    def blue_line(self):
        print(f"{Fore.BLUE}{'-'*50}")

    def cyan_line(self):
        print(f"{Fore.CYAN}{'-'*50}")
