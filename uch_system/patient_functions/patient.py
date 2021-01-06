import datetime
import json
import logging
from core import User
import tkinter.font as tkFont
from tkinter import Label, Button, Toplevel, Entry, ttk, messagebox, END, Tk, CENTER, Text, Checkbutton, NO, W, \
    IntVar

# Create and configure logger
logging.basicConfig(filename="../uch_system/newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
logger = logging.getLogger()


class Patient(User):
    """
    Patient methods that initiated from the patient portal, creates an instance with the information from patient
    json database
    """

    def __init__(self, username, f_name, l_name, password, gender, dob, tel_number, regular_drugs, prescriptions,
                 nhs_number, assigned_gp, verified, feedback, notes, allergies, referral):
        User.__init__(self, username, f_name, l_name, password)
        self.gender = gender
        self.dob = dob
        self.tel_number = tel_number
        self.regular_drugs = regular_drugs
        self.prescriptions = prescriptions
        self.nhs_number = nhs_number
        self.assigned_gp = assigned_gp
        self.verified = verified
        self.feedback = feedback
        self.notes = notes
        self.allergies = allergies
        self.referral = referral

    def give_feedback(self):

        """
        Opens a text entry window where the user enters feedback, saves the feedback as a string with the date of
        writing it and saves in the json database (under 'Feedback' key)
        Arguments:
            patient's instance (username to identify the patient key in the database)
        Returns:
            updates json database ('Feedback') for the patient with feedback (string date+entry text)
            messagebox
        """

        if self.assigned_gp == '':
            messagebox.showinfo("No GP", 'You do not have any assigned GP who could accept your feedback.')
            return None

        # sets up the window and fonts that will be used
        fb_window = Tk()
        fb_window.title('UCLH patient portal: Feedback')
        fb_window.geometry("800x600")

        # takes the entry from the text widget, connects it with the date and updates the database
        def submit():
            try:
                user_entry = feedback_box.get("1.0", 'end-1c')
                if len(user_entry) > 0:
                    database = json.load(open('../uch_system/database.json'))
                    feedback_date = str(datetime.date.today())  # assumes 'today' as the day of writing
                    full_feedback = feedback_date + ': ' + user_entry  # creates string of date and entry
                    database[self.username]['Feedback'].append(full_feedback)  # appends the list of user's feedbacks
                    json.dump(database, open('../uch_system/database.json', 'w'))
                    fb_window.destroy()
                    messagebox.showinfo("Feedback", "Your feedback has been submitted")  # raises messagebox
                else:
                    messagebox.showinfo("Alert", "You cannot upload empty feedback.")
            except ValueError:
                messagebox.showinfo("Error", "We are sorry, the function is not working at the moment")

        Label(fb_window, text="Write your feedback in the box below.").place(relx=0.5, rely=0.15, anchor=CENTER)
        feedback_box = Text(fb_window, bg='honeydew2', width=60, height=20)  # text entry window
        feedback_box.place(relx=0.5, rely=0.5, anchor=CENTER)
        Label(fb_window, text="Thank you for providing the feedback, it will be carefully evaluated by your GP.") \
            .place(relx=0.5, rely=0.8, anchor=CENTER)

        # button that calls the submit function
        submit_button = Button(fb_window, text="Submit", command=submit)
        submit_button.place(relx=0.5, rely=0.88, anchor=CENTER)

        fb_window.mainloop()

    @staticmethod
    def check_covid(window):

        """
        Opens a window with 5 checkboxes for the symptoms, user chooses and then runs the covid_submit to return the
        messagebox with COVID-19 positive or negative symptoms.
        Arguments:
            window where check_covid originates
            local scope variables: var1-var5 (integer 0/1 variables indicating presence of COVID symptoms)
        Returns:
            messagebox with recommendation to take a test/ stay alert
        """

        # Takes IntVariables, converts into 0/1, sums up and calculates the full score, raises a messagebox of
        # symptom indication
        def covid_submit(*args):
            full_score = 0
            for i in range(5):
                full_score += args[i].get()  # adds up the 0/1 to a final score
            if full_score >= 1:  # checking any box indicates that the person should get tested
                messagebox.showinfo("COVID-19", "You are likely to have COVID-19. Please, sign up for a test here: "
                                                "https://www.gov.uk/get-coronavirus-test.")
            else:
                messagebox.showinfo("COVID-19", "At the moment you do not have indications of COVID-19. Stay alert!")

        # sets up the window and fonts that will be used
        root = Toplevel(window)
        root.title('Check COVID symptoms')
        root.geometry('340x220')
        fontStyle2 = tkFont.Font(family="Lucida Grande", size=16)
        Label(root, text="Check what applies to you:", font=fontStyle2, pady=10).grid(row=0, column=0)

        # introduces the variables and checkboxes, IntVar = integer variable of 0/1 based on being checked/unchecked
        var1 = IntVar()
        c = Checkbutton(root, text="New persistent cough", variable=var1)
        c.grid(row=1, column=0, sticky=W)
        var2 = IntVar()
        c = Checkbutton(root, text="Loss of smell", variable=var2)
        c.grid(row=2, column=0, sticky=W)
        var3 = IntVar()
        c = Checkbutton(root, text="Loss of taste", variable=var3)
        c.grid(row=3, column=0, sticky=W)
        var4 = IntVar()
        c = Checkbutton(root, text="High temperature", variable=var4)
        c.grid(row=4, column=0, sticky=W)
        var5 = IntVar()
        c = Checkbutton(root, text="I had contact with COVID-19 positive person", variable=var5)
        c.grid(row=5, column=0, sticky=W, pady=(0, 10))

        # submit button that calls the covid_submit function with all the IntVariables above + destroys the window
        submit_button = Button(root, text="Submit",
                               command=lambda: (covid_submit(var1, var2, var3, var4, var5), root.destroy()))
        submit_button.grid(row=16, column=0)

        root.mainloop()

    def prescription(patient):
        """
        Shows patient's precriptions, patient can request prescription that GP has to approve
        Arguments:
            json database
        Returns:
            updates database (GP has to approve)
        """

        def confirm_request():

            db = json.load(open('../uch_system/database.json'))

            request_list['Reason for request'] = request_box.get("1.0", 'end-1c')
            request_date = str(datetime.date.today())
            full_request = {request_date: request_list}
            db[patient.username]['Feedback'].append(full_request)

            json.dump(db, open('../uch_system/database.json', 'w'), indent=2)
            meds_window.destroy()
            messagebox.showinfo("Request", "Your request has been confirmed")

        def request():

            global request_list, request_box
            meds_window.geometry("800x650")

            selected = my_tree.selection()
            request_list = {}
            print_records = ''
            if selected == ():
                messagebox.showwarning("Problem", "No prescription was selected. Please try again.")
                return
            for rec in selected:
                value = my_tree.item(rec, 'values')
                print_records += str(value[2]) + " " + str(value[3]) + "\n"
                request_list[value[2]] = value[3]

            Label(meds_window, text='Reason for request').grid(row=4, column=0, pady=10, columnspan=2)
            request_box = Text(meds_window, bg='honeydew2', width=60, height=10)
            request_box.grid(row=5, column=0, columnspan=2)
            Label(meds_window, text='Thank you, your GP will have a look at the request and get back to you shortly.') \
                .grid(row=6, column=0, columnspan=2)
            Button(meds_window, text="Confirm Request", command=confirm_request).grid(row=7, column=0, pady=20, columnspan=2)

            value_label = Label(meds_window, text=print_records)
            value_label.grid(row=3, column=0, columnspan=2)

        # Show all of patient's medications
        meds_window = Tk()
        meds_window.title('My Prescriptions')
        meds_window.geometry("800x350")

        data = json.load(open('../uch_system/database.json'))
        my_tree = ttk.Treeview(meds_window)

        # Define columns
        my_tree['columns'] = ('ID', 'Start Date', 'Name', 'Dosage', 'Quantity', 'Duration (days)', 'Expiry Date')

        # Format columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("ID", anchor=CENTER, width=80, stretch=NO)
        my_tree.column("Start Date", anchor=CENTER, width=100)
        my_tree.column("Name", anchor=W, width=140)
        my_tree.column("Dosage", anchor=W, width=140)
        my_tree.column("Quantity", anchor=CENTER, width=80)
        my_tree.column("Duration (days)", anchor=CENTER, width=100)
        my_tree.column("Expiry Date", anchor=CENTER, width=100)

        # Create headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("ID", text="ID", anchor=CENTER)
        my_tree.heading("Start Date", text="Start Date", anchor=CENTER)
        my_tree.heading("Name", text="Name", anchor=W)
        my_tree.heading("Dosage", text="Dosage", anchor=W)
        my_tree.heading("Quantity", text="Quantity", anchor=CENTER)
        my_tree.heading("Duration (days)", text="Duration (days)", anchor=CENTER)
        my_tree.heading("Expiry Date", text="Expiry Date", anchor=CENTER)

        count = 0
        for recs in data.values():
            if patient.nhs_number == recs["NHS_number"]:
                for med in recs['prescriptions']:
                    my_tree.insert(parent='', index='end', iid=count, text="",
                                   values=(med['uid'], med['start_date'],
                                           med['med_name'], med['dosage'],
                                           med['quantity'], med['duration'],
                                           med['expiry']))
                    my_tree.grid(row=0, column=0, columnspan=2, padx=20, pady=10)
                    count += 1
                    exp = datetime.datetime.strptime(med['expiry'], '%Y-%m-%d').date()
                    now = datetime.date.today()
                    if exp < now:
                        messagebox.showwarning("EXPIRED", med['med_name'] + " " + med['expiry'])

        json.dump(data, open('../uch_system/database.json', 'w'), indent=2)

        request_label = Label(meds_window, text="Medication requests")
        request_label.grid(row=1, column=0, pady=10, columnspan=2)

        request_btn = Button(meds_window, text="Request selected medication", command=request)
        request_btn.grid(row=2, column=0, columnspan=2, pady=10)
        if count == 0:
            meds_window.destroy()
            messagebox.showwarning("Notice", "You have not been assigned any prescriptions by your GP")

    def my_summary(self):

        """
        The window that provides patient with summary of their health status.
        Arguments:
            instance of patient class (with the parameters from database)
        Returns:
            set of labels with the information from database
        """

        from datetime import datetime

        # sets up the window and fonts that will be used
        summary_window = Tk()
        summary_window.title('Patient health summary')
        summary_window.geometry('1000x750+80+40')
        fontStyle2 = tkFont.Font(family="Lucida Grande", size=16)

        # demographic information about the patient
        Label(summary_window, text=self.f_name + ' ' + self.l_name, font=fontStyle2).place(
            relx=0.5, rely=0.08, anchor=CENTER)
        if self.dob == 'TBC':  # if patient did not enter the DOB in correct format/ unknown exception
            Label(summary_window, text='Date of Birth: not uploaded').place(relx=0.5, rely=0.13, anchor=CENTER)
            Label(summary_window, text='Age: not uploaded').place(relx=0.5, rely=0.16, anchor=CENTER)
        else:
            datetime_object = datetime.strptime(self.dob, '%d/%m/%Y')  # rewrites the string into datetime object
            datetime_object2 = datetime.strftime(datetime_object, '%d.%m.%Y')  # changes format of datetime object
            Label(summary_window, text='Date of Birth: ' + datetime_object2).place(relx=0.5, rely=0.13, anchor=CENTER)
            age = datetime.today().year - datetime_object.year  # calculates the age
            Label(summary_window, text='Age: ' + str(age)).place(relx=0.5, rely=0.16, anchor=CENTER)
        Label(summary_window, text='NHS number: ' + str(self.nhs_number)).place(relx=0.5, rely=0.19, anchor=CENTER)
        Label(summary_window, text='Telephone number: ' + str(self.tel_number)).place(relx=0.5, rely=0.22,
                                                                                      anchor=CENTER)
        Label(summary_window, text='Gender: ' + self.gender).place(relx=0.5, rely=0.25, anchor=CENTER)

        # prints regular non-prescribed drugs
        if not self.regular_drugs:
            Label(summary_window, text='You have not claimed any regular non-prescribed drugs').place(
                relx=0.5, rely=0.28, anchor=CENTER)
        else:
            drug_string = ''
            for drug in self.regular_drugs:
                drug_string += ('#' + drug + ' ')  # creates string of non-prescription drugs
            Label(summary_window, text='Non-prescription drugs: ' + drug_string).place(relx=0.5, rely=0.28,
                                                                                       anchor=CENTER)

        # prints patient's allergies
        if not self.allergies:
            Label(summary_window, text='You have not claimed any allergies').place(relx=0.5, rely=0.31, anchor=CENTER)
        else:
            allergy_string = ''
            for allergy in self.allergies:
                allergy_string += ('#' + allergy + ' ')  # creates string of allergies
            Label(summary_window, text='Allergies: ' + allergy_string).place(relx=0.5, rely=0.31, anchor=CENTER)

        # BMI calculator with two entries and submit button
        input_weight = Entry(summary_window)
        input_weight.place(relx=0.30, rely=0.36, anchor=CENTER)
        Label(summary_window, text='My Weight [kg]').place(relx=0.15, rely=0.36, anchor=CENTER)
        input_height = Entry(summary_window)
        input_height.place(relx=0.60, rely=0.36, anchor=CENTER)
        Label(summary_window, text='My Height [cm]').place(relx=0.45, rely=0.36, anchor=CENTER)
        calculate_BMI = Button(summary_window, text='Calculate my BMI', command=lambda: bmi_calc_patient())
        calculate_BMI.place(relx=0.78, rely=0.36, anchor=CENTER)

        # calculates the BMI based on the user height and weight entries, returns messagebox
        def bmi_calc_patient():

            try:

                weight = input_weight.get()
                height = input_height.get()

                if float(weight) > 0 and float(height) > 0:

                    BMI = float(weight) / ((float(height) / 100) ** 2)  # standard BMI calculation
                    BMI = int(BMI)
                    if BMI <= 18.5:
                        messagebox.showinfo("BMI",
                                            'Your BMI is ' + str(BMI) + '. This is underweight, contact your GP.')
                    elif 25.0 < BMI <= 30.0:
                        messagebox.showinfo("BMI", 'Your BMI is ' + str(BMI) + '. This is overweight.')
                    elif BMI > 30.0:
                        messagebox.showinfo("BMI", 'Your BMI is ' + str(BMI) + '. This is obese, ask your GP for help.')
                    else:
                        messagebox.showinfo("BMI", 'Your BMI is ' + str(BMI) + '. This is in the healthy range.')

                else:
                    messagebox.showinfo("BMI error", 'We do not accept negative input.')
                    logger.error("Incorrect BMI input")

            except ValueError:
                messagebox.showinfo("BMI error", 'You have not written a correct input.')
                logger.error("Incorrect BMI input")

            except:
                messagebox.showinfo("BMI error", 'We are sorry, the function is not working at the moment, try again '
                                                 'later.')
                logger.error("Incorrect BMI input")

        # prints GP's entry notes from consultations
        Label(summary_window, text='Notes from consultations', font=fontStyle2).place(
            relx=0.5, rely=0.47, anchor=CENTER)
        full_notes = ''
        if len(self.notes) > 0:
            for note in self.notes:  # corrects for longer notes than 1 standard line (breaks into max 3 lines)
                if len(note) > 170:
                    note = note[:170] + '\n' + note[170:]
                elif len(note) > 340:
                    note = note[:170] + '\n' + note[170:340] + '\n' + note[340:]
                if len(note) > 510:
                    logger.critical("Too long note to show.")
                single_note = note + '\n\n'
                full_notes += single_note
        else:
            full_notes = 'Your GP has not uploaded any consultation notes from previous appointments'
        Label(summary_window, text=full_notes).place(relx=0.5, rely=0.55, anchor=CENTER)
        Button(summary_window, text='Return', command=lambda:(summary_window.destroy())).place(
            relx=0.5, rely=0.95, anchor=CENTER)
