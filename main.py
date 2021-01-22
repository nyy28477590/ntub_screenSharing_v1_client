from time import sleep
from zlib import decompress
from threading import Thread
from tkinter import Tk, BOTH, YES, Label
from socket import socket, AF_INET, SOCK_DGRAM
from PIL.Image import frombytes
from PIL.ImageTk import PhotoImage


root = Tk()
root.title('北商商務系廣播系統|學生端')
root.geometry('1062x600+0+0')
root.iconbitmap('./seanleetech.ico')
root.attributes('-topmost', True)


lbImage = Label(root)
lbImage.pack(fill=BOTH, expand=YES)

BUFFER_SIZE = 60*1024
data = []

def disable_event():
    pass

def show_image(image_bytes, image_size):
    screen_width = root.winfo_width()
    screen_height = root.winfo_height()

    global im
    try:
        im = frombytes('RGB', image_size, image_bytes)
    except:
        return

    im = im.resize((screen_width, screen_height))
    im = PhotoImage(im)
    lbImage['image'] = im
    lbImage.image = im

def recv_image():
    global receiving, im

    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(('', 22222))

    while receiving:
        while receiving:
            chunk, _ = sock.recvfrom(BUFFER_SIZE)

            if chunk == b'start':
                break
            elif chunk == b'close':
                sleep(0.0001)
        else:
            break

        while receiving:
            chunk, _ = sock.recvfrom(BUFFER_SIZE)
            if chunk.startswith(b'_over'):
                image_size = eval(chunk[5:])
                try:
                    image_data = decompress(b''.join(data))
                except:
                    break

                data.clear()

                global thread_show
                thread_show = Thread(target=show_image, args=(image_data, image_size))
                thread_show.daemon = True
                thread_show.start()
                data.clear()
                break
            elif chunk == b'close':
                sleep(0.0001)
            data.append(chunk)

def updListen():
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(('', 10000))
    while True:
        data, addr = sock.recvfrom(100)
        if data == b'small':
            root.state('withdrawn')
        elif data == b'big':
            root.deiconify()

root.state('withdrawn')

receiving = True
thread_sender = Thread(target=recv_image)
thread_sender.daemon = True
thread_sender.start()

thread_listener = Thread(target=updListen)
thread_listener.start()

def close_window():
    global receiving
    receiving = False
    sleep(0.0001)
    root.destroy()

root.protocol('WM_DELETE_WINDOW', disable_event)

root.mainloop()