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


def setup_jump():
    if input("Do you want to setup jump? (y/n)\n") != "y":
        return None, None, None
    combo_key = keyhandling.to_key_code(input("Input your Jump Combo Key\n"))
    jump_button = keyhandling.to_key_code(input("Input your Jump Button\n"))
    jump_thread_handler = ThreadHandler()
    return combo_key, jump_button, jump_thread_handler


def setup_spell():
    if input("Do you want to setup spell? (y/n)\n") != "y":
        return None, None, None
    combo_key = keyhandling.to_key_code(input("Input your Spell Combo Key\n"))
    spell_button = keyhandling.to_key_code(input("Input your Spell Button\n"))
    spell_thread_handler = ThreadHandler()
    return combo_key, spell_button, spell_thread_handler

def setup_sneak():
    if input("Do you want to setup sneak? (y/n)\n") != "y":
        return None, None, None
    combo_key = keyhandling.to_key_code(input("Input your Sneak Combo Key\n"))
    button1 = keyhandling.to_key_code(input("Input your Sneak Button 1\n"))
    button2 = keyhandling.to_key_code(input("Input your Sneak Button 2\n"))
    sneak_buttons = [button1, button2]
    sneak_thread_handler = ThreadHandler()
    return combo_key, sneak_buttons, sneak_thread_handler


def setup_quick_menu():
    if input("Do you want to setup quick_menu? (y/n)\n") != "y":
        return None, None, []
    combo_key = keyhandling.to_key_code(input("Input your Quick Menu Combo Key\n"))
    quick_menu_thread_handlers = []
    quick_menu_buttons = {}
    while True:
        key = input("Input which quick_menu slots you use (1-8) or exit using q\n")
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
    sck, sb, sth = setup_spell()
    jck, jb, jth = setup_jump()
    snck, snb, snth = setup_sneak()
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
