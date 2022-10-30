import tkinter as tk


class QueryGUI:
    """This class creates a window with a text entry box and a button.
     The user can enter a query in the text entry box and click the button to execute the query."""

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Query GUI")
        self.window.geometry("500x500")
        self.window.resizable(False, False)
        self.window.configure(bg="white")
        self.query_entry = tk.Entry(self.window, width=50, font=("Arial", 12))
        self.query_entry.place(x=20, y=20)
        self.execute_button = tk.Button(self.window, text="Execute", font=("Arial", 12), command=self.execute_query)
        self.execute_button.place(x=20, y=50)
        self.window.mainloop()

    def execute_query(self):
        print("oi")


def __main():
    query_gui = QueryGUI()


if __name__ == "__main__":
    __main()
