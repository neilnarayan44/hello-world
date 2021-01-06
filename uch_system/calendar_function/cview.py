# call this cview.py as it is an imported module
import calendar
import datetime
import tkinter as tk


class Calv:

    """Return the format of the calendar_function."""

    def __init__(self, a, b):
        """Instantiate the calendar_function. """
        self.a = a
        self.b = b
        self.c = calendar.TextCalendar(calendar.SUNDAY)
        self.year = datetime.date.today().year
        self.month = datetime.date.today().month
        self.w = []
        self.day_select = 1
        self.month_select = self.month
        self.year_select = self.year
        self.day_name = ''
        self.colour_day_buttons = 'green'
        self.colour_a_day_buttons = 'red'

        self.setup(self.year, self.month)

    # reset buttons
    def reset(self):
        """Clear the date selected on the calendar_function."""
        for r in self.w[:]:
            r.grid_forget()
            # r.destroy()
            self.w.remove(r)

    # moves to previous month/year
    def go_back(self):
        """Button to move to previous month or year."""
        if self.month > 1:
            self.month -= 1
        else:
            self.month = 12
            self.year -= 1
        # self.selected = (self.month, self.year)
        self.reset()
        self.setup(self.year, self.month)

    # moves to next month/year
    def go_forward(self):
        """Button to move to next month or year."""
        if self.month < 12:
            self.month += 1
        else:
            self.month = 1
            self.year += 1

        # self.selected = (self.month, self.year)
        self.reset()
        self.setup(self.year, self.month)

    # date selection
    def s(self, day, name):
        """Obtains data for selected day, month and year."""

        pass

    # calendar_function creation
    def setup(self, y, m):
        """Create calendar_function buttons."""
        left = tk.Button(self.a, text='<', command=self.go_back)
        self.w.append(left)
        left.grid(row=0, column=1)

        header = tk.Label(self.a, height=2, text='{}   {}'.format(calendar.month_abbr[m], str(y)))
        self.w.append(header)
        header.grid(row=0, column=2, columnspan=3)

        right = tk.Button(self.a, text='>', command=self.go_forward)
        self.w.append(right)
        right.grid(row=0, column=5)

        days = ['Sunday',
                'Monday',
                'Tuesday',
                'Wednesday',
                'Thursday',
                'Friday',
                'Saturday']
        for n, name in enumerate(days):
            t = tk.Label(self.a, text=name[:3])
            self.w.append(t)
            t.grid(row=1, column=n)

        for i, week in enumerate(self.c.monthdayscalendar(y, m), 2):
            for d, day in enumerate(week):
                if day:
                    b = tk.Button(self.a, width=1, text=day,
                                  command=lambda day=day: self.s(day, calendar.day_name[(day) % 7]))

                    b.grid(row=i, column=d, sticky='nsew')

    def return_home(self):
        """Reset calendar_function after date selected."""
        self.a.destroy()
