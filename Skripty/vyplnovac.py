#!/bin/python3

import tkinter as tk
from typing import Dict

import yaml
import os
from tkinter import ttk
from pathlib import Path


def create_gui():
    """

    :return:
    """
# todo typ: papousek, dravec, sova, vodni, morsky, pevec
    root = tk.Tk()
    root.geometry('300x200')
    # Frames:
    head_color = ttk.LabelFrame(root, text='Hlava')

    radio_var = tk.IntVar(root, 0)
    check_var = tk.IntVar(root, 2)
    radio_var_1 = tk.IntVar(root, 1)

    label = tk.Label(text="Database filler")

    R1 = tk.Radiobutton(head_color, text="Option 1", value=1, variable=radio_var)
    R1.pack()
    R2 = tk.Radiobutton(head_color, text="Option 2", value=2, variable=radio_var)
    R2.pack()
    R3 = tk.Radiobutton(head_color, text="Option 3", value=3, variable=radio_var)
    R3.pack()

    R4 = tk.Radiobutton(root, text="Option 4", value=4, variable=radio_var_1)
    R5 = tk.Radiobutton(root, text="Option 5", value=5, variable=radio_var_1)

    c1 = tk.Checkbutton(root, text='Python', variable=check_var, onvalue=1, offvalue=0)

    button = tk.Button(text="Save", bg="green")

    label1 = tk.Label(text="New color")
    entry = tk.Entry(width=50)

    # TODO fill colors and attributes for each gender.
    # TODO add picture from wiki url, automatic rename.
    # TODO open wiki page in firefox.
    # TODO add new color option.
    # TODO add dodatek.
    # TODO automatic image resize and make file smaller

    head_color.pack()
    root.mainloop()


def analyze_yaml() -> Dict:
    """
    Get typ, velikost, barvy from both samec and samice.
    :return: Dictionary.
    """
    color_dictionary = {'hlava': set(),
                        'křídla': set(),
                        'hruď': set(),
                        'ocas': set(),
                        'nohy': set(),
                        'záda': set(),
                        'zobák': set(),
                        'typ': set(),
                        'velikost': set()}
    with open('data.yml', 'r') as file:
        metadata = yaml.safe_load(file)
        color_dictionary['typ'].add(metadata['typ'])
        color_dictionary['velikost'].add(metadata['velikost'])
        available_genders = ['samec']
        if metadata['popis']['samice']:
            available_genders.append('samice')
        for gender in available_genders:
            parts = metadata['popis'][gender]['barvy']
            for body_part in parts:
                key = list(body_part.keys())[0]
                color_set = color_dictionary[key]
                colors = set(body_part[list(body_part.keys())[0]])
                new_colors = color_set.union(colors)
                color_dictionary[key] = new_colors
    return color_dictionary


def scan_options():
    """
    Scan finished files to create options for the gui.
    :return:
    """
    working_directory = Path(Path.cwd() / Path('../databaze/finished'))
    os.chdir(working_directory)
    for path in Path(Path.cwd()).iterdir():
        if path.is_dir():
            try:
                os.chdir(path)
                analyze_yaml()
            except Exception as e:
                print(f'Error: {path}, {e}')
            finally:
                os.chdir(working_directory)


if __name__ == '__main__':
    scan_options()
    #create_gui()
