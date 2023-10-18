#!/bin/python3

import tkinter as tk
from typing import Dict

import yaml
import os
from tkinter import ttk
from pathlib import Path


def create_gui(values: Dict):
    # TODO open wiki page in firefox.
    # TODO picture from wiki url, automatic rename based on species, gender+number.

    # TODO optimize all photos once done and cropped.

    # TODO choices papousek, dravec, sova, vodni, pevec

    root.geometry()
    gender_frames = []

    main_frame = ttk.LabelFrame(root, text=str(Path.cwd().name.replace('_', ' ').capitalize()))
    for gender in ['samec', 'samice']:
        g_frame = ttk.LabelFrame(main_frame, text=gender)
        for key in values.keys():
            if str(key) in ['hlava', 'křídla', 'hruď', 'ocas', 'nohy', 'záda', 'zobák']:
                frame = ttk.LabelFrame(g_frame, text=str(key))
                for color in values[key]:
                    check_var = tk.IntVar(g_frame, 0)
                    elements[f'color_ch_{key}_{color}_{gender}'] = tk.Checkbutton(frame, text=color, variable=check_var,
                                                                                  onvalue=1, offvalue=0,
                                                                                  name=f'color_ch_{key}_'
                                                                                       f'{color}_{gender}')
                    elements[f'color_ch_{key}_{color}_{gender}'].pack(expand=True)
                elements[f'color_text_{key}_{gender}'] = tk.Entry(frame, width=10, name=f'color_text_{key}_{gender}')
                elements[f'color_text_{key}_{gender}'].pack()
                frame.pack(side=tk.LEFT, fill='both')
        o_frame = ttk.LabelFrame(g_frame, text='Vlastnosti')
        img_frame = ttk.LabelFrame(o_frame, text='Přidat obrázek z URL')
        elements[f'img1_text_{gender}'] = tk.Entry(img_frame, width=20, name=f'img1_text_{gender}')
        elements[f'img1_text_{gender}'].pack(side=tk.BOTTOM)
        elements[f'img2_text_{gender}'] = tk.Entry(img_frame, width=20, name=f'img2_text_{gender}')
        elements[f'img2_text_{gender}'].pack(side=tk.BOTTOM)
        img_frame.pack()
        p_frame = ttk.LabelFrame(o_frame, text='Dodatek')
        elements[f'note_text_{gender}'] = tk.Entry(p_frame, width=20, name=f'note_text_{gender}')
        elements[f'note_text_{gender}'].pack(side=tk.BOTTOM)
        p_frame.pack()

        check_var = tk.IntVar(g_frame, 0)
        elements[f'spotted_{gender}'] = tk.Checkbutton(o_frame, text='Kropenatost', variable=check_var, onvalue=1,
                                                       offvalue=0, name=f'spotted_{gender}')
        elements[f'spotted_{gender}'].pack()
        o_frame.pack(fill='both', expand=True)
        gender_frames.append(g_frame)

    check_var = tk.IntVar(g_frame, 0)
    elements[f'add_female'] = tk.Checkbutton(main_frame, text='Přidat samičku', variable=check_var, onvalue=1,
                                             offvalue=0, name=f'add_female')
    gender_frames[0].pack()
    elements[f'add_female'].pack()
    gender_frames[1].pack()

    t_frame = ttk.LabelFrame(main_frame, text='Typ')
    radio_var = tk.StringVar()
    for typ in values['typ']:
        elements[f'radio_typ_{typ}'] = tk.Radiobutton(t_frame, text=typ, value=typ, variable=radio_var,
                                                      name=f'radio_typ_{typ}')
        elements[f'radio_typ_{typ}'].pack(expand=True)
    elements[f'typ_text'] = tk.Entry(t_frame, width=10, name=f'typ_text')
    elements[f'typ_text'].pack()

    v_frame = ttk.LabelFrame(main_frame, text='Velikost')
    radio_var = tk.StringVar()
    for size in values['velikost']:
        elements[f'radio_size_{size}'] = tk.Radiobutton(v_frame, text=size, value=size, variable=radio_var,
                                                        name=f'radio_size_{size}')
        elements[f'radio_size_{size}'].pack(expand=True)
    elements[f'size_text'] = tk.Entry(v_frame, width=10, name=f'size_text')
    elements[f'size_text'].pack()

    t_frame.pack(side=tk.LEFT)
    v_frame.pack(side=tk.LEFT)
    button = tk.Button(main_frame, text="Save", bg="green", command=save_action)
    button.pack(side=tk.LEFT)
    button = tk.Button(main_frame, text="Rescan", bg="yellow")
    button.pack(side=tk.LEFT)
    button = tk.Button(main_frame, text="Quit", bg="red")
    button.pack(side=tk.LEFT)
    main_frame.pack()


def save_action():
    for name, element in elements.items():
        print(name, element)
    root.destroy()


def find_head_color(gender: str) -> str:
    pass


def analyze_yaml(collected_keywords: Dict) -> Dict:
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
        elements = {}

        for u_path in Path(unfinished_working_directory).iterdir():
            if u_path.is_dir():
                try:
                    root = tk.Tk()
                    previous_values = scan_options(finished_working_directory)
                    create_gui(previous_values)
                    os.chdir(u_path.resolve())
                    print(f'Working on: {u_path}')
                    root.mainloop()
                except Exception as e:
                    print(f'Error: {u_path.resolve()}, {e}')
                finally:
                    os.chdir(unfinished_working_directory)
    except KeyboardInterrupt as _:
        print('Stopped')
