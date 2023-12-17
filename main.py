import tkinter as tk
from tkinter import ttk
from sql_connection import SqlConnection, SqlExecutor
import re
from datetime import datetime

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
        self.medal_per_country_button = None
        self.participant_results_button = None
        self.schedule_of_starts_button = None
        self.save_csv_button = None

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
        self.label.config(text="Report Generator")
        self.reports_page('olympiad.medals_per_cuntries')

    def destroy_existing_elements(self):
        # Destroy existing table and buttons
        if self.current_table:
            self.current_table.destroy()
            self.current_table = None
        if self.new_record_button:
            self.new_record_button.destroy()
            self.new_record_button = None
        if self.columns_filter_button:
            self.columns_filter_button.destroy()
            self.columns_filter_button = None
        if self.new_sorting_button:
            self.new_sorting_button.destroy()
            self.new_sorting_button = None
        if self.update_row_button:
            self.update_row_button.destroy()
            self.update_row_button = None
        if self.delete_row_button:
            self.delete_row_button.destroy()
            self.delete_row_button = None
        if self.refresh_button:
            self.refresh_button.destroy()
            self.refresh_button = None
        if self.medal_per_country_button:
            self.medal_per_country_button.destroy()
            self.medal_per_country_button = None
        if self.participant_results_button:
            self.participant_results_button.destroy()
            self.participant_results_button = None
        if self.schedule_of_starts_button:
            self.schedule_of_starts_button.destroy()
            self.schedule_of_starts_button = None
        if self.save_csv_button:
            self.save_csv_button.destroy()
            self.save_csv_button = None

    def reports_page(self, table_name: str, columns_into_table: tuple = None, needed_conditions: str = '', sorting: dict = {}, all_col: bool = True):
        self.destroy_existing_elements()

        df = self.executor.select_query_builder(table_name, columns_into_table, needed_conditions, sorting, all_col)
        columns = tuple(df.columns)

        medal_per_country_button = tk.Button(self.table_frame, text="Medals Per Country", bg='#7da832', command=lambda: self.reports_page('olympiad.medals_per_cuntries'))
        medal_per_country_button.grid(row=0, column=0, pady=10, padx=5, sticky="nsew")
        self.medal_per_country_button = medal_per_country_button

        participant_results_button = tk.Button(self.table_frame, text="Participant Results", bg='#7da832', command=lambda: self.reports_page('olympiad.participant_results'))
        participant_results_button.grid(row=0, column=1, pady=10, padx=5, sticky="nsew")
        self.participant_results_button = participant_results_button

        schedule_of_starts_button = tk.Button(self.table_frame, text="Schedule Of Starts", bg='#7da832', command=lambda: self.reports_page('olympiad.start_schedule_on_date'))
        schedule_of_starts_button.grid(row=0, column=2, pady=10, padx=5, sticky="nsew")
        self.schedule_of_starts_button = schedule_of_starts_button

        new_sorting_button = tk.Button(self.table_frame, text="Sorting Columns", command=lambda: self.sorting_columns_dialog(table_name, columns))
        new_sorting_button.grid(row=0, column=3, pady=10, padx=5, sticky="nsew")
        self.new_sorting_button = new_sorting_button

        columns_filter_button = tk.Button(self.table_frame, text="Filter Columns", command=lambda: self.open_filter_dialog(table_name, columns, df))
        columns_filter_button.grid(row=0, column=4, pady=10, padx=5, sticky="nsew")
        self.columns_filter_button = columns_filter_button

        save_csv_button = tk.Button(self.table_frame, text="Save As CSV", command=lambda: self.save_to_csv(df), bg="#32a852")
        save_csv_button.grid(row=0, column=5, pady=10, padx=5, sticky="nsew")
        self.save_csv_button = save_csv_button

        # Add a table
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        self.tree.column("#0", width=0, stretch=False)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        for index, row in df.iterrows():
            self.tree.insert("", tk.END, values=[row[column] for column in df.columns])

        self.tree.grid(row=1, column=0, columnspan=6, pady=10, padx=5, sticky="nsew")

        self.table_frame.columnconfigure(0, weight=1)
        self.table_frame.columnconfigure(1, weight=1)
        self.table_frame.columnconfigure(2, weight=1)
        self.table_frame.columnconfigure(3, weight=1)
        self.table_frame.columnconfigure(4, weight=1)
        self.table_frame.columnconfigure(5, weight=1)

        self.table_frame.grid_columnconfigure(0, uniform="buttons")
        self.table_frame.grid_columnconfigure(1, uniform="buttons")
        self.table_frame.grid_columnconfigure(2, uniform="buttons")
        self.table_frame.grid_columnconfigure(3, uniform="buttons")
        self.table_frame.grid_columnconfigure(4, uniform="buttons")
        self.table_frame.grid_columnconfigure(5, uniform="buttons")

        self.current_table = self.tree

    def save_to_csv(self, df):
        df.to_csv(f"csv_files/{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}", sep=';')


    def create_and_fill_table(self, table_name: str, columns_into_table: tuple = None, needed_conditions: str = '', sorting: dict = {}, all_col: bool = True) -> None:
        self.destroy_existing_elements()
        appropriate_functions = {
            'olympiad.results_table_view': self.open_new_record_results_dialog,
            'olympiad.schedule_table_view': self.open_new_record_schedule_dialog
        }
        appropriate_functions_update = {
            'olympiad.results_table_view': self.open_update_results_dialog,
            'olympiad.schedule_table_view': self.open_update_schedule_dialog
        }
        appropriate_functions_delete = {
            'olympiad.results_table_view': self.open_delete_results_dialog,
            'olympiad.schedule_table_view': self.open_delete_schedule_dialog
        }
        df = self.executor.select_query_builder(table_name, columns_into_table, needed_conditions, sorting, all_col)
        columns = tuple(df.columns)

        # Buttons
        columns_filter_button = tk.Button(self.table_frame, text="Filter Columns", command=lambda: self.open_filter_dialog(table_name, columns, df))
        columns_filter_button.grid(row=0, column=0, pady=10, padx=5, sticky=tk.S)
        self.columns_filter_button = columns_filter_button

        new_record_button = tk.Button(self.table_frame, text="New Record", command=lambda: appropriate_functions.get(table_name, self.open_new_record_dialog)(columns, table_name))
        new_record_button.grid(row=0, column=1, pady=10, padx=5, sticky=tk.S)
        self.new_record_button = new_record_button

        update_row_button = tk.Button(self.table_frame, text="Update Record", command=lambda: appropriate_functions_update.get(table_name, self.update_record_dialog)(table_name, columns))
        update_row_button.grid(row=0, column=2, pady=10, padx=5, sticky=tk.S)
        self.update_row_button = update_row_button

        delete_row_button = tk.Button(self.table_frame, text="Delete Record", command=lambda: appropriate_functions_delete.get(table_name, self.delete_record_dialog)(table_name))
        delete_row_button.grid(row=0, column=3, pady=10, padx=5, sticky=tk.S)
        self.delete_row_button = delete_row_button

        new_sorting_button = tk.Button(self.table_frame, text="Sorting Columns", command=lambda: self.sorting_columns_dialog(table_name, columns))
        new_sorting_button.grid(row=0, column=4, pady=10, padx=5, sticky=tk.S)
        self.new_sorting_button = new_sorting_button

        refresh_button = tk.Button(self.table_frame, text="Refresh Page", bg="#429ef5", command=lambda: self.create_and_fill_table(table_name))
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

    def open_new_record_results_dialog(self, columns: tuple, table_name: str):
        self.new_record_window = tk.Toplevel(self.master)
        self.new_record_window.title("New Record")

        label = tk.Label(self.new_record_window, text="Enter details for a new record:")
        label.pack()

        """Enter fields for filling"""
        all_sport_type_names = [str(row['id']) + ': ' + row['name'] for index, row in self.executor.select_query_builder('olympiad.sports_type').iterrows()]
        all_participant_names = [str(row['id']) + ': ' + row['name'] + " " + row['surname'] for index, row in self.executor.select_query_builder('olympiad.participants').iterrows()]
        all_sport_ground_names = [str(row['id']) + ': ' + row['name'] for index, row in self.executor.select_query_builder('olympiad.sports_grounds').iterrows()]

        label = tk.Label(self.new_record_window, text="Choose sport type:")
        label.pack()
        sport_type_var = tk.StringVar()
        combobox = ttk.Combobox(self.new_record_window, textvariable=sport_type_var, values=all_sport_type_names)
        combobox.pack()

        label = tk.Label(self.new_record_window, text="Choose participant:")
        label.pack()
        participant_var = tk.StringVar()
        combobox = ttk.Combobox(self.new_record_window, textvariable=participant_var, values=all_participant_names)
        combobox.pack()

        label = tk.Label(self.new_record_window, text="Choose sport ground:")
        label.pack()
        sport_ground_var = tk.StringVar()
        combobox = ttk.Combobox(self.new_record_window, textvariable=sport_ground_var, values=all_sport_ground_names)
        combobox.pack()

        label = tk.Label(self.new_record_window, text="Enter Result (sec) or keep it empry")
        label.pack()
        sec_result_var = tk.StringVar()
        entry = tk.Entry(self.new_record_window, textvariable=sec_result_var)
        entry.pack()

        label = tk.Label(self.new_record_window, text="Enter place:")
        label.pack()
        place_result_var = tk.StringVar()
        entry = tk.Entry(self.new_record_window, textvariable=place_result_var)
        entry.pack()

        insert_button = tk.Button(self.new_record_window, text="Insert", command=lambda: self.insert_result_record(table_name, sport_type_var, participant_var, sport_ground_var, sec_result_var, place_result_var))
        insert_button.pack(pady=10)

    def insert_result_record(self, table_name, sport_type_var, participant_var, sport_ground_var, sec_result_var, place_result_var):
        sport_type_id = sport_type_var.get().split(': ')[0]
        participant_id = participant_var.get().split(': ')[0]
        sport_ground_id = sport_ground_var.get().split(': ')[0]
        sec_result = sec_result_var.get()
        place_result = place_result_var.get()

        self.executor.insert_row_for_result('olympiad.start_results', ('id', 'sport_type_id', 'participant_id', 'sport_ground_id', 'result_sec', 'position'), [sport_type_id, participant_id, sport_ground_id, sec_result if sec_result != '' else 0, place_result])

        self.new_record_window.destroy()
        self.create_and_fill_table(table_name)

    def open_update_results_dialog(self, table_name, columns):
        self.new_update_window = tk.Toplevel(self.master)
        self.new_update_window.title("Update Record")

        label = tk.Label(self.new_update_window, text="If you don't want to change some fields just keep it empty.")
        label.pack()

        label = tk.Label(self.new_update_window, text="Enter updating row's id:")
        label.pack()

        entry_id_var = tk.StringVar()
        entry = tk.Entry(self.new_update_window, textvariable=entry_id_var)
        entry.pack()

        """Enter fields for filling"""
        all_sport_type_names = [str(row['id']) + ': ' + row['name'] for index, row in self.executor.select_query_builder('olympiad.sports_type').iterrows()]
        all_participant_names = [str(row['id']) + ': ' + row['name'] + " " + row['surname'] for index, row in self.executor.select_query_builder('olympiad.participants').iterrows()]
        all_sport_ground_names = [str(row['id']) + ': ' + row['name'] for index, row in self.executor.select_query_builder('olympiad.sports_grounds').iterrows()]

        label = tk.Label(self.new_update_window, text="Choose sport type:")
        label.pack()
        sport_type_var = tk.StringVar()
        combobox = ttk.Combobox(self.new_update_window, textvariable=sport_type_var, values=all_sport_type_names)
        combobox.pack()

        label = tk.Label(self.new_update_window, text="Choose participant:")
        label.pack()
        participant_var = tk.StringVar()
        combobox = ttk.Combobox(self.new_update_window, textvariable=participant_var, values=all_participant_names)
        combobox.pack()

        label = tk.Label(self.new_update_window, text="Choose sport ground:")
        label.pack()
        sport_ground_var = tk.StringVar()
        combobox = ttk.Combobox(self.new_update_window, textvariable=sport_ground_var, values=all_sport_ground_names)
        combobox.pack()

        label = tk.Label(self.new_update_window, text="Enter Result (sec) or keep it empry")
        label.pack()
        sec_result_var = tk.StringVar()
        entry = tk.Entry(self.new_update_window, textvariable=sec_result_var)
        entry.pack()

        label = tk.Label(self.new_update_window, text="Enter place:")
        label.pack()
        place_result_var = tk.StringVar()
        entry = tk.Entry(self.new_update_window, textvariable=place_result_var)
        entry.pack()

        save_button = tk.Button(self.new_update_window, text="Update", command=lambda: self.update_result_record(table_name, entry_id_var, sport_type_var, participant_var, sport_ground_var, sec_result_var, place_result_var))
        save_button.pack(pady=10)

    def update_result_record(self, table_name, entry_id_var, sport_type_var, participant_var, sport_ground_var, sec_result_var, place_result_var):
        id_ = entry_id_var.get()
        sport_type_id = sport_type_var.get().split(': ')[0]
        participant_id = participant_var.get().split(': ')[0]
        sport_ground_id = sport_ground_var.get().split(': ')[0]
        sec_result = sec_result_var.get()
        place_result = place_result_var.get()

        values = {'sport_type_id': sport_type_id, 'participant_id': participant_id, 
        'sport_ground_id': sport_ground_id, 'result_sec': sec_result, 'position': place_result}
        values = {key: values[key] for key in values if values[key] != ''}

        self.executor.update_row_for_result('olympiad.start_results', id_, values)

        self.new_update_window.destroy()
        self.create_and_fill_table(table_name)

    def open_delete_results_dialog(self, table_name: str):
        self.new_delete_window = tk.Toplevel(self.master)
        self.new_delete_window.title('Delete Record')

        label = tk.Label(self.new_delete_window, text="If you want to delete several records just write their ids with comma, like 19,20,21")
        label.pack()

        label = tk.Label(self.new_delete_window, text="Enter deleting row's id:")
        label.pack()

        entry_id_var = tk.StringVar()
        entry = tk.Entry(self.new_delete_window, textvariable=entry_id_var)
        entry.pack()

        save_button = tk.Button(self.new_delete_window, text="Delete", command=lambda: self.delete_result_record(table_name, entry_id_var))
        save_button.pack(pady=10)

    def delete_result_record(self, table_name, entry_id_var):
        id_ = entry_id_var.get()
        if ',' in id_:
            for current_id in id_.split(','):
                self.executor.delete_row_query_builder('olympiad.start_results', current_id)
        else:
            self.executor.delete_row_query_builder('olympiad.start_results', id_)
        self.new_delete_window.destroy()
        self.create_and_fill_table(table_name)

    def open_new_record_schedule_dialog(self, columns:tuple, table_name: str):
        self.new_record_window = tk.Toplevel(self.master)
        self.new_record_window.title("New Record")

        label = tk.Label(self.new_record_window, text="Enter details for a new record:")
        label.pack()

        """Enter fields for filling"""
        all_sport_type_names = [str(row['id']) + ': ' + row['name'] for index, row in self.executor.select_query_builder('olympiad.sports_type').iterrows()]
        all_sport_ground_names = [str(row['id']) + ': ' + row['name'] for index, row in self.executor.select_query_builder('olympiad.sports_grounds').iterrows()]

        label = tk.Label(self.new_record_window, text="Choose sport type:")
        label.pack()
        sport_type_var = tk.StringVar()
        combobox = ttk.Combobox(self.new_record_window, textvariable=sport_type_var, values=all_sport_type_names)
        combobox.pack()

        label = tk.Label(self.new_record_window, text="Choose sport ground:")
        label.pack()
        sport_ground_var = tk.StringVar()
        combobox = ttk.Combobox(self.new_record_window, textvariable=sport_ground_var, values=all_sport_ground_names)
        combobox.pack()

        label = tk.Label(self.new_record_window, text="Start Date")
        label.pack()
        start_date_var = tk.StringVar()
        entry = tk.Entry(self.new_record_window, textvariable=start_date_var)
        entry.pack()

        label = tk.Label(self.new_record_window, text="Start Time")
        label.pack()
        start_time_var = tk.StringVar()
        entry = tk.Entry(self.new_record_window, textvariable=start_time_var)
        entry.pack()

        insert_button = tk.Button(self.new_record_window, text="Insert", command=lambda: self.insert_schedule_record(table_name, sport_type_var, sport_ground_var, start_date_var, start_time_var))
        insert_button.pack(pady=10)

    def insert_schedule_record(self, table_name, sport_type_var, sport_ground_var, start_date_var, start_time_var):
        sport_type_id = sport_type_var.get().split(': ')[0]
        sport_ground_id = sport_ground_var.get().split(': ')[0]
        start_date = start_date_var.get()
        start_time = start_time_var.get()

        self.executor.insert_row_for_result('olympiad.starts_schedule', ('id', 'sport_type_id', 'start_date', 'start_time', 'sport_ground_id'), [sport_type_id, start_date, start_time, sport_ground_id])

        self.new_record_window.destroy()
        self.create_and_fill_table(table_name)

    def open_update_schedule_dialog(self, table_name, columns):
        self.new_update_window = tk.Toplevel(self.master)
        self.new_update_window.title("Update Record")

        label = tk.Label(self.new_update_window, text="If you don't want to change some fields just keep it empty.")
        label.pack()

        label = tk.Label(self.new_update_window, text="Enter updating row's id:")
        label.pack()

        entry_id_var = tk.StringVar()
        entry = tk.Entry(self.new_update_window, textvariable=entry_id_var)
        entry.pack()

        """Enter fields for filling"""
        all_sport_type_names = [str(row['id']) + ': ' + row['name'] for index, row in self.executor.select_query_builder('olympiad.sports_type').iterrows()]
        all_sport_ground_names = [str(row['id']) + ': ' + row['name'] for index, row in self.executor.select_query_builder('olympiad.sports_grounds').iterrows()]

        label = tk.Label(self.new_update_window, text="Choose sport type:")
        label.pack()
        sport_type_var = tk.StringVar()
        combobox = ttk.Combobox(self.new_update_window, textvariable=sport_type_var, values=all_sport_type_names)
        combobox.pack()

        label = tk.Label(self.new_update_window, text="Choose sport ground:")
        label.pack()
        sport_ground_var = tk.StringVar()
        combobox = ttk.Combobox(self.new_update_window, textvariable=sport_ground_var, values=all_sport_ground_names)
        combobox.pack()

        label = tk.Label(self.new_update_window, text="Start Date")
        label.pack()
        start_date_var = tk.StringVar()
        entry = tk.Entry(self.new_update_window, textvariable=start_date_var)
        entry.pack()

        label = tk.Label(self.new_update_window, text="Start Time")
        label.pack()
        start_time_var = tk.StringVar()
        entry = tk.Entry(self.new_update_window, textvariable=start_time_var)
        entry.pack()

        insert_button = tk.Button(self.new_update_window, text="Insert", command=lambda: self.update_schedule_record(table_name, entry_id_var, sport_type_var, sport_ground_var, start_date_var, start_time_var))
        insert_button.pack(pady=10)

    def update_schedule_record(self, table_name, entry_id_var, sport_type_var, sport_ground_var, start_date_var, start_time_var):
        id_ = entry_id_var.get()
        sport_type_id = sport_type_var.get().split(': ')[0]
        sport_ground_id = sport_ground_var.get().split(': ')[0]
        start_date = start_date_var.get()
        start_time = start_time_var.get()

        values = {'sport_type_id': sport_type_id, 'sport_ground_id': sport_ground_id, 'start_date': start_date, 'start_time': start_time}
        values = {key: values[key] for key in values if values[key] != ''}

        self.executor.update_row_for_result('olympiad.starts_schedule', id_, values)

        self.new_update_window.destroy()
        self.create_and_fill_table(table_name)

    def open_delete_schedule_dialog(self, table_name: str):
        self.new_delete_window = tk.Toplevel(self.master)
        self.new_delete_window.title('Delete Record')

        label = tk.Label(self.new_delete_window, text="If you want to delete several records just write their ids with comma, like 19,20,21")
        label.pack()

        label = tk.Label(self.new_delete_window, text="Enter deleting row's id:")
        label.pack()

        entry_id_var = tk.StringVar()
        entry = tk.Entry(self.new_delete_window, textvariable=entry_id_var)
        entry.pack()

        save_button = tk.Button(self.new_delete_window, text="Delete", command=lambda: self.delete_schedule_record(table_name, entry_id_var))
        save_button.pack(pady=10)

    def delete_schedule_record(self, table_name, entry_id_var):
        id_ = entry_id_var.get()
        if ',' in id_:
            for current_id in id_.split(','):
                self.executor.delete_row_query_builder('olympiad.starts_schedule', current_id)
        else:
            self.executor.delete_row_query_builder('olympiad.starts_schedule', id_)
        self.new_delete_window.destroy()
        self.create_and_fill_table(table_name)

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

        if table_name in ("olympiad.medals_per_cuntries", "olympiad.participant_results", "olympiad.start_schedule_on_date"):
            self.new_filter_window.destroy()
            self.reports_page(table_name, columns_into_table=needed_columns, needed_conditions=needed_conditions, all_col=False)
        else:
            self.new_filter_window.destroy()
            self.create_and_fill_table(table_name, columns_into_table=needed_columns, needed_conditions=needed_conditions, all_col=False)

    def generate_condition(self, entry_values: dict) -> str:
        result = []
        for column in entry_values.keys():
            if entry_values[column] == '':
                continue
            string = ''
            if any(it in entry_values[column] for it in ('>', '>=', '=', '<', '<=')):
                string = column + ' ' + entry_values[column]
            elif self.is_valid_date(entry_values[column]):
                string =  column + " = '" + entry_values[column] + "'"
            else:
                string = column + " ~ '.*" + entry_values[column] + ".*'"
            result.append(string)
        return ' AND '.join(result)

    def is_valid_date(self, date_string, date_format='%Y-%m-%d'):
        try:
            datetime.strptime(date_string, date_format)
            return True
        except ValueError:
            return False


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
        
        if table_name in ("olympiad.medals_per_cuntries", "olympiad.participant_results", "olympiad.start_schedule_on_date"):
            self.new_sorting_window.destroy()
            self.reports_page(table_name, sorting={entry_values[indx]: combobox_values[entry_values[indx]] for indx in dict(sorted(entry_values.items(), key=lambda x: int(x[0])))})
        else:
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
