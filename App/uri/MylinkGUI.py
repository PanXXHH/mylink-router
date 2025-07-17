import tkinter as tk
from tkinter import ttk


class MylinkGUI:
    def __init__(self, command_queue):
        self.root = tk.Tk()
        self.root.title("搜索中...")
        self.progressbar = ttk.Progressbar(self.root, mode='indeterminate')
        self.progressbar.pack()
        self.progressbar.start(50)
        self.command_queue = command_queue

    def set_on_close_callback(self, callback):
        self.root.protocol("WM_DELETE_WINDOW", callback)