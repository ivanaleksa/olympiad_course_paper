import tkinter as tk
from tkinter import ttk
from sql_connection import SqlConnection, SqlExecutor
import re

class OlympiadApp:
    def __init__(self, master):
        self.conn = SqlConnection()
        self.executor = SqlExecutor()
        self.master = master
        self.current_table = None
        self.new_record_button = None
        self.new_record_window = None

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
        self.label = tk.Label(self.main_content, text="Welcome! Choose what you need on the side bar!", font=("Arial", 24), bg='White')
        self.label.pack(pady=10)

        # Add a table
        self.table_frame = tk.Frame(self.main_content, bg="white")
        self.table_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    def participant_option(self):
        self.label.config(text="Participants page")
        self.create_and_fill_table('olympiad.participants')

    def result_option(self):
        self.label.config(text="Results page")
        self.create_and_fill_table('olympiad.start_results')

    def schedule_option(self):
        self.label.config(text="Schedule page")
        self.create_and_fill_table('olympiad.starts_schedule')

    def sport_types_option(self):
        self.label.config(text="Sport types")
        self.create_and_fill_table('olympiad.sports_type')

    def sportground_option(self):
        self.label.config(text="Sportgrounds page")
        self.create_and_fill_table('olympiad.sports_grounds')

    def country_option(self):
        self.label.config(text="Countries page")
        self.create_and_fill_table('olympiad.countries')

    def report_option(self):
        self.label.config(text="You selected Option 7")
        self.destroy_existing_elements()

    def destroy_existing_elements(self):
        # Destroy existing table and buttons
        if self.current_table:
            self.current_table.destroy()
        if self.new_record_button:
            self.new_record_button.destroy()

    def create_and_fill_table(self, table_name: str) -> None:
        self.destroy_existing_elements()
        df = self.executor.select_query_builder(table_name)
        columns = tuple(df.columns)

        # Add a table
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        self.tree.column("#0", width=0, stretch=False)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col)        

        # Fill the table
        # for row in df:
        #     self.tree.insert("", tk.END, values=row)

        for index, row in df.iterrows():
            self.tree.insert("", tk.END, values=[row[column] for column in df.columns])

        new_record_button = tk.Button(self.table_frame, text="New Record", command=lambda: self.open_new_record_dialog(columns, query))
        new_record_button.pack(pady=10, side=tk.TOP, anchor=tk.NE)
        self.new_record_button = new_record_button

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.current_table = self.tree

    def open_new_record_dialog(self, columns: tuple, table_name: str):
        self.new_record_window = tk.Toplevel(self.master)
        self.new_record_window.title("New Record")

        label = tk.Label(self.new_record_window, text="Enter details for a new record:")
        label.pack()

        entry_vars = []
        for label_text in columns[1:]:
            label = tk.Label(self.new_record_window, text=label_text)
            label.pack()

            entry_var = tk.StringVar()
            entry_vars.append(entry_var)

            entry = tk.Entry(self.new_record_window, textvariable=entry_var)
            entry.pack()

        # Add a "Save" button to save the new record to the database
        save_button = tk.Button(self.new_record_window, text="Save", command=lambda: self.save_new_record(entry_vars, columns, query))
        save_button.pack(pady=10)

    def save_new_record(self, entry_vars: list, columns:tuple, table_name: str):
        entry_values = [entry_var.get() for entry_var in entry_vars]

        self.executor.insert_row_query_builder(table_name, columns, entry_values)

        self.new_record_window.destroy()
        self.create_and_fill_table(table_name)



def main():
    root = tk.Tk()
    app = OlympiadApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
