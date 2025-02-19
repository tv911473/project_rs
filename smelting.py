"""smelting bot"""
import pyautogui
import time
import random
import winsound
from pynput import mouse, keyboard

stop_flag = False

def record_positions():
    positions = []
    print("Move the mouse to the desired position and right-click to record the position")
    print("Press 'f' to finish recording")

    def on_click(x, y, button, pressed):
        if pressed:
            if button == mouse.Button.right:
                positions.append((x, y))
                print(f"Position recorded: {x}, {y}")

    def on_press(key):
        try:
            if key.char == 'f':
                print("Recording finished")
                return False
        except AttributeError:
            pass

    with mouse.Listener(on_click=on_click) as mouse_listener, \
        keyboard.Listener(on_press=on_press) as keyboard_listener:
        keyboard_listener.join()
        mouse_listener.stop()

    return positions

# Bezier curve formula
def bezier_curve(p0, p1, p2, p3, t):
    return (
        (1 - t) ** 3 * p0 +
        3 * (1 - t) ** 2 * t * p1 +
        3 * (1 - t) * t ** 2 * p2 +
        t ** 3 * p3
    )
# human-like manner, with controlled curves
def move_mouse_smoothly(start, end, duration, max_offset=50):
    x1, y1 = start
    x4, y4 = end

    x2, y2 = x1 + random.uniform(-max_offset, max_offset), y1 + random.uniform(-max_offset / 2, max_offset)
    x3, y3 = x4 + random.uniform(-max_offset, max_offset), y4 + random.uniform(-max_offset / 2, max_offset)

    if y2 < y1 - max_offset / 3:
        y2 = y1 - random.uniform(0, max_offset / 3)
    if y3 < y4 - max_offset / 3:
        y3 = y4 - random.uniform(0, max_offset / 3)

    start_time = time.time()

    while time.time() - start_time < duration:
        if stop_flag:
            return
        t = (time.time() - start_time) / duration
        x = bezier_curve(x1, x2, x3, x4, t)
        y = bezier_curve(y1, y2, y3, y4, t)
        pyautogui.moveTo(x, y)
        time.sleep(0.01)

    pyautogui.moveTo(x4, y4)

def perform_actions(positions):
    global stop_flag
    saved_click_pos = positions[0]
    break_start = 51
    break_stop = 56

    if stop_flag:
        return

    # left-click on position
    x1_pos = saved_click_pos[0] + random.uniform(-50, 50)
    y1_pos = saved_click_pos[1] + random.uniform(-50, 50)
    move_mouse_smoothly(pyautogui.position(), (x1_pos, y1_pos), duration=random.uniform(0.2, 0.8))
    pyautogui.mouseDown(button='left')
    time.sleep(random.uniform(0.05, 0.25))
    pyautogui.mouseUp(button='left')
    time.sleep(random.uniform(0.7, 1.2))

    if stop_flag:
        return

    # deposit with key 1
    pyautogui.keyDown('1')
    time.sleep(random.uniform(0.07, 0.23))  # Delay between press and release
    pyautogui.keyUp('1')
    time.sleep(random.uniform(0.5, 1))

    if stop_flag:
        return

    pyautogui.keyDown('space')
    time.sleep(random.uniform(0.07, 0.23))
    pyautogui.keyUp('space')

    # random in-game delay
    if random.random() < 0.2:
        random_break = random.uniform(5, 20)
        print(f"Random break for {random_break:.2f} seconds")
        time.sleep(random_break)

    if stop_flag:
        return

    break_length = random.uniform(break_start, break_stop)
    print(f"Break for {break_length:.2f} seconds")
    time.sleep(break_length)

def auto_clicker(position, cycles):
    global stop_flag

    initial_delay = 5
    print(f"Starting in {initial_delay} seconds")
    time.sleep(initial_delay)

    time_start = time.time()

    print("Auto clicking started. Press 'q' to stop")

    def on_press(key):
        global stop_flag
        try:
            if key.char == 'q':
                print("Auto clicking stopped")
                stop_flag = True
                return False
        except AttributeError:
            pass

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    try:
        for cycle in range(cycles):
            if stop_flag:
                break
            print(f"Cycle {cycle + 1}/{cycles}")
            perform_actions(position)

    except KeyboardInterrupt:
        print("Bot interrupted.")
    finally:
        time_stop = time.time()
        listener.stop()
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)


    total_time = time_stop - time_start
    hours, reminder = divmod(total_time, 3600)
    minutes, seconds = divmod(reminder, 60)
    print(f"Total time spent:  {int(hours)}:{int(minutes)}:{int(seconds)}")

def get_numeric_input(prompt):
    while True:
        user_input = input(prompt).strip()
        # Filter out non-numeric characters
        numeric_input = ''.join(filter(str.isdigit, user_input))
        if numeric_input:
            return int(numeric_input)
        else:
            print("Enter a numeric value")

# Main script
if __name__ == "__main__":
    print("Recording mouse positions")
    recorded_positions = record_positions()

    if recorded_positions:
        cycles = get_numeric_input("Enter the number of cycles to run: ")
        auto_clicker(recorded_positions, cycles)
    else:
        print("No positions recorded. Exiting")