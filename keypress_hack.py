import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


KEY_UP = 17
KEY_DOWN = 45
KEY_LEFT = 30
KEY_RIGHT = 32
SPACE_BAR = 52

KEY_UP_LEFT = 16
KEY_UP_RIGHT = 18
KEY_DOWN_LEFT = 44
KEY_DOWN_RIGHT = 46

class AliceGameExeInputSender:
    def upKey(self):
        PressKey(KEY_UP)
        time.sleep(0.4)
        ReleaseKey(KEY_UP)
        time.sleep(0.4)
    def downKey(self):
        PressKey(KEY_DOWN)
        time.sleep(0.4)
        ReleaseKey(KEY_DOWN)
        time.sleep(0.4)
    def leftKey(self):
        PressKey(KEY_LEFT)
        time.sleep(0.4)
        ReleaseKey(KEY_LEFT)
        time.sleep(0.4)
    def rightKey(self):
        PressKey(KEY_RIGHT)
        time.sleep(0.4)
        ReleaseKey(KEY_RIGHT)
        time.sleep(0.4)
    def move(self):
        PressKey(SPACE_BAR)
        time.sleep(0.4)
        ReleaseKey(SPACE_BAR)
        time.sleep(0.4)
    def __directionKey(self, pathPos, previousPathPos): 
        xPos = pathPos[0]; xPreviousPos = previousPathPos[0]
        yPos = pathPos[1]; yPreviousPos = previousPathPos[1]
        xDelay = abs(xPreviousPos-xPos)
        yDelay = abs(yPreviousPos-yPos)
        if yPos == yPreviousPos:
            if xPos < xPreviousPos:
                return (KEY_UP, xDelay)
            if xPos > xPreviousPos:
                return (KEY_DOWN, xDelay)
        if xPos == xPreviousPos:
            if yPos < yPreviousPos:
                return (KEY_LEFT, yDelay)  
            if yPos > yPreviousPos:
                return (KEY_RIGHT, yDelay)
        if xPos < xPreviousPos:
            if yPos < yPreviousPos:
                return (KEY_UP_LEFT, xDelay + yDelay)
            if yPos > yPreviousPos:
                return (KEY_UP_RIGHT, xDelay + yDelay)
        if xPos > xPreviousPos:
            if yPos < yPreviousPos:
                return (KEY_DOWN_LEFT, xDelay + yDelay)
            if yPos > yPreviousPos:
                return (KEY_DOWN_RIGHT, xDelay + yDelay)
          
    def automate(self, shortestPath):
        time.sleep(2)
        previousPos = None
        for pathPos in shortestPath:
            if previousPos:
                print(pathPos)     
                directionKey = self.__directionKey(pathPos, previousPos)
                PressKey(directionKey[0])
                time.sleep(0.4)
                ReleaseKey(directionKey[0])
                time.sleep(0.4)
                print(directionKey)
                time.sleep(0.9)
                self.move()
                time.sleep(0.2*directionKey[1])
                print('move')
            previousPos = pathPos