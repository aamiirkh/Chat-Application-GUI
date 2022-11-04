from tkinter import *
import socket
import _thread

IP = '127.0.0.1'


def connection():
    global conn
    PORT = port_no.get()
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serv.bind((IP, int(PORT)))
        serv.listen()

        conn, addr = serv.accept()
    except Exception as e:
        print(e)


def send():
    global conn
    data = textbox.get("0.0", END)

    try:
        conn.send(data.encode('utf-8'))
        chat.config(state=NORMAL)
        chat.insert(END, 'SERVER>>' + data)
        chat.config(state=DISABLED)
    except Exception as e:
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
                chat.insert(END, 'CLIENT>>' + data)
                chat.config(state=DISABLED)
        except Exception as e:
            pass


def press(event):
    send()


def click():
    _thread.start_new_thread(connection, ())


def gui():
    global chat
    global textbox
    global port_no
    global submit

    # initialize tkinter object
    gui = Tk()
    # set title for the window
    gui.title("Server Chat")
    gui.geometry("380x430")
    # initialize chat box
    chat = Text(gui, bg='white')
    chat.config(state=DISABLED)
    # initialize send button
    button = Button(gui, bg='orange', fg='red', text='SEND', command=send)
    # initialize port_no textbox
    port_no = Entry(gui)

    text = Label(gui, text="PORT")
    # initialize submit button
    submit = Button(gui, bg='grey', fg='black', text='SUBMIT', command=click)
    # initialize text box
    textbox = Text(gui, bg='white')

    text.place(x=15, y=25)
    chat.place(x=6, y=80, height=310, width=370)
    textbox.place(x=6, y=401, height=20, width=265)
    button.place(x=300, y=401, height=20, width=50)
    submit.place(x=230, y=12, height=50, width=120)

    port_no.grid(row=0, column=10, pady=26, padx=55)

    textbox.bind("<KeyRelease-Return>", press)

    _thread.start_new_thread(receive, ())

    gui.mainloop()


if __name__ == "__main__":
    chat = textbox = port_no = None
    conn = submit = None
    gui()