import json
import math
import tkinter as tk

# import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from color import Color

plt.rc("font", family="Malgun Gothic")

class GraphFrame(tk.Frame):
    colors = [Color.VISUALIZE1, Color.VISUALIZE2, Color.FOCUS, Color.GRAY, Color.BUTTON]

    def __init__(self, root, width, height, **kwargs):
        super().__init__(root, **kwargs)
        self.data = None
        self.canvas = None
        self.width = width
        self.height = height

    def draw_plot(self, data, title="Sample"):
        self.data = data

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(self.width / 100, self.height / 100), dpi=100)
        for key, y in self.data["y"].items():
            ax.plot(self.data["x"], y, label=key)
        ax.set_title(title)
        # ax.set_xlabel("X axis")
        # ax.set_ylabel("Y axis")
        ax.legend()

        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.get_tk_widget().pack()

    def draw_bar(self, data, title="Sample"):
        self.data = data

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        l = len(self.data["y"])
        bar_width = (0.8 / l)
        fig, ax = plt.subplots(figsize=(self.width / 100, self.height / 100), dpi=100)
        for i, (key, y) in enumerate(self.data["y"].items()):
            xs = [x + i * bar_width - bar_width / 2 * (l - 1) for x in range(len(self.data["x"]))]
            ax.bar(xs, y, width=bar_width, label=key, color=GraphFrame.colors[i % len(GraphFrame.colors)])

        ax.set_xticks(range(len(self.data["x"])))
        if len(self.data["x"]) > 5:
            # ax.set_xticklabels(["\n".join(x.split()) for x in self.data["x"]], rotation=45, ha="right")
            ax.set_xticklabels(self.data["x"], rotation=45, ha="right")
        else:
            ax.set_xticklabels(self.data["x"])


        fig.tight_layout()
        fig.subplots_adjust(top=0.9)
        ax.set_title(title)
        # ax.set_xlabel("X axis")
        # ax.set_ylabel("Y axis")
        ax.legend()

        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.get_tk_widget().pack()

    def draw_pie(self, data, title="Sample"):
        self.data = data

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(self.width / 100, self.height / 100), dpi=100)
        for y in self.data["y"].values():
            wedges, _ = ax.pie(y, labels=[f"{v * 100:.0f}%" for v in y], startangle=90, pctdistance=0.85, labeldistance=1.1, colors=GraphFrame.colors)

            ax.set_title(title)

            ax.legend(wedges, data["x"], loc="upper left", bbox_to_anchor=(-0.5, 1))

        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.get_tk_widget().pack()

class DashboardFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1300, height=700, bg=Color.GRAY)
        self.root = root

        self.fr_top_left = tk.Frame(self, width=650, height=350, bg=Color.VISUALIZE1)
        self.fr_top_right = tk.Frame(self, width=650, height=350, bg=Color.VISUALIZE2)
        self.fr_bot_left = tk.Frame(self, width=650, height=350, bg=Color.FOCUS)
        self.fr_bot_right = tk.Frame(self, width=650, height=350, bg=Color.GRAY)

        self.gr_top_left = GraphFrame(self.fr_top_left, 650, 350)
        self.gr_top_right = GraphFrame(self.fr_top_right, 650, 350)
        self.gr_bot_left = GraphFrame(self.fr_bot_left, 650, 350)
        self.gr_bot_right = GraphFrame(self.fr_bot_right, 650, 350)

        self.gr_top_left.place(x=0, y=0)
        self.gr_top_right.place(x=0, y=0)
        self.gr_bot_left.place(x=0, y=0)
        self.gr_bot_right.place(x=0, y=0)

        self.fr_top_left.grid(row=0, column=0)
        self.fr_top_right.grid(row=0, column=1)
        self.fr_bot_left.grid(row=1, column=0)
        self.fr_bot_right.grid(row=1, column=1)

    def after_init(self):
        data = {
            "code": 99999,
            "args": {}
        }
        self.root.send_(json.dumps(data, ensure_ascii=False))

    def recv(self, **kwargs):
        print("code:", kwargs.get("code"))
        print("sign:", kwargs.get("sign"))
        print("data:", kwargs.get("data"))
        code = kwargs.get("code")
        sign = kwargs.get("sign")
        data = kwargs.get("data")

        if code != 99999 or sign != 1:
            return

        data1 = data.get("data1")
        data2 = data.get("data2")
        data3 = data.get("data3")
        data4 = data.get("data4")

        if data1 is not None:
            self.gr_top_left.after(0, lambda a: self.gr_top_left.draw_bar(data1, title="Total Material Cost in Receiving"), None)
        if data2 is not None:
            self.gr_top_right.after(0, lambda a: self.gr_top_right.draw_bar(data2, title="Total Material Cost in Shipping"), None)
        if data3 is not None:
            self.gr_bot_left.after(0, lambda a: self.gr_bot_left.draw_pie(data3, title="Top 5 Overrun in Production Costs"), None)
        if data4 is not None:
            self.gr_bot_right.after(0, lambda a: self.gr_bot_right.draw_bar(data4, title="Top 5 Production Costs"), None)
        # self.gr_top_left.after(0, lambda a: self.gr_top_left.draw_plot(data1, title="Best 5"), None)
        # self.gr_top_left.draw(data1)

if __name__ == "__main__":
    r = tk.Tk()
    r.geometry("1600x900")
    r.config(bg="white")
    fr = DashboardFrame(r)
    fr.place(x=0, y=130)
    r.mainloop()

