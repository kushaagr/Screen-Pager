import sys
import re
import socket
import threading
import keyboard as kb
import pyautogui as pgui

import debug_utils
from debug_utils import debug

debug_utils.dev_mode = False

valid_ip = re.compile(r'(?:\d{1,3}\.){3}\d{1,3}')
is_valid_ip = lambda address : valid_ip.search(address) != None

SS_NAME = "Screenshot.png"
PORT = 80
host_address = ''
have_ip = False

if len(sys.argv) > 1:
    host_address = sys.argv[1]
    have_ip = True
    debug(host_address)

debug("0.0.0.0 is valid?", is_valid_ip("0.0.0.0"))
debug("localhost is valid?", is_valid_ip("localhost"))

# while not have_ip or not is_valid_ip(host_address):
#     host_address = input("Enter Host IPv4 address: ")
#     have_ip = True

while True:
    if is_valid_ip(host_address):
        break
    elif have_ip:
        print("Not a valid IPv4 address.")
        print()
    host_address = input("Enter receiver's IPv4 address: ")
    have_ip = True


def capture_and_send_ss(client: socket.socket) -> None:
    ss = pgui.screenshot(SS_NAME)
    print(F"Captured and saved {SS_NAME}")
    client.send(b'start')
    with open(SS_NAME, 'rb') as file:
        data = file.read()
        client.sendall(data)
    print("Sent Successfully.")
    # client.send(b'end')


def listen_for_messages(client: socket.socket) -> None:
    stop_hotkey = "ctrl+q"
    kb.add_hotkey("ctrl+shift+print_screen", lambda: capture_and_send_ss(client))
    print(f"Press {stop_hotkey} to stop.")
    kb.wait(stop_hotkey)
    # client.send(b"")
    # client.send(b"end")
    client.close()


# ONE-TO-ONE CONNECTION
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host_address, PORT))
except OSError as ose:
    print(f"Connot connect to {host_address} on {PORT}")
    print(ose)
    raise SystemExit

listening_thread = threading.Thread(target=listen_for_messages, args=(client, ))
listening_thread.run()