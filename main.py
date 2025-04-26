import threading
import time

import keyhandling

VK_ALT = 0x12
VK_R_CTRL = 0xA3


def is_combo_pressed(combo_key):
    return (keyhandling.is_pressed(VK_ALT) or keyhandling.is_pressed(VK_R_CTRL)) and keyhandling.is_pressed(combo_key)


def worker(button, event, delay):
    while not event.is_set():
        keyhandling.press(button)
        time.sleep(delay)


def toggle_thread(button, thread, event, delay=0.):
    if thread and thread.is_alive():
        print("Stopping thread")
        event.set()
        thread.join()
        return None, event
    else:
        print("Starting thread")
        event.clear()
        thread = threading.Thread(target=worker, args=(button, event, delay), daemon=True)
        thread.start()
        return thread, event


def handle(combo_key, button, thread, event, delay=0.):
    if is_combo_pressed(combo_key):
        thread, event = toggle_thread(button, thread, event, delay)
        time.sleep(0.5)
    return thread, event


def handle_multiple(combo_key, button_dict, threads, events):
    if len(button_dict) > 0 and is_combo_pressed(combo_key):
        for i, (key, value) in enumerate(button_dict.items()):
            threads[i], events[i] = toggle_thread(key, threads[i], events[i], float(value))
        time.sleep(0.5)
    return threads, events


def setup_jump():
    combo_key = keyhandling.to_key_code(input("Input your Jump Combo Key\n"))
    jump_button = keyhandling.to_key_code(input("Input your Jump Button\n"))
    jump_thread = None
    jump_event = threading.Event()
    return combo_key, jump_button, jump_thread, jump_event


def setup_spell():
    combo_key = keyhandling.to_key_code(input("Input your Spell Combo Key\n"))
    spell_button = keyhandling.to_key_code(input("Input your Spell Button\n"))
    spell_thread = None
    spell_event = threading.Event()
    return combo_key, spell_button, spell_thread, spell_event


def setup_quick_menu():
    combo_key = keyhandling.to_key_code(input("Input your Quick Menu Combo Key\n"))
    quick_menu_events = []
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
        quick_menu_events.append(threading.Event())
    quick_menu_threads = [None] * len(quick_menu_buttons)
    return combo_key, quick_menu_buttons, quick_menu_threads, quick_menu_events


def main():
    sck, sb, st, se = setup_spell()
    jck, jb, jt, je = setup_jump()
    qmck, qmb, qmt, qme = setup_quick_menu()

    try:
        while True:
            st, se = handle(sck, sb, st, se)
            jt, je = handle(jck, jb, jt, je, 0.1)
            qmt, qme = handle_multiple(qmck, qmb, qmt, qme)

    except KeyboardInterrupt:
        print("Exiting\n")


if __name__ == "__main__":
    main()
