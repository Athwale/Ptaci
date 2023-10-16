#!/bin/python3

import tkinter as tk
from typing import Dict

import yaml
import os
from tkinter import ttk
from pathlib import Path


def run_filler(values: Dict):
    """

    :return:
    """
    # TODO fill colors and attributes for each gender.
    # TODO add picture from wiki url, automatic rename.
    # TODO open wiki page in firefox.
    # TODO add new color option.
    # TODO add dodatek.
    # TODO automatic image resize and make file smaller
    # TODO save must close the window to let a new instance run.
    # todo typ: papousek, dravec, sova, vodni, morsky, pevec

    print(values)
    root = tk.Tk()
    root.geometry('800x400')
    elements = {}

    # TODO finish and save+rescan buttons
    # TODO make female as copy of a male, add "add female button"
    # TODO side by side arrangement
    for key in values.keys():
        if str(key) in ['hlava', 'křídla', 'hruď', 'ocas', 'nohy', 'záda', 'zobák']:
            frame = ttk.LabelFrame(root, text=str(key))
            radio_var = tk.StringVar()
            for color in values[key]:
                elements[f'{color}_radio_{key}'] = tk.Radiobutton(frame, text=color, value=color, variable=radio_var,
                                                                  name=f'{color}_radio_{key}')
                elements[f'{color}_radio_{key}'].pack()
            new_color = tk.Label(frame, text="New color")
            new_color.pack()
            elements[f'color_text_{key}'] = tk.Entry(frame, width=10, name=f'color_text_{key}')
            elements[f'color_text_{key}'].pack()
            frame.pack(side=tk.LEFT)

    check_var = tk.IntVar(root, 1)
    elements['spotted'] = tk.Checkbutton(root, text='Kropenatost', variable=check_var, onvalue=1, offvalue=0,
                                         name='spotted')
    elements['spotted'].pack()
    button = tk.Button(text="Save", bg="green")
    root.mainloop()


def analyze_yaml(collected_keywords: Dict) -> Dict:
    """
    Get typ, velikost, barvy from both samec and samice.
    :param collected_keywords: Previously used colors and values.
    :return: Dictionary with newly added values.
    """
    with open('data.yml', 'r') as file:
        metadata = yaml.safe_load(file)
        collected_keywords['typ'].add(metadata['typ'])
        collected_keywords['velikost'].add(metadata['velikost'])
        available_genders = ['samec']
        if metadata['popis']['samice']:
            available_genders.append('samice')
        for gender in available_genders:
            parts = metadata['popis'][gender]['barvy']
            for body_part in parts:
                key = list(body_part.keys())[0]
                color_set = collected_keywords[key]
                colors = set(body_part[list(body_part.keys())[0]])
                new_colors = color_set.union(colors)
                collected_keywords[key] = new_colors
    return collected_keywords


def scan_options(work_dir: Path) -> Dict:
    """
    Scan finished files to create options for the gui.
    :return: A dictionary of all previously used values.
    """
    used_values = {'hlava': set(),
                   'křídla': set(),
                   'hruď': set(),
                   'ocas': set(),
                   'nohy': set(),
                   'záda': set(),
                   'zobák': set(),
                   'typ': set(),
                   'velikost': set()}
    os.chdir(work_dir)
    for path in Path(Path.cwd()).iterdir():
        if path.is_dir():
            try:
                os.chdir(path)
                used_values = analyze_yaml(used_values)
            except Exception as ex:
                print(f'Error: {path}, {ex}')
            finally:
                os.chdir(work_dir)
    return used_values


if __name__ == '__main__':
    try:
        unfinished_working_directory = Path(Path.cwd() / Path('../databaze/unfinished')).resolve()
        finished_working_directory = Path(Path.cwd() / Path('../databaze/finished')).resolve()

        for u_path in Path(unfinished_working_directory).iterdir():
            if u_path.is_dir():
                try:
                    previous_values = scan_options(finished_working_directory)
                    os.chdir(u_path.resolve())
                    print(f'Working on: {u_path}')
                    run_filler(previous_values)
                except Exception as e:
                    print(f'Error: {u_path.resolve()}, {e}')
                finally:
                    os.chdir(unfinished_working_directory)
    except KeyboardInterrupt as _:
        print('Stopped')
