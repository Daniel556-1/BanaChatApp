import tkinter as tk

# App setup
root = tk.Tk()
root.geometry("1000x600")
root.resizable(False, False)
root.title("Banana Chat App Client")

# variables
room = ""


# Wipe helper function
def wipe():
    for i in root.winfo_children():
        i.destroy()

# Main Menu Function
def mainMenu():
    wipe()

    background = tk.Frame(root, bg = "lightblue")
    background.pack(expand = True, fill = "both")

    frame = tk.Frame(background)
    frame.place(relx = 0.5, rely = 0.5, anchor = "center")

    title = tk.Label(frame, text = "Banana Chat App", font = ("Sans Serif", 30, "bold"))
    title.pack(pady = 20, padx = 20)

    prompt = tk.Label(frame, text = "Please enter a room name:", font = ("Sans Serif", 16))
    prompt.pack(pady = 10, padx = 20)

    roomname = tk.Entry(frame, font = ("Sans Serif", 16))
    roomname.pack(pady = 10, padx = 20)

    # Joining room logic here

    button = tk.Button(frame, text = "Enter", font = ("Sans Serif", 16))
    button.pack(pady = 20, padx = 20)

def connectingPage():
    wipe()

    background = tk.Frame(root, bg = "lightblue")
    background.pack(expand = True, fill = "both")

    frame = tk.Frame(background)
    frame.place(relx = 0.5, rely = 0.5, anchor = "center")

    title = tk.Label(frame, text = "Connecting...", font = ("Sans Serif", 30))
    title.pack(pady = 20, padx = 20)

    # Connection logic here

# Chat Page Function
def chatPage():
    wipe()

    background = tk.Frame(root, bg = "lightblue")
    background.pack(expand = True, fill = "both")

    frame = tk.Frame(background)
    frame.place(relx = 0.5, rely = 0.5, anchor = "center")

    title = tk.Label(frame, text = "Connected to room: ", font = ("Sans Serif", 30))
    title.pack(pady = 20, padx = 20)

# Start
chatPage()
root.mainloop()