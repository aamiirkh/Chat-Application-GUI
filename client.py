from tkinter import *
import socket
import _thread


def connection():
    global conn
    global connect
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP = ip_text.get()
    PORT = port_text.get()
    try:
        conn.connect((IP, int(PORT)))
        chat.config(state=NORMAL)
        chat.insert(END, 'Remote connection established\n')
        chat.config(state=DISABLED)

        connect.config(text="CONNECTED")
        connect.config(state=DISABLED)
    except Exception as e:
        chat.config(state=NORMAL)
        chat.insert(END, 'Remote connection disabled\n')
        chat.config(state=DISABLED)


def send():
    global conn
    data = textbox.get("0.0", END)

    try:
        conn.send(data.encode('utf-8'))
        chat.config(state=NORMAL)
        chat.insert(END, 'CLIENT>>' + data)
        chat.config(state=DISABLED)
    except:
        chat.config(state=NORMAL)
        chat.insert(END, 'Remote connection disabled\n')
        chat.config(state=DISABLED)

    textbox.delete("0.0", END)


def receive():
    global conn
    while True:
        try:
            data = conn.recv(4096).decode('utf-8')
            if data != '':
                chat.config(state=NORMAL)
                chat.insert(END, 'SERVER>>' + data)
                chat.config(state=HIDDEN)
        except Exception as e:
            pass


def press(event):
    send()


def click():
    _thread.start_new_thread(connection, ())


def gui():
    global chat
    global textbox
    global port_text
    global ip_text
    global connect

    # initialize tkinter object
    gui = Tk()
    # set title for the window
    gui.title("Client Chat")
    gui.geometry("380x430")

    chat = Text(gui, bg='white')
    chat.config(state=DISABLED)

    # set ip textbox
    ip_text = Entry(gui)
    ip_text.grid(row=0, column=10, pady=13, padx=50)
    # set port textbox
    port_text = Entry(gui)
    port_text.grid(row=1, column=10, pady=0, padx=50)

    connect = Button(gui, bg='grey', fg='black', text='CONNECT', command=click)
    button = Button(gui, bg='orange', fg='red', text='SEND', command=send)
    textbox = Text(gui, bg='white')

    chat.place(x=6, y=80, height=310, width=370)
    textbox.place(x=6, y=400, height=20, width=265)
    button.place(x=300, y=401, height=20, width=50)
    connect.place(x=230, y=12, height=50, width=120)

    # set IP label
    text = Label(gui, text="IP")
    text.place(x=8, y=10)
    # set PORT label
    text = Label(gui, text="PORT")
    text.place(x=5, y=40)

    textbox.bind("<KeyRelease-Return>", press)

    _thread.start_new_thread(receive, ())

    gui.mainloop()


if __name__ == "__main__":
    chat = textbox = ip_text = port_text = None
    conn = connect = None
    gui()
