import tkinter as tk
from tkinter import ttk
import sqlite3
from tkcalendar import Calendar, DateEntry


class PlannerApp:

    def __init__(self, master):
        self.master = master
        master.title("Planner App")

        # create a connection to the database
        self.conn = sqlite3.connect('planner.db')

        # create a notes table if it doesn't exist
        self.conn.execute('''CREATE TABLE IF NOT EXISTS notes
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              date TEXT NOT NULL,
                              note TEXT NOT NULL);''')

        # create a calendar view
        self.calendar_frame = tk.Frame(master, width=400, height=300)
        self.calendar_frame.grid(row=0, column=0, padx=10, pady=10)

        # create a calendar widget
        self.calendar = Calendar(self.calendar_frame, selectmode="day", date_pattern='y-mm-dd')
        self.calendar.pack(fill="both", expand=True)

        # bind a function to the <<CalendarSelected>> event
        self.calendar.bind("<<CalendarSelected>>", self.show_notes)

        # create a notes view
        self.notes_frame = tk.Frame(master, width=400, height=300)
        self.notes_frame.grid(row=0, column=1, padx=10, pady=10)

        # create a text widget for notes
        self.notes_text = tk.Text(self.notes_frame, wrap=tk.WORD)
        self.notes_text.pack(fill=tk.BOTH, expand=1)

        # create a button to save notes
        self.save_notes_button = tk.Button(self.notes_frame, text="Save Notes", command=self.save_notes)
        self.save_notes_button.pack(pady=10)

    def show_notes(self, event=None):
        # get the selected date from the calendar widget
        date = self.calendar.get_date()

        # fetch the notes for the selected date from the database
        cursor = self.conn.execute("SELECT note FROM notes WHERE date=?", (str(date),))
        rows = cursor.fetchall()

        # display the notes in the text widget
        self.notes_text.delete("1.0", tk.END)
        for row in rows:
            self.notes_text.insert(tk.END, row[0] + "\n")

    def save_notes(self):
        # get the selected date from the calendar widget
        date = self.calendar.get_date()

        # get the notes from the text widget
        notes = self.notes_text.get("1.0", tk.END)

        # delete existing notes for the selected date from the database
        self.conn.execute("DELETE FROM notes WHERE date=?", (str(date),))

        # insert the new notes into the database
        self.conn.execute("INSERT INTO notes (date, note) VALUES (?, ?)", (str(date), notes))
        self.conn.commit()

root = tk.Tk()
app = PlannerApp(root)
root.mainloop()

