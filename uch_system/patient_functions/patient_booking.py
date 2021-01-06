import tkinter as tk
from tkinter import messagebox, ttk, NO, CENTER, W
from uch_system.calendar_function.cal import Cal
import json
from datetime import timedelta, datetime, date
import calendar

def bookappt(bookappointment, datepicker, start, patient):
    """
    Allows user to check appointment times for a certain day and only allows for booking of available days

    :param bookappointment: Booking screen frame
    :param datepicker:
    :param start: Home screen frame
    :param patient: Instance of the Patient class with details of the currrent patient's profile
    """
    if patient.assigned_gp == "":
        messagebox.showwarning("No GP", "You can not book appointments until you have been assigned to a GP. "
                            "Please contact system admin for any queries")
        return None
    bookappointment.tkraise()

    def check_times():
        """Function to check that patient appointment is valid

        Checks that patient has selected a date within the next 28 days, not on the weekend, GP is not on holiday etc"""

        # Load appointment and GP database
        appointments = json.load(open('../uch_system/appointments.json'))
        gp_database = json.load(open("../uch_system/gp_database.json"))

        # Saves date selected into the format D/M/YYYY
        date_selected = str(datepicker.day_select) + "/" + str(datepicker.month_select) + "/" + str(datepicker.year_select)

        # Check what day of the week the selected date falls on
        check_weekday = date(year=datepicker.year_select, month=datepicker.month_select, day=datepicker.day_select).weekday()
        selected_weekday = calendar.day_name[check_weekday]

        # Iterates through GP database to retrieve the username of the patient's GP
        for doctor in gp_database.keys():
            if gp_database[doctor]["GMC_Number"] == patient.assigned_gp:
                gp_username = doctor

        # Raises warning if patient has attempted to book on the weekend
        if selected_weekday == "Saturday" or selected_weekday == "Sunday":
            messagebox.showwarning("Weekend booking", "This GP surgery is closed on weekends. If you need to be seen "
                                                      "urgently please visit your nearest A&E ")
            return

        # Using make_date function to easily convert D/M/YYYY format to YYYY-MM-DD to enable easy comparison of dates
        date_chosen = make_date(date_selected)

        # Check whether selected appointment is within next 28 days
        if date.today() + timedelta(days=28) < date_chosen:
            messagebox.showwarning("Warning", "Can't book more than 28 days in advance. Please try an earlier date")
            return

        # Checks whether GP has any holidays
        for i in range(len(gp_database[gp_username]["Holidays"])):
            holiday_start = gp_database[gp_username]["Holidays"][i][0]
            holiday_start = make_date(holiday_start)
            holiday_end = gp_database[gp_username]["Holidays"][i][1]
            holiday_end = make_date(holiday_end)

            # Raises warning if the patient is attempting to book a date that falls within a GPs holiday
            if holiday_start <= date_chosen <= holiday_end:
                messagebox.showwarning("Unavailable", "The GP will not be available between {} and {}. Please"
                                                      " book an alternative time.".format(holiday_start, holiday_end))
                return

        # Defining consultation duration to be 10 minutes and start time to be 9am (date info is irrelevant)
        consultation_duration = timedelta(minutes=10)
        app_time = datetime(year=2000, month=1, day=1, hour=9, minute=0)

        # Load patient database
        db = json.load(open('../uch_system/database.json'))

        appointment_times = []

        # Adds every appointment slot between 09:00 and 16:50 list of appointment_times
        for i in range(48):
            appointment_times.append(app_time.strftime("%H:%M"))
            app_time += consultation_duration

        # Defines a list of times that are not available which will soon be populated e.g. if someone has already booked
        not_available = []

        # Iterates through every approved appointment
        for nhs_number, profile in appointments["Approved"].items():
            # Checks if date in appointment matches selected date
            if date_selected in profile.keys():
                for user_profile in db.values():
                    # Checks if the user being looked at in the patient database matches with appointment database
                    # And checks whether they assigned to the same GP as the patient of interest
                    if user_profile["NHS_number"] == nhs_number and user_profile["assigned_gp"] == patient.assigned_gp:
                        # This indicates another patient with the same GP has booked appointment for same day
                        # Add the time of that appointment to the "not avaialable" list
                        not_available.append(profile[date_selected])

        # Same as before for list of appointments in the "Requested" list
        for nhs_number, profile in appointments["Requested"].items():
            if date_selected in profile.keys():
                for user_profile in db.values():
                    if user_profile["NHS_number"] == nhs_number and user_profile["assigned_gp"] == patient.assigned_gp:
                        not_available.append(profile[date_selected])

        # Save start and end of the GPs shift for that particular weekday
        start_time = gp_database[gp_username]["Availability"][selected_weekday + " Start"]
        end_time = gp_database[gp_username]["Availability"][selected_weekday + " End"]

        # Checks whether any of the appointment times fall outside of the doctor's shift times on that weekday
        for i in appointment_times:
            if i < start_time:
                not_available.append(i)
            elif i > end_time:
                not_available.append(i)
            elif i[:2] == gp_database[gp_username]["Availability"]["Lunch"][:2]:
                not_available.append(i)

        # Removes all of the unavailable appointments from the appointment_times list
        for i in not_available:
            if i in appointment_times:
                appointment_times.remove(i)

        # Creates drop down box with only the available appointments
        time_options = ttk.Combobox(bookappointment)
        time_options["values"] = tuple(appointment_times)

        # Ensures there is at least one appointment time available otherwuse raise warning
        try:
            time_options.current(0)
        except:
            messagebox.showwarning("No appointments available", "Unfortunately there are no more bookings available "
                                                                "on this day - please select another date from the "
                                                                "Calendar and try again. ")
            return None

        time_options.grid(row=3, column=2)

        # Button to book the selected appointment date and time
        tk.Button(bookappointment, bg='white', text="Book Appointment",
                  command=lambda: makeappt(datepicker, time_options, start, patient, gp_username), width=20).grid(row=6, column=2, pady=5)

    # Button to update drop down list with only the available times for the selected day
    tk.Button(bookappointment, bg='white', text="Click to show available times",
              command=check_times).grid(row=5, column=2, pady=10)


def manage_appointments(appview, start, patient):
    """Allows patient to view and manage all their appointments """

    def remove_app():
        """Removes selected appointment from database"""
        selected = my_tree.selection()

        for rec in selected:
            value = my_tree.item(rec, 'values')
            nhs_number = patient.nhs_number
            date_selected = value[0]
            status = value[2]
            # Removes appointment from appointment database
            del appointments[status][nhs_number][date_selected]
            #  Updates changes to appointment database
            json.dump(appointments, open('../uch_system/appointments.json', 'w'), indent=2)
            manage_appointments(appview, start, patient)

        messagebox.showinfo("REQUEST", "Your changes have been confirmed")

    # Loads appointment database
    appointments = json.load(open('../uch_system/appointments.json'))

    list_of_app = []

    # Iterates through appointment database (Approved, Requested and Cancelled) and adds all appointment to list_of_app

    if patient.nhs_number in appointments["Approved"]:
        for key, value in appointments["Approved"][patient.nhs_number].items():
            list_of_app.append([key, value, "Approved"])

    if patient.nhs_number in appointments["Requested"]:
        for key, value in appointments["Requested"][patient.nhs_number].items():
            list_of_app.append([key, value, "Requested"])

    if patient.nhs_number in appointments["Cancelled"]:
        for key, value in appointments["Cancelled"][patient.nhs_number].items():
            list_of_app.append([key, value, "Cancelled"])

    # Show all of patients that require approval
    if len(list_of_app) > 0:

        appview.tkraise()

        # tk.Button(appview, bg="white", text="Back", command=lambda: home(start)).grid(row=5, column=1)
        my_tree = ttk.Treeview(appview)

        # Define columns
        my_tree['columns'] = ('Date', 'Time', 'Status')

        # Format columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Date", anchor=CENTER, width=100, stretch=NO)
        my_tree.column("Time", anchor=CENTER, width=100)
        my_tree.column("Status", anchor=W, width=130)

        # Create headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("Date", text="Date", anchor=CENTER)
        my_tree.heading("Time", text="Time", anchor=CENTER)
        my_tree.heading("Status", text="Status", anchor=W)

        count = 0

        # Add appointment data from list into table
        for requests in list_of_app:
            my_tree.insert(parent='', index='end', iid=count, text="",
                           values=(requests[0], requests[1],
                                   requests[2])
                           )
            my_tree.grid(row=3, column=2, columnspan=2, padx=20, pady=10)
            count += 1

        # Button which removes the selected appointment from the database
        request_btn = tk.Button(appview, text="Remove booking", command=remove_app)
        request_btn.grid(row=6, column=3, pady=10)

    else:
        messagebox.showinfo("Information", "No appointments booked!")
        start.tkraise()


def makeappt(datepicker, time_options, start, patient, gp_username):
    """
    Allows patient to book an appointment with their GP

    :param datepicker:
    :param time_options:
    :param start:
    :param patient:
    :param gp_username:
    :return:
    """
    date_datetime = date(year=datepicker.year_select, month=datepicker.month_select, day=datepicker.day_select)

    # Check which day of the week the selected appointment is for
    selected_weekday = calendar.day_name[date_datetime.weekday()]

    # Load GP, patient and appointment database
    gp_database = json.load(open('../uch_system/gp_database.json'))
    db = json.load(open('../uch_system/database.json'))
    appointments = json.load(open('../uch_system/appointments.json'))

    # Warning message if patient has selected a weekend
    if selected_weekday == "Saturday" or selected_weekday == "Sunday":
        messagebox.showwarning("Weekend booking", "This GP surgery is closed on weekends. If you need to be seen "
                                                  "urgently please visit your nearest A&E ")
        return None

    # Saves start and end times for GP's shift on day of selected appointment
    start_time = gp_database[gp_username]["Availability"][selected_weekday + " Start"]
    end_time = gp_database[gp_username]["Availability"][selected_weekday + " End"]
    appt_date = str(datepicker.day_select) + "/" + str(datepicker.month_select) + "/" + str(datepicker.year_select)
    appt_time = time_options.get()

    # Check to make sure the selected appointment time isn't blank
    if appt_time == "":
        messagebox.showwarning("No time selected",
                               "Please select a time from the drop down list. If all appointments are taken "
                               "please try a different date from calendar_function. ")
        return None

    # Check if selected appointment time is before the GP's shift start time or after GP's end time

    if appt_time < start_time or appt_time > end_time \
            or appt_time[:2] == gp_database[gp_username]["Availability"]["Lunch"][:2]:
        messagebox.showwarning("Warning!", "This appointment slot is not available. Please click the 'Click to show "
                                           "available times' button to view availability.")
        return None

        # Checks whether GP has any holidays
    for i in range(len(gp_database[gp_username]["Holidays"])):
        holiday_start = gp_database[gp_username]["Holidays"][i][0]
        holiday_start = make_date(holiday_start)
        holiday_end = gp_database[gp_username]["Holidays"][i][1]
        holiday_end = make_date(holiday_end)
        check_selected = make_date(appt_date)

        # Raises warning if the patient is attempting to book a date that falls within a GPs holiday
        if holiday_start <= check_selected <= holiday_end:
            messagebox.showwarning("Unavailable", "The GP will not be available between {} and {}. Please"
                                                  " book an alternative time.".format(holiday_start, holiday_end))
            return

    today = datetime.now()

    try:
        # Save the selected appointment date and time as a datetime instance to allow for easy comparison
        split_date = appt_date.split("/")
        split_time = appt_time.split(":")
        appt_datetime = datetime(year=int(split_date[2]), month=int(split_date[1]), day=int(split_date[0]),
                                 hour=int(split_time[0]), minute=int(split_time[1]))
    except:
        messagebox.showwarning("Error", "Please ensure you have selected a valid time from the drop down options")
        return None

    # Checks whether the appointment has already happened
    if appt_datetime < today:
        messagebox.showwarning("Warning!", "This appointment slot has already happened, please select a date "
                                           "in the future and try again.")
        return None

    if today + timedelta(days=28) < appt_datetime:
        messagebox.showwarning("Warning", "Can't book more than 28 days in advance. Please try an earlier date")
        return
    # Iterate through the each patient's profile in the approved appointment database
    for nhs_number, profile in appointments["Approved"].items():
        # Checks whether the patient has an appointment on the selected date
        if appt_date in profile.keys():
            # Checks whether the appointment time is also at the selected time
            if profile[appt_date] == appt_time:
                # Iterates through the patient database to check whether this patient has the same assigned GP
                for user_profile in db.values():
                    if user_profile["NHS_number"] == nhs_number and user_profile["assigned_gp"] == patient.assigned_gp:
                        messagebox.showinfo("Warning!", "This appointment slot has been taken, "
                                                        "please pick an alternative")
                        return None

    # Repeat same process for any appointments that are in the requested appointment database
    for nhs_number, profile in appointments["Requested"].items():
        if appt_date in profile.keys():
            if profile[appt_date] == appt_time:
                for user_profile in db.values():
                    if user_profile["NHS_number"] == nhs_number and user_profile["assigned_gp"] == patient.assigned_gp:
                        messagebox.showinfo("Warning!", "This appointment slot has been taken, "
                                                        "please pick an alternative")
                        return None

    # If patient has already made a booking before, a new key is made with the selected date.
    # The selected time is saved as the value
    if patient.nhs_number in appointments["Requested"]:
        appointments["Requested"][patient.nhs_number][appt_date] = appt_time
        json.dump(appointments, open('../uch_system/appointments.json', 'w'))  # Save changes
        messagebox.showinfo("Appointment Requested!", "You have successfully requested an appointment on {} at {}."
                                                      " Your GP will review this within 24 hours.\n You can check "
                                                      "the status via the 'View appointments tab'."
                            .format(appt_date, appt_time))
        start.tkraise()

    # If patient has never requested a booking before a dictionary is created for their appointments
    # and the selected data and time are added as a key, value pair.
    else:
        appointments["Requested"][patient.nhs_number] = {}
        appointments["Requested"][patient.nhs_number][appt_date] = appt_time
        json.dump(appointments, open('../uch_system/appointments.json', 'w'))  # Save changes
        messagebox.showinfo("Appointment Requested!", "You have successfully requested an appointment on {} at {}."
                                                      " Your GP will review this within 24 hours.\n You can check "
                                                      "the status via the 'View appointments tab'."
                            .format(appt_date, appt_time))
        start.tkraise()


def booking_system(patient):
    """Main screen from which patients can select to view all their appointments or make a new booking"""
    root = tk.Tk()
    root.title("Book an appointment")

    # Defining  frames
    start = tk.Frame(root)
    appview = tk.Frame(root)
    bookappointment = tk.Frame(root)

    frames = [start, appview, bookappointment]

    for frame in frames:
        frame.grid(row=0, column=0, sticky='news')
        frame.configure(bg='white')

    # Creating labels and buttons for the main patient appointment booking system home screen
    tk.Label(start, text="Patient Appointment Booking System", bg='white').place(relx=0.5, rely=0.2,anchor=CENTER)

    tk.Button(start, bg='white', text="View Appointments",
              command= lambda: manage_appointments(appview, start, patient)).place(relx=0.5, rely=0.4,anchor=CENTER)
    tk.Button(start, bg="white", text="Appointment Booking",
              command=lambda: bookappt(bookappointment, datepicker, start, patient)).place(relx=0.5, rely=0.6,
                                                                                           anchor=CENTER)

    # Label and button for the screen in which patients can view their upcoming appointments
    tk.Label(appview, text="Upcoming Appointments:", bg="white").grid(row=0, column=1, columnspan=5)
    tk.Button(appview, bg="white", text="Back", command=start.tkraise).grid(row=6, column=2)

    # Labels and button for the screen where patients can select date and time for their appointment
    tk.Label(bookappointment, text="Select a date:", bg='white').grid(row=1, column=1, columnspan=5)
    tk.Label(bookappointment, text="Select a time:", bg='white').grid(row=3, column=1, padx=10)
    tk.Button(bookappointment, bg='white', text="Back", command=start.tkraise).grid(row=5, column=1, pady=10)

    # Calendar for the patient booking screen
    calframe = tk.Frame(bookappointment, borderwidth=5, bg='white')
    calframe.grid(row=2, column=1, columnspan=5, padx=30)
    datepicker = Cal(calframe, {})

    # Set length of consultation time (10 minutes)
    consultation_duration = timedelta(minutes=10)

    # Initial datetime instance set as 09:00
    app_time = datetime(year=2000, month=1, day=1, hour=9, minute=0)

    appointment_times = []

    # 10 minutes repeatedly added on to create all the appointment times. Each time saved to list.
    for i in range(48):
        appointment_times.append(app_time.strftime("%H:%M"))
        app_time += consultation_duration

    # Drop down box created for the book appointment frame which displays all possible appointment times.
    time_options = ttk.Combobox(bookappointment)
    time_options["values"] = tuple(appointment_times)
    time_options.current(0)
    time_options.grid(row=3, column=2)

    start.tkraise()
    root.mainloop()


def make_date(date_to_convert):
    """Converts date in D/M/YYYY to datetime instance with standard YYYY-MM-DD formatting to allow easier comparisons"""
    date_split = date_to_convert.split("/")
    f_date = date(year=int(date_split[2]), month=int(date_split[1]), day=int(date_split[0]))
    return f_date






