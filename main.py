import tkinter as tk

class OlympiadApp:
    def __init__(self, master):
        self.master = master

        # adjust the main window
        master.title("Olympiad App")
        master.geometry("1280x720")
        master.minsize(1280, 720)
        master.maxsize(1280, 720)

        # Create a side menu
        self.side_menu = tk.Frame(master, width=150, bg="lightgray")
        self.side_menu.pack(side=tk.LEFT, fill=tk.Y)

        # Create buttons for the side menu
        self.button1 = tk.Button(self.side_menu, text="Участники", command=self.option1)
        self.button1.pack(pady=30)

        self.button2 = tk.Button(self.side_menu, text="Результаты", command=self.option2)
        self.button2.pack(pady=30, anchor='center')

        self.button3 = tk.Button(self.side_menu, text="Расписание\nстартов", command=self.option3)
        self.button3.pack(pady=30, anchor='center')

        self.button4 = tk.Button(self.side_menu, text="Виды спорта", command=self.option4)
        self.button4.pack(pady=30, anchor='center')

        self.button5 = tk.Button(self.side_menu, text="Спортивные\nплощадки", command=self.option5)
        self.button5.pack(pady=30, anchor='center')

        self.button6 = tk.Button(self.side_menu, text="Страны", command=self.option6)
        self.button6.pack(pady=30, anchor='center')

        self.button7 = tk.Button(self.side_menu, text="Отчеты", command=self.option7)
        self.button7.pack(pady=30, anchor='center')

        # Create a main content area
        self.main_content = tk.Frame(master, bg="white", padx=20, pady=20)
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Add a label to the main content area
        self.label = tk.Label(self.main_content, text="Здравствуйте! Выберете в боковом меню нужный раздел", font=("Arial", 24))
        self.label.pack(pady=10)

    def option1(self):
        self.label.config(text="You selected Option 1")

    def option2(self):
        self.label.config(text="You selected Option 2")

    def option3(self):
        self.label.config(text="You selected Option 3")

    def option4(self):
        self.label.config(text="You selected Option 4")

    def option5(self):
        self.label.config(text="You selected Option 5")

    def option6(self):
        self.label.config(text="You selected Option 6")

    def option7(self):
        self.label.config(text="You selected Option 7")


def main():
    root = tk.Tk()
    app = OlympiadApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
