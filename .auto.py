# Imports
import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode, Key, Controller as KeyboardController

# Configurações
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
        print("Iniciando clicks...")
        self.running = True

    def stop_clicking(self):
        print("Parando clicks...")
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

class Snake(threading.Thread):
    def __init__(self):
        super(Snake, self).__init__()
        self.running = False
        self.program_running = True

    def start_snaking(self):
        print("Iniciando modo Snake...")
        self.running = True

    def stop_snaking(self):
        print("Parando modo Snake...")
        self.running = False

    def exit(self):
        self.stop_snaking()
        self.program_running = False

    def run(self):
        while self.program_running:
            firstTime = True
            while self.running:
                if firstTime:
                    try:
                        keyboard.release(Key.ctrl)
                        keyboard.release(Key.shift)
                        keyboard.release('g')
                        keyboard.press(Key.shift)
                        keyboard.press('a')
                    except:
                        keyboard.press(Key.shift)
                        keyboard.press('a')
                    print("to preso")

                # Fora do IF
                keyboard.press('a')
                print("teste")
                #print("To rodando...")
                print(current)
                # Fora do While
                try:
                    keyboard.release(Key.ctrl)
                    keyboard.release(Key.shift)
                    keyboard.release('g')
                except:
                    pass
            try:
                keyboard.release(Key.ctrl)
                keyboard.release(Key.shift)
                keyboard.release('g')
            except:
                pass
            time.sleep(0.1)


mouse = Controller()
keyboard = KeyboardController()

click_thread = ClickMouse(delay, button)
click_thread.start()

snack_thread = Snake()
snack_thread.start()

def execute():

    # 0 == Não possui diferença
    # 1 > Possui diferença

    hasDifference = 0
    pressedHotKeyValues = []

    for i in range(len(COMBINATIONS)):
        pressedHotKeyValues.append(len(current.difference(COMBINATIONS[i])))

    if (pressedHotKeyValues[0] == hasDifference or pressedHotKeyValues[1] == hasDifference):
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
    elif (pressedHotKeyValues[4] == hasDifference or pressedHotKeyValues[5] == hasDifference):
        if snack_thread.running:
            snack_thread.stop_snaking()
        else:
            snack_thread.start_snaking()
    """
    elif (pressedHotKeyValues[6] == hasDifference or pressedHotKeyValues[7] == hasDifference):
        click_thread.exit()
        moviment_thread.exit()
        listener.stop()
    """
def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        try:
            current.remove(key)    
        except erro:
            print(erro)

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
