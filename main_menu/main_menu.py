from . import options
import standard as std

OPT_PROJECT = ["Load project", "Create project", "Save project"]
OPT_MODPACK = ["Add mod(s)", "Remove mod(s)"]
OPT_CONFIG = ["Change project name", "Change project version", "Change mod loader", "Change Minecraft version"]


def menu_options(flags) -> None:
    opt = std.get_functions(options)
    for i in range(len(OPT_PROJECT)):
        print(f"{i+1}:  ")


def main_menu():
    done = False
    opt = std.get_functions(options)
    print(opt)
    while not done:
        sel = int(input("Please enter your selected option: "))
        if sel <= 0 or sel-1 >= len(opt):
            print(f"Option {sel} is not a valid option.")
            return
        func = opt[sel-1]
        options.func()