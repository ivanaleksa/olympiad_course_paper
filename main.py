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
        self.columns_filter_button = None
        self.new_sorting_button = None
        self.delete_row_button = None
        self.update_row_button = None
        self.refresh_button = None

        self.new_record_window = None
        self.new_update_window = None
        self.new_delete_window = None
        self.new_sorting_window = None
        self.new_filter_window = None

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
        self.create_and_fill_table('olympiad.results_table_view')

    def schedule_option(self):
        self.label.config(text="Schedule page")
        self.create_and_fill_table('olympiad.schedule_table_view')

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
        if self.columns_filter_button:
            self.columns_filter_button.destroy()
        if self.new_sorting_button:
            self.new_sorting_button.destroy()
        if self.update_row_button:
            self.update_row_button.destroy()
        if self.delete_row_button:
            self.delete_row_button.destroy()

    def create_and_fill_table(self, table_name: str, columns_into_table: tuple = None, needed_conditions: str = '', sorting: dict = {}, all_col: bool = True) -> None:
        self.destroy_existing_elements()
        df = self.executor.select_query_builder(table_name, columns_into_table, needed_conditions, sorting, all_col)
        columns = tuple(df.columns)

        # Buttons
        columns_filter_button = tk.Button(self.table_frame, text="Filter Columns", command=lambda: self.open_filter_dialog(table_name, columns, df))
        columns_filter_button.grid(row=0, column=0, pady=10, padx=5, sticky=tk.S)
        self.columns_filter_button = columns_filter_button

        new_record_button = tk.Button(self.table_frame, text="New Record", command=lambda: self.open_new_record_dialog(columns, table_name))
        new_record_button.grid(row=0, column=1, pady=10, padx=5, sticky=tk.S)
        self.new_record_button = new_record_button

        update_row_button = tk.Button(self.table_frame, text="Update Record", command=lambda: self.update_record_dialog(table_name, columns))
        update_row_button.grid(row=0, column=2, pady=10, padx=5, sticky=tk.S)
        self.update_row_button = update_row_button

        delete_row_button = tk.Button(self.table_frame, text="Delete Record", command=lambda: self.delete_record_dialog(table_name))
        delete_row_button.grid(row=0, column=3, pady=10, padx=5, sticky=tk.S)
        self.delete_row_button = delete_row_button

        new_sorting_button = tk.Button(self.table_frame, text="Sorting Columns", command=lambda: self.sorting_columns_dialog(table_name, columns))
        new_sorting_button.grid(row=0, column=4, pady=10, padx=5, sticky=tk.S)
        self.new_sorting_button = new_sorting_button

        refresh_button = tk.Button(self.table_frame, text="Refresh Page", command=lambda: self.create_and_fill_table(table_name))
        refresh_button.grid(row=0, column=5, pady=10, padx=5, sticky=tk.S)
        self.refresh_button = refresh_button

        # Add a table
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        self.tree.column("#0", width=0, stretch=False)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)        

        for index, row in df.iterrows():
            self.tree.insert("", tk.END, values=[row[column] for column in df.columns])

        # Treeview
        self.tree.grid(row=1, column=0, columnspan=6, pady=10, padx=5, sticky=tk.W+tk.E+tk.N+tk.S)

        # Configure row and column weights to make them fill the available space
        self.table_frame.columnconfigure(0, weight=1)
        self.table_frame.columnconfigure(1, weight=1)
        self.table_frame.columnconfigure(2, weight=1)
        self.table_frame.columnconfigure(3, weight=1)
        self.table_frame.columnconfigure(4, weight=1)
        self.table_frame.columnconfigure(5, weight=1)
        self.table_frame.rowconfigure(1, weight=1)

        # Set uniform size for buttons
        self.table_frame.grid_columnconfigure(0, uniform="buttons")
        self.table_frame.grid_columnconfigure(1, uniform="buttons")
        self.table_frame.grid_columnconfigure(2, uniform="buttons")
        self.table_frame.grid_columnconfigure(3, uniform="buttons")
        self.table_frame.grid_columnconfigure(4, uniform="buttons")
        self.table_frame.grid_columnconfigure(5, uniform="buttons")

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
        save_button = tk.Button(self.new_record_window, text="Save", command=lambda: self.save_new_record(entry_vars, columns, table_name))
        save_button.pack(pady=10)

    def save_new_record(self, entry_vars: list, columns:tuple, table_name: str):
        entry_values = [entry_var.get() for entry_var in entry_vars]

        self.executor.insert_row_query_builder(table_name, columns, entry_values)

        self.new_record_window.destroy()
        self.create_and_fill_table(table_name)

    def open_filter_dialog(self, table_name: str, columns: tuple, df):
        self.new_filter_window = tk.Toplevel(self.master)
        self.new_filter_window.title("Filter records and columns")

        label = tk.Label(self.new_filter_window, text="""Set checkbox true if you want to render this columns.
            If a columns is numeric field you can filter it as: >, >=, <, <=, = (example: > 10)
            If the column is text field just write needed substring for searching""")
        label.pack()

        entry_vars = []
        checkbox_vars = []

        for label_text in columns:
            label = tk.Label(self.new_filter_window, text=label_text)
            label.pack()

            entry_var = tk.StringVar()
            entry_vars.append(entry_var)

            checkbox_var = tk.BooleanVar(value=True)
            checkbox = tk.Checkbutton(self.new_filter_window, variable=checkbox_var)
            checkbox_vars.append(checkbox_var)
            checkbox.pack()

            entry = tk.Entry(self.new_filter_window, textvariable=entry_var)
            entry.pack()

        filter_button = tk.Button(self.new_filter_window, text="Filter", command=lambda: self.filter_records(table_name, entry_vars, checkbox_vars, columns))
        filter_button.pack(pady=10)

    def filter_records(self, table_name, entry_vars, checkbox_vars, columns):
        entry_values = {columns[i]: entry_vars[i].get() for i in range(len(entry_vars))}
        checkbox_values = {columns[i]: checkbox_vars[i].get() for i in range(len(entry_vars))}
        
        needed_columns = [column for column in checkbox_values if checkbox_values[column]]
        needed_conditions = "WHERE " + self.generate_condition(entry_values) if not all([entry_values[column] == '' for column in entry_values]) else ''

        self.new_filter_window.destroy()
        self.create_and_fill_table(table_name, columns_into_table=needed_columns, needed_conditions=needed_conditions, all_col=False)

    @staticmethod
    def generate_condition(entry_values: dict) -> str:
        result = []
        for column in entry_values.keys():
            if entry_values[column] == '':
                continue
            string = ''
            if any(it in entry_values[column] for it in ('>', '>=', '=', '<', '<=')):
                string = column + ' ' + entry_values[column]
            else:
                string = column + " ~ '.*" + entry_values[column] + ".*'"
            result.append(string)
        return ' AND '.join(result)


    def sorting_columns_dialog(self, table_name: str, columns: tuple):
        self.new_sorting_window = tk.Toplevel(self.master)
        self.new_sorting_window.title("Sorting fields")

        label = tk.Label(self.new_sorting_window, text="If you want to sort with ceartain fields write theit sort number (first'll be first)\nand choose the sorting option.\nElse keep it empty")
        label.pack()

        entry_vars = []
        combobox_vars = {}

        for label_text in columns[1:]:
            label = tk.Label(self.new_sorting_window, text=label_text)
            label.pack()

            entry_var = tk.StringVar()
            entry_vars.append(entry_var)

            entry = tk.Entry(self.new_sorting_window, textvariable=entry_var)
            entry.pack()

            combobox_var = tk.StringVar()
            combobox_vars[label_text] = combobox_var

            options = ['ASC', 'DESC']
            combobox = ttk.Combobox(self.new_sorting_window, textvariable=combobox_var, values=options)
            combobox.pack()

        sort_button = tk.Button(self.new_sorting_window, text="Sort", command=lambda: self.sort_records(table_name, entry_vars, combobox_vars, columns))
        sort_button.pack(pady=10)

    def sort_records(self, table_name: str, entry_vars, combobox_vars, columns: tuple):
        entry_values = {entry_vars[i].get(): columns[i + 1] for i in range(len(entry_vars)) if entry_vars[i].get() != ''}
        combobox_values = {elem: combobox_vars[elem].get() for elem in combobox_vars}
        
        self.new_sorting_window.destroy()
        self.create_and_fill_table(table_name, sorting={entry_values[indx]: combobox_values[entry_values[indx]] for indx in dict(sorted(entry_values.items(), key=lambda x: int(x[0])))})


    def update_record_dialog(self, table_name: str, columns: tuple):
        self.new_update_window = tk.Toplevel(self.master)
        self.new_update_window.title("Update Record")

        label = tk.Label(self.new_update_window, text="If you don't want to change some fields just keep it empty.")
        label.pack()

        label = tk.Label(self.new_update_window, text="Enter updating row's id:")
        label.pack()

        entry_id_var = tk.StringVar()
        entry = tk.Entry(self.new_update_window, textvariable=entry_id_var)
        entry.pack()

        entry_vars = []
        for label_text in columns[1:]:
            label = tk.Label(self.new_update_window, text=label_text)
            label.pack()

            entry_var = tk.StringVar()
            entry_vars.append(entry_var)

            entry = tk.Entry(self.new_update_window, textvariable=entry_var)
            entry.pack()

        save_button = tk.Button(self.new_update_window, text="Update", command=lambda: self.update_record(table_name, entry_id_var, entry_vars, columns))
        save_button.pack(pady=10)

    def update_record(self, table_name: str, entry_id_var, entry_vars, columns: tuple):
        id_ = entry_id_var.get()
        values = {columns[i + 1]: entry_vars[i].get() for i in range(len(columns) - 1) if entry_vars[i].get() != ''}

        self.executor.update_row_query_builder(table_name, id_, values)

        self.new_update_window.destroy()
        self.create_and_fill_table(table_name)

    def delete_record_dialog(self, table_name: str):
        self.new_delete_window = tk.Toplevel(self.master)
        self.new_delete_window.title('Delete Record')

        label = tk.Label(self.new_delete_window, text="If you want to delete several records just write their ids with comma, like 19,20,21")
        label.pack()

        label = tk.Label(self.new_delete_window, text="Enter deleting row's id:")
        label.pack()

        entry_id_var = tk.StringVar()
        entry = tk.Entry(self.new_delete_window, textvariable=entry_id_var)
        entry.pack()

        save_button = tk.Button(self.new_delete_window, text="Delete", command=lambda: self.delete_record(table_name, entry_id_var))
        save_button.pack(pady=10)

    def delete_record(self, table_name: str, entry_id_var):
        id_ = entry_id_var.get()
        if ',' in id_:
            for current_id in id_.split(','):
                self.executor.delete_row_query_builder(table_name, current_id)
        else:
            self.executor.delete_row_query_builder(table_name, id_)
        self.new_delete_window.destroy()
        self.create_and_fill_table(table_name)



def main():
    root = tk.Tk()
    app = OlympiadApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
