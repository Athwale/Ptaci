#!/bin/python3

import tkinter as tk

if __name__ == '__main__':
    # todo typ: papousek, dravec, sova, vodni, morsky, pevec
    window = tk.Tk()
    radio_var = tk.IntVar(window, 0)
    check_var = tk.IntVar(window, 2)
    radio_var_1 = tk.IntVar(window, 1)

    label = tk.Label(text="Database filler")
    label.pack()

    R1 = tk.Radiobutton(window, text="Option 1", value=1, variable=radio_var)
    R1.pack()
    R2 = tk.Radiobutton(window, text="Option 2", value=2, variable=radio_var)
    R2.pack()
    R3 = tk.Radiobutton(window, text="Option 3", value=3, variable=radio_var)
    R3.pack()

    R4 = tk.Radiobutton(window, text="Option 4", value=4, variable=radio_var_1)
    R4.pack()
    R5 = tk.Radiobutton(window, text="Option 5", value=5, variable=radio_var_1)
    R5.pack()

    c1 = tk.Checkbutton(window, text='Python', variable=check_var, onvalue=1, offvalue=0)
    c1.pack()

    button = tk.Button(text="Save", bg="green")
    button.pack()

    label = tk.Label(text="New color")
    entry = tk.Entry(width=50)
    label.pack()
    entry.pack()

    # TODO fill colors and attributes for each gender.
    # TODO add picture from wiki url, automatic rename.
    # TODO open wiki page in firefox.
    # TODO add new color option.
    # TODO add dodatek.
    # TODO automatic image resize and make file smaller

    window.mainloop()
