# https://veres.tech
# ver. 0.1

import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import time
import board
import math
import busio
import terminalio
import displayio
from adafruit_display_text import label
import gc9a01



# Function to display image on the screen
def display_image(path):
    img_bitmap = displayio.OnDiskBitmap(open(path, "rb"))
    img_palette = displayio.ColorConverter()
    img_tilegrid = displayio.TileGrid(img_bitmap, pixel_shader=img_palette)
    main.append(img_tilegrid)


def navigate_menu():
    display_image ("/images/navigate_menu.bmp")
    menu_idle_timer = 0
    exit_timer = 0
    time.sleep(1)
    while True:
        if not buttons[0].value:
            kbd.press(Keycode.ENTER)
            time.sleep(.09)
            kbd.release(Keycode.ENTER)
            time.sleep(.09)
            menu_idle_timer = 0
        if not buttons[1].value:
            kbd.press(Keycode.UP_ARROW)
            time.sleep(.09)
            kbd.release(Keycode.UP_ARROW)
            time.sleep(.09)
            menu_idle_timer = 0
# Hold down for exit to main menu.
        if not buttons[2].value:
            if exit_timer < 50:
                exit_timer = exit_timer + 1
                menu_idle_timer = 0
            elif exit_timer >= 50:
                display_image ("/images/main_menu.bmp")
                time.sleep(1)
                return
# Release for 'down' navigation
        if buttons[2].value:
            if exit_timer !=0:
                kbd.press(Keycode.DOWN_ARROW)
                time.sleep(.09)
                kbd.release(Keycode.DOWN_ARROW)
                time.sleep(.09)
                menu_idle_timer = 0
                exit_timer = 0
        if not buttons[3].value:
            kbd.press(Keycode.ONE)
            time.sleep(.09)
            kbd.release(Keycode.ONE)
            time.sleep(.09)
            menu_idle_timer = 0
        if not buttons[4].value:
            kbd.press(Keycode.TWO)
            time.sleep(.09)
            kbd.release(Keycode.TWO)
            time.sleep(.09)
            menu_idle_timer = 0
        if menu_idle_timer == 1500:
            display_image ("/images/main_menu.bmp")
            time.sleep(1)
            return
        menu_idle_timer = menu_idle_timer + 1
        time.sleep(0.01)

def media_menu():
    display_image ("/images/media_menu.bmp")
    menu_idle_timer = 0
    time.sleep(1)
    while True:
        if not buttons[1].value:
            kbd.press(Keycode.X)
            time.sleep(.09)
            kbd.release(Keycode.X)
            time.sleep(.09)
            menu_idle_timer = 0
        if not buttons[2].value:
            display_image ("/images/main_menu.bmp")
            time.sleep(1)
            return
        if not buttons[3].value:
            kbd.press(Keycode.V)
            time.sleep(.09)
            kbd.release(Keycode.V)
            time.sleep(.09)
            menu_idle_timer = 0
        if not buttons[4].value:
            kbd.press(Keycode.N)
            time.sleep(.09)
            kbd.release(Keycode.N)
            time.sleep(.09)
            menu_idle_timer = 0
        if menu_idle_timer == 3000:
            display_image ("/images/main_menu.bmp")
            time.sleep(1)
            return
        menu_idle_timer = menu_idle_timer + 1
        time.sleep(0.01)
        
def display_menu():
    display_image ("/images/display_menu.bmp")
    menu_idle_timer = 0
    time.sleep(1)
    while True:
        if not buttons[1].value:
            kbd.press(Keycode.F2)
            time.sleep(.09)
            kbd.release(Keycode.F2)
            time.sleep(.09)
            menu_idle_timer = 0
        if not buttons[2].value:
            display_image ("/images/main_menu.bmp")
            time.sleep(1)
            return
        if not buttons[3].value:
            kbd.press(Keycode.F9)
            time.sleep(.09)
            kbd.release(Keycode.F9)
            time.sleep(.09)
            menu_idle_timer = 0
        if not buttons[4].value:
            kbd.press(Keycode.F10)
            time.sleep(.09)
            kbd.release(Keycode.F10)
            time.sleep(.09)
            menu_idle_timer = 0
        if menu_idle_timer == 1500:
            display_image ("/images/main_menu.bmp")
            time.sleep(1)
            return
        menu_idle_timer = menu_idle_timer + 1
        time.sleep(0.01)

def apps_menu():
    display_image ("/images/apps_menu.bmp")
    menu_idle_timer = 0
    time.sleep(1)
    while True:
        if not buttons[1].value:
            kbd.press(Keycode.J)
            time.sleep(.09)
            kbd.release(Keycode.J)
            time.sleep(.09)
            menu_idle_timer = 0
        if not buttons[2].value:
            display_image ("/images/main_menu.bmp")
            time.sleep(1)
            return
        if not buttons[3].value:
            kbd.press(Keycode.M)
            time.sleep(.09)
            kbd.release(Keycode.M)
            time.sleep(.09)
            menu_idle_timer = 0
        if not buttons[4].value:
            kbd.press(Keycode.F)
            time.sleep(.09)
            kbd.release(Keycode.F)
            time.sleep(.09)
            menu_idle_timer = 0
        if menu_idle_timer == 1500:
            display_image ("/images/main_menu.bmp")
            time.sleep(1)
            return
        menu_idle_timer = menu_idle_timer + 1
        time.sleep(0.01)
        
def screen_saver():
    display_image ("/images/a.bmp")
    time.sleep(1)
    while True:
        if not buttons[1].value:
            display_image ("/images/main_menu.bmp")
            time.sleep(1)
            return
        if not buttons[2].value:
            display_image ("/images/main_menu.bmp")
            time.sleep(1)
            return
        if not buttons[3].value:
            display_image ("/images/main_menu.bmp")
            time.sleep(1)
            return
        if not buttons[4].value:
            display_image ("/images/main_menu.bmp")
            time.sleep(1)
            return
        time.sleep(0.01)
        
# Release any resources currently in use for the displays
displayio.release_displays()

#setup GPIO for display
tft_clk = board.GP10 # must be a SPI CLK
tft_mosi= board.GP11 # must be a SPI TX
tft_rst = board.GP12
tft_dc  = board.GP8
tft_cs  = board.GP9
tft_bl  = board.GP13
spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)
#setup GPIO for joystick
joySel   = board.GP19
joyUp    = board.GP21
joyDown  = board.GP18
joyLeft  = board.GP20
joyRight = board.GP17

button_pins = (joySel, joyUp, joyDown, joyLeft, joyRight)
buttons = []
for button_pin in button_pins:
    pin = digitalio.DigitalInOut(button_pin)
    pin.switch_to_input(digitalio.Pull.UP)
    buttons.append(pin)
    


# Make the displayio SPI bus and the GC9A01 display
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = gc9a01.GC9A01(display_bus, width=240, height=240, backlight_pin=tft_bl)

# Make the main display context
main = displayio.Group()
display.show(main)

# Draw boot timer text label
display_image ("/images/a.bmp")
text = ""
text_area = label.Label(terminalio.FONT, text=text, color=0x000000, anchor_point=(0.5,0.5), anchored_position=(0,0))
text_group = displayio.Group(scale=4)
text_group.append(text_area) 
main.append(text_group)

# Animate the text 
theta = math.pi
r = 75
x = 30

while x > 0:
    text_area.text = str(x)
    #debug
    #print(time.monotonic(),str(x))
    text_group.x = 120 + int(r * math.sin(theta))
    text_group.y = 120 + int(r * math.cos(theta))
    theta -= 0.1
    time.sleep(1)
    x = x -1
main.pop()  # remove image
#display_image ("/images/lets_go.bmp")

#time.sleep(5)
# Initialize Keybaord
kbd = Keyboard(usb_hid.devices)
#main.pop()  # remove image
time.sleep(1)
display_image ("/images/main_menu.bmp")
screensaver = 0
while True:
    if not buttons[1].value:
        screensaver = 0
        media_menu()
    if not buttons[2].value:
        screensaver = 0
        apps_menu()
    if not buttons[3].value:
        screensaver = 0
        navigate_menu()
    if not buttons[4].value:
        screensaver = 0
        display_menu()
    if screensaver == 9000:
        screensaver = 0
        screen_saver()
    screensaver = screensaver + 1
    time.sleep(0.01)
