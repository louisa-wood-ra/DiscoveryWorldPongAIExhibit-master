import PySimpleGUI as sg

# import Queue
import threading
import time
from queue import Queue
# layout = [[sg.Button(f'{row}, {col}') for col in range(4)] for row in range(4)]

# event, values = sg.Window('List Comprehensions', layout, no_titlebar=True, alpha_channel=0.7).read(close=True)
import os
import exhibit.game
from exhibit.game import game_driver as gd
import exhibit.visualization
from exhibit.visualization import visualization_driver as vd
import importlib


killObject = "endThreads"
q = Queue()
q.put('noneActive')
def openMqttShell():
    fileLoc = 'cd C:\\"Program Files"\\Mosquitto\\' #cd C:\'Program Files'\Mosquitto\
    commandM = 'C:\\"Program Files"\\Mosquitto\\mosquitto -v -c ./mosquitto.conf'
    #"C:\Users\lawood\OneDrive - Rockwell Automation, Inc\Desktop\windowsPongScriptMosquitto.bat"
    os.system('start C:\\users\\"DW Pong"\\windowsPongScriptMosquitto.bat')
    #os.system(commandM)
#     #os.system("start " + fileName)
# def closeMosquittoShell():
#     os.system(str(signal.SIGINT))
def openEmulate3DShell():
    # fileLoc = 'cd C:\\Users\\"DW Pong"\\Downloads\\DiscoveryWorldPongAIExhibit-master\\DiscoveryWorldPongAIExhibit-master\\' 
    # commandM = 'C:\\"Program Files"\\Mosquitto\\mosquitto -v -c ./mosquitto.conf'
    #"C:\Users\lawood\OneDrive - Rockwell Automation, Inc\Desktop\windowsPongScriptMosquitto.bat"
    os.system('start C:\\Users\\"DW Pong"\\Downloads\\DiscoveryWorldPongAIExhibit-master\\DiscoveryWorldPongAIExhibit-master\\Pong_with_level.demo3d')
def closeEmulate3D():
    # print('not yet implemented')
    os.system("taskkill/im Demo3D2020x86.exe")

def long_function_thread(window):
    time.sleep(3)
    window.write_event_value('-THREAD DONE-', '')

def long_function():
    y.start()
    #time.sleep(1)

mqttActive = False
gameActive = False
visualizationActive = False
emulate3DActive = False

sg.theme('DarkAmber')   #
mqttButton = sg.Button('mqtt server',button_color=(sg.theme_element_text_color() +' on '+ sg.theme_background_color()))
gameButton = sg.Button('game',button_color=(sg.theme_element_text_color() +' on '+ sg.theme_background_color()))
visualizationButton = sg.Button('visualization',button_color=(sg.theme_element_text_color() +' on '+ sg.theme_background_color()))
Emulate3DButton = sg.Button('Emulate3D',button_color=(sg.theme_element_text_color() +' on '+ sg.theme_background_color()))
# All the stuff inside your window.

def startGameDriver():
    #import exhibit.game.game_driver as gd
    # reload(exhibit.game.game_driver)  
    # exhibit.game.game_driver.reload(gd)
    importlib.reload(gd)
    # functionT = gd.main
    threading.Thread(target=gd.main, args=(q,), name='gameThread', daemon=True).start()
    time.sleep(0.5)

def startVisualizationDriver():
    threading.Thread(target=vd.main, args=('',), name='visualizationThread', daemon=True).start()
def openVisualizationBrowser():
    os.system('start C:\\Users\\"DW Pong"\\Downloads\\DiscoveryWorldPongAIExhibit-master\\DiscoveryWorldPongAIExhibit-master\\visualizer\\index.html')

layout = [  [sg.Text('Some text on Row 1')],
            [sg.Text('Enter something on Row 2'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Close')],
            [mqttButton, gameButton, visualizationButton, Emulate3DButton] ]

# Create the Window
window = sg.Window('Pong Controller', layout, no_titlebar=True, alpha_channel=0.9, keep_on_top=True)
# Event Loop to process "events" and get the "values" of the inputs
#z = threading.Thread(target=gd.main, args=(q,), name='gameThread', daemon=True)
y = threading.Thread(target=long_function_thread, args=(window,), name='testThread', daemon=True)

while True:

    event, values = window.read(timeout=250)

    if not q.empty():
        tempQ2 = q.get()
        q.put(tempQ2)
        if tempQ2 == 'noneActive':
            gameActive = False
            gameButton.update(button_color=(sg.theme_element_text_color() +' on '+ sg.theme_background_color()))

    if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
        # close down everything
        break
    elif event == 'mqtt server':
        if False: #mqttActive:
            print('shuting down mqtt server')
            mqttActive = False
            mqttButton.update(button_color=(sg.theme_element_text_color() +' on '+ sg.theme_background_color()))

        elif mqttActive == False:
            mqttActive = True
            print('starting up mqtt server')
            openMqttShell()
            #mqttButton.button_text = "ehh"
            #mqttButton.ButtonColor = sg.theme_background_color()            
            mqttButton.update(button_color=(sg.theme_background_color() +' on '+ sg.theme_element_text_color()))

    elif event == 'game':
        if gameActive:
            
            if q.empty():
                print('shutting down game driver')
                q.put("endThreads")
                #z.join()                
                
                # gameActive = False
                # gameButton.update(button_color=(sg.theme_element_text_color() +' on '+ sg.theme_background_color()))
            else:
                print('no game thread active')

        else:
            
            if not q.empty():
                tempQ = q.get()
                if tempQ == 'noneActive':
                    while not q.empty(): # clear the queue
                        q.get()
                    print('starting up game driver')
                    gameActive = True
                    startGameDriver()
                    gameButton.update(button_color=(sg.theme_background_color() +' on '+ sg.theme_element_text_color()))
                else:
                    print('old game thread is not exited yet')

    elif event == 'visualization':
        if not visualizationActive:
            startVisualizationDriver()
            openVisualizationBrowser()
            visualizationActive = True
            visualizationButton.update(button_color=(sg.theme_background_color() +' on '+ sg.theme_element_text_color()))
            print('starting up visualization')

    elif event == 'Emulate3D':
        if emulate3DActive:
            closeEmulate3D()
            emulate3DActive = False
            Emulate3DButton.update(button_color=(sg.theme_element_text_color() +' on '+ sg.theme_background_color()))

        else:
            print('starting up Emulate3D')
            openEmulate3DShell()                    
            Emulate3DButton.update(button_color=(sg.theme_background_color() +' on '+ sg.theme_element_text_color()))
            emulate3DActive = True

    elif event == 'Ok':
        print('You entered ', values[0])
        long_function()
        print('Long function has returned from starting')

    elif event == '-THREAD DONE-':
        print('Your long operation completed')
    #else:
    #    print(event, values)
q.put("endThreads")
closeEmulate3D()
# if z.is_alive:
#     z.join()
#y.join()
window.close()