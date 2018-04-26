# coding=<UTF-8>
"""First example with Tkinter"""

from tkinter import *

# Create a new window
window = Tk()

# Create a label. First argument is the interface window
label = Label(window, text="Hello, world")
# Put the label on the window
label.pack()

loremIpsum = StringVar()
textLine = Entry(window, textvariable=loremIpsum, width=30)
textLine.pack()


quitButton = Button(window, text="Quitter", command=window.quit)
quitButton.pack()

window.mainloop()
