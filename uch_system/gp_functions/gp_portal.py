import tkinter.font as tkFont
from tkinter import Label, Button, CENTER, Tk
import logging

# Create and configure logger
logging.basicConfig(filename="../uch_system/newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
logger = logging.getLogger()


def gp_portal(gp):
    """
    The main portal for the gp with 7 buttons - connect to other functions: appointment_today, consultation,
     consultation help tools, prescriptions, appointments and see_feedback + return button.
    Arguments:
        instance of a GP class (includes methods that the function initiates and details of the gp)
    Returns:
        initiates functions consultation, see_feedback (methods of the GP class), appointment_today, appointments
         (takes 'gp' instance as an argument) + consultation_help and prescription (irrespective of the GP)
    """

    import uch_system.gp_functions.gp_helpers as gp_helpers
    import uch_system.gp_functions.gp_appointment_schedule as gp_appointment_schedule

    # sets up the window and the fonts that will be used
    window = Tk()
    window.geometry("800x600")
    window.title('GP portal UCLH')
    fontStyle = tkFont.Font(family="Lucida Grande", size=14)

    # welcome label + details of the gp (full name, GMC number)
    Label(window, text='Welcome to your UCLH GP portal', fg='cyan4', font=('Lucinda Grande', 19)).place(
        relx=0.5, rely=0.25, anchor=CENTER)
    Label(window, text='Dr ' + gp.f_name + ' ' + gp.l_name + ';  GMC number: ' + str(gp.gmc_number)). \
        place(relx=0.5, rely=0.3, anchor=CENTER)
    Label(window, text='MENU', font=fontStyle).place(relx=0.5, rely=0.43, anchor=CENTER)

    # Six main buttons that send user to the given functions
    Button(window, text="New consultation", width=20, command=lambda: gp.consultation()).place(
        relx=0.5, rely=0.5, anchor=CENTER)
    Button(window, text="Today's appointments", width=20, command=lambda: gp_appointment_schedule.app_today(gp)).place(
        relx=0.5, rely=0.555, anchor=CENTER)
    Button(window, text="See appointment schedule", width=20, command=lambda: gp_appointment_schedule.gp_appointments(gp)). \
        place(relx=0.5, rely=0.61, anchor=CENTER)
    Button(window, text="See feedback and requests", width=20, command=lambda: gp.see_feedback()).place(
        relx=0.5, rely=0.665, anchor=CENTER)
    Button(window, text="Help tools", width=20, command=lambda: gp_helpers.consultation_help(window)).place(
        relx=0.5, rely=0.72, anchor=CENTER)

    # destroys the window and returns to the login/sign in screen
    def return_home():
        window.destroy()
        from uch_system.core import start_program
        start_program()
        logger.info("Returned to main screen")

    Button(window, text="Return", command=return_home).place(relx=0.5, rely=0.9, anchor=CENTER)

    window.mainloop()
