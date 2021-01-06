import json
from tkinter import messagebox, Label, Toplevel, Button, END, Entry
from uch_system.patient_functions import patient_portal
from uch_system.gp_functions.gp import GP
from uch_system.patient_functions.patient import Patient
import logging

from uch_system.gp_functions import gp_portal

# Create and configure logger
logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')

# Creating an object
logger = logging.getLogger()


def gp_login(master):
    """Tkinter window for gp login.
    :param master: initial programme window.
    :return: request_gp_sign_in.
    """
    gp_login_screen = Toplevel()
    gp_login_screen.title("Login to your account")
    gp_login_screen.geometry("400x250")
    Label(gp_login_screen, text="Please enter your username and password").pack()

    gp_username_label = Label(gp_login_screen, text="Username:")
    gp_username_label.pack()
    gp_username_entry = Entry(gp_login_screen)
    gp_username_entry.pack()

    gp_password_label = Label(gp_login_screen, text="Password:")
    gp_password_label.pack()
    gp_password_entry = Entry(gp_login_screen, show="*")
    gp_password_entry.pack()

    def request_gp_sign_in(username, password):
        """Login to the GP home screen.
        :param username: input username created from registration.
        :param password: input password created from registration.
        :return: userportal.gp_portal.
        """
        gp_username_entry.delete(0, END)
        gp_password_entry.delete(0, END)

        gp_database = json.load(open('gp_database.json'))

        if username in gp_database:
            if gp_database[username]["password"] == password:
                if gp_database[username]["Verified"] is False:
                    logging.info("Admin needs to verify gp.")
                    messagebox.showinfo("Information", "Still awaiting verification by admin")
                else:
                    gp_login_screen.destroy()

                    gp = GP(gp_database[username]["username"],
                            gp_database[username]["First Name"],
                            gp_database[username]["Last Name"],
                            gp_database[username]["password"],
                            gp_database[username]["GMC_Number"],
                            gp_database[username]["assigned_patients"],
                            gp_database[username]["Verified"],
                            gp_database[username]["Availability"]["Monday Start"],
                            gp_database[username]["Availability"]["Monday End"],
                            gp_database[username]["Availability"]["Tuesday Start"],
                            gp_database[username]["Availability"]["Tuesday End"],
                            gp_database[username]["Availability"]["Wednesday Start"],
                            gp_database[username]["Availability"]["Wednesday End"],
                            gp_database[username]["Availability"]["Thursday Start"],
                            gp_database[username]["Availability"]["Thursday End"],
                            gp_database[username]["Availability"]["Friday Start"],
                            gp_database[username]["Availability"]["Friday End"])

                    logging.info("gp login successful.")
                    gp_login_screen.destroy()
                    master.destroy()
                    gp_portal.gp_portal(gp)
            if gp_database[username]["password"] != password:
                Label(gp_login_screen, text="Your username or password was incorrect. Please try again.").pack()
                logging.warning("Incorrect gp login details entered.")
        else:
            Label(gp_login_screen, text="Your username or password was incorrect. Please try again.").pack()
            logging.warning("Incorrect gp login details entered.")

    login_click = Button(gp_login_screen, text="Sign in", command=lambda: request_gp_sign_in(gp_username_entry.get(),
                                                                                             gp_password_entry.get()))
    login_click.pack(pady=10)


def patient_login(master):
    """Tkinter window for patient login.
    :param master: initial programme window.
    :return: request_sign_in.
    """
    login_screen = Toplevel()
    login_screen.title("Login to your account")
    login_screen.geometry("400x250")
    Label(login_screen, text="Please enter your username and password").pack()

    username_label = Label(login_screen, text="Username:")
    username_label.pack()
    username_entry = Entry(login_screen)
    username_entry.pack()

    password_label = Label(login_screen, text="Password:")
    password_label.pack()
    password_entry = Entry(login_screen, show="*")
    password_entry.pack()

    def request_sign_in(username, password):
        """checks input with json database key:values to sign in.
        :param username: username input
        :param password: password input
        :return: userportal.patient_portal
        """
        username_entry.delete(0, END)
        password_entry.delete(0, END)

        database = json.load(open('database.json'))
        if username in database:
            if database[username]["password"] == password:
                if database[username]["Verified"] is False:
                    logging.info("Admin needs to verify patient.")
                    messagebox.showinfo("Information", "Still awaiting verification by admin")
                else:
                    patient = create_patient_instance(username)
                    logging.info("Patient login successful.")
                    login_screen.destroy()
                    master.destroy()
                    patient_portal.patient_portal(patient)
            if database[username]["password"] != password:
                Label(login_screen, text="Your username or password was incorrect. Please try again").pack()
                logging.warning("Incorrect patient login details entered.")
        else:
            Label(login_screen, text="Your username or password was incorrect. Please try again.").pack()
            logging.warning("Incorrect patient login details entered.")

    login_click = Button(login_screen, text="Sign in", command=lambda: request_sign_in(username_entry.get(),
                                                                                       password_entry.get()))
    login_click.pack(pady=10)


def admin_login(admin_user_entry, admin_pass_entry):
    """Login to the admin portal.
    :param admin_user_entry: admin username.
    :param admin_pass_entry: admin password.
    :return: admin_side.admin_home().
    """
    import admin
    if admin_user_entry.get() == "admin" and admin_pass_entry.get() == "admin":
        logging.info("Successful admin login")
        admin_user_entry.delete(0, END)
        admin_pass_entry.delete(0, END)
        admin.admin_home()
    else:
        messagebox.showinfo("Invalid login", "Your username or password was incorrect. Please try again.")
        logging.warning("Invalid admin login.")
        admin_user_entry.delete(0, END)
        admin_pass_entry.delete(0, END)


def create_patient_instance(username):
    """Creates instance of patient class.
    :param username: key for json database.
    :return: instance of patient class.
    """
    database = json.load(open('database.json'))
    patient = Patient(database[username]["username"],
                      database[username]["First Name"],
                      database[username]["Last Name"],
                      database[username]["password"],
                      database[username]["gender"],
                      database[username]["DOB"],
                      database[username]["tel_number"],
                      database[username]["regular_drugs"],
                      database[username]["prescriptions"],
                      database[username]["NHS_number"],
                      database[username]["assigned_gp"],
                      database[username]["Verified"],
                      database[username]["Feedback"],
                      database[username]["Notes"],
                      database[username]["Allergies"],
                      database[username]['Referral'])
    json.dump(database, open('database.json', 'w'))
    return patient
