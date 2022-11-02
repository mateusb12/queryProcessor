import tkinter as tk
from tkinter import messagebox

import networkx as nx
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from queries.relational_algebra_splitter import get_sql_instruction_example_A, get_sql_instruction_example_B, \
    get_sql_instruction_example_C, get_sql_instruction_example_D
from queryTree.network_tree import NetworkNxTree
from queryTree.tree import build_example_tree
from networkx.drawing.nx_pydot import graphviz_layout

from queryTree.utils import break_down_sql_line
from sql_parser.sql_query_parser import QueryParser


class QueryGUI:
    """This class creates a window with a text entry box and a button.
     The user can enter a query in the text entry box and click the button to execute the query."""

    def __init__(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=300, height=500, relief='raised')
        self.anchor_point_x = 20
        self.anchor_point_y = 90
        self.query_entry = tk.Entry()
        self.execute_button = tk.Button()
        self.entry_label = tk.Label()
        self.answer_label = tk.Label()
        self.relational_label = tk.Label()
        self.drop_down_options = self.__get_drop_down_options_dict()
        self.drop_down = None
        self.drop_down_menu = None
        self.main_pipeline()

    def main_pipeline(self):
        self.set_config_pipeline()
        self.__mouse_position_capturing()
        self.window.mainloop()

    @staticmethod
    def __get_drop_down_options_dict() -> dict:
        return {"A": get_sql_instruction_example_A(), "B": get_sql_instruction_example_B(),
                "C": get_sql_instruction_example_C(), "D": get_sql_instruction_example_D(),
                "none": "aaaaa"}

    def set_config_pipeline(self):
        self.set_window_config()
        self.set_drop_down_config(self.anchor_point_x + 160, self.anchor_point_y - 70)
        self.set_entry_config(x=self.anchor_point_x, y=self.anchor_point_y)
        self.set_entry_label_config(x=self.anchor_point_x + 140, y=self.anchor_point_y - 25)
        self.set_button_config(x=self.anchor_point_x + 170, y=self.anchor_point_y + 30)
        self.set_answer_label_config(x=self.anchor_point_x + 180, y=self.anchor_point_y + 80)
        self.set_relational_label_config(x=self.anchor_point_x + 600, y=self.anchor_point_y + 120)

    def set_window_config(self):
        self.window.title("Query GUI")
        self.window.geometry("1100x700")
        self.window.resizable(False, False)
        self.window.configure(bg="white")

    def set_relational_label_config(self, x: int, y: int):
        self.relational_label = tk.Label(self.window, text="RELATIONAL ALGEBRA", bg="white")
        self.relational_label.place(x=x, y=y)

    def set_entry_config(self, x: int, y: int):
        self.query_entry = tk.Entry(self.window, width=50, font=("Arial", 12))
        self.query_entry.place(x=x, y=y)

    def set_drop_down_config(self, x: int, y: int):
        self.drop_down_menu = tk.StringVar(self.window)
        self.drop_down_menu.set("Select a SQL example")
        options = list(self.drop_down_options.keys())
        self.drop_down = tk.OptionMenu(self.window, self.drop_down_menu, options[0], *options[1:],
                                       command=self.event_drop_down_function)
        self.drop_down.pack()
        self.drop_down.place(x=x, y=y)

    def set_button_config(self, x: int, y: int):
        self.execute_button = tk.Button(self.window, text="Execute", font=("Arial", 12),
                                        command=self.event_execute_query, bg='brown', fg='white')
        self.execute_button.place(x=x, y=y)

    def set_entry_label_config(self, x: int, y: int):
        self.entry_label = tk.Label(self.window, text="Enter your SQL instruction", bg="white")
        self.entry_label.place(x=x, y=y)

    def set_answer_label_config(self, x: int, y: int):
        self.answer_label = tk.Label(self.window, text="ANSWER", bg="white", justify="center")
        self.answer_label.place(x=x, y=y)

    def event_execute_query(self):
        entry_text = self.query_entry.get()
        try:
            parser = QueryParser(entry_text)
        except ValueError:
            messagebox.showerror("Error", "Invalid SQL instruction")
            return
        new_line_text = break_down_sql_line(entry_text)
        text_size = len(entry_text)
        self.answer_label.config(text=new_line_text)
        left_margin = 0.35 * text_size
        # answer_label_positions = self.answer_label.place_info()
        # new_x = int(answer_label_positions['x']) - left_margin
        # new_y = answer_label_positions['y']
        self.answer_label.place(x=600-left_margin, y=10)
        legend_text = self.plot_tree_graph_on_canvas()
        self.relational_label.config(text=legend_text)

    def event_mouse_motion(self, event):
        x, y = event.x, event.y
        self.window.title(f'{x}, {y}')

    def event_drop_down_function(self, event):
        self.query_entry.delete(0, tk.END)
        drop_down_choice = self.drop_down_menu.get()
        choice_sql = self.drop_down_options[drop_down_choice]
        self.query_entry.insert(0, choice_sql)

    def __mouse_position_capturing(self):
        self.window.bind('<Motion>', self.event_mouse_motion)

    # def __plot_placeholder_chart_on_canvas(self):
    #     fig, ax = plt.subplots()
    #     fig.set_size_inches(5, 4)
    #     fig.set_dpi(100)
    #
    #     plt.grid(visible=True, which='major', color='#666666', linestyle='-', zorder=0, linewidth=0.35)
    #     plt.ylabel("Collision amount")
    #     plt.xlabel("Bucket Index")
    #     colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
    #     df_bar_example = pd.DataFrame({"Bucket Index": [1, 2, 3, 4, 5, 6, 7],
    #                                    "Collision amount": [1, 2, 3, 4, 5, 6, 7],
    #                                    "Color": colors})
    #     df_bar_example.plot.bar(x="Bucket Index", y="Collision amount", color=df_bar_example["Color"],
    #     ax=ax, zorder=3)
    #     self.canvas = FigureCanvasTkAgg(fig, master=self.window)
    #     self.canvas.draw()
    #     self.canvas.get_tk_widget().place(x=5, y=200)

    def plot_tree_graph_on_canvas(self) -> str:
        fig, ax = plt.subplots()
        drop_down_choice = self.drop_down_menu.get()
        if drop_down_choice == "none":
            example_sql = self.query_entry.get()
        else:
            example_sql = self.drop_down_options[drop_down_choice]
        try:
            example_tree = build_example_tree(example_sql)
        except IndexError:
            messagebox.showerror("Error", "Problem when building the tree")
            return ""
        nxt = NetworkNxTree(example_tree)
        nxt.draw_graph(ax)
        self.canvas = FigureCanvasTkAgg(fig, master=self.window)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=-40, y=200)
        return nxt.get_legend_text()


def __main():
    query_gui = QueryGUI()


if __name__ == "__main__":
    __main()
