import tkinter.font as tkFont
from tkinter import Label, Button, CENTER, Tk
import uch_system.patient_functions.patient_booking as patient_booking
import datetime
import json
import logging

# Create and configure logger
logging.basicConfig(filename="../uch_system/newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
logger = logging.getLogger()


def patient_portal(patient):
    """
    The main portal for the patient with 6 buttons - connect to other functions: my_summary, booking_system,
    prescription, give_feedback and check_covid + return button.
    Arguments:
        instance of a Patient class (includes methods that the function initiates and details of the patient)
        json gp_database (used to find the full name of the assigned GP)
    Returns:
        initiates functions my_summary, prescription, give_feedback, check_covid (methods of the Patient class) and
        booking_system (takes 'patient' instance as an argument)
    """

    # sets up the window and the fonts that will be used
    window = Tk()
    window.geometry("800x600")
    window.title('Patient portal UCLH')
    fontStyle = tkFont.Font(family="Lucida Grande", size=14)

    # welcome label + details of the patient (full name, NHS number)
    Label(window, text='Welcome to your UCLH patient portal', fg='cyan4', font=('Lucinda Grande', 19)).place(
        relx=0.5, rely=0.25, anchor=CENTER)
    Label(window, text='Patient: ' + patient.f_name.capitalize() + ' ' + patient.l_name.capitalize() +
                       '; NHS number: ' + str(patient.nhs_number)).place(relx=0.5, rely=0.3, anchor=CENTER)

    # if the json database contains referral of the patient to different UCLH department, labels the department and
    # date of referral
    if patient.referral != '':
        Label(window, text='You were referred to UCLH ' + patient.referral + ' on ' +
                           str(datetime.date.today().strftime('%d/%m/%Y')) + '.').place(relx=0.5, rely=0.36,
                                                                                        anchor=CENTER)

    # finds the full name of patient's GP (based on the GMC_number of assigned GP that is in the patient instance)
    # in the gp_database and prints it
    if patient.assigned_gp == '':
        Label(window, text='No assigned GP').place(relx=0.5, rely=0.33, anchor=CENTER)
    else:
        gp_database = json.load(open('../uch_system/gp_database.json'))
        gp_list = list(gp_database.keys())
        for gp in gp_list:
            if str(gp_database[gp]['GMC_Number']) == patient.assigned_gp:
                gp_username = gp
        gp_string = 'Your GP is Dr ' + gp_database[gp_username]['First Name'].capitalize() + ' ' + \
                    gp_database[gp_username]['Last Name'].capitalize()
        Label(window, text=gp_string).place(relx=0.5, rely=0.33, anchor=CENTER)
        json.dump(gp_database, open('../uch_system/gp_database.json', 'w'))

    Label(window, text='MENU', font=fontStyle).place(relx=0.5, rely=0.43, anchor=CENTER)

    # Five main buttons that send user to the given functions
    Button(window, text="Appointments", width=20, command=lambda: patient_booking.booking_system(patient)).place(
        relx=0.5, rely=0.5, anchor=CENTER)
    Button(window, text="My Health Summary", width=20, command=lambda: patient.my_summary()).place(
        relx=0.5, rely=0.555, anchor=CENTER)
    Button(window, text="View/Order Prescriptions", width=20, command=patient.prescription).place(
        relx=0.5, rely=0.61, anchor=CENTER)
    Button(window, text="Check COVID symptoms", width=20, command=lambda: patient.check_covid(window)).place(
        relx=0.5, rely=0.665, anchor=CENTER)
    Button(window, text="Give feedback", width=20, command=lambda: patient.give_feedback()).place(
        relx=0.5, rely=0.72, anchor=CENTER)

    # destroys the window and returns to the login/sign in screen
    def return_home():
        window.destroy()
        from core import start_program
        start_program()
        logger.info("Returned to main screen")

    Button(window, text="Return", command=return_home).place(relx=0.5, rely=0.9, anchor=CENTER)


