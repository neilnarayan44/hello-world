"""GP Prescriptions
This script allows the user (a GP) to view, add, update and remove prescriptions for a specific patient.
It is assumed that the NHS number of the patient is already known. This file can also be imported as a module.
"""

# Standard library imports
import logging
import json
from tkinter import END, Label, Tk, Frame, Button, Entry, NO, CENTER, W, ttk, messagebox
import datetime
from random import randint
import re

# Local application imports
from uch_system.calendar_function.cal import Cal

# Create and configure logger
logging.basicConfig(filename='../uch_system/newfile.log',
                    format='%(asctime)s %(message)s',
                    filemode='a'
                    )

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


def remove(username):
    """Remove a patient's medication from the database.
    :raises IndexError: if no medication is selected before removing
    """
    if len(my_tree.selection()) > 1:
        messagebox.showwarning("Multiple prescriptions selected", "Please select only one prescription to delete at a time")
        return None
    try:
        select = my_tree.selection()[0]
        value = my_tree.item(select, 'value')
    except IndexError:
        # Exception handling to make sure user selects a drug before removing
        select_something = Label(meds, text='Please select a drug to remove')
        select_something.grid(row=13, column=2)
    else:
        # Open the patient database
        with open('../uch_system/database.json') as file:
            database = json.load(file)
            for entry in database[username]['prescriptions']:
                if value[0] == entry['uid']:
                    # If the ids of the selected medication match, remove the prescription from the database
                    database[username]['prescriptions'].remove(entry)
                    # Add information to the log
                    logger.info('Prescription removed: Id {}, {}'.format(entry['uid'], entry['med_name']))
                    with open('../uch_system/database.json', 'w') as f:
                        json.dump(database, f, indent=2)
                    break

        # Once the database has been updated, delete the prescription from the table
        my_tree.delete(select)

        # Show the table of medications again
        show(username)


def save(username):
    """Save the updated prescription into the patient database."""
    # Show a message if any of the text boxes are empty to ensure that the user enters all fields
    error = 0
    if (date_added_edit.get() == '' or name_edit.get() == '' or dosage_edit.get() == '' or
            quantity_edit.get() == '' or duration_edit.get() == '' or expiry_edit.get() == ''):
        enter_all = Label(editor, text='Please enter all fields')
        enter_all.grid(row=8, column=2)
        error += 1

    # Exception handling to make sure the user selects a valid date from the calendar_function
    try:
        datetime.datetime.strptime(date_added_edit.get(), '%Y-%m-%d').date()
    except ValueError:
        not_date = Label(editor, text='This is not valid. Please select from the calendar_function above.')
        not_date.grid(row=1, column=2)
        error += 1

    # Exception handling to make sure the user enters an integer for the 'Quantity' text box
    try:
        int(quantity_edit.get())
    except ValueError:
        not_int = Label(editor, text='This is not valid. Please enter a whole number.')
        not_int.grid(row=4, column=2)
        error += 1

    # Exception handling to make sure the user enters an integer for the 'Duration' text box
    try:
        int(duration_edit.get())
    except ValueError:
        not_whole = Label(editor, text='This is not valid. Please enter a whole number.')
        not_whole.grid(row=5, column=2)
        error += 1

    # Exception handling to make sure the user adds the duration and confirms the expiry date
    try:
        datetime.datetime.strptime(expiry_edit.get(), '%Y-%m-%d').date()
    except ValueError:
        wrong_value = Label(editor, text='This is not valid. Please add the duration and confirm expiry.')
        wrong_value.grid(row=7, column=2)
        error += 1

    # If there are no errors, complete this block
    if error == 0:
        # Open the patient database
        with open('../uch_system/database.json') as file:
            database = json.load(file)

        for entry in database[username]['prescriptions']:
            if values[0] == entry['uid'] and len(database[username]['Allergies']) == 0:
                # If the ids of the selected medication match and the patient has no allergies,
                # update the database with the new prescription.
                entry['start_date'] = date_added_edit.get()
                entry['med_name'] = name_edit.get()
                entry['dosage'] = dosage_edit.get()
                entry['quantity'] = quantity_edit.get()
                entry['duration'] = duration_edit.get()
                entry['expiry'] = expiry_edit.get()
                # Add information to the log
                logger.info('Prescription updated: Id {}, {}'.format(entry['uid'], entry['med_name']))
                break
            elif values[0] == entry['uid']:
                for allergy in database[username]['Allergies']:
                    # Add alert for medication which may cause an allergy
                    if re.search(allergy, name_edit.get(), flags=re.IGNORECASE):
                        messagebox.showwarning('WARNING', 'ALLERGIC TO:' + ' ' + allergy)
                        break
                else:
                    # Update the database with the new prescription
                    entry['start_date'] = date_added_edit.get()
                    entry['med_name'] = name_edit.get()
                    entry['dosage'] = dosage_edit.get()
                    entry['quantity'] = quantity_edit.get()
                    entry['duration'] = duration_edit.get()
                    entry['expiry'] = expiry_edit.get()
                    # Add information to the log
                    logger.info('Prescription updated: Id {}, {}'.format(entry['uid'], entry['med_name']))
                    break

        # Update the database with the new, edited prescription
        with open('../uch_system/database.json', 'w') as f:
            json.dump(database, f, indent=2)

        # Once the update is saved, close the window and show the table of medications again
        editor.destroy()
        show(username)


def exp_date_edit():
    """Calculate the expiry date of a prescription.
    :raises ValueError: if the input for duration (days) is not a whole number
    """

    # Delete the entry box each time a new date is added
    expiry_edit.delete(0, END)

    try:
        # Use the module datetime to convert the start date into a date object
        start = datetime.datetime.strptime(date_added_edit.get(), '%Y-%m-%d').date()

        # If-else statement to make sure that the user enters a positive number for duration (days)
        if int(duration_edit.get()) < 0:
            not_positive = Label(editor, text='This is not valid. Please enter a positive number.')
            not_positive.grid(row=5, column=2)
        else:
            # Insert the calculated expiry date (date_added + duration) into the 'Expiry' text box
            period = int(duration_edit.get())
            if period > 999999:
                period = 999999
            end = start + datetime.timedelta(days=period)
            expiry_edit.insert(0, end)

    except ValueError:
        # Exception handling to make sure user enters a whole number for duration (days)
        invalid = Label(editor, text='This is not valid. Please enter a whole number.')
        invalid.grid(row=5, column=2)


def set_date_edit():
    """Set the date from calendar_function selection and insert into the 'Start Date' text box."""
    # Delete the entry box each time a new date is added
    date_added_edit.delete(0, END)

    # Insert the selection from the calendar_function into the 'Start Date' text box and destroy the calendar_function window
    date_set = str(cal_edit.year_select) + '-' + str(cal_edit.month_select) + '-' + str(cal_edit.day_select)
    date_added_edit.insert(0, date_set)
    my_cal_edit.destroy()


def get_date_edit():
    """View and select specific dates from a calendar_function."""
    global my_cal_edit, cal_edit

    # Create a new calendar_function window to edit the date
    my_cal_edit = Tk()
    my_cal_edit.title('Calendar')

    # Show a calendar_function (imported from cal.py) which allows the user to select a specific day
    cal_frame = Frame(my_cal_edit, borderwidth=5, bg='white')
    cal_frame.grid(row=2, column=2, columnspan=5)
    cal_edit = Cal(cal_frame, {})

    # Create a button to set a new date from the calendar_function
    select = Button(my_cal_edit, text='Select Date', command=set_date_edit)
    select.grid(row=3, column=4)

    my_cal_edit.mainloop()


def update(username):
    """Update the patient's prescription by changing specific details."""
    # Grab the record number for a selected prescription and all its values
    global values
    selected = my_tree.focus()
    values = my_tree.item(selected, 'values')

    # If-else statement to make sure user selects a drug before updating
    if selected:

        # Create new window to update a prescription
        global editor
        editor = Tk()
        editor.geometry('420x320')
        editor.title('Update')

        # Create a button to view a calendar_function
        calendar_edit = Button(editor, text='Calendar', command=get_date_edit, width=30)
        calendar_edit.grid(row=0, column=1, padx=20, pady=(10, 0))

        # Create text boxes
        global date_added_edit, name_edit, dosage_edit, quantity_edit, duration_edit, expiry_edit
        date_added_edit = Entry(editor, width=30)
        date_added_edit.grid(row=1, column=1)
        name_edit = Entry(editor, width=30)
        name_edit.grid(row=2, column=1)
        dosage_edit = Entry(editor, width=30)
        dosage_edit.grid(row=3, column=1)
        quantity_edit = Entry(editor, width=30)
        quantity_edit.grid(row=4, column=1)
        duration_edit = Entry(editor, width=30)
        duration_edit.grid(row=5, column=1)
        expiry_edit = Entry(editor, width=30)
        expiry_edit.grid(row=7, column=1)

        # Create text box labels
        date_label = Label(editor, text='Start Date')
        date_label.grid(row=0, column=0, pady=(10, 0))
        name_label = Label(editor, text='Drug Name')
        name_label.grid(row=2, column=0)
        dosage_label = Label(editor, text='Dosage')
        dosage_label.grid(row=3, column=0)
        quantity_label = Label(editor, text='Quantity')
        quantity_label.grid(row=4, column=0)
        duration_label = Label(editor, text='Duration (days)')
        duration_label.grid(row=5, column=0)
        expiry_label = Label(editor, text='Expiry Date')
        expiry_label.grid(row=7, column=0)

        # Insert the current details of the prescription into entry boxes
        date_added_edit.insert(0, values[1])
        name_edit.insert(0, values[2])
        dosage_edit.insert(0, values[3])
        quantity_edit.insert(0, values[4])
        duration_edit.insert(0, values[5])
        expiry_edit.insert(0, values[6])

        # Create a button to confirm the expiry date
        expiry_btn = Button(editor, text='Confirm Expiry Date', command=exp_date_edit)
        expiry_btn.grid(row=6, column=1, pady=5)

        # Create a button to save the updated prescription to the database
        save_btn = Button(editor, text='Save', command=lambda: save(username))
        save_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=145)

        editor.mainloop()
    # else:
    #     # Show a message if a drug has not been selected to update
    #     select_something = Label(meds, text='Please select a drug to update')
    #     select_something.grid(row=12, column=2)


def show(username):
    """Show the patient's prescriptions in a table."""
    # Create a tkinter table
    global my_tree
    my_tree = ttk.Treeview(meds)

    # Define columns
    my_tree['columns'] = ('ID', 'Start Date', 'Drug Name', 'Dosage', 'Quantity', 'Duration (days)', 'Expiry Date')

    # Format columns
    my_tree.column('#0', width=0, stretch=NO)
    my_tree.column('ID', anchor=CENTER, width=80)
    my_tree.column('Start Date', anchor=CENTER, width=100)
    my_tree.column('Drug Name', anchor=W, width=140)
    my_tree.column('Dosage', anchor=W, width=140)
    my_tree.column('Quantity', anchor=CENTER, width=80)
    my_tree.column('Duration (days)', anchor=CENTER, width=100)
    my_tree.column('Expiry Date', anchor=CENTER, width=100)

    # Create headings
    my_tree.heading('#0', text='', anchor=W)
    my_tree.heading('ID', text='ID', anchor=CENTER)
    my_tree.heading('Start Date', text='Start Date', anchor=CENTER)
    my_tree.heading('Drug Name', text='Drug Name', anchor=W)
    my_tree.heading('Dosage', text='Dosage', anchor=W)
    my_tree.heading('Quantity', text='Quantity', anchor=CENTER)
    my_tree.heading('Duration (days)', text='Duration (days)', anchor=CENTER)
    my_tree.heading('Expiry Date', text='Expiry Date', anchor=CENTER)

    # Open the patient database
    database = json.load(open('../uch_system/database.json'))

    count = 0

    for med in database[username]['prescriptions']:
        # Insert all of the patient's medications from the database into a table
        my_tree.insert(parent='', index='end', iid=count, text='', values=(med['uid'], med['start_date'],
                                                                            med['med_name'], med['dosage'],
                                                                            med['quantity'], med['duration'],
                                                                            med['expiry']
                                                                            ))

        count += 1

        # Show a warning for expired medication if today's date passes the expiry date
        exp = datetime.datetime.strptime(med['expiry'], '%Y-%m-%d').date()
        now = datetime.date.today()
        if exp < now:
            messagebox.showwarning('EXPIRED', med['med_name'] + ' ' + med['expiry'])

    my_tree.grid(row=11, column=0, columnspan=3, padx=10, pady=10)
    # Create a button to update medication selected from the table
    update_btn = Button(meds, text='Update Selected', command=lambda: update(username))
    update_btn.grid(row=12, column=1, pady=10, padx=10, ipadx=100)

    # Create a button to remove medication selected from the table
    remove_btn = Button(meds, text='Remove Selected', command=lambda: remove(username))
    remove_btn.grid(row=12, column=2, pady=10, padx=10, ipadx=100)


def add(username):
    """Add a prescription to the database."""
    # Show a message if any of the text boxes are empty to ensure that the user enters all fields
    error = 0
    if (date_added.get() == '' or name.get() == '' or dosage.get() == '' or
            quantity.get() == '' or duration.get() == '' or expiry.get() == ''):
        enter_all = Label(meds, text='Please enter all fields')
        enter_all.grid(row=9, column=2)
        error += 1

    # Exception handling to make sure the user selects a valid date from the calendar_function
    try:
        datetime.datetime.strptime(date_added.get(), '%Y-%m-%d').date()
    except ValueError:
        not_date = Label(meds, text='This is not valid. Please select from the calendar_function above.')
        not_date.grid(row=2, column=2)

    # Exception handling to make sure the user enters an integer for the 'Quantity' text box
    try:
        int(quantity.get())
    except ValueError:
        not_int = Label(meds, text='This is not valid. Please enter a whole number.')
        not_int.grid(row=5, column=2)
        error += 1

    # Exception handling to make sure the user enters an integer for the 'Duration' text box
    try:
        int(duration.get())
    except ValueError:
        not_whole = Label(meds, text='This is not valid. Please enter a whole number.')
        not_whole.grid(row=6, column=2)
        error += 1

    # Exception handling to make sure the user adds the duration and confirms the expiry date
    try:
        datetime.datetime.strptime(expiry.get(), '%Y-%m-%d').date()
    except ValueError:
        wrong_value = Label(meds, text='This is not valid. Please add the duration and confirm expiry.')
        wrong_value.grid(row=8, column=2)
        error += 1

    # If there are no errors, complete this block
    if error == 0:




        # Create a random three-digit id number for each medication
        unique_id = str(randint(100, 999))

        # Create a dictionary of prescription details which will be added to the patient database
        drug = {'uid': unique_id,
                'start_date': date_added.get(),
                'med_name': name.get(),
                'dosage': dosage.get(),
                'quantity': quantity.get(),
                'duration': duration.get(),
                'expiry': expiry.get()
                }

        # Open the patient database
        with open('../uch_system/database.json') as file:
            database = json.load(file)

        if len(database[username]['Allergies']) == 0:  # If the patient has no allergies, add the drug to the database
            database[username]['prescriptions'].append(drug)
            # Add information to the log
            logger.info('Prescription added: Id {}, {}'.format(drug['uid'], drug['med_name']))
        else:
            for allergy in database[username]['Allergies']:
                # Add alert for medication which may cause an allergy
                if re.search(allergy, name.get(), flags=re.IGNORECASE):
                    messagebox.showwarning('WARNING', 'ALLERGIC TO:' + ' ' + allergy)
                    break
            else:
                # Add the dictionary of prescription details to the database
                database[username]['prescriptions'].append(drug)
                # Add information to the log
                logger.info('Prescription added: Id {}, {}'.format(drug['uid'], drug['med_name']))

        # Add the new prescription to the database
        with open('../uch_system/database.json', 'w') as f:
            json.dump(database, f, indent=2)

        date_added.delete(0, END)
        name.delete(0, END)
        dosage.delete(0, END)
        quantity.delete(0, END)
        duration.delete(0, END)
        expiry.delete(0, END)

        # Once the medication is added, show table of medications
        show(username)

    # Clear the text boxes to allow the GP to add a new set of medications
    # date_added.delete(0, END)
    # name.delete(0, END)
    # dosage.delete(0, END)
    # quantity.delete(0, END)
    # duration.delete(0, END)
    # expiry.delete(0, END)


def exp_date():
    """Calculate the expiry date of a prescription.
    :raises ValueError: if the input for duration (days) is not a whole number
    """

    # Delete the entry box each time a new date is added
    expiry.delete(0, END)

    try:
        # Use the module datetime to convert the start date into a date object
        start = datetime.datetime.strptime(date_added.get(), '%Y-%m-%d').date()
        if int(duration.get()) < 0:
            not_positive = Label(meds, text='This is not valid. Please enter a positive number.')
            not_positive.grid(row=6, column=2)
        else:
            # Insert the calculated expiry date (date_added + duration) into the 'Expiry' text box
            period = int(duration.get())
            if period > 999999:
                period = 999999
            end = start + datetime.timedelta(days=period)
            expiry.insert(0, end)
    except ValueError:
        # Exception handling to make sure user enters a whole number for duration (days)
        invalid = Label(meds, text='This is not valid. Please enter a whole number.')
        invalid.grid(row=6, column=2)


def set_date():
    """Set the date from calendar_function selection and insert into the 'Start Date' text box."""
    # Delete the entry box each time a new date is added
    date_added.delete(0, END)

    # Insert the selection from the calendar_function into the 'Start Date' text box and destroy the calendar_function window
    date_set = str(cal.year_select) + '-' + str(cal.month_select) + '-' + str(cal.day_select)
    date_added.insert(0, date_set)
    my_cal.destroy()


def get_date():
    """View and select specific dates from a calendar_function."""
    global my_cal, cal

    # Create a new calendar_function window
    my_cal = Tk()
    my_cal.title('Calendar')

    # Show a calendar_function (imported from cal.py) which allows the user to select a specific day
    cal_frame = Frame(my_cal, borderwidth=5, bg='white')
    cal_frame.grid(row=2, column=2, columnspan=5)
    cal = Cal(cal_frame, {})

    # Create a button to set a specific date from the calendar_function
    select = Button(my_cal, text='Select Date', command=set_date)
    select.grid(row=3, column=4)

    my_cal.mainloop()


def meds_window(patient_table, type="general"):
    """A window for adding, viewing, updating and removing prescriptions for a specific patient.
    :param patient_finder: Destroy previous window for searching a patient.
    :param details: Show the details of the patient on the new window.
    :returns: A window for editing/viewing prescriptions for a patient.
    """

    selected = patient_table.selection()
    if selected == ():
        messagebox.showinfo("None selected", "Please select a patient from the table first.")
        return None
    database = json.load(open('../uch_system/database.json'))
    # Iterates through all selected patients from table
    for rec in selected:

        value = patient_table.item(rec, 'values')
        if type == "today":
            nhs_number = value[2]
        else:
            nhs_number = value[3]
        for i in database.values():
            if i["NHS_number"] == nhs_number:
                patient_username = i["username"]

    # Create a new medications window
    global meds
    meds = Tk()
    meds.geometry('800x600')
    meds.title('Medications')

    # Show patient details
    patient_name = Label(meds,
                         text=database[patient_username]['First Name'] + ' ' + database[patient_username]['Last Name'] +
                              '\nNHS Number: ' + str(database[patient_username]['NHS_number']))
    patient_name.grid(row=0, column=1)

    # Create a button to view a calendar_function
    calendar = Button(meds, text='Calendar', command=get_date, width=30)
    calendar.grid(row=1, column=1, padx=20, pady=(10, 0))

    # Create text boxes
    global date_added, name, dosage, quantity, duration, expiry
    date_added = Entry(meds, width=30)
    date_added.grid(row=2, column=1)
    name = Entry(meds, width=30)
    name.grid(row=3, column=1)
    dosage = Entry(meds, width=30)
    dosage.grid(row=4, column=1)
    quantity = Entry(meds, width=30)
    quantity.grid(row=5, column=1)
    duration = Entry(meds, width=30)
    duration.grid(row=6, column=1)
    expiry = Entry(meds, width=30)
    expiry.grid(row=8, column=1)

    # Create text box labels
    date_label = Label(meds, text='Start Date')
    date_label.grid(row=1, column=0, pady=(10, 0))
    name_label = Label(meds, text='Drug Name')
    name_label.grid(row=3, column=0)
    dosage_label = Label(meds, text='Dosage')
    dosage_label.grid(row=4, column=0)
    quantity_label = Label(meds, text='Quantity')
    quantity_label.grid(row=5, column=0)
    duration_label = Label(meds, text='Duration (days)')
    duration_label.grid(row=6, column=0)
    expiry_label = Label(meds, text='Expiry Date')
    expiry_label.grid(row=8, column=0)

    # Create a button to confirm expiry date
    expiry_btn = Button(meds, text='Confirm Expiry Date', command=exp_date)
    expiry_btn.grid(row=7, column=1)

    # Create a button to add medication
    add_btn = Button(meds, text='Add', command=lambda: add(patient_username))
    add_btn.grid(row=9, column=1, pady=10, padx=10, ipadx=120)

    # Create a button to show all current medications
    # query_btn = Button(meds, text='Show Medication', command=lambda: show(patient_username))
    # query_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=137)
    show(patient_username)

    meds.mainloop()
