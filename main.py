import keyhandling
from threadhandling import ThreadHandler

VK_ALT = 0x12
VK_R_CTRL = 0xA3


def is_combo_pressed(combo_key):
    return (keyhandling.is_pressed(VK_ALT) or keyhandling.is_pressed(VK_R_CTRL)) and keyhandling.is_pressed(combo_key)


def handle(combo_key, button, thread_handler, delay=0.):
    if is_combo_pressed(combo_key):
        thread_handler.toggle_thread(button, delay)


def handle_multiple(combo_key, button_dict, thread_handlers):
    if len(button_dict) > 0 and is_combo_pressed(combo_key):
        for i, (key, value) in enumerate(button_dict.items()):
            thread_handlers[i].toggle_thread(key, float(value))


def setup_jump():
    combo_key = keyhandling.to_key_code(input("Input your Jump Combo Key\n"))
    jump_button = keyhandling.to_key_code(input("Input your Jump Button\n"))
    jump_thread_handler = ThreadHandler()
    return combo_key, jump_button, jump_thread_handler


def setup_spell():
    combo_key = keyhandling.to_key_code(input("Input your Spell Combo Key\n"))
    spell_button = keyhandling.to_key_code(input("Input your Spell Button\n"))
    spell_thread_handler = ThreadHandler()
    return combo_key, spell_button, spell_thread_handler


def setup_quick_menu():
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
    qmck, qmb, qmth = setup_quick_menu()

    try:
        while True:
            handle(sck, sb, sth)
            handle(jck, jb, jth, 0.1)
            handle_multiple(qmck, qmb, qmth)

    except KeyboardInterrupt:
        print("Exiting\n")
    finally:
        for thread_handler in [sth, jth] + qmth:
            thread_handler.stop_thread()


if __name__ == "__main__":
    main()
