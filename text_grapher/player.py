import os
import tkinter as tk
from tkinter.filedialog import askdirectory, asksaveasfilename

class TGPlayer(tk.Tk):
    def __init__(self, folder=None, play_on_open=False):
        super().__init__()
        self.title("TG Player")
        self.rowconfigure(0, minsize=800, weight=1)
        self.columnconfigure(1, minsize=800, weight=1)

        self.graphs = []
        self.paused = True
        self.frame = 0
        self.mode = 'light'

        self.add_widgets()

        # render method in scene can open the player in the dst
        if folder:
            self.open_sequence(folder)

        if play_on_open:
            self.play()

    def add_widgets(self):
        self.txt = tk.Text(self)
        self.toolbar = tk.Frame(self, relief=tk.RAISED, bd=2)
        self.btn_open = tk.Button(
            self.toolbar,
            text="Open",
            command=self.open_sequence
            )
        self.btn_play = tk.Button(
            self.toolbar,
            text='Play',
            command=self.play
            )
        self.btn_pause = tk.Button(
            self.toolbar,
            text='Pause',
            command=self.pause
            )
        self.btn_invert = tk.Button(
            self.toolbar,
            text='Invert',
            command=self.invert
            )

        self.btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.btn_play.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.btn_pause.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.btn_invert.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        self.toolbar .grid(row=0, column=0, sticky="ns")
        self.txt.grid(row=0, column=1, sticky="nsew")

    def open_sequence(self, folder=None):
        if not folder:
            folder = askdirectory()

        if not folder:
            return

        files = [
            f for f in os.listdir(folder)
            if os.path.splitext(f)[1].lower() == '.txt']

        files.sort()

        for file in files:
            filepath = os.path.join(folder, file)
            with open(filepath, 'r') as infile:
                self.graphs.append(infile.read())

        print(f'{len(self.graphs)} graphs found')
        self.txt.delete(1.0, tk.END)
        text = self.graphs[0]
        self.txt.insert(tk.END, text)
        self.title(f"TG Player - {filepath}")

    def play_next(self):
        if not self.paused:
            self.frame += 1
            if self.frame == len(self.graphs):
                self.frame = 0
            self.txt.delete(1.0, tk.END)
            self.txt.insert(tk.END, self.graphs[self.frame])

            # framerate
            self.after(33, self.play_next)

    def invert(self):
        if self.mode == 'light':
            self.mode = 'dark'
            self.txt.configure(
                {"background": "black",
                "foreground": "white"})
        else:
            self.mode = 'light'
            self.txt.configure(
                {"background": "white",
                "foreground": "black"})

    def play(self):
        self.paused = False
        self.play_next()

    def pause(self):
        self.paused = True

def open_graph_sequence(folder):
    tg_player = TGPlayer(folder, play_on_open=True)
    tg_player.mainloop()

if __name__ == '__main__':

    tg_player = TGPlayer()
    tg_player.mainloop()
