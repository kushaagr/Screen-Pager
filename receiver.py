import socket
import threading
import os
import keyboard as kb
import datetime as dt

import debug_utils
from debug_utils import debug

debug_utils.dev_mode = True

HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)
PORT = 80
CONNECTIONS_LIMIT = 1 # ONE-TO-ONE CONNECTION


def create_dir(directory: str) -> str:
    """ A utility function to create a directory
    :type directory: str
    :rtype: str
    """
    parentPath = '.'
    path = os.path.join(parentPath, directory)
    # path = directory
    try:
        os.mkdir(path)
    except FileNotFoundError:
        print(FileNotFoundError)
    finally:
        return path


def client_handler(client: socket.socket) -> None:
    images_path = create_dir('Images')
    file = None
    print("Press Ctrl+PauseBr to stop.")
    while True:
        data = client.recv(4096)
        if not data:
            debug("`no data` => client.close() called")
            break
        if data == b'start':
            newfile = str(
                dt.datetime.today()
            ).replace(':','').replace('.', '') + '.png'
            filepath = os.path.join(images_path, newfile)
            file = open(filepath, 'ab')
            debug("START TRANSFER")
        # elif data == b'end':
        #     debug("Received file end signal.")
        #     debug("END TRANSFER")
        #     if file and not file.closed: 
        #         # file.close()
        #         print(f"{newfile} saved at {images_path}")
        else:
            file.write(data)
            # debug("IN PROCESS", end="--")
            debug("[{0}]".format(data[-6:]), end="--")


print("Starting server...")
debug("dev_mode ON: DEBUG messages will be printed!")
while True:
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOSTNAME, PORT))
        server.listen(CONNECTIONS_LIMIT)
        print()
        print(f"Server listening on {HOST} : {PORT} (Press Ctrl+Pause to stop.)")
        client, c_addr = server.accept()
        print(f"Connected to client on {c_addr}")
        # print("Available methods on client: ", dir(client))

    except OSError as ose:
        print(f"Unable to host server {HOST}:{PORT}")
        print(ose)
        raise SystemExit

    handler_thread = threading.Thread(target=client_handler, args=(client,))
    handler_thread.run()