import logging
import tkinter.font as tkFont
from tkinter import Label, Button, Entry, ttk, Tk, CENTER

# Create and configure logger
logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
logger = logging.getLogger()


def start_program():
    """
    Window with GP/patient login and registration + admin login
    Arguments:
        user input
    Returns:
        opens the given windows (login/sign-in/admin window)
    """

    global master
    import registration, login

    # sets up the window and fonts
    master = Tk()
    master.title("Welcome to the University College Hospital Portal")
    master.geometry("600x600")
    fontStyle2 = tkFont.Font(family="Lucida Grande", size=16)

    # divides the window into tabs for patient, GP and admin
    tab_control = ttk.Notebook(master)
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab3 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="   Patient   ")
    tab_control.add(tab2, text="     GP      ")
    tab_control.add(tab3, text="    Admin    ")
    tab_control.pack(expand=1, fill="both")

    # patient sign in and registration buttons
    patient_welcome1 = Label(tab1, text="""Welcome to the University College Hospital Patient Portal""",
                             font=fontStyle2, fg='cyan4', bg='#ECECEC')
    patient_welcome2 = Label(tab1, text="""Please sign in, or register your details to make an account.\n
    Admin will approve your details before you can login to the portal.""", bg='#ECECEC')
    patient_welcome1.place(relx=0.5, rely=0.25, anchor=CENTER)
    patient_welcome2.place(relx=0.5, rely=0.335, anchor=CENTER)
    patient_sign_in = Button(tab1, text="Sign in", height="2", width="30", command=lambda: login.patient_login(master))
    patient_sign_in.place(relx=0.5, rely=0.46, anchor=CENTER)
    patient_register = Button(tab1, text="Register", height="2", width="30", command=registration.register_patient)
    patient_register.place(relx=0.5, rely=0.54, anchor=CENTER)

    # gp sign in and registration buttons
    gp_welcome1 = Label(tab2, text="""Welcome to the University College Hospital GP Portal""", font=fontStyle2,
                        fg='cyan4', bg='#ECECEC')
    gp_welcome2 = Label(tab2, text="""Please sign in, or register your details to make an account.\n
    Your details will have to be approved before you can login to the portal.""", bg='#ECECEC')
    gp_welcome1.place(relx=0.5, rely=0.25, anchor=CENTER)
    gp_welcome2.place(relx=0.5, rely=0.335, anchor=CENTER)
    gp_sign_in = Button(tab2, text="Sign in", height="2", width="30", command=lambda: login.gp_login(master))
    gp_sign_in.place(relx=0.5, rely=0.46, anchor=CENTER)
    gp_register = Button(tab2, text="Register", height="2", width="30", command=registration.register_gp)
    gp_register.place(relx=0.5, rely=0.54, anchor=CENTER)

    # admin sign in with username and password entries
    admin_welcome = Label(tab3, text="Enter the Admin login", bg='#ECECEC')
    admin_welcome.place(relx=0.5, rely=0.36, anchor=CENTER)
    admin_username = Label(tab3, text="Admin username:", bg='#ECECEC')
    admin_username.place(relx=0.5, rely=0.42, anchor=CENTER)
    admin_user_entry = Entry(tab3)
    admin_user_entry.place(relx=0.5, rely=0.47, anchor=CENTER)
    admin_password = Label(tab3, text="Admin password:", bg='#ECECEC')
    admin_password.place(relx=0.5, rely=0.52, anchor=CENTER)
    admin_pass_entry = Entry(tab3, show="*")  # writes * when typing password
    admin_pass_entry.place(relx=0.5, rely=0.57, anchor=CENTER)

    # initiates the admin functions
    Button(tab3, text="Sign in", command=lambda: login.admin_login(admin_user_entry, admin_pass_entry)).place(
        relx=0.5, rely=0.63, anchor=CENTER)

    master.mainloop()


class User:
    """
    Class with username, f_name, l_name and password that GP and Patient classes inherit
    """

    def __init__(self, username, f_name, l_name, password):
        self.username = username
        self.f_name = f_name
        self.l_name = l_name
        self.password = password




