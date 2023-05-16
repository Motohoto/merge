# Merge és Compare funkciók Motohoto
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

import matplotlib.pyplot as plt
import numpy as np


# file megnyitás dialóg
def open_file_dialog(file_path_var):
    file_path = filedialog.askopenfilename()
    file_path_var.set(file_path)
# összehasonlítás
def compare_files(original_file, patch_file, tuned_file):
    with open(original_file, 'rb') as f:
        original_data = np.fromfile(f, dtype=np.uint8)
    with open(patch_file, 'rb') as f:
        patch_data = np.fromfile(f, dtype=np.uint8)
    with open(tuned_file, 'rb') as f:
        tuned_data = np.fromfile(f, dtype=np.uint8)

    diff1 = np.nonzero(original_data - patch_data)[0]
    diff2 = np.nonzero(original_data - tuned_data)[0]

    plt.plot(diff1, np.zeros_like(diff1), 'ro', label='Original vs Patch')
    plt.plot(diff2, np.zeros_like(diff2), 'bo', label='Original vs Tuned')
    plt.legend()
    plt.show()

def save_result(original_file, patch_file, tuned_file):
    with open(original_file, 'rb') as f:
        original_data = np.fromfile(f, dtype=np.uint8)
    with open(patch_file, 'rb') as f:
        patch_data = np.fromfile(f, dtype=np.uint8)
    with open(tuned_file, 'rb') as f:
        tuned_data = np.fromfile(f, dtype=np.uint8)

    result_data = np.copy(original_data)
# na ez a rész trükkös
    diff1 = np.nonzero(original_data - patch_data)[0]
    diff2 = np.nonzero(original_data - tuned_data)[0]
# hiba
    common_diff = np.intersect1d(diff1, diff2)
    if len(common_diff) > 0:
        print("Error: Both patch and tuned files have differences at the same positions:", common_diff)
        return

    result_data[diff1] = patch_data[diff1]
    result_data[diff2] = tuned_data[diff2]
#ez még nem kiforrott
    patch_filename = Path(patch_file).name
    tuned_filename = Path(tuned_file).name
    default_filename = patch_filename + '_' + ''.join(c for c in tuned_filename if c not in patch_filename) + '.md2'

    save_path = filedialog.asksaveasfilename(defaultextension=".md2", initialfile=default_filename)
    if save_path:
        with open(save_path, 'wb') as f:
            result_data.tofile(f)
#főablak -nincs is más
root = tk.Tk()
root.title("File-ok összehasonlitása és egyesitése")
root.geometry("400x100")

original_file_path = tk.StringVar()
patch_file_path = tk.StringVar()
tuned_file_path = tk.StringVar()

original_button = tk.Button(root, text="Original", command=lambda:open_file_dialog(original_file_path))
original_button.pack(side=tk.LEFT, padx=10, pady=10)

patch_button = tk.Button(root, text="Patch", command=lambda:open_file_dialog(patch_file_path))
patch_button.pack(side=tk.LEFT, padx=10, pady=10)

tuned_button = tk.Button(root, text="Tuned", command=lambda:open_file_dialog(tuned_file_path))
tuned_button.pack(side=tk.LEFT, padx=10, pady=10)

compare_button = tk.Button(root, text="Compare", command=lambda:compare_files(original_file_path.get(),
                                                                              patch_file_path.get(), tuned_file_path.get()))
compare_button.pack(side=tk.LEFT, padx=10, pady=10)

save_button = tk.Button(root, text="Save", command=lambda:save_result(original_file_path.get(),
                                                                      patch_file_path.get(), tuned_file_path.get()))
save_button.pack(side=tk.LEFT, padx=10, pady=10)

root.mainloop()