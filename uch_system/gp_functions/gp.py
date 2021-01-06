import importlib.resources
import json
import logging
from uch_system.core import User
import webbrowser
from tkinter import Label, Button, Entry, ttk, messagebox, END, Tk, CENTER, Text, NO, W
import tkinter.font as tkFont

import uch_system.gp_functions.gp_prescriptions as gp_prescriptions

# Create and configure logger
log = importlib.resources.path('uch_system','newfile.log')

logging.basicConfig(filename=log,
                    format='%(asctime)s %(message)s',
                    filemode='a')
logger = logging.getLogger()


class GP(User):
    """
    GP methods that initiated from the GP portal, creates an instance with the information from GP_database +
    appointment information
    """

    def __init__(self, username, f_name, l_name, password, gmc_number, assigned_patients, verified, holidays, lunch, monday_s="09:00",
                 monday_e="16:50", tuesday_s="09:00", tuesday_e="16:50",
                 wednesday_s="09:00", wednesday_e="16:50", thursday_s="09:00", thursday_e="16:50", friday_s="09:00",
                 friday_e="16:50"):
        User.__init__(self, username, f_name, l_name, password)
        self.gmc_number = gmc_number
        self.assigned_patients = assigned_patients
        self.verified = verified
        self.holidays = holidays
        self.lunch = lunch
        self.monday_s = monday_s
        self.monday_e = monday_e
        self.tuesday_s = tuesday_s
        self.tuesday_e = tuesday_e
        self.wednesday_s = wednesday_s
        self.wednesday_e = wednesday_e
        self.thursday_s = thursday_s
        self.thursday_e = thursday_e
        self.friday_s = friday_s
        self.friday_e = friday_e

    def see_feedback(self):

        """
        Concatenates a string of feedbacks from the patient json database for all patients of the GP + reads requests
        for medications
        Arguments:
            GP instance (assigned patients list)
            patient json database
        Returns:
            concatenated str of feedback/requests for all patients of the GP
        """

        # opens patient database (feedback) for each patient and creates a string that is printed in the window
        database = json.load(open('../uch_system/database.json'))
        general_feedback = ''
        drug_request = ''
        for patient in self.assigned_patients:
            if len(database[patient]['Feedback']) > 0:  # if feedback/request was given by the patient
                for feedback in (database[patient]['Feedback']):
                    if type(feedback) is str:  # feedback has a data type of str
                        if len(feedback) > 100:  # corrects for the length of str to break the line in window
                            feedback = feedback[:100] + '\n' + feedback[100:]
                        elif len(feedback) > 200:
                            feedback = feedback[:100] + '\n' + feedback[100:200] + '\n' + feedback[200:]
                        single_feedback = ('Patient name: {} {} \n {}\n\n'.format(database[patient]['First Name'],
                                                                                  database[patient]['Last Name'],
                                                                                  feedback))

                        general_feedback += single_feedback  # creates the concatenated string for all patients
                    elif type(feedback) is dict:  # request has a data type of dict
                        for key, value in feedback.items():     # creates a formatted string of request
                            format_request = 'Date: ' + key + ' - ' + list(value.keys())[0].capitalize() + ' (dosage ' +\
                                             list(value.values())[0] + ')' + '\n' + list(value.keys())[1] + ': ' + \
                                             list(value.values())[1]
                        single_feedback = ('Patient name: {} {} \n {}\n\n'.format(database[patient]['First Name'],
                                                                                  database[patient]['Last Name'],
                                                                                  format_request))

                        drug_request += single_feedback  # creates the concatenated string for all patients
        json.dump(database, open('../uch_system/database.json', 'w'))

        if general_feedback == '' and drug_request == '':
            messagebox.showinfo("No entry", 'You do not have any drug requests or feedback.')
            return None

        # sets up the window and fonts that will be used
        fb_window = Tk()
        fb_window.title('UCLH GP portal: Feedback')
        fb_window.geometry("800x600")
        fontStyle2 = tkFont.Font(family="Lucida Grande", size=8)

        # sets up the Request and Feedback tabs of the window
        tab_control = ttk.Notebook(fb_window)
        tab1 = ttk.Frame(tab_control)
        tab2 = ttk.Frame(tab_control)
        tab_control.add(tab1, text="   General Feedback   ")
        tab_control.add(tab2, text="     Drug Requests    ")
        tab_control.pack(expand=1, fill="both")
        Label(tab1, text=('This is your feedback, Dr {}'.format(self.l_name)), font=fontStyle2).place(
            relx=0.5, rely=0.2, anchor=CENTER)
        Label(tab2, text=('These are your prescription requests, Dr {}'.format(self.l_name)),
              font=fontStyle2).place(
            relx=0.5, rely=0.2, anchor=CENTER)

        # button to return back to the GP menu
        Label(tab1, text=general_feedback).place(relx=0.5, rely=0.4, anchor=CENTER)
        Button(tab1, text='Back to Menu', command=lambda: fb_window.destroy()).place(relx=0.5, rely=0.1,
                                                                                     anchor=CENTER)
        Label(tab2, text=drug_request).place(relx=0.5, rely=0.4, anchor=CENTER)
        Button(tab2, text='Back to Menu', command=lambda: fb_window.destroy()).place(relx=0.5, rely=0.1,
                                                                                     anchor=CENTER)

        fb_window.mainloop()

    def consultation(self, patient_search=0):

        """
        GP is presented with their patients and chooses the attending patient
        Arguments:
            GP instance (assigned patients list)
            patient json database
        Returns:
            consultation_patient argument for the consultation_body() function
        """

        if not self.assigned_patients:
            messagebox.showinfo("Empty database", 'We are sorry, you do not have any assigned patients yet.')
            return None

        # opens the consultation_body window with consultation_patient argument
        def get_patient():
            selected = my_tree.selection()

            if len(selected) == 1:
                value = my_tree.item(selected, 'values')
                nhs_number = value[3]
                for profile in database.keys():
                    if database[profile]["NHS_number"] == nhs_number:
                        master.destroy()
                        GP.consultation_body(profile)

        def search():
            global surname
            surname = surname_search.get()

            surname_exists = False
            for profile in database.keys():
                if surname.lower() == database[profile]["Last Name"].lower():
                    surname = database[profile]["Last Name"]
                    surname_exists = True
            if surname_exists is True:
                master.destroy()
                self.consultation(patient_search=1)

            else:
                messagebox.showwarning("Search error", "No patients found with that surname, "
                                                       "please check spelling and try again!")

        database = json.load(open('../uch_system/database.json'))

        # Checks if there are patients that have registered
        if len(database.values()) > 0:

            master = Tk()
            master.title('All patients')
            master.geometry("520x380")

            my_tree = ttk.Treeview(master)

            surname_search = Entry(master)
            surname_search.place(relx=0.5, rely=0.1, anchor=CENTER)

            # Define columns
            my_tree['columns'] = ('First Name', 'Last Name', 'DOB', 'NHS Number')

            # Format columns
            my_tree.column("#0", width=0, stretch=NO)
            my_tree.column("First Name", anchor=CENTER, width=100)
            my_tree.column("Last Name", anchor=CENTER, width=100)
            my_tree.column("DOB", anchor=CENTER, width=150)
            my_tree.column("NHS Number", anchor=CENTER, width=100)

            # Create headings
            my_tree.heading("#0", text="", anchor=W)
            my_tree.heading("First Name", text="First Name", anchor=CENTER)
            my_tree.heading("Last Name", text="Last Name", anchor=CENTER)
            my_tree.heading("DOB", text="DOB", anchor=CENTER)
            my_tree.heading("NHS Number", text="NHS Number", anchor=CENTER)

            count = 0
            # Iterates through patients in database and if they are verified, adds them to table
            if patient_search == 1:
                for patient in self.assigned_patients:
                    try:
                        if database[patient]['Last Name'] == surname:
                            my_tree.insert(parent='', index='end', iid=count, text="",
                                           values=(database[patient]['First Name'].capitalize(),
                                                   database[patient]['Last Name'].capitalize(),
                                                   database[patient]['DOB'],
                                                   database[patient]['NHS_number']
                                                   ))
                            my_tree.place(relx=0.5, rely=0.5, anchor=CENTER)
                            count += 1
                    except:
                        pass
            else:
                for patient in self.assigned_patients:
                    my_tree.insert(parent='', index='end', iid=count, text="",
                                   values=(database[patient]['First Name'].capitalize(),
                                           database[patient]['Last Name'].capitalize(), database[patient]['DOB'],
                                           database[patient]['NHS_number']
                                           ))
                    my_tree.place(relx=0.5, rely=0.5, anchor=CENTER)
                    count += 1

            request_label = Label(master, text="Search by surname")
            request_label.place(relx=0.2, rely=0.1, anchor=CENTER)

            Button(master, text="Open consultation", command=get_patient).place(relx=0.8, rely=0.9, anchor=CENTER)
            Button(master, text="Search", command=search).place(relx=0.8, rely=0.1, anchor=CENTER)
            Button(master, text="Add/View Prescriptions", command=lambda: gp_prescriptions.meds_window(my_tree))\
                .place(relx=0.2, rely=0.9, anchor=CENTER)
            master.mainloop()


        else:
            messagebox.showinfo("Information",
                                "You currently do not have any assigned patients. If you think this is"
                                " a problem please contact the system administrator")

    @staticmethod
    def consultation_body(consultation_patient):

        """
        Consultation window for a patient chosen in gp.consultation(), GP can alter the patient database with allergies,
        non-prescription drugs, consultation notes, calculate BMI and see historical notes of the patient
        Arguments:
            consultation_patient (key in the patient database)
            patient database (allergies, regular_drugs are edited)
        Returns:
            edits the database with 'Notes', 'regular_drugs' and 'Allergies'
        """

        import datetime
        database = json.load(open('../uch_system/database.json'))

        # sets up the window and fonts that will be used
        consult_window = Tk()
        consult_window.title('Patient consultation')
        consult_window.geometry("1000x800+80+40")
        fontStyle2 = tkFont.Font(family="Lucida Grande", size=16)

        # demographic information about the patient
        Label(consult_window, text='Patient Name: ' + database[consultation_patient]['First Name'].capitalize() + ' '
                                   + database[consultation_patient]['Last Name'].capitalize(), font=fontStyle2).place(
            relx=0.5, rely=0.08, anchor=CENTER)
        if database[consultation_patient]['DOB'] == 'TBC':  # if patient did not enter the DOB in correct format
            Label(consult_window, text='Date of Birth: not known').place(relx=0.5, rely=0.13, anchor=CENTER)
            Label(consult_window, text='Age: not known').place(relx=0.5, rely=0.16, anchor=CENTER)
        else:
            datetime_object = datetime.datetime.strptime(database[consultation_patient]['DOB'], '%d/%m/%Y')
            Label(consult_window, text='Date of Birth: ' + database[consultation_patient]['DOB']).place(
                relx=0.5, rely=0.13, anchor=CENTER)
            age = datetime.datetime.today().year - datetime_object.year  # calculates age
            Label(consult_window, text='Age: ' + str(age)).place(relx=0.5, rely=0.16, anchor=CENTER)
        Label(consult_window, text='NHS number: ' + str(database[consultation_patient]['NHS_number'])).place(
            relx=0.5, rely=0.19, anchor=CENTER)
        Label(consult_window, text='Telephone number: ' + str(database[consultation_patient]['tel_number'])).place(
            relx=0.5, rely=0.22, anchor=CENTER)
        Label(consult_window, text='Gender: ' + str(database[consultation_patient]['gender'])).place(
            relx=0.5, rely=0.25, anchor=CENTER)

        # non-prescription drugs
        if not database[consultation_patient]['regular_drugs']:
            drug_label = Label(consult_window, text='Patient has not claimed any regular non-prescribed drugs')
            drug_label.place(relx=0.5, rely=0.28, anchor=CENTER)
        else:
            drug_string = ''
            for drug in database[consultation_patient]['regular_drugs']:
                drug_string += ('#' + drug + ' ')  # string of drugs from the list in the database
            drug_label = Label(consult_window, text='Non-prescription drugs: ' + drug_string)
            drug_label.place(relx=0.5, rely=0.28, anchor=CENTER)
        added_drug = Entry(consult_window)  # entry of a new drug to update database
        added_drug.place(relx=0.40, rely=0.32, anchor=CENTER)
        submit_drugs = Button(consult_window, text='Add drug', command=lambda: submit_drugs())
        submit_drugs.place(relx=0.53, rely=0.32, anchor=CENTER)
        Label(consult_window,
              text='Note that this input is different from prescription drugs. To make prescription, go to main '
                   'menu.').place(relx=0.5, rely=0.35, anchor=CENTER)

        # searches the entry term in the BNF (British National Formulary)
        search_button = Button(consult_window, text='Search BNF', command=lambda: search_nice())
        search_button.place(relx=0.63, rely=0.32, anchor=CENTER)

        # allergies
        if not database[consultation_patient]['Allergies']:
            allergy_label = Label(consult_window, text='Patient has not claimed any allergies')
            allergy_label.place(relx=0.5, rely=0.38, anchor=CENTER)
        else:
            allergy_string = ''
            for allergy in database[consultation_patient]['Allergies']:
                allergy_string += ('#' + allergy + ' ')  # string of allergies from the list in the database
            allergy_label = Label(consult_window, text='Allergies: ' + allergy_string)
            allergy_label.place(relx=0.5, rely=0.38, anchor=CENTER)
        added_allergy = Entry(consult_window)
        added_allergy.place(relx=0.45, rely=0.42, anchor=CENTER)
        submit_allergy = Button(consult_window, text='Add allergy', command=lambda: submit_allergy())
        submit_allergy.place(relx=0.58, rely=0.42, anchor=CENTER)

        # referral of the patient to other UCLH department
        specialties_options = ttk.Combobox(consult_window) # drop-down list with UCLH departments
        specialties_options['values'] = ['Accident & emergency', 'Bariatric surgery', 'Bladder cancer', 'Cardiology',
                            'Child care', 'COPD service', 'Colorectal cancer', 'Dementia services', 'Diabetology',
                            'Endoscopy', 'Endocrine medicine', 'GI services', 'General surgery', 'Geriatric medicine',
                            'Gyneacology', 'Haematology', 'Imaging', 'Intensive Care', 'Liver unit',
                            'Lung cancer services', 'Ophtamology', 'Orthopaedics', 'Pharmacy services', 'Physiotherapy',
                            'Respiratory medicine', 'Rheumatology', 'Skin cancer services', 'Speech services',
                            'Sports medicine', 'Stroke unit', 'Urgent care']  # UCLH departments
        specialties_options.current(0)
        specialties_options.place(relx=0.43, rely=0.50, anchor=CENTER)
        if not database[consultation_patient]['Referral']:
            referral_label = Label(consult_window, text='Patient has not been referred to other UCLH department.')
            referral_label.place(relx=0.5, rely=0.46, anchor=CENTER)
        else:
            referral_label = Label(consult_window,
                                   text=('Patient referred to UCLH ' + database[consultation_patient]['Referral']
                                         + ' on ' + str(datetime.date.today().strftime('%d/%m/%Y')) + '.'))
            referral_label.place(relx=0.5, rely=0.46, anchor=CENTER)
        referral_button = Button(consult_window, text='Refer patient', command=lambda: refer())
        referral_button.place(relx=0.58, rely=0.50, anchor=CENTER)

        # BMI calculator
        input_weight = Entry(consult_window)
        input_weight.place(relx=0.30, rely=0.54, anchor=CENTER)
        Label(consult_window, text='Weight [kg]').place(relx=0.15, rely=0.54, anchor=CENTER)
        input_height = Entry(consult_window)
        input_height.place(relx=0.60, rely=0.54, anchor=CENTER)
        Label(consult_window, text='Height [cm]').place(relx=0.45, rely=0.54, anchor=CENTER)
        calculate_BMI = Button(consult_window, text='Calculate BMI', command=lambda: bmi_calc())
        calculate_BMI.place(relx=0.78, rely=0.54, anchor=CENTER)

        # notes
        Label(consult_window, text='Consultation notes:').place(relx=0.5, rely=0.575, anchor=CENTER)
        notes_box = Text(consult_window, bg='honeydew2', width=70, height=17)  # entry box for consultation notes
        notes_box.place(relx=0.5, rely=0.77, anchor=CENTER)

        # three buttons that save the notes, see old notes and go to web National Institute for Health and Care
        # excellence (NICE)
        Button(consult_window, text="Save notes and exit", command=lambda: save_notes()).place(
            relx=0.5, rely=0.97, anchor=CENTER)
        Button(consult_window, text="Notes from past consultations", command=lambda: old_notes()).place(
            relx=0.72, rely=0.97, anchor=CENTER)
        Button(consult_window, text="NICE Guidelines", command=lambda: hyperlink()).place(
            relx=0.28, rely=0.97, anchor=CENTER)

        json.dump(database, open('../uch_system/database.json', 'w'))

        # opens a webpage with the NICE guidelines - official guidelines for evidence-based care recommendations
        def hyperlink():

            webbrowser.open_new("https://www.nice.org.uk/guidance")
            logger.info("Opened a web browser")

        # opens database and saves consultation notes with the date of writing into patient's records
        def save_notes():

            database1 = json.load(open('../uch_system/database.json'))
            user_entry = notes_box.get("1.0", 'end-1c')  # gets the entry from the notes box
            if len(user_entry) > 0:
                notes_date = datetime.datetime.today()
                notes_date2 = datetime.datetime.strftime(notes_date, '%Y-%m-%d %H:%M')
                full_notes = notes_date2 + ' - ' + user_entry  # adds date of writing to the notes
                database1[consultation_patient]['Notes'].append(full_notes)
                consult_window.destroy()
                messagebox.showinfo("Save", "Your input has been saved")
                logger.info("Saved notes input")
            else:
                messagebox.showinfo("Alert", "You cannot upload empty notes")
            json.dump(database1, open('../uch_system/database.json', 'w'))

        # updates the database with the new non-prescription drugs
        def submit_drugs():

            database1 = json.load(open('../uch_system/database.json'))
            user_entry = added_drug.get()  # gets the GP entry for the new non-prescribed drug
            database1[consultation_patient]['regular_drugs'].append(user_entry)
            drug_label.destroy()
            drug_string = ''
            for drug in database1[consultation_patient]['regular_drugs']:
                drug_string += ('#' + drug + ' ')  # creates a new string of drugs that updates the drug label
            Label(consult_window, text='Non-prescription drugs: ' + drug_string).place(relx=0.5, rely=0.28,
                                                                                       anchor=CENTER)
            added_drug.delete(0, END)  # erases the entry from the entry window
            logger.info("Saved drugs input")
            json.dump(database1, open('../uch_system/database.json', 'w'))

        # creates a string that is used as a web address that is then launched
        def search_nice():

            entry = added_drug.get()
            webstring = 'https://bnf.nice.org.uk/drug/' + entry + '.html'
            webbrowser.open_new(webstring)
            logger.info("Opened a web browser")

        # updates the database with the new allergies
        def submit_allergy():

            database1 = json.load(open('../uch_system/database.json'))
            user_entry = added_allergy.get()  # gets the GP entry for the new allergies
            database1[consultation_patient]['Allergies'].append(user_entry)
            allergy_label.destroy()
            allergy_string = ''
            for allergy in database1[consultation_patient]['Allergies']:
                allergy_string += ('#' + allergy + ' ')  # creates a new string of allergies that updates the label
            Label(consult_window, text='Allergies: ' + allergy_string).place(relx=0.5, rely=0.38, anchor=CENTER)
            added_allergy.delete(0, END)  # erases the entry from the enry window
            logger.info("Saved allergy input")
            json.dump(database1, open('../uch_system/database.json', 'w'))

        # BMI calculator, based on the weight and height input calculates patient's BMI
        def bmi_calc():

            try:
                weight = input_weight.get()
                height = input_height.get()

                if float(weight) > 0 and float(height) > 0:

                    BMI = float(weight) / ((float(height) / 100) ** 2)  # standard BMI calculation
                    BMI = int(BMI)
                    if BMI <= 18.5:
                        messagebox.showinfo("BMI",
                                            'BMI of the patient is ' + str(
                                                BMI) + '. This is underweight, consider therapy.')
                    elif 25.0 < BMI <= 30.0:
                        messagebox.showinfo("BMI", 'BMI of the patient is ' + str(BMI) + '. This is overweight.')
                    elif BMI > 30.0:
                        messagebox.showinfo("BMI",
                                            'BMI of the patient is ' + str(BMI) + '. This is obese, consider therapy.')
                    else:
                        messagebox.showinfo("BMI", 'BMI of the patient is ' + str(BMI) + '. This is in the healthy '
                                                                                         'range.')

                else:
                    messagebox.showinfo('BMI error', 'We do not accept negative input.')
                    logger.error("Incorrect BMI input")

            except ValueError:  # corrects for the str input instead of int
                messagebox.showinfo('BMI error', 'We are sorry but you have not written a correct input.')
                logger.error("Incorrect BMI input")

            except:
                messagebox.showinfo('BMI error', 'There has been a technical issue with this function. We are sorry, '
                                                 'administrator will check it as soon as possible.')
                logger.error("Incorrect BMI input")

        # updates the patient database with referral
        def refer():

            database1 = json.load(open('../uch_system/database.json'))
            referral = specialties_options.get()
            database1[consultation_patient]['Referral'] = referral  # rewrites the database referral element
            referral_label.config(text='Patient referred to UCLH ' + referral + ' on ' +
                                       str(datetime.date.today().strftime('%d/%m/%Y')) + '.')  # adds date to referral
            logger.info("Saved referral input")
            json.dump(database1, open('../uch_system/database.json', 'w'))

        # opens new window with the historical notes from consultations
        def old_notes():

            # opens the database and sets up the window
            database1 = json.load(open('../uch_system/database.json'))

            if len(database1[consultation_patient]['Notes']) > 0:
                old_notes_window = Tk()
                old_notes_window.geometry("850x450")
                old_notes_window.title('Patient historical notes')

                all_notes = ''
                for note in (database1[consultation_patient]['Notes']):
                    if type(note) is str:  # corrects for the str length, breaks the line to fit the window
                        if len(note) > 120:
                            note = note[:120] + '\n' + note[240:]
                        elif len(note) > 240:
                            note = note[:120] + '\n' + note[120:240] + '\n' + note[240:]
                        all_notes += (note + '\n')
                Label(old_notes_window, text=all_notes).pack()
            else:
                messagebox.showinfo("Notes", 'There are no historical notes for this patient')
            json.dump(database1, open('../uch_system/database.json', 'w'))

        consult_window.mainloop()




