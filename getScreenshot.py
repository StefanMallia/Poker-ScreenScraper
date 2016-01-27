import win32gui
import win32ui
import win32con
from ctypes import windll
from PIL import Image
import ctypes
from ctypes import windll, byref, wintypes

#install pywin32 and set environment variable to C:\Python34\Lib\site-packages\pywin32_system32


def getWindowTitle(string_input):
    #input part of title to get full title
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible

    titles = []
    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):       
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            titles.append((hwnd, buff.value))
        return True
    EnumWindows(EnumWindowsProc(foreach_window), 0)

    index = -1
    for i in range(len(titles)):
        if string_input in titles[i][1]:
            index = i

    return titles[index][1]

            
def getScreenshot(string_input):

    
    #http://stackoverflow.com/questions/19695214/python-screenshot-of-inactive-window-printwindow-win32gui
        
    hwnd = win32gui.FindWindow(None, string_input)
    win32gui.MoveWindow(hwnd, 0, 0, 1493, 1058, 0)


    # Change the line below depending on whether you want the whole window
    # or just the client area. 
    #left, top, right, bot = win32gui.GetClientRect(hwnd)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area. 
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    #print(result)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        #PrintWindow Succeeded
        return im
