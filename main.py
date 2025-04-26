import keyhandling
from threadhandling import ThreadHandler

VK_ALT = 0x12
VK_R_CTRL = 0xA3


def is_combo_pressed(combo_key):
    return (keyhandling.is_pressed(VK_ALT) or keyhandling.is_pressed(VK_R_CTRL)) and keyhandling.is_pressed(combo_key)

def handle(combo_key, function, button, thread_handler, delay=0.):
    if combo_key is not None and is_combo_pressed(combo_key):
        thread_handler.toggle_thread(function,button, delay)


def handle_multiple(combo_key, function, button_dict, thread_handlers):
    if combo_key is not None and len(button_dict) > 0 and is_combo_pressed(combo_key):
        for i, (key, value) in enumerate(button_dict.items()):
            thread_handlers[i].toggle_thread(function,key, float(value))


def setup_simple(setup_type:str):
    if input(f"Do you want to setup {setup_type}? (y/n)\n") != "y":
        return None, None, None
    combo_key = keyhandling.to_key_code(input(f"Input your {setup_type} Combo Key\n"))
    button = keyhandling.to_key_code(input(f"Input your {setup_type} Button\n"))
    thread_handler = ThreadHandler()
    return combo_key, button, thread_handler

def setup_alternating(setup_type:str):
    if input("Do you want to setup sneak? (y/n)\n") != "y":
        return None, None, None
    combo_key = keyhandling.to_key_code(input(f"Input your {setup_type} Combo Key\n"))
    i = 1
    buttons = []
    while True:
        key = input(f"Input your {setup_type} Button {i} or escape using q\n")
        if key == "q":
            break
        i += 1
        buttons.append(keyhandling.to_key_code(key))
    thread_handler = ThreadHandler()
    return combo_key, buttons, thread_handler


def setup_quick_menu():
    if input("Do you want to setup quick_menu? (y/n)\n") != "y":
        return None, None, []
    combo_key = keyhandling.to_key_code(input("Input your Quick Menu Combo Key\n"))
    quick_menu_thread_handlers = []
    quick_menu_buttons = {}
    while True:
        key = input("Input which quick_menu slots you use (1-8) or escape using q\n")
        if key == "q":
            print("Finished creating quick menu buttons")
            break
        if not key.isdigit() or int(key) > 8 or int(key) < 1:
            print("Invalid input. Try again!")
            continue
        try:
            delay = float(input("Input how long you want to wait before next usage in seconds\n"))
        except ValueError:
            print("Invalid delay. Try again!")
            continue
        quick_menu_buttons[keyhandling.to_key_code(key)] = delay
        quick_menu_thread_handlers.append(ThreadHandler())
    return combo_key, quick_menu_buttons, quick_menu_thread_handlers


def main():
    sck, sb, sth = setup_simple("spell")
    jck, jb, jth = setup_simple("jump")
    snck, snb, snth = setup_alternating("sneak")
    qmck, qmb, qmth = setup_quick_menu()

    print("Finished setup")

    try:
        while True:
            handle(sck,keyhandling.press , sb, sth)
            handle(jck,keyhandling.press, jb, jth, 0.1)
            handle(snck,keyhandling.alternate_press, snb, snth)
            handle_multiple(qmck,keyhandling.press, qmb, qmth)

    except KeyboardInterrupt:
        print("Exiting\n")
    finally:
        for thread_handler in [sth, jth, snth] + qmth:
            if thread_handler:
                thread_handler.stop_thread()


if __name__ == "__main__":
    main()
