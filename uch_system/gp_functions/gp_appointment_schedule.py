import tkinter as tk
from tkinter import messagebox, ttk
from uch_system.calendar_function.cal import Cal
import json
import datetime
from tkinter import *
from uch_system.gp_functions.gp import GP
import operator
import uch_system.gp_functions.gp_prescriptions as gp_prescriptions
from tkinter import font as tkFont
from datetime import date

#defining frames
def rFrame(frame):
    frame.tkraise()

#defining homepage
def home(start):
    rFrame(start)

#defining appointment view page
def viewAppointments(viewappt):
    rFrame(viewappt)


#defining booking holiday page
def holiday(hol, gp):
    rFrame(hol)
    holiday_bookings(hol, gp)

def holiday_bookings(hol, gp):
    gp = initialise_current_gp(gp.username)
    if len(gp.holidays) >= 0:

        my_tree = ttk.Treeview(hol)

        # Define columns
        my_tree['columns'] = ('Start Date', 'End Date', 'Approved')

        # Format columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Start Date", anchor=CENTER, width=100, stretch=NO)
        my_tree.column("End Date", anchor=CENTER, width=100)
        my_tree.column("Approved", anchor=W, width=100)

        # Create headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("Start Date", text="Start Date", anchor=CENTER)
        my_tree.heading("End Date", text="End Date", anchor=CENTER)
        my_tree.heading("Approved", text="Approved", anchor=W)

        count = 0

        for i in gp.holidays:

            my_tree.insert(parent='', index='end', iid=count, text="", values=(i[0], i[1], i[2]))

            count += 1


        my_tree.grid(row=0, column=5, columnspan=2, padx=60, pady=10)

        def cancel_booking():
            gp_database = json.load(open('../uch_system/gp_database.json'))

            selected = my_tree.selection()

            print_records = ''

            # Changes Verified status for all selected GPs to True
            for rec in selected:
                value = my_tree.item(rec, 'values')
                index = -1
                for i in gp_database[gp.username]["Holidays"]:
                    index += 1
                    if i[0] == value[0] and i[1] == value[1]:
                        gp_database[gp.username]["Holidays"].pop(index)

                    print_records += str(value[0]) + "\n"

            # Updates GP database
            json.dump(gp_database, open('../uch_system/gp_database.json', 'w'), indent=2)
            messagebox.showinfo("REQUEST", "Your changes have been confirmed")

            holiday_bookings(hol, gp)

        Button(hol, text="Cancel holiday", command=cancel_booking).grid(row=5, column=5, columnspan=2)


def bookings_to_approve(aprv_app, gp, start):
    """
    Displays a table of all the requested appointments patients have made for the current GP

    Can choose to reject or approve any of the appointments by selecting them and clicking the corresponding button
    :param aprv_app: the tkinter Frame that displays all the appointments that require approval
    :param gp: instance of the class GP for the current GP that is logged in
    :param start: the tkinter Frame that displays the generic appointment portal
    """
    def confirm_request():
        """Changes selected appointment from 'requested' status to 'approved' status"""

        # Loads patient database
        database = json.load(open('../uch_system/database.json'))

        selected = my_tree.selection()

        # Iterates through the selected appointments
        for rec in selected:
            # Loads appointment database
            appointments = json.load(open('../uch_system/appointments.json'))
            value = my_tree.item(rec, 'values')
            nhs_number = value[2]
            date_selected = value[3]
            time_selected = value[4]
            # Checks whether patient is already in appointments database
            if nhs_number in appointments["Approved"]:
                # Adds date and time to approved section of appointments database
                appointments["Approved"][nhs_number][date_selected] = time_selected
                # Deletes date and time from requested section of appointments database
                del appointments["Requested"][nhs_number][date_selected]
                # Saves changes and calls function to update table
                json.dump(appointments, open('../uch_system/appointments.json', 'w'), indent=2)
                bookings_to_approve(aprv_app, gp, start)
            else:
                appointments["Approved"][nhs_number] = {date_selected:time_selected}
                del appointments["Requested"][nhs_number][date_selected]
                json.dump(appointments, open('../uch_system/appointments.json', 'w'), indent=2)
                bookings_to_approve(aprv_app, gp, start)

        messagebox.showinfo("REQUEST", "Your changes have been confirmed")

    def reject_request():
        """Changes selected appointment from 'requested' status to 'cancelled' status"""
        selected = my_tree.selection()

        # Iterates through all the appointments that have been selected
        for rec in selected:
            appointments = json.load(open('../uch_system/appointments.json'))
            value = my_tree.item(rec, 'values')
            nhs_number = value[2]
            date_selected = value[3]
            time_selected = value[4]
            # Checks whether patient is already in cancelled section of patient data set
            if nhs_number in appointments["Cancelled"]:
                # Add booking to cancelled section and delete from the requested section
                appointments["Cancelled"][nhs_number][date_selected] = time_selected
                del appointments["Requested"][nhs_number][date_selected]
            else:
                appointments["Cancelled"][nhs_number] = {date_selected:time_selected}

            json.dump(appointments, open('../uch_system/appointments.json', 'w'), indent=2)
            bookings_to_approve(aprv_app, gp, start)

        messagebox.showinfo("REQUEST", "Your changes have been confirmed")

    # Load patient and appointments database
    db = json.load(open('../uch_system/database.json'))
    appointments = json.load(open('../uch_system/appointments.json'))

    list_of_app = []

    # Iterates through requested appointments
    for nhs_number, profile in appointments["Requested"].items():
        for user_profile in db.values():
            # Cross-references nhs_number and GP from appointment database with user database
            if user_profile["NHS_number"] == nhs_number and user_profile["assigned_gp"] == gp.gmc_number:
                for date_of_app, time_of_app in profile.items():
                    # Adds details to list of appointments
                    list_of_app.append([user_profile["First Name"], user_profile["Last Name"],
                                        user_profile["NHS_number"], date_of_app, time_of_app, date_of_app])

    def sort_appointments(list_of_app):
        """Converts date in D/M/YYYY to datetime instance with standard YYYY-MM-DD formatting to allow easier comparisons"""
        for i in list_of_app:
            date_split = i[5].split("/")
            f_date = date(year=int(date_split[2]), month=int(date_split[1]), day=int(date_split[0]))
            i[5] = f_date
        list_of_app.sort(key=lambda x: x[5])
        return list_of_app

    # Sorts the appointments by date and then time
    list_of_app = sort_appointments(list_of_app)

    if len(list_of_app) > 0:
        # Show all of patients that require approval
        rFrame(aprv_app)
        tk.Button(aprv_app, bg="white", text="Back", command=start.tkraise).grid(row=2, column=0, padx=(70,0))
        my_tree = ttk.Treeview(aprv_app)

        # Define columns
        my_tree['columns'] = ('First Name', 'Last Name', 'NHS Number', 'Date', 'Time')

        # Format columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("First Name", anchor=CENTER, width=100, stretch=NO)
        my_tree.column("Last Name", anchor=CENTER, width=100)
        my_tree.column("NHS Number", anchor=CENTER, width=100)
        my_tree.column("Date", anchor=CENTER, width=100)
        my_tree.column("Time", anchor=CENTER, width=100)

        # Create headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("First Name", text="First Name", anchor=CENTER)
        my_tree.heading("Last Name", text="Last Name", anchor=CENTER)
        my_tree.heading("NHS Number", text="NHS Number", anchor=CENTER)
        my_tree.heading("Date", text="Date", anchor=CENTER)
        my_tree.heading("Time", text="Time", anchor=CENTER)

        count = 0

        # Adds each appointment to table
        for requests in list_of_app:
            my_tree.insert(parent='', index='end', iid=count, text="",
                               values=(requests[0], requests[1],
                                       requests[2], requests[3],
                                       requests[4]
                                       ))

            count += 1
        my_tree.grid(row=1, column=0, columnspan=3, padx=100, pady=10)

        request_label = Label(aprv_app, text="Requested Appointments")
        request_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Button to approve the selected appointments
        request_btn = Button(aprv_app, text="Approve appointment request", command=confirm_request)
        request_btn.grid(row=2, column=1, pady=10)

        # Button to reject the selected appointments
        request_btn = Button(aprv_app, text="Reject appointment request", command=reject_request)
        request_btn.grid(row=2, column=2, pady=10, padx=(0,50))

    else:
        messagebox.showinfo("Information", "No more bookings that require approval!")
        start.tkraise()


def set_availability(set_av, gp, start):
    """Allows GP to set their weekly schedule, by setting a start and end time for their shift"""
    from datetime import timedelta, datetime
    rFrame(set_av)

    # This re-initialises the gp instance each time
    # the function is called so that changes in the database are reflected.
    gp = initialise_current_gp(gp.username)

    # Define length of consultation.
    consultation_duration = timedelta(minutes=10)

    # Creating datetime object for the initial 9am appointment time.
    app_time = datetime(year=2000, month=1, day=1, hour=9, minute=0)

    appointment_times = []

    # For loop to create all the appointment times in a 9-5pm day.
    for i in range(48):
        appointment_times.append(app_time.strftime("%H:%M"))
        app_time += consultation_duration

    Label(set_av, text="Start of shift: ").grid(row=1, column=2)
    Label(set_av, text="End of shift: ").grid(row=1, column=3)

    # For each day of the week a drop down box is created with all the appointment times for GP
    # to be able to choose start and end time of their shift

    # Monday

    Label(set_av, text= "Monday: ").grid(row = 3, column = 1)

    monday_start = ttk.Combobox(set_av)
    monday_start["values"] = tuple(appointment_times)
    monday_start.current(appointment_times.index(gp.monday_s))
    monday_start.grid(row=3, column=2)

    monday_end = ttk.Combobox(set_av)
    monday_end["values"] = tuple(appointment_times)
    monday_end.current(appointment_times.index(gp.monday_e))
    monday_end.grid(row=3, column=3)

    # Tuesday

    Label(set_av, text= "Tuesday: ").grid(row = 4, column = 1)

    tuesday_start = ttk.Combobox(set_av)
    tuesday_start["values"] = tuple(appointment_times)
    tuesday_start.current(appointment_times.index(gp.tuesday_s))
    tuesday_start.grid(row=4, column=2)

    tuesday_end = ttk.Combobox(set_av)
    tuesday_end["values"] = tuple(appointment_times)
    tuesday_end.current(appointment_times.index(gp.tuesday_e))
    tuesday_end.grid(row=4, column=3)

    # Wednesday

    Label(set_av, text= "Wednesday: ").grid(row = 5, column = 1)

    wednesday_start = ttk.Combobox(set_av)
    wednesday_start["values"] = tuple(appointment_times)
    wednesday_start.current(appointment_times.index(gp.wednesday_s))
    wednesday_start.grid(row=5, column=2)

    wednesday_end = ttk.Combobox(set_av)
    wednesday_end["values"] = tuple(appointment_times)
    wednesday_end.current(appointment_times.index(gp.wednesday_e))
    wednesday_end.grid(row=5, column=3)

    # Thursday

    Label(set_av, text= "Thursday: ").grid(row = 6, column = 1)

    thursday_start = ttk.Combobox(set_av)
    thursday_start["values"] = tuple(appointment_times)
    thursday_start.current(appointment_times.index(gp.thursday_s))
    thursday_start.grid(row=6, column=2)

    thursday_end = ttk.Combobox(set_av)
    thursday_end["values"] = tuple(appointment_times)
    thursday_end.current(appointment_times.index(gp.thursday_e))
    thursday_end.grid(row=6, column=3)

    # Friday

    Label(set_av, text= "Friday: ").grid(row = 7, column = 1)

    friday_start = ttk.Combobox(set_av)
    friday_start["values"] = tuple(appointment_times)
    friday_start.current(appointment_times.index(gp.friday_s))
    friday_start.grid(row=7, column=2)

    friday_end = ttk.Combobox(set_av)
    friday_end["values"] = tuple(appointment_times)
    friday_end.current(appointment_times.index(gp.friday_e))
    friday_end.grid(row=7, column=3)

    Label(set_av, text="Choose Lunch Hour: ").grid(row=8, column=1)
    lunch_hour = ttk.Combobox(set_av)
    lunch_time_options = ("09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00")
    lunch_hour["values"] = lunch_time_options
    lunch_hour.current(lunch_time_options.index(gp.lunch))
    lunch_hour.grid(row=8, column=2)

    def confirm_av():
        """First checks that all shift end times are actually later than start times, then saves info in gp_database"""
        gp_database = json.load(open("../uch_system/gp_database.json"))

        schedule_error = False

        # For each day checks that the start time is before (or equal) to end time and they are both valid times
        if monday_start.get() <= monday_end.get() \
                and monday_start.get() in appointment_times and monday_end.get() in appointment_times:
            gp_database[gp.username]["Availability"]["Monday Start"] = monday_start.get()
            gp_database[gp.username]["Availability"]["Monday End"] = monday_end.get()
        else:
            schedule_error = True

        if tuesday_start.get() <= tuesday_end.get() \
                and tuesday_start.get() in appointment_times and tuesday_end.get() in appointment_times:
            gp_database[gp.username]["Availability"]["Tuesday Start"] = tuesday_start.get()
            gp_database[gp.username]["Availability"]["Tuesday End"] = tuesday_end.get()
        else:
            schedule_error = True

        if wednesday_start.get() <= wednesday_end.get() \
                and wednesday_start.get() in appointment_times and wednesday_end.get() in appointment_times:
            gp_database[gp.username]["Availability"]["Wednesday Start"] = wednesday_start.get()
            gp_database[gp.username]["Availability"]["Wednesday End"] = wednesday_end.get()
        else:
            schedule_error = True

        if thursday_start.get() <= thursday_end.get() \
                and thursday_start.get() in appointment_times and thursday_end.get() in appointment_times:
            gp_database[gp.username]["Availability"]["Thursday Start"] = thursday_start.get()
            gp_database[gp.username]["Availability"]["Thursday End"] = thursday_end.get()
        else:
            schedule_error = True

        if friday_start.get() <= friday_end.get() \
                and friday_start.get() in appointment_times and friday_end.get() in appointment_times:
            gp_database[gp.username]["Availability"]["Friday Start"] = friday_start.get()
            gp_database[gp.username]["Availability"]["Friday End"] = friday_end.get()
        else:
            schedule_error = True

        if lunch_hour.get() in lunch_time_options:
            gp_database[gp.username]["Availability"]["Lunch"] = lunch_hour.get()
        else:
            schedule_error = True

        # Raises error if shift start time is later than shift end time for any of the weekdays.
        if schedule_error is True:
            messagebox.showwarning("Incorrect schedule", "Please only select times from drop down list and "
                                                         "ensure the start times are always before end times")
        else:
            messagebox.showinfo("Changes confirmed", "Your changes have been confirmed. "
                                                     "These will prevent future appointments being booked outside "
                                                     "of your availability, though any appointments already approved "
                                                     "remain.")
            start.tkraise()

        # Updates the GP appointment database
        json.dump(gp_database, open('../uch_system/gp_database.json', 'w'))

    # Important notice to diplay for GPs so that they understand the effect of changing their schedule
    Label(set_av, text="Important notice: Changes to your weekly schedule prevent future appointments\n being "
                       "booked outside of your availability however any appointments \nalready booked remain "
                       "the same unless cancelled individually",
          fg="red", bg="light blue").grid(row=9, column=2, columnspan=2, pady=10, padx=10)

    # Button to go back to main appointment portal
    Button(set_av, bg="white", text="Back", command=start.tkraise, width=15).grid(row=10, column=2, columnspan=1)
    # Button to save changes (also takes GP back to main appointment portal)
    Button(set_av, text="Confirm weekly schedule", command=confirm_av).grid(row=10, column=3, columnspan=1, pady=20)


def app_today(gp):
    """Displays GP's appointments today and allows GP to cancel or open the consultation"""

    appointments_today = Tk()
    appointments_today.geometry("550x300")
    appointments_today.title("Today\'s Appointments")

    # Loads patient and appointment database
    db = json.load(open('../uch_system/database.json'))
    appointments = json.load(open('../uch_system/appointments.json'))

    list_of_app = []

    # Iterates through every approved appointment
    for id, profile in appointments["Approved"].items():
        for user_profile in db.values():
            # Cross-references nhs_number for patient in appointment system with patient database
            # and checks if their GP is the currently logged in GP
            if user_profile["NHS_number"] == id and user_profile["assigned_gp"] == gp.gmc_number:
                for date, time in profile.items():
                    # Reformat data so can easily be compared with today's date using datetime module
                    date_split = date.split("/")
                    date_datetime = datetime.date(year=int(date_split[2]), month=int(date_split[1]),
                                                  day=int(date_split[0]))

                    if date_datetime == datetime.date.today():
                        list_of_app.append([user_profile["First Name"], user_profile["Last Name"],
                                            user_profile["NHS_number"], date, time])

    if len(list_of_app) > 0:

        # Show all of patients that require approval

        my_tree = ttk.Treeview(appointments_today)

        # Define columns
        my_tree['columns'] = ('First Name', 'Last Name', 'NHS Number', 'Date', 'Time')

        # Format columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("First Name", anchor=CENTER, width=100, stretch=NO)
        my_tree.column("Last Name", anchor=CENTER, width=100)
        my_tree.column("NHS Number", anchor=W, width=100)
        my_tree.column("Date", anchor=W, width=100)
        my_tree.column("Time", anchor=W, width=100)

        # Create headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("First Name", text="First Name", anchor=CENTER)
        my_tree.heading("Last Name", text="Last Name", anchor=CENTER)
        my_tree.heading("NHS Number", text="NHS Number", anchor=W)
        my_tree.heading("Date", text="Date", anchor=W)
        my_tree.heading("Time", text="Time", anchor=W)

        count = 0

        # Orders the appointments by time
        list_of_app.sort(key=lambda x: x[4])

        # Adds appointments to table
        for requests in list_of_app:
            my_tree.insert(parent='', index='end', iid=count, text="",
                           values=(requests[0], requests[1],
                                   requests[2], requests[3],
                                   requests[4]
                                   ))
            my_tree.grid(row=0, column=0, columnspan=2, padx=20, pady=10)
            count += 1

        def open_consultation():
            from uch_system.gp_functions.gp import GP
            selected = my_tree.selection()

            # For each item selected extracts nhs_number from table and checks which patient this corresponds to
            for rec in selected:
                value = my_tree.item(rec, 'values')
                nhs_number = value[2]
                database = json.load(open('../uch_system/database.json'))
                for patient in database.keys():
                    if database[patient]["NHS_number"] == nhs_number:
                        # Open consultation panel for the patient selected
                        GP.consultation_body(patient)


        # Button to open a consultation
        request_btn = Button(appointments_today, text="Open selected consultation", command=lambda: open_consultation())
        request_btn.grid(row=2, column=1, pady=10)
        Button(appointments_today, text="Add/View Prescriptions",
               command=lambda: gp_prescriptions.meds_window(my_tree, type="today")).grid(row=2, column=0)

    else:
        messagebox.showinfo("Information", "No appointments on selected day!")
        appointments_today.destroy()


def listofappt(apptlist, dpicker, start, gp, viewappt, select):
    """
    Shows approved appointments for a selected day

    :param apptlist: tkinter Frame which displays the table with the selected day's appointments
    :param dpicker:
    :param start: tkinter Frame which displays the main appointment portal
    :param gp: instance of the class GP for the current GP that is logged in
    :param viewappt: tkinter Frame that displays calendar_function for GP to select a date
    """
    # Load patient and appointment databases
    db = json.load(open('../uch_system/database.json'))
    appointments = json.load(open('../uch_system/appointments.json'))

    date_selected = str(dpicker.day_select) + "/" + str(dpicker.month_select) + "/" + str(dpicker.year_select)

    list_of_app = []

    # Iterates through patient records in appointment database
    for nhs_number, profile in appointments["Approved"].items():
        for user_profile in db.values():
            # Cross-references patient appointment records with patient database
            # and checks whether their assigned GP is the current GP that is logged in
            if user_profile["NHS_number"] == nhs_number and user_profile["assigned_gp"] == gp.gmc_number:

                for date, time in profile.items():

                    if select == "all":
                        list_of_app.append([user_profile["First Name"], user_profile["Last Name"],
                                                user_profile["NHS_number"], date, time])

                    elif select == "one" and date == date_selected:
                    # Checks whether date of appointment is same as date selected

                        list_of_app.append([user_profile["First Name"], user_profile["Last Name"],
                                            user_profile["NHS_number"], date, time])

    if len(list_of_app) > 0:
        # Show all of patients that require approval
        apptlist.tkraise()

        my_tree = ttk.Treeview(apptlist)

        # Define columns
        my_tree['columns'] = ('First Name', 'Last Name', 'NHS Number', 'Date', 'Time')

        # Format columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("First Name", anchor=CENTER, width=100, stretch=NO)
        my_tree.column("Last Name", anchor=CENTER, width=100)
        my_tree.column("NHS Number", anchor=W, width=100)
        my_tree.column("Date", anchor=W, width=100)
        my_tree.column("Time", anchor=W, width=100)

        # Create headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("First Name", text="First Name", anchor=CENTER)
        my_tree.heading("Last Name", text="Last Name", anchor=CENTER)
        my_tree.heading("NHS Number", text="NHS Number", anchor=W)
        my_tree.heading("Date", text="Date", anchor=W)
        my_tree.heading("Time", text="Time", anchor=W)

        count = 0

        if select == "one":
            # Sorts the appointments by time (earliest to latest)
            list_of_app.sort(key=lambda x: x[4])
        else:
            list_of_app.sort(key=operator.itemgetter(3, 4))


        # Adds each appointment to table
        for requests in list_of_app:
            my_tree.insert(parent='', index='end', iid=count, text="",
                               values=(requests[0], requests[1],
                                       requests[2], requests[3],
                                       requests[4]
                                       ))

            count += 1
        my_tree.grid(row=1, column=0, columnspan=3, padx=100, pady=10)
        if select == "one":
            request_label = Label(apptlist, text="Appointments on {}".format(date_selected))
            request_label.grid(row=0, column=0, columnspan=3, pady=10)
        else:
            request_label = Label(apptlist, text="All upcoming appointments")
            request_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Allows GP to go back to calendar_function frame to select another date to view the appointments for
        tk.Button(apptlist, bg="white", text="Back", command=viewappt.tkraise).grid(row=2, column=0, pady=30,padx=40)

        def open_consultation():
            from uch_system.gp_functions.gp import GP

            selected = my_tree.selection()

            # Iterates through selected appointments
            for rec in selected:
                value = my_tree.item(rec, 'values')
                # Extract nhs_number of selected patient from table
                nhs_number = value[2]
                database = json.load(open('../uch_system/database.json'))
                for patient in database.keys():
                    # Use matching NHS-number to figure out which patient has been selected and open consultation window
                    if database[patient]["NHS_number"] == nhs_number:
                        GP.consultation_body(patient)

        def cancel():

            selected = my_tree.selection()

            # Iterates through selected appointments
            for rec in selected:
                database = json.load(open('../uch_system/database.json'))
                value = my_tree.item(rec, 'values')
                # Extract nhs_number of selected patient from table
                nhs_number = value[2]
                date_selected = value[3]
                time_selected = value[4]
                for patient in database.keys():
                    # Use matching NHS-number to figure out which patient has been selected
                    if database[patient]["NHS_number"] == nhs_number:
                        # Double check with GP whether they want to cancel this appointment
                        ans = messagebox.askyesno("Cancel appointment", "Are you sure you want to cancel "
                                                  + database[patient]["First Name"] + " "
                                                  + database[patient]["Last Name"] + "'s appointment on {} at {}"
                                                  .format(date_selected, time_selected))

                        if ans is True:
                            # Add appointment information to cancelled section of appointment database
                            if nhs_number in appointments["Cancelled"]:
                                appointments["Cancelled"][nhs_number][date_selected] = time_selected
                            else:
                                appointments["Cancelled"][nhs_number] = {date_selected: time_selected}
                            # Delete appointment from approved section of appointment database
                            del appointments["Approved"][nhs_number][date_selected]

                            # Update appointment database
                            json.dump(appointments, open('../uch_system/appointments.json', 'w'), indent=2)
                            # Call function to reload the screen without appointments just cancelled
                            listofappt(apptlist, dpicker, start, gp, viewappt, select)

        # Buttons to either open a consultation for a selected appointment or cancel it
        request_btn1 = Button(apptlist, text="Open consultation", command=open_consultation)
        request_btn2 = Button(apptlist, text="Cancel appointment", command=cancel)
        request_btn1.grid(row=2, column=1, pady=30)
        request_btn2.grid(row=2, column=2, pady=30, padx=(0, 30))

    else:
        if select == "one":
            messagebox.showinfo("Information", "No appointments on selected day!")
            viewappt.tkraise()
        else:
            messagebox.showinfo("Information", "No appointments booked!")
            viewappt.tkraise()


def gp_appointments(gp):
    """
    Central hub from which GP can choose different features that all involve appointments

    From this screen the GP can approve appointments, view appointments, set their weekly
    availability as well as book time off.

    :param gp: instance of the class GP for the current GP that is logged in

    """

    root = tk.Tk()
    root.title("GP Appointments Overview")
    root.geometry("700x400")

    # Defining frames for each feature
    start = tk.Frame(root)
    viewappt = tk.Frame(root)
    set_av = tk.Frame(root)
    aprv_app = tk.Frame(root)
    hol = tk.Frame(root)
    apptlist = tk.Frame(root)

    frames = [start, viewappt, set_av, aprv_app, hol, apptlist]

    for frame in frames:
        frame.grid(row=0, column=0, sticky='news')
        frame.configure(bg="white")
    fontStyle2 = tkFont.Font(family="Lucida Grande", size=16)
    # Creating labels for start Frame (main GP appointment portal)
    tk.Label(start, text="GP Appointment Schedule", bg="white", font=fontStyle2, fg='cyan4').grid(row=0, column=4, padx=230, pady=20)

    # Creating Buttons for start Frame (main GP appointment portal)
    tk.Button(start, bg="white",
              text="Approve Appointments", width=25, height=2,
              command=lambda: bookings_to_approve(aprv_app, gp, start)).grid(row=1, column=4, pady=10, padx=230)
    tk.Button(start, bg="white", text="View Appointments", width=25, height=2,
              command=viewappt.tkraise).grid(row=2, column=4, pady=10, padx=230)
    tk.Button(start, bg="white", text="Set availability", width=25, height=2,
              command=lambda: set_availability(set_av, gp, start)).grid(row=3, column=4, pady=10, padx=230)
    tk.Button(start, bg="white", text="Book Time Off", width=25, height=2,
              command=lambda: holiday(hol, gp)).grid(row=5, column=4, pady =10, padx=230)

    # Creates Buttons for viewappt Frame (to select a date to view appointments for) or go back to appointment portal
    tk.Button(viewappt, bg="white", text="Select Date", width=20,
              command=lambda: listofappt(apptlist, dpicker, start, gp, viewappt, select="one")).grid(row=2, column=2, pady=3)
    tk.Button(viewappt, bg="white", text="View all appointments", width=20,
              command=lambda: listofappt(apptlist, dpicker, start, gp, viewappt, select="all")).grid(row=3, column=2, pady=3)
    tk.Button(viewappt, bg="white", text="Back", command=start.tkraise, width=20).grid(row=4, column=2, pady=3)

    # Creates calendar_function for viewappt frame
    cframe = tk.Frame(viewappt, borderwidth=5, bg="white")
    cframe.grid(row=1, column=1, columnspan=3, padx=200)
    dpicker = Cal(cframe, {})

    tk.Label(viewappt, text="Choose a date", bg="white").grid(row=0, column=0, columnspan=5)

    # Creates buttons for GP to choose the start and end date for their holiday / time off
    tk.Button(hol, bg="white", text="Select start date", command=lambda:selectdate(hol,datepicker, gp, start, type="start")).grid(row=5, column=1, pady=3)
    tk.Button(hol, bg="white", text="Select end date", command=lambda:selectdate(hol, datepicker, gp, start, type="end")).grid(row=5, column=2, pady=3)
    tk.Button(hol, bg="white", text="Back", command=lambda: home(start)).grid(row=7, column=0, pady=10, padx=5)

    # Creates calendar_function for holiday frame
    calframe = tk.Frame(hol, borderwidth=5, bg="white")
    calframe.grid(row=0, column=0, columnspan=5, padx=30)
    datepicker = Cal(calframe, {})

    start.tkraise()
    root.mainloop()


def selectdate(hol, datepicker, gp, start, type):

    # Define global variables
    global s_date, start_label, e_date, end_label

    # Depending on whether the 'Select start date' or 'Select end date' button was pressed
    if type == "start":
        s_date = str(datepicker.day_select) + "/" + str(datepicker.month_select) + "/" + str(datepicker.year_select)
        # Displays the selected date as a label
        start_label = tk.Label(hol, text="  {}  ".format(s_date), bg="white")
        start_label.grid(row=6, column=1)
        s_date = start_label.cget("text").strip()

    elif type == "reset":
        s_date = ""
        e_date = ""

    elif type == "end":
        e_date = str(datepicker.day_select) + "/" + str(datepicker.month_select) + "/" + str(datepicker.year_select)
        # Displays the selected date as a label
        end_label = tk.Label(hol, text="  {}  ".format(e_date), bg="white")
        end_label.grid(row=6, column=2)
        e_date = end_label.cget("text").strip()

    def bookholiday():
        """Checks whether date is valid and saves holiday information to GP database"""

        try:
            if 'end_label' in globals():
                end_label.destroy()
            if 'start_label' in globals():
                start_label.destroy()
            # Convert string dates into a standard datetime format for comparison
            s_date_split = s_date.split("/")
            s_date_date = datetime.date(year=int(s_date_split[2]), month=int(s_date_split[1]), day=int(s_date_split[0]))
            e_date_split = e_date.split("/")
            e_date_date = datetime.date(year=int(e_date_split[2]), month=int(e_date_split[1]), day=int(e_date_split[0]))
            # Checks whether the holiday start date is after the end date and raises a warning
            if s_date_date > e_date_date:
                messagebox.showwarning("Incorrect dates", "Please ensure your start date is before your end date")
                selectdate(hol, datepicker, gp, start, type="reset")
                return None
            # Checks whether holiday start date is within 28 days of today's date
            elif datetime.date.today() + datetime.timedelta(days=28) > s_date_date:
                messagebox.showwarning("Incorrect dates", "Please ensure your start date is at least 28 days after today's date")
                selectdate(hol, datepicker, gp, start, type="reset")
                return None

            # Loads GP database, adds holiday start date and end date and then updates databases
            gp_database = json.load(open('../uch_system/gp_database.json'))
            gp_database[gp.username]["Holidays"].append([s_date, e_date, False])
            json.dump(gp_database, open('../uch_system/gp_database.json', 'w'), indent=2)
        except:

            messagebox.showwarning("Dates not selected", "Please choose both a start and end date for your time off.")
            selectdate(hol, datepicker, gp, start, type="reset")
        else:
            # Destroys labels and returns to appointment start screen
            messagebox.showinfo("Time off requested", "You have successfully requested time off between {} and {}"
                                .format(s_date,e_date))
            end_label.destroy()
            start_label.destroy()

            # start.tkraise()
            holiday_bookings(hol,gp)
            selectdate(hol, datepicker, gp, start, type="reset")

    # Button to confirm selected dates for the holiday
    tk.Button(hol, bg="white", text="Confirm dates", command=bookholiday, width=20).grid(row=7, column=1, columnspan=2, pady=3)


def initialise_current_gp(username):
    """
    Takes all GP information and creates into an instance of GP class

    :param username: this is the username of the GP that is currently logged in
    :return: gp (instance of the GP class)
    """

    gp_database = json.load(open("../uch_system/gp_database.json"))
    gp = GP(gp_database[username]["username"], gp_database[username]["First Name"],
            gp_database[username]["Last Name"],
            gp_database[username]["password"], gp_database[username]["GMC_Number"],
            gp_database[username]["assigned_patients"],
            gp_database[username]["Verified"],
            gp_database[username]["Holidays"],
            gp_database[username]["Availability"]["Lunch"],
            gp_database[username]["Availability"]["Monday Start"],
            gp_database[username]["Availability"]["Monday End"],
            gp_database[username]["Availability"]["Tuesday Start"],
            gp_database[username]["Availability"]["Tuesday End"],
            gp_database[username]["Availability"]["Wednesday Start"],
            gp_database[username]["Availability"]["Wednesday End"],
            gp_database[username]["Availability"]["Thursday Start"],
            gp_database[username]["Availability"]["Thursday End"],
            gp_database[username]["Availability"]["Friday Start"],
            gp_database[username]["Availability"]["Friday End"],
            )

    return gp

