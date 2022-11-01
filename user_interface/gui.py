import tkinter as tk


class QueryGUI:
    """This class creates a window with a text entry box and a button.
     The user can enter a query in the text entry box and click the button to execute the query."""

    def __init__(self):
        self.window = tk.Tk()
        self.query_entry = tk.Entry()
        self.execute_button = tk.Button()
        self.set_window_config()
        self.set_entry_config()
        self.set_button_config()

        self.window.mainloop()

    def set_window_config(self):
        self.window.title("Query GUI")
        self.window.geometry("500x500")
        self.window.resizable(False, False)
        self.window.configure(bg="white")

    def set_entry_config(self):
        self.query_entry = tk.Entry(self.window, width=50, font=("Arial", 12))
        self.query_entry.place(x=20, y=20)

    def set_button_config(self):
        self.execute_button = tk.Button(self.window, text="Execute", font=("Arial", 12), command=self.execute_query)
        self.execute_button.place(x=20, y=50)

    def execute_query(self):
        print("oi")


def __main():
    query_gui = QueryGUI()


if __name__ == "__main__":
    __main()
