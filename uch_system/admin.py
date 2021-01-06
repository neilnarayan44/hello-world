import json
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import font as tkFont
from calendar_function.cal import Cal
import datetime
import random



def admin_home():
    """Admin home screen

     Four options: manage patients / approve profiles / manage GPS / view calendar_function
     """

    # Setting up Tkinter window
    admin_home_screen = Tk()
    admin_home_screen.title("UCH Admin Portal")
    admin_home_screen.geometry("800x400")
    fontStyle2 = tkFont.Font(family="Lucida Grande", size=12)


    global start
    # Defining  frames
    start = Frame(admin_home_screen)
    manage_patients = Frame(admin_home_screen)
    manage_gps = Frame(admin_home_screen)
    calender_frame = Frame(admin_home_screen)
    apptlist = Frame(admin_home_screen)
    hol_frame = Frame(admin_home_screen)

    frames = [start, manage_patients, manage_gps, calender_frame, apptlist, hol_frame]

    for frame in frames:
        frame.grid(row=0, column=0, sticky='news')
        frame.configure(bg='white')

    # Title of the page
    admin_welcome = Label(start, text="""Welcome to the University College Hospital Admin Portal""",
                          font=fontStyle2, fg='cyan4')
    admin_welcome.pack(padx=200, pady=20)

    # 4 buttons which each takes user to a different function
    Button(start, text="Manage Patients", command=lambda: view_edit_patients(manage_patients), height="2",
           width="30").pack(padx=200, pady=10)
    Button(start, text="Manage GPs", command=lambda: view_edit_GPs(manage_gps), height="2",
           width="30").pack(padx=200, pady=10)
    Button(start, text="View Calendar", command=lambda: view_calendar(calender_frame, apptlist), height="2", width="30")\
        .pack(padx=200, pady=10)
    Button(start, text="Manage Holidays", command=lambda: manage_holidays(hol_frame, tab1, tab2), height="2", width="30")\
        .pack(padx=200, pady=10)

    # sets up the Request and Feedback tabs of the window
    tab_control = ttk.Notebook(hol_frame)
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="   Approved Holidays   ")
    tab_control.add(tab2, text="   Requested Holidays   ")
    tab_control.pack(expand=1, fill="both")


    def return_home():
        """Closes the admin portal"""
        admin_home_screen.destroy()

    Button(start, text="Exit", command=return_home).pack(pady=50)

    start.tkraise()
    admin_home_screen.mainloop()


def view_calendar(calendar_frame, apptlist):
    """Calendar to view appointments.

    Calendar has interactive buttons to select a date.
    Can then view appointments on selected day or click a button to view all appointments
    """

    # Creating tkinter window, defining title and size


    # viewappt allows admin to select the date


    # apptlist displays all the Accepted appointments on a given day




    Label(calendar_frame, text="Choose a date", bg="white").grid(row=0, column=0, columnspan=5)

    # Button which will display all appointments on selected day
    Button(calendar_frame, bg="white", text="Select Date",
              command=lambda: listofappt(apptlist, dpicker, calendar_frame), width=15).grid(row=2, column=1, pady=(0,3))

    # Button to display all appointments for all days
    Button(calendar_frame, bg="white", text="View all appointments",
           command=lambda: allappt(apptlist, dpicker, calendar_frame), width=15).grid(row=3, column=1, pady=3)

    Button(calendar_frame, text="Back", command=start.tkraise, width=15).grid(row=4, column=1, pady=3)

    # Defines calendar_function and displays
    cframe = Frame(calendar_frame, borderwidth=5, bg="white")
    cframe.grid(row=1, column=0, columnspan=3, padx=250)
    dpicker = Cal(cframe, {})
    calendar_frame.tkraise()


def listofappt(apptlist, dpicker, calendar_frame):
    """
    Allows the admin to view or cancel appointments on a given day

    :param apptlist: Tkinter Frame which displays all appointments on a selected date
    :param dpicker: Cal object which
    :param viewappt: Tkinter Frame which displays appointment calendar_function
    :return:
    """

    # Load databases into local dictionaries
    db = json.load(open('database.json'))
    appointments = json.load(open('appointments.json'))
    gp_database = json.load(open('gp_database.json'))

    # Retrieves the date selected from the calendar_function in the previous frame
    date_selected = str(dpicker.day_select) + "/" + str(dpicker.month_select) + "/" + str(dpicker.year_select)

    list_of_app = []

    # Iterates through each key (nhs number), value (appointment date : time) in the Approved appointments database
    for id, profile in appointments["Approved"].items():
        # Iterates through each appointment date : time pair
        for date, time in profile.items():
            # Checks if the date of the appointment in the database is the same as the selected date from calendar_function
            if date == date_selected:
                # Iterates through every patient in the patient database to check if their id matches
                # the NHS number from the appointment database
                for p in db.keys():
                    if db[p]["NHS_number"] == id:
                        gp_number = db[p]["assigned_gp"]
                        # Now that the date and NHS number match, check to see which GP this patient is assigned to
                        for a in gp_database.keys():
                            if gp_database[a]["GMC_Number"] == gp_number:
                                gp_name ="Dr " + gp_database[a]["First Name"] + " " + gp_database[a]["Last Name"]
                                # Adds all information to the list_of_app (so that it can then be displayed in table)
                                list_of_app.append([db[p]["First Name"], db[p]["Last Name"],
                                            db[p]["NHS_number"], date, time, gp_name])

    # Checks that there is at least one appointment to display
    if len(list_of_app) > 0:

        # Calling the apptlist frame
        apptlist.tkraise()

        # Title of the frame, showing which date the appointments are being shown for
        request_label = Label(apptlist, text="Appointments on {}".format(date_selected))
        request_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Define table
        my_tree = ttk.Treeview(apptlist)

        # Define columns
        my_tree['columns'] = ('First Name', 'Last Name', 'NHS Number', 'Date', 'Time', 'GP')

        # Format columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("First Name", anchor=CENTER, width=100, stretch=NO)
        my_tree.column("Last Name", anchor=CENTER, width=100)
        my_tree.column("NHS Number", anchor=W, width=100)
        my_tree.column("Date", anchor=W, width=100)
        my_tree.column("Time", anchor=W, width=100)
        my_tree.column("GP", anchor=W, width=100)

        # Create headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("First Name", text="First Name", anchor=CENTER)
        my_tree.heading("Last Name", text="Last Name", anchor=CENTER)
        my_tree.heading("NHS Number", text="NHS Number", anchor=W)
        my_tree.heading("Date", text="Date", anchor=W)
        my_tree.heading("Time", text="Time", anchor=W)
        my_tree.heading("GP", text="GP", anchor=W)

        count = 0

        # Orders the appointments by the "Time" column, from earliest to latest
        list_of_app.sort(key=lambda x: x[4])

        # Iterates through every appointment in the appointment list and adds it tto the table
        for requests in list_of_app:
            my_tree.insert(parent='', index='end', iid=count, text="",
                           values=(requests[0], requests[1],
                                   requests[2], requests[3],
                                   requests[4], requests[5]
                                   ))

            count += 1
        my_tree.grid(row=1, column=0, columnspan=2, padx=100, pady=10)
        # Back button which returns admin to calendar_function screen
        Button(apptlist, bg="white", text="Back", command=lambda: view_calendar(calendar_frame, apptlist)).grid(row=2, column=0)

        def cancel():
            """Function to allow admin to cancel any appointment"""

            selected = my_tree.selection()

            # Iterates through all selected patients from table
            for rec in selected:
                database = json.load(open('database.json'))
                value = my_tree.item(rec, 'values')
                nhs_number = value[2]
                date_selected = value[3]
                time_selected = value[4]
                # Iterates through database to find the patient with a matching NHS number to selected appointment
                for patient in database.keys():
                    if database[patient]["NHS_number"] == nhs_number:
                        # Double check admin is sure they want to cancel
                        ans = messagebox.askyesno("Cancel appointment", "Are you sure you want to cancel "
                                                  + database[patient]["First Name"] + " "
                                                  + database[patient]["Last Name"] + "'s appointment on {} at {}"
                                                  .format(date_selected, time_selected))

                        # If admin confirms, booking is deleted from "Approved" section and moved to "Cancelled"
                        if ans is True:
                            if nhs_number in appointments["Cancelled"]:
                                appointments["Cancelled"][nhs_number][date_selected] = time_selected
                            else:
                                appointments["Cancelled"][nhs_number] = {date_selected: time_selected}
                            del appointments["Approved"][nhs_number][date_selected]

                            # Updating appointment database with new changes
                            json.dump(appointments, open('appointments.json', 'w'), indent=2)

                # Calls function to reload the table with updated information
                listofappt(apptlist, dpicker, calendar_frame)

        # Button that allows admin to cancel a user's appointment by calling cancel() function
        request_btn = Button(apptlist, text="Cancel appointment", command=cancel)
        request_btn.grid(row=2, column=1, pady=10)

    # Gets triggered if len(list_of_app) == 0
    else:
        messagebox.showinfo("Information", "No appointments on selected day!")


def allappt(apptlist, dpicker, calendar_frame):
    """
    Displays every single approved appointment (for all GPs and all dates)

    :param apptlist: this is the frame where the table of appointments is displayed
    :param dpicker:
    :param viewappt: this is the frame where the calendar_function is displayed
    :return:
    """
    # Load databases into local dictionaries
    db = json.load(open('database.json'))
    appointments = json.load(open('appointments.json'))
    gp_database = json.load(open('gp_database.json'))

    date_selected = str(dpicker.day_select) + "/" + str(dpicker.month_select) + "/" + str(dpicker.year_select)

    list_of_app = []

    # Iterates through each key (nhs number), value (appointment date : time) in the Approved appointments database
    for nhs_number, profile in appointments["Approved"].items():
        # Iterates through each appointment date : time pair
        for date, time in profile.items():
            # Iterates through every patient in the patient database to check if their id matches
            # the NHS number from the appointment database
            for p in db.keys():
                if db[p]["NHS_number"] == nhs_number:
                    gp_number = db[p]["assigned_gp"]
                    # Now that the date and NHS number match, check to see which GP this patient is assigned to
                    for doctor in gp_database.keys():
                        if gp_database[doctor]["GMC_Number"] == gp_number:
                            gp_name ="Dr " + gp_database[doctor]["First Name"] + " " + gp_database[doctor]["Last Name"]
                            # Adds all information to the list_of_app (so that it can then be displayed in table)
                            list_of_app.append([db[p]["First Name"], db[p]["Last Name"],
                                            db[p]["NHS_number"], date, time, gp_name])

    for requests in list_of_app:
        # Converts date format (e.g. 1/1/2021 to 2021-01-01) to allow easier comparison of dates and sorting
        date_split = requests[3].split("/")
        date_of_app = datetime.date(year=int(date_split[2]), month=int(date_split[1]), day=int(date_split[0]))
        requests.append(date_of_app)

    # Sorts appointments in order of date
    list_of_app.sort(key=lambda x: x[6])

    today = datetime.date.today()

    remove = []
    for requests in list_of_app:

        # Checks whether appointment date is in the past (if so then skips it).
        if today > requests[6]:
            remove.append(requests)

    for i in remove:
        if i in list_of_app:
            list_of_app.remove(i)

    # Checks that there is at least one appointment to display
    if len(list_of_app) > 0:

        # Show all of patients that require approval
        apptlist.tkraise()

        request_label = Label(apptlist, text="All upcoming appointments")
        request_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Define a table that we will use to display all appointments
        my_tree = ttk.Treeview(apptlist)

        # Define columns
        my_tree['columns'] = ('First Name', 'Last Name', 'NHS Number', 'Date', 'Time', 'GP')

        # Format columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("First Name", anchor=CENTER, width=100, stretch=NO)
        my_tree.column("Last Name", anchor=CENTER, width=100)
        my_tree.column("NHS Number", anchor=W, width=100)
        my_tree.column("Date", anchor=W, width=100)
        my_tree.column("Time", anchor=W, width=100)
        my_tree.column("GP", anchor=W, width=100)

        # Create headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("First Name", text="First Name", anchor=CENTER)
        my_tree.heading("Last Name", text="Last Name", anchor=CENTER)
        my_tree.heading("NHS Number", text="NHS Number", anchor=W)
        my_tree.heading("Date", text="Date", anchor=W)
        my_tree.heading("Time", text="Time", anchor=W)
        my_tree.heading("GP", text="GP", anchor=W)

        count = 0

        for requests in list_of_app:
            my_tree.insert(parent='', index='end', iid=count, text="",
                            values=(requests[0], requests[1],
                                    requests[2], requests[3],
                                    requests[4], requests[5]
                                    ))
            my_tree.grid(row=1, column=0, columnspan=2, padx=100, pady=10)
            count += 1

        # Button to return to the calendar_function view frame
        Button(apptlist, bg="white", text="Back", command=calendar_frame.tkraise).grid(row=2, column=0)


        def cancel():
            """Function to allow admin to cancel any appointment"""
            selected = my_tree.selection()

            for rec in selected:
                database = json.load(open('database.json'))
                value = my_tree.item(rec, 'values')
                nhs_number = value[2]
                date_selected = value[3]
                time_selected = value[4]
                # Iterates through database to find the patient with a matching NHS number to selected appointment
                for patient in database.keys():
                    if database[patient]["NHS_number"] == nhs_number:
                        # Double check admin is sure they want to cancel
                        ans = messagebox.askyesno("Cancel appointment", "Are you sure you want to cancel "
                                                  + database[patient]["First Name"] + " "
                                                  + database[patient]["Last Name"] + "'s appointment on {} at {}"
                                                  .format(date_selected, time_selected))

                        # If admin confirms, booking is deleted from "Approved" section and moved to "Cancelled"
                        if ans is True:
                            if nhs_number in appointments["Cancelled"]:
                                appointments["Cancelled"][nhs_number][date_selected] = time_selected
                            else:
                                appointments["Cancelled"][nhs_number] = {date_selected: time_selected}
                            del appointments["Approved"][nhs_number][date_selected]
                            json.dump(appointments, open('appointments.json', 'w'), indent=2)
                            # Calls allappt function so that changes are reflected in the table immediately
                            allappt(apptlist, dpicker, calendar_frame)

        # Button to cancel selected appointment(s)
        request_btn = Button(apptlist, text="Cancel appointment", command=cancel)
        request_btn.grid(row=2, column=1, pady=10)

    else:
        # If there are no appointments to display, raises info box and return to calendar_function (viewappt) frame
        messagebox.showinfo("Information", "No appointments to display!")
        calendar_frame.tkraise()


def view_edit_patients(manage_patients, patient_search=0, type="n_show"):
    """Allows admin to manage patient records and account settings

    Shows admin all patients that are approved and allows
    admin to change the patient's GP, de-activate or delete the account
    """

    def search():
        global surname
        surname = surname_search.get()

        surname_exists = False
        for profile in database.keys():
            if surname.lower() == database[profile]["Last Name"].lower():
                surname = database[profile]["Last Name"]
                surname_exists = True
        if surname_exists is True:

            view_edit_patients(manage_patients, patient_search=1)

        else:
            messagebox.showwarning("Search error", "No patients found with that surname, "
                                                   "please check spelling and try again!")

    request_label = Label(manage_patients, text="Search by surname")
    request_label.grid(row=0, column=0, pady=10)

    surname_search = Entry(manage_patients)
    surname_search.grid(row=0, column=1, pady=10)
    Button(manage_patients, text="Search", command=search).grid(row=0, column=2, pady=10)



    def save_changes(assigned_GP, edit_window, username, list_of_GPs):

        # Loads GP database (patient database already saved in variable database)
        gp_database = json.load(open('gp_database.json'))
        appointments = json.load(open('appointments.json'))
        # If they have not been assigned to a GP empty value is saved for the "assigned_gp" key
        if assigned_GP.get() == "No approved GPs":
            database[username]["assigned_gp"] = ""
        elif assigned_GP.get() not in list_of_GPs:
            messagebox.showwarning("Incorrect value", "Please only select GP from drop down menu.")
            return
        elif database[username]["assigned_gp"] == assigned_GP.get()[-8:-1]:
            pass
        else:
            database[username]["assigned_gp"] = assigned_GP.get()[-8:-1]
            nhs_number = database[username]["NHS_number"]
            try:
                del appointments["Approved"][nhs_number]
            except KeyError:
                pass

        # Exception handling to ensure that the GP is one of the ones in the GP database

        # If a GP has been selected from the drop down list then the GMC_number part is saved into patient's profile

        # To reflect changes in the GP database as well, firstly the patient is removed from anywhere in GP database
        for i in gp_database.keys():
            if username in gp_database[i]["assigned_patients"]:
                gp_database[i]["assigned_patients"].remove(username)

                # However, for the correct GP the patient's username is then added to their "assigned_patients" list
            if gp_database[i]["GMC_Number"] == database[username]["assigned_gp"]:
                gp_database[i]["assigned_patients"].append(username)


        # Saving changes to patient and GP databases
        json.dump(database, open('database.json', 'w'), indent=2)
        json.dump(gp_database, open('gp_database.json', 'w'), indent=2)
        json.dump(appointments, open('appointments.json', 'w'), indent=2)

        edit_window.destroy()

        view_edit_patients(manage_patients)

    def delete_user(edit_window, username):
        """Deletes selected user from the database"""

        # Load GP database into variable gp_database
        gp_database = json.load(open('gp_database.json'))
        appointments = json.load(open('appointments.json'))

        # Check to confirm admin is certain that they want to delete the user's account
        msgbox = messagebox.askquestion('Delete User', "Are you sure you want to delete this user's profile?",
                                        icon='warning')

        if msgbox == 'yes':
            # Removes the user from their GP's list of assigned patients
            for gp in gp_database.values():
                if username in gp["assigned_patients"]:
                    gp["assigned_patients"].remove(username)

            # Then deletes the user from the patient database
            nhs_number = database[username]["NHS_number"]
            try:
                del appointments["Approved"][nhs_number]
            except KeyError:
                pass
            del database[username]


            # Save changes to patient and GP database
            json.dump(database, open('database.json', 'w'), indent=2)
            json.dump(gp_database, open('gp_database.json', 'w'), indent=2)
            json.dump(appointments, open('appointments.json', 'w'), indent=2)

            edit_window.destroy()

            view_edit_patients(manage_patients, type="show")

    def deactivate_user(edit_window, username):
        """Deactivates the user selected by admin"""

        # Check to confirm admin is certain that they want to delete the user's account
        msgbox = messagebox.askquestion('De-activate User', "Are you sure you want to de-activate this user's profile?",
                                            icon='warning')
        appointments = json.load(open('appointments.json'))
        if msgbox == 'yes':
            # Changes verified status to False
            database[username]["Verified"] = False
            # Saves changes to database
            json.dump(database, open('database.json', 'w'), indent=2)

            nhs_number = database[username]["NHS_number"]
            try:
                del appointments["Approved"][nhs_number]
            except KeyError:
                pass

            edit_window.destroy()
            json.dump(appointments, open('appointments.json', 'w'), indent=2)
            view_edit_patients(manage_patients)

    def activate_user():
        """Activates the selected GP profile(s)"""

        selected = my_tree.selection()

        print_records = ''

        # Changes Verified status for all selected GPs to True
        for rec in selected:
            value = my_tree.item(rec, 'values')
            username = value[0]
            already_true = database[username]["Verified"]
            database[username]["Verified"] = True
            print_records += str(value[0]) + "\n"

            list_of_gmc_numbers = []
            for i in gp_database.values():
                if i["Verified"] is False:
                    continue
                list_of_gmc_numbers.append(i["GMC_Number"])

            # If there are no GPs they are assigned "No Assigned GP",
            # otherwise patient is randomly allocated a new GP
            if len(list_of_gmc_numbers) == 0:
                their_gp = ""
                database[username]["assigned_gp"] = their_gp

            elif already_true is False:
                their_gp = random.choice(list_of_gmc_numbers)
                for doctor in gp_database.keys():
                    if gp_database[doctor]["GMC_Number"] == their_gp and username not in gp_database[doctor]["assigned_patients"]:
                        # Add patient to list of GP's assigned patient
                        gp_database[doctor]["assigned_patients"].append(username)
            # Add GP to the patient's assigned GP key in the dictionary
                database[username]["assigned_gp"] = their_gp
        messagebox.showinfo("REQUEST", "Your changes have been confirmed")

        # Updates GP database
        json.dump(database, open('database.json', 'w'), indent=2)
        json.dump(gp_database, open('gp_database.json', 'w'), indent=2)


        view_edit_patients(manage_patients)

    def confirm_request():
        """Displays a window with patient information

        Via this window admin can view patient information, changed assigned GP,
        de-activate or delete a patient's account
        """

        # Load GP database into variable
        gp_database = json.load(open('gp_database.json'))

        selected = my_tree.selection()

        if len(selected) == 1:
            value = my_tree.item(selected, 'values')
            username = value[0]
            edit_window = Tk()
            edit_window.title("Edit User Information")

            # Populates labels with information from patient database
            Label(edit_window, text="Username: {}".format(username)).grid(row=0, column=0, columnspan=2)
            Label(edit_window, text="First Name: {}".format(database[username]["First Name"])).grid(row=1, column=0, columnspan=2)
            Label(edit_window, text="Last Name: {}".format(database[username]["Last Name"])).grid(row=2, column=0, columnspan=2)

            gmc_number = database[username]["assigned_gp"]

            list_of_GPs = []
            # Searches for patient's GP details in the GP database
            for i in gp_database.values():
                if i["GMC_Number"] == gmc_number:
                    gp_name = i["Last Name"]
                    current_selection = "Dr " + i["First Name"] + " " + i["Last Name"] + " " + "(" + i["GMC_Number"] + ")"

                    break

            else:
                gp_name = "[No Assigned GP]"
                current_selection = 0
            Label(edit_window, text="Assigned GP: Dr {}".format(gp_name)).grid(row=4, column=0, columnspan=2)



            # Goes through GP database and adds GP details to list
            number_of_verified_GPs = 0
            for i in gp_database.values():
                if i["Verified"] is True:
                    list_of_GPs.append(
                    "Dr " + i["First Name"] + " " + i["Last Name"] + " " + "(" + i["GMC_Number"] + ")")
                    number_of_verified_GPs+=1


            if number_of_verified_GPs == 0:

                list_of_GPs = ["No approved GPs"]

            assigned_GP = ttk.Combobox(edit_window)

            assigned_GP["values"] = tuple(list_of_GPs)

            try:
                index = list_of_GPs.index(current_selection)
            except ValueError:
                index = 0

            # Displays drop down menu where the default selection is the GP the patient is already assigned to
            assigned_GP.current(index)

            Label(edit_window, text="Change GP: ").grid(row=5, column=0, padx=(70,0))
            assigned_GP.grid(row=5, column=1, padx=(0, 30))

            Label(edit_window, text="Verified: {}".format(database[username]["Verified"])).grid(row=3, column=0, columnspan=2)
            Button(edit_window, text="De-activate account?", command=lambda: deactivate_user(edit_window, username)).grid(row=6, column=0, pady=10, padx=(50,0))
            Button(edit_window, text="Delete account?", command=lambda: delete_user(edit_window, username)).grid(row=6, column=1, pady=10)

            Button(edit_window, text="Save changes",
                       command=lambda: save_changes(assigned_GP, edit_window, username, list_of_GPs), width=30).grid(row=7, column=0, columnspan=2, pady=10)

    # Load patient database
    database = json.load(open('database.json'))
    gp_database = json.load(open('gp_database.json'))

    # Checks if there are patients that have registered
    if len(database.values()) > 0 or type=="show":
        manage_patients.tkraise()

        my_tree = ttk.Treeview(manage_patients)

        # Define columns
        my_tree['columns'] = ('Username', 'First Name', 'Last Name', 'DOB', 'NHS Number','Assigned GP', 'Verified')

        # Format columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Username", anchor=CENTER, width=100, stretch=NO)
        my_tree.column("First Name", anchor=CENTER, width=100)
        my_tree.column("Last Name", anchor=CENTER, width=100)
        my_tree.column("DOB", anchor=CENTER, width=100)
        my_tree.column("NHS Number", anchor=CENTER, width=100)
        my_tree.column("Assigned GP", anchor=CENTER, width=150)
        my_tree.column("Verified", anchor=CENTER, width=80)

        # Create headings
        my_tree.heading("#0", text="", anchor=CENTER)
        my_tree.heading("Username", text="Username", anchor=CENTER)
        my_tree.heading("First Name", text="First Name", anchor=CENTER)
        my_tree.heading("Last Name", text="Last Name", anchor=CENTER)
        my_tree.heading("NHS Number", text="NHS Number", anchor=CENTER)
        my_tree.heading("DOB", text="DOB", anchor=CENTER)
        my_tree.heading("Assigned GP", text="Assigned GP", anchor=CENTER)
        my_tree.heading("Verified", text="Verified", anchor=CENTER)

        count = 0
        # Iterates through patients in database and if they are verified, adds them to table
        print(patient_search)
        if patient_search == 1:
            for recs in database.values():
                    for i in gp_database.values():
                        try:
                            if recs['Last Name'] == surname and i["GMC_Number"] == recs["assigned_gp"]:
                                gp_name = "Dr " + i["First Name"] + " " + i["Last Name"]
                                my_tree.insert(parent='', index='end', iid=count, text="",
                                                   values=(recs['username'], recs['First Name'],
                                                           recs['Last Name'], recs['DOB'],
                                                           recs['NHS_number'], gp_name, recs['Verified'],
                                                           ))
                                count += 1
                                break
                        except:
                            pass
                    else:
                        if recs['Last Name'] == surname:
                            gp_name = "No Assigned GP"
                            my_tree.insert(parent='', index='end', iid=count, text="",
                                           values=(recs['username'], recs['First Name'],
                                                   recs['Last Name'], recs['DOB'],
                                                   recs['NHS_number'], gp_name, recs['Verified'],
                                                   ))
                            count+=1
        else:
            for recs in database.values():
                    for i in gp_database.values():
                        if i["GMC_Number"] == recs["assigned_gp"]:
                            gp_name = "Dr " + i["First Name"] + " " + i["Last Name"]
                            my_tree.insert(parent='', index='end', iid=count, text="",
                                           values=(recs['username'], recs['First Name'],
                                                   recs['Last Name'], recs['DOB'],
                                                   recs['NHS_number'], gp_name, recs['Verified'],
                                                   ))
                            count += 1
                            break
                    else:
                        gp_name = "No Assigned GP"
                        my_tree.insert(parent='', index='end', iid=count, text="",
                                       values=(recs['username'], recs['First Name'],
                                               recs['Last Name'], recs['DOB'],
                                               recs['NHS_number'], gp_name, recs['Verified'],
                                               ))
                        count+=1

        my_tree.grid(row=1, column=0, columnspan=3, padx=20, pady=20)
        Button(manage_patients, text="Back", command=start.tkraise, width=10).grid(row=2, column=0, pady=20)

        request_btn = Button(manage_patients, text="Edit Patient Profile", command=confirm_request)
        request_btn.grid(row=2, column=1, pady=20)

        request_btn = Button(manage_patients, text="Approve Patient(s)", command=activate_user)
        request_btn.grid(row=2, column=2, pady=20)

        # manage_patients.mainloop()
    else:
        # If there are no patients that are approved
        messagebox.showinfo("Information", "No patients have registered.")


def view_edit_GPs(manage_gps, type="n_show"):

    """Allows admin to view, activate, de-activate or delete GP profiles"""

    def activate_user():
        """Activates the selected GP profile(s)"""

        selected = my_tree.selection()

        print_records = ''

        # Changes Verified status for all selected GPs to True
        for rec in selected:
            value = my_tree.item(rec, 'values')
            username = value[0]
            gp_database[username]["Verified"] = True
            print_records += str(value[0]) + "\n"



        # Updates GP database
        json.dump(gp_database, open('gp_database.json', 'w'), indent=2)
        messagebox.showinfo("REQUEST", "Your changes have been confirmed")

        view_edit_GPs(manage_gps)

    def delete_user():
        """Deletes the GP that has been selected by the admin"""

        selected = my_tree.selection()

        # Defines and populates usernames list with username of all selected GPs
        usernames = []
        for rec in selected:
            value = my_tree.item(rec, 'values')
            usernames.append(value[0])

        # Confirm whether admin is sure they want to permanently delete the GP profile(s)
        msgbox = messagebox.askquestion('Delete User', "Are you sure you want to delete this GP's profile?",
                                        icon='warning')

        if msgbox == 'yes':
            # Load patient and GP database
            database = json.load(open('database.json'))
            gp_database = json.load(open('gp_database.json'))
            for user in usernames:
                # Retrieve GMC number of selected GP(s) before deleting their profiles and updating database
                gmc_number = gp_database[user]["GMC_Number"]
                del gp_database[user]
                json.dump(gp_database, open('gp_database.json', 'w'), indent=2)
                # Checks if any patients were assigned to that GMC using the GMC number
                for patient in database.keys():
                    if database[patient]["assigned_gp"] == gmc_number:
                        nhs_number = database[patient]["NHS_number"]
                        appointments = json.load(open('appointments.json'))
                        for account in appointments["Approved"].keys():
                            if account == nhs_number:

                                for date, time in appointments["Approved"][nhs_number].items():
                                    if nhs_number in appointments["Cancelled"]:
                                        appointments["Cancelled"][nhs_number][date] = time
                                    else:
                                        appointments["Cancelled"][nhs_number] = {date: time}
                        # Delete appointment from approved section of appointment database
                        try:
                            del appointments["Approved"][nhs_number]
                        except KeyError:
                            pass

                        json.dump(appointments, open('appointments.json', 'w'), indent=2)
                        # Append all remaining GMC Numbers to list
                        list_of_gmc_numbers = []
                        for i in gp_database.values():
                            if i["Verified"] is False:
                                continue
                            list_of_gmc_numbers.append(i["GMC_Number"])

                            # If there are no GPs they are assigned "No Assigned GP",
                            # otherwise patient is randomly allocated a new GP
                        if len(list_of_gmc_numbers) == 0:
                            their_gp = ""
                        else:
                            their_gp = random.choice(list_of_gmc_numbers)
                            for doctor in gp_database.keys():
                                if gp_database[doctor]["GMC_Number"] == their_gp:
                                    # Add patient to list of GP's assigned patient
                                    gp_database[doctor]["assigned_patients"].append(patient)
                        # Add GP to the patient's assigned GP key in the dictionary
                        database[patient]["assigned_gp"] = their_gp

                # Update GP and patient databases
                json.dump(gp_database, open('gp_database.json', 'w'), indent=2)
                json.dump(database, open('database.json', 'w'), indent=2)

            view_edit_GPs(manage_gps, type="show")

    def deactivate_user():
        """Function to allow admin to deactivate selected GP(s)"""

        selected = my_tree.selection()
        usernames = []

        # Saves all of the selected usernames into a list
        for rec in selected:
            value = my_tree.item(rec, 'values')
            usernames.append(value[0])

        # Checks whether admin is sure they want to deactivate the selected GP profile(s)
        msgbox = messagebox.askquestion('De-activate User', "Are you sure you want to de-activate this GP's profile?",
                                            icon='warning')
        if msgbox == 'yes':
            # Load patient and GP database
            database = json.load(open('database.json'))
            gp_database = json.load(open('gp_database.json'))
            for user in usernames:
                # Changes verification status to False and updates the GP database
                gmc_number = gp_database[user]["GMC_Number"]
                gp_database[user]["assigned_patients"] = []
                gp_database[user]["Verified"] = False
                json.dump(gp_database, open('gp_database.json', 'w'), indent=2)
                for patient in database.keys():
                    if database[patient]["assigned_gp"] == gmc_number:

                        nhs_number = database[patient]["NHS_number"]
                        appointments = json.load(open('appointments.json'))
                        for account in appointments["Approved"].keys():
                            if account == nhs_number:

                                for date, time in appointments["Approved"][nhs_number].items():
                                    if nhs_number in appointments["Cancelled"]:
                                        appointments["Cancelled"][nhs_number][date] = time
                                    else:
                                        appointments["Cancelled"][nhs_number] = {date: time}
                        # Delete appointment from approved section of appointment database
                        try:
                            del appointments["Approved"][nhs_number]
                        except Exception:
                            pass

                        json.dump(appointments, open('appointments.json', 'w'), indent=2)
                        list_of_gmc_numbers = []
                        for i in gp_database.values():
                            if i["Verified"] == True:
                                # Append all remaining GMC Numbers to list
                                list_of_gmc_numbers.append(i["GMC_Number"])
                            # If there are no GPs they are assigned "No Assigned GP",
                            # otherwise patient is randomly allocated a new GP
                        if len(list_of_gmc_numbers) == 0:
                            their_gp = ""
                        else:
                            their_gp = random.choice(list_of_gmc_numbers)
                        for doctor in gp_database.keys():
                            if gp_database[doctor]["GMC_Number"] == their_gp:
                                # Add patient to list of GP's assigned patient
                                gp_database[doctor]["assigned_patients"].append(patient)
                        # Add GP to the patient's assigned GP key in the dictionary
                        database[patient]["assigned_gp"] = their_gp

                        # Update GP and patient databases
                        json.dump(gp_database, open('gp_database.json', 'w'), indent=2)
                        json.dump(database, open('database.json', 'w'), indent=2)

            view_edit_GPs(manage_gps)

    # Loads the GP database
    gp_database = json.load(open('gp_database.json'))

    # Checks if there are any GPs in database
    if len(gp_database.values()) > 0 or type == "show":

        fontStyle2 = tkFont.Font(family="Lucida Grande", size=16)
        admin_welcome = Label(manage_gps, text="Manage GPs",
                              font=fontStyle2, fg='cyan4')
        admin_welcome.grid(row=0, column=0, columnspan=4, pady=10)

        my_tree = ttk.Treeview(manage_gps)

        # Define columns
        my_tree['columns'] = ('Username', 'First Name', 'Last Name', 'GMC Number', 'Verified')

        # Format columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Username", anchor=CENTER, width=120, stretch=NO)
        my_tree.column("First Name", anchor=CENTER, width=120)
        my_tree.column("Last Name", anchor=CENTER, width=120)
        my_tree.column("GMC Number", anchor=CENTER, width=120)
        my_tree.column("Verified", anchor=CENTER, width=120)

        # Create headings
        my_tree.heading("#0", text="", anchor=CENTER)
        my_tree.heading("Username", text="Username", anchor=CENTER)
        my_tree.heading("First Name", text="First Name", anchor=CENTER)
        my_tree.heading("Last Name", text="Last Name", anchor=CENTER)
        my_tree.heading("GMC Number", text="GMC Number", anchor=CENTER)
        my_tree.heading("Verified", text="Verified", anchor=CENTER)

        count = 0

        # Adds each GP from database to the table to display to the admin
        for recs in gp_database.values():
            my_tree.insert(parent='', index='end', iid=count, text="",
                               values=(recs['username'], recs['First Name'],
                                       recs['Last Name'], recs['GMC_Number'], recs['Verified'],
                                       ))

            count += 1

        my_tree.grid(row=1, column=0, columnspan=4, padx=100, pady=(10,40))

        # Three buttons to allow admin to activate, deactivate and delete a GP account respectively
        request_btn = Button(manage_gps, text="Activate GP", command=activate_user)
        request_btn.grid(row=2, column=1)

        request_btn = Button(manage_gps, text="Deactivate GP", command=deactivate_user)
        request_btn.grid(row=2, column=2)

        request_btn = Button(manage_gps, text="Delete GP", command=delete_user)
        request_btn.grid(row=2, column=3)

        Button(manage_gps, text="Back", command=start.tkraise).grid(row=2, column=0, padx=(30,0))

        manage_gps.tkraise()

    else:
        messagebox.showinfo("Information", "No GPs have registered.")

def manage_holidays(hol_frame, tab1, tab2):

    def reject_holiday():

        selected = requests.selection()

        print_records = ''

        # Changes Verified status for all selected GPs to True
        for rec in selected:
            value = requests.item(rec, 'values')
            username = value[0]
            index = -1

            for i in gp_database[username]["Holidays"]:
                index += 1

                if i[0] == value[4] and i[1] == value[5]:

                    gp_database[username]["Holidays"].pop(index)

                print_records += str(value[0]) + "\n"

        # Updates GP database
        json.dump(gp_database, open('gp_database.json', 'w'), indent=2)
        messagebox.showinfo("REQUEST", "Your changes have been confirmed")

        manage_holidays(hol_frame, tab1, tab2)

    def approve_holiday():

        selected = requests.selection()

        print_records = ''

        # Changes Verified status for all selected GPs to True
        for rec in selected:
            value = requests.item(rec, 'values')
            username = value[0]
            index = -1
            for i in gp_database[username]["Holidays"]:
                index += 1
                if i[0] == value[4] and i[1] == value[5]:

                    gp_database[username]["Holidays"][index][2] = True

                print_records += str(value[0]) + "\n"

        # Updates GP database
        json.dump(gp_database, open('gp_database.json', 'w'), indent=2)
        messagebox.showinfo("REQUEST", "Your changes have been confirmed")

        manage_holidays(hol_frame, tab1, tab2)





    gp_database = json.load(open('gp_database.json'))



    my_tree = ttk.Treeview(tab1)

    # Define columns
    my_tree['columns'] = ('Username', 'First Name', 'Last Name', 'GMC Number', 'Start Date', 'End Date')

    # Format columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Username", anchor=W, width=100)
    my_tree.column("First Name", anchor=CENTER, width=100, stretch=NO)
    my_tree.column("Last Name", anchor=CENTER, width=100, stretch=NO)
    my_tree.column("GMC Number", anchor=CENTER, width=100, stretch=NO)
    my_tree.column("Start Date", anchor=CENTER, width=100, stretch=NO)
    my_tree.column("End Date", anchor=CENTER, width=100)


    # Create headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Username", text="Username", anchor=W)
    my_tree.heading("First Name", text="First Name", anchor=CENTER)
    my_tree.heading("Last Name", text="Last Name", anchor=CENTER)
    my_tree.heading("GMC Number", text="GMC Number", anchor=CENTER)
    my_tree.heading("Start Date", text="Start Date", anchor=CENTER)
    my_tree.heading("End Date", text="End Date", anchor=CENTER)


    requests = ttk.Treeview(tab2)
    # Define columns
    requests['columns'] = ('Username', 'First Name', 'Last Name', 'GMC Number', 'Start Date', 'End Date')

    # Format columns
    requests.column("#0", width=0, stretch=NO)
    requests.column("Username", anchor=W, width=100)
    requests.column("First Name", anchor=CENTER, width=100, stretch=NO)
    requests.column("Last Name", anchor=CENTER, width=100, stretch=NO)
    requests.column("GMC Number", anchor=CENTER, width=100, stretch=NO)
    requests.column("Start Date", anchor=CENTER, width=100, stretch=NO)
    requests.column("End Date", anchor=CENTER, width=100)


    # Create headings
    requests.heading("#0", text="", anchor=W)
    requests.heading("Username", text="Username", anchor=W)
    requests.heading("First Name", text="First Name", anchor=CENTER)
    requests.heading("Last Name", text="Last Name", anchor=CENTER)
    requests.heading("GMC Number", text="GMC Number", anchor=CENTER)
    requests.heading("Start Date", text="Start Date", anchor=CENTER)
    requests.heading("End Date", text="End Date", anchor=CENTER)


    count_1 = 0
    count_2 = 0

    for profile in gp_database.values():
        for holiday in profile["Holidays"]:
            if holiday[2]:
                my_tree.insert(parent='', index='end', iid=count_1, text="", values=(
                                                                                   profile["username"],
                                                                                   profile["First Name"],
                                                                                   profile["Last Name"],
                                                                                   profile["GMC_Number"],
                                                                                   holiday[0], holiday[1],
                                                                                   ))
                count_1 += 1
            else:
                requests.insert(parent='', index='end', iid=count_2, text="", values=(
                                                                                   profile["username"],
                                                                                   profile["First Name"],
                                                                                   profile["Last Name"],
                                                                                   profile["GMC_Number"],
                                                                                   holiday[0], holiday[1],
                                                                                   ))
                count_2 += 1


    my_tree.grid(row=0, column=0, columnspan=3, padx=70, pady=10)
    requests.grid(row=0, column=0, columnspan=3, padx=70, pady=10)
    Button(tab2, text="Reject holiday request", command=reject_holiday).grid(row=6, column=2, pady=10)
    Button(tab2, text="Approve holiday request", command=approve_holiday).grid(row=6, column=1, pady=10)
    Button(tab1, text="Back", command=start.tkraise, width=15).grid(row=7, column=0,columnspan=3, pady=10)
    Button(tab2, text="Back", command=start.tkraise, width=15).grid(row=6, column=0, pady=10)

    hol_frame.tkraise()
