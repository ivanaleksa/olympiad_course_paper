import tkinter as tk
from tkinter import ttk
from sql_connection import SqlConnection

class OlympiadApp:
    def __init__(self, master):
        self.conn = SqlConnection()
        self.master = master
        self.current_table = None

        # adjust the main window
        master.title("Olympiad App")
        master.geometry("1280x720")
        master.minsize(1280, 720)
        master.maxsize(1280, 720)

        # Create a side menu
        self.side_menu = tk.Frame(master, width=150, bg="lightgray")
        self.side_menu.pack(side=tk.LEFT, fill=tk.Y)

        # Create buttons for the side menu
        self.participant_button = tk.Button(self.side_menu, text="Participants", command=self.participant_option)
        self.participant_button.pack(pady=30, fill=tk.X)

        self.result_button = tk.Button(self.side_menu, text="Results", command=self.result_option)
        self.result_button.pack(pady=30, fill=tk.X)

        self.schedule_button = tk.Button(self.side_menu, text="Schedule", command=self.schedule_option)
        self.schedule_button.pack(pady=30, fill=tk.X)

        self.sport_types_button = tk.Button(self.side_menu, text="Sport types", command=self.sport_types_option)
        self.sport_types_button.pack(pady=30, fill=tk.X)

        self.sportground_button = tk.Button(self.side_menu, text="Sportgrounds", command=self.sportground_option)
        self.sportground_button.pack(pady=30, fill=tk.X)

        self.country_button = tk.Button(self.side_menu, text="Countries", command=self.country_option)
        self.country_button.pack(pady=30, fill=tk.X)

        self.report_button = tk.Button(self.side_menu, text="Reports", command=self.report_option)
        self.report_button.pack(pady=30, fill=tk.X)

        # Create a main content area
        self.main_content = tk.Frame(master, bg="white", padx=20, pady=20)
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Add a label to the main content area
        self.label = tk.Label(self.main_content, text="Welcome! Choose what you need on the side bar!", font=("Arial", 24))
        self.label.pack(pady=10)

        # Add a table
        self.table_frame = tk.Frame(self.main_content, bg="white")
        self.table_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    def participant_option(self):
        self.label.config(text="Participants page")
        self.create_and_fill_table(('ID',
                                    'Country code',
                                    'Name',
                                    'Surname', 
                                    'Birthdate'), 
                                    'SELECT * FROM olympiad.participants')

    def result_option(self):
        self.label.config(text="Results page")
        self.create_and_fill_table(('ID',
                                    'Sport type',
                                    'Sportground',
                                    'Result',
                                    'Place'),
                                    'SELECT * FROM olympiad.start_results')

    def schedule_option(self):
        self.label.config(text="Schedule page")
        self.create_and_fill_table(('ID',
                                    'Sport type',
                                    'Date',
                                    'Time',
                                    'Sport ground'),
                                    'SELECT * FROM olympiad.starts_schedule')

    def sport_types_option(self):
        self.label.config(text="Sport types")
        self.create_and_fill_table(('ID',
                                    'Title',
                                    'Type',
                                    'Desciption',
                                    'Season'),
                                    'SELECT * FROM olympiad.sports_type')

    def sportground_option(self):
        self.label.config(text="Sportgrounds page")
        self.create_and_fill_table(('ID',
                                    'Title',
                                    'Placement',
                                    'Allowed sports'),
                                    'SELECT * FROM olympiad.sports_grounds')

    def country_option(self):
        self.label.config(text="Countries page")
        self.create_and_fill_table(('ID',
                                    'Title'),
                                    'SELECT * FROM olympiad.countries')

    def report_option(self):
        self.label.config(text="You selected Option 7")

    def create_and_fill_table(self, columns: tuple, query: str) -> None:
        if self.current_table:
            self.current_table.destroy()

        # Add a table
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        self.tree.column("#0", width=0, stretch=False)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col)        

        # Fill the table
        for row in self.conn.execute_query(query):
            self.tree.insert("", tk.END, values=row)

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.current_table = self.tree



def main():
    root = tk.Tk()
    app = OlympiadApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import ttk
from sql_connection import SqlConnection

class OlympiadApp:
    def __init__(self, master):
        self.conn = SqlConnection()
        self.master = master
        self.current_table = None

        # adjust the main window
        master.title("Olympiad App")
        master.geometry("1280x720")
        master.minsize(1280, 720)
        master.maxsize(1280, 720)

        # Create a side menu
        self.side_menu = tk.Frame(master, width=150, bg="lightgray")
        self.side_menu.pack(side=tk.LEFT, fill=tk.Y)

        # Create buttons for the side menu
        self.participant_button = tk.Button(self.side_menu, text="Participants", command=self.participant_option)
        self.participant_button.pack(pady=30, fill=tk.X)

        self.result_button = tk.Button(self.side_menu, text="Results", command=self.result_option)
        self.result_button.pack(pady=30, fill=tk.X)

        self.schedule_button = tk.Button(self.side_menu, text="Schedule", command=self.schedule_option)
        self.schedule_button.pack(pady=30, fill=tk.X)

        self.sport_types_button = tk.Button(self.side_menu, text="Sport types", command=self.sport_types_option)
        self.sport_types_button.pack(pady=30, fill=tk.X)

        self.sportground_button = tk.Button(self.side_menu, text="Sportgrounds", command=self.sportground_option)
        self.sportground_button.pack(pady=30, fill=tk.X)

        self.country_button = tk.Button(self.side_menu, text="Countries", command=self.country_option)
        self.country_button.pack(pady=30, fill=tk.X)

        self.report_button = tk.Button(self.side_menu, text="Reports", command=self.report_option)
        self.report_button.pack(pady=30, fill=tk.X)

        # Create a main content area
        self.main_content = tk.Frame(master, bg="white", padx=20, pady=20)
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Add a label to the main content area
        self.label = tk.Label(self.main_content, text="Welcome! Choose what you need on the side bar!", font=("Arial", 24))
        self.label.pack(pady=10)

        # Add a table
        self.table_frame = tk.Frame(self.main_content, bg="white")
        self.table_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    def participant_option(self):
        self.label.config(text="Participants page")
        self.create_and_fill_table(('ID',
                                    'Country code',
                                    'Name',
                                    'Surname', 
                                    'Birthdate'), 
                                    'SELECT * FROM olympiad.participants')

    def result_option(self):
        self.label.config(text="Results page")
        self.create_and_fill_table(('ID',
                                    'Sport type',
                                    'Sportground',
                                    'Result',
                                    'Place'),
                                    'SELECT * FROM olympiad.start_results')

    def schedule_option(self):
        self.label.config(text="Schedule page")
        self.create_and_fill_table(('ID',
                                    'Sport type',
                                    'Date',
                                    'Time',
                                    'Sport ground'),
                                    'SELECT * FROM olympiad.starts_schedule')

    def sport_types_option(self):
        self.label.config(text="Sport types")
        self.create_and_fill_table(('ID',
                                    'Title',
                                    'Type',
                                    'Desciption',
                                    'Season'),
                                    'SELECT * FROM olympiad.sports_type')

    def sportground_option(self):
        self.label.config(text="Sportgrounds page")
        self.create_and_fill_table(('ID',
                                    'Title',
                                    'Placement',
                                    'Allowed sports'),
                                    'SELECT * FROM olympiad.sports_grounds')

    def country_option(self):
        self.label.config(text="Countries page")
        self.create_and_fill_table(('ID',
                                    'Title'),
                                    'SELECT * FROM olympiad.countries')

    def report_option(self):
        self.label.config(text="You selected Option 7")

    def create_and_fill_table(self, columns: tuple, query: str) -> None:
        if self.current_table:
            self.current_table.destroy()

        # Add a table
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        self.tree.column("#0", width=0, stretch=False)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col)        

        # Fill the table
        for row in self.conn.execute_query(query):
            self.tree.insert("", tk.END, values=row)

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.current_table = self.tree



def main():
    root = tk.Tk()
    app = OlympiadApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
