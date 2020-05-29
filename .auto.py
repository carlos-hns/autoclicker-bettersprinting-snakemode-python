# Imports
import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode, Key, Controller as KeyboardController

# Configs AutoClicker
delay = 0.06
button = Button.left

# HotKeys
COMBINATIONS = [

    # ATTACK
    {Key.ctrl, KeyCode(char='r')},
    {Key.ctrl, KeyCode(char='R')},

    # RUN IN GAME
    {Key.ctrl, KeyCode(char='f')},
    {Key.ctrl, KeyCode(char='F')},
    
    # SHIFT IN GAME
    {Key.ctrl, KeyCode(char='g')},
    {Key.ctrl, KeyCode(char='G')},

    # CLOSE PROCESS
    {Key.ctrl, KeyCode(char='v')},
    {Key.ctrl, KeyCode(char='V')},

]

current = set()

# Threads
class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(self.delay)  
            time.sleep(0.1)


class Snaker(threading.Thread):
    def __init__(self):
        super(Snaker, self).__init__()
        self.running = False
        self.program_running = True

    def start_snaking(self):
        self.running = True

    def stop_snaking(self):
        self.running = False

    def exit(self):
        self.stop_snaking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                keyboard.press(Key.shift_l)
                
            keyboard.release("G")
            keyboard.release(Key.shift_l)
            time.sleep(1)

class Runner(threading.Thread):
    def __init__(self):
        super(Runner, self).__init__()
        self.running = False
        self.program_running = True

    def start_snaking(self):
        self.running = True

    def stop_snaking(self):
        self.running = False

    def exit(self):
        self.stop_snaking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                keyboard.press(Key.ctrl_l)
                
            keyboard.release("F")
            keyboard.release(Key.ctrl_l)
            time.sleep(1)

# Draw Screen Console
def drawScreen():

    print("\n"*140)
    print("MADE BY: carlos-hns".center(90))
    print("AutoClicker: {}".format("[Ativado]" if click_thread.running else ["Desativado"]).center(89))
    print("Snake Mode: {}".format("[Ativado]" if snack_thread.running else ["Desativado"]).center(89))
    print("Run Mode: {}".format("[Ativado]" if run_thread.running else ["Desativado"]).center(89))
    
    print("\n"*5)


# Starting APP
mouse = Controller()
keyboard = KeyboardController()

click_thread = ClickMouse(delay, button)
click_thread.start()

snack_thread = Snaker()
snack_thread.start()

run_thread = Runner()
run_thread.start()

drawScreen()

# Setting Keyboard Listener

def execute():
    # 0 == don't has difference
    # 1 > has difference

    hasDifference = 0
    pressedHotKeyValues = []

    for i in range(len(COMBINATIONS)):
        pressedHotKeyValues.append(len(current.difference(COMBINATIONS[i])))

    if (pressedHotKeyValues[0] == hasDifference or pressedHotKeyValues[1] == hasDifference):
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
    elif (pressedHotKeyValues[2] == hasDifference or pressedHotKeyValues[3] == hasDifference):
        if run_thread.running:
            run_thread.stop_snaking()
        else:
            run_thread.start_snaking()
    elif (pressedHotKeyValues[4] == hasDifference or pressedHotKeyValues[5] == hasDifference):
        if snack_thread.running:
            snack_thread.stop_snaking()
        else:
            snack_thread.start_snaking()
    elif (pressedHotKeyValues[6] == hasDifference or pressedHotKeyValues[7] == hasDifference):
        click_thread.exit()
        snack_thread.exit()
        run_thread.exit()
        listener.stop()

    drawScreen()

def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        
        # De alguma forma esse método de exclusão
        # deixava um item dentro do set, por isso em cada função
        # é necessario remove-lo...

        #print("Debugando {}".format(current))
        #print("Tecla: {}".format(key))
        
        if key in current:
            current.remove(key)

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

