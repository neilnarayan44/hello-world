import json
from tkinter import Label, Button, Toplevel, Entry, ttk, messagebox, END
import logging
import datetime

# Create and configure logger
logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')

# Creating an object
logger = logging.getLogger()


def register_gp():
    """Tkinter programme for gp registration.
    :return: register_gp_button().
    """
    gp_register = Toplevel()
    gp_register.title("Register to create an account")
    gp_register.geometry("500x400")
    Label(gp_register, text="Enter your details to make an account.\n"
                            "Your details will need to be verified by an admin before you can login.").grid(row=0,
                                                                                                            column=2, padx=40)

    first_name_label = Label(gp_register, text="First name:")
    first_name_label.grid(row=1, column=2)
    first_name_entry = Entry(gp_register)
    first_name_entry.grid(row=2, column=2)

    last_name_label = Label(gp_register, text="Last name:")
    last_name_label.grid(row=3, column=2)
    last_name_entry = Entry(gp_register)
    last_name_entry.grid(row=4, column=2)

    username_label = Label(gp_register, text="Create Username:")
    username_label.grid(row=5, column=2)
    gp_username_entry = Entry(gp_register)
    gp_username_entry.grid(row=6, column=2)

    password_label = Label(gp_register, text="Create Password:")
    password_label.grid(row=7, column=2)
    gp_password_entry = Entry(gp_register, show="*")
    gp_password_entry.grid(row=8, column=2)

    gmc_label = Label(gp_register, text="7-digit GMC Number")
    gmc_label.grid(row=9, column=2)
    gmc_entry = Entry(gp_register)
    gmc_entry.grid(row=10, column=2)

    def register_gp_button():
        """Creates new GP profile. Entered into json gp database.
        :return: messagebox for registration confirmation.
        """
        error = 0
        gp_database = json.load(open("gp_database.json"))

        # checks if all fields were filled
        if (gp_username_entry.get() == "" or gp_password_entry.get() == "" or first_name_entry.get() == "" or
                last_name_entry.get() == "" or gmc_entry.get() == ""):
            Label(gp_register, text="Please enter all required fields.").grid(row=12, column=2)
            logger.info("Empty fields for gp registration.")
            error += 1

        # checks the format of the username, name and if the username is unique
        if gp_username_entry.get() in gp_database.keys():
            gp_register.geometry("800x400")
            Label(gp_register, text="Username already taken. Please choose another.").grid(row=6, column=3)
            logger.warning("Username already in database.")
            gp_username_entry.delete(0, END)
            error += 1
        if gp_username_entry == " ":
            gp_register.geometry("800x400")
            Label(gp_register, text="Please enter a valid username.").grid(row=6, column=3)
            logger.info("Space given as username.")
            gp_username_entry.delete(0, END)
            error += 1
        if first_name_entry.get() == " ":
            gp_register.geometry("800x400")
            Label(gp_register, text="Please enter your given first name.").grid(row=2, column=3)
            logger.info("Space given as first name.")
            first_name_entry.delete(0, END)
            error += 1
        if any(i.isdigit() for i in first_name_entry.get()):
            gp_register.geometry("800x400")
            Label(gp_register, text="Please enter your given first name.").grid(row=2, column=3)
            logger.info("Number in first name. Invalid input.")
            first_name_entry.delete(0, END)
            error += 1
        if last_name_entry.get() == " ":
            gp_register.geometry("800x400")
            Label(gp_register, text="Please enter your given last name.").grid(row=4, column=3)
            logger.info("Space given as last name.")
            last_name_entry.delete(0, END)
            error += 1
        if any(i.isdigit() for i in last_name_entry.get()):
            gp_register.geometry("800x400")
            Label(gp_register, text="Please enter your given last name.").grid(row=4, column=3)
            logger.info("Number in last name. Invalid input.")
            last_name_entry.delete(0, END)
            error += 1

        # checks the format of GMC number
        if len(gmc_entry.get()) != 7:
            gp_register.geometry("800x400")
            Label(gp_register, text="GMC Number Invalid - Please enter 7 digits.").grid(row=10, column=3)
            logger.info("GMC number length invalid.")
            gmc_entry.delete(0, END)
            error += 1
        try:
            int(gmc_entry.get())
        except ValueError:
            gp_register.geometry("800x400")
            Label(gp_register, text="GMC Number Invalid - Please enter 7 digits").grid(row=10, column=3)
            logger.info("GMC number input not integers.")
            gmc_entry.delete(0, END)
            error += 1

        # checks if the GMC number is unique
        gmc_list = []
        for gp in gp_database.keys():
            gmc_list.append(str(gp_database[gp]['GMC_Number']))
        if str(gmc_entry.get()) in gmc_list:
            gp_register.geometry("800x400")
            Label(gp_register, text="GMC Number Invalid - already registered.").grid(row=10, column=3)
            logger.warning("GMC number already in database.")
            gmc_entry.delete(0, END)
            error += 1
        json.dump(gp_database, open('gp_database.json', 'w'))

        if error == 0:
            gp_database = json.load(open('gp_database.json'))
            gp_database[gp_username_entry.get()] = {"username": gp_username_entry.get(),
                                                    "password": gp_password_entry.get(),
                                                    "First Name": first_name_entry.get(),
                                                    "Last Name": last_name_entry.get(),
                                                    "GMC_Number": gmc_entry.get(),
                                                    "assigned_patients": [],
                                                    "Verified": False,
                                                    "Holidays": [],
                                                    "Availability": {"Monday Start": "09:00", "Monday End": "16:50",
                                                                     "Tuesday Start": "09:00", "Tuesday End": "16:50",
                                                                     "Wednesday Start": "09:00", "Wednesday End":
                                                                         "16:50",
                                                                     "Thursday Start": "09:00", "Thursday End": "16:50",
                                                                     "Friday Start": "09:00", "Friday End": "16:50",
                                                                     "Lunch": "13:00"}}

            json.dump(gp_database, open('gp_database.json', 'w'))
            logger.info("New GP Profile created: {}".format(gp_username_entry.get()))
            gp_register.destroy()
            messagebox.showinfo("Registration", "Thank you for registering your details. These will be reviewed by a "
                                                "member of the admin team within 24 hours, who will then "
                                                "activate your account.")

    Button(gp_register, text="Register", command=register_gp_button).grid(row=11, column=2, pady=10)


def register_patient():
    """Tkinter programme for registering patients as json database entries.
    :return: register_button().
    """
    register_screen = Toplevel()
    register_screen.title("Register to create an account")
    register_screen.geometry("720x550")
    Label(register_screen, text="Please enter your details to create an account\n"
                                "Your details will need to be verified by an admin\n"
                                "before you can sign in.").grid(row=0, column=1)

    first_name_label = Label(register_screen, text="First name:")
    first_name_label.grid(row=1, column=1)
    first_name_entry = Entry(register_screen)
    first_name_entry.grid(row=2, column=1)

    last_name_label = Label(register_screen, text="Last name:")
    last_name_label.grid(row=3, column=1)
    last_name_entry = Entry(register_screen)
    last_name_entry.grid(row=4, column=1)

    genders_label = Label(register_screen, text="Gender:")
    genders_label.grid(row=5, column=1)
    genders_options = ttk.Combobox(register_screen)
    genders_options["values"] = ("Male", "Female", "Prefer not to say")
    genders_options.grid(row=6, column=1)

    dob_label = Label(register_screen, text="Date of Birth:")
    dob_label.grid(row=7, column=1)
    day_options = ttk.Combobox(register_screen)
    day_options["values"] = ("Day", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                             "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                             "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31")
    day_options.current(0)
    day_options.grid(row=8, column=0, padx=5)

    month_options = ttk.Combobox(register_screen)
    month_options["values"] = ("Month", "1", "2", "3", "4", "5", "6",
                               "7", "8", "9", "10", "11", "12")
    month_options.current(0)
    month_options.grid(row=8, column=1)
    year_options = ttk.Combobox(register_screen)
    year_options["values"] = ("Year", "2005", "2004", "2003", "2002", "2001", "2000", "1999", "1998", "1997",
                              "1996", "1995", "1994", "1993", "1992", "1991", "1990", "1989", "1988", "1987",
                              "1986", "1985", "1984", "1983", "1982", "1981", "1980", "1979", "1978", "1977",
                              "1976", "1975", "1974", "1973", "1972", "1971", "1970", "1969", "1968", "1967",
                              "1966", "1965", "1964", "1963", "1962", "1961", "1960", "1959", "1958", "1957",
                              "1956", "1955", "1954", "1953", "1952", "1951", "1950", "1949", "1948", "1947",
                              "1946", "1945", "1944", "1943", "1942", "1941", "1940", "1939", "1938", "1937",
                              "1936", "1935", "1934", "1933", "1932", "1931", "1930", "1929", "1928", "1927",
                              "1926", "1925", "1924", "1923", "1922", "1921", "1920")
    year_options.current(0)
    year_options.grid(row=8, column=2)

    phone_number_label = Label(register_screen, text="Telephone number:")
    phone_number_label.grid(row=9, column=1)
    phone_number_entry = Entry(register_screen)
    phone_number_entry.grid(row=10, column=1)

    nhs_number_label = Label(register_screen, text="NHS number:")
    nhs_number_label.grid(row=11, column=1)
    nhs_number_entry = Entry(register_screen)
    nhs_number_entry.grid(row=12, column=1)

    username_label = Label(register_screen, text="Create Username:")
    username_label.grid(row=13, column=1)
    username_entry = Entry(register_screen)
    username_entry.grid(row=14, column=1)

    password_label = Label(register_screen, text="Create Password:")
    password_label.grid(row=15, column=1)
    password_entry = Entry(register_screen, show="*")
    password_entry.grid(row=16, column=1)

    def register_button():
        """Creates patient entry in json database.
        :return: messagebox for registration success.
        """
        error = 0
        if (username_entry.get() == "" or password_entry.get() == "" or first_name_entry.get() == "" or
                last_name_entry.get() == "" or genders_options.get() == "" or nhs_number_entry.get() == "" or
                day_options.get() == "" or month_options.get() == "" or year_options.get() == ""
                or phone_number_entry.get() == ""):
            Label(register_screen, text="Please enter all required fields.").grid(row=18, column=1)
            logging.info("Empty fields for patient registration.")
            error += 1
        database = json.load(open("database.json"))

        # checks formats of username and name + checks if username is unique
        if username_entry.get() in database.keys():
            register_screen.geometry("1000x550")
            Label(register_screen, text="Username already taken. Please choose another.").grid(row=14, column=4)
            logging.warning("Username already in patient database.")
            username_entry.delete(0, END)
            error += 1
        if username_entry.get() == " ":
            register_screen.geometry("1000x550")
            Label(register_screen, text="Invalid username. Please choose another.").grid(row=14, column=4)
            logging.info("Space given as username.")
            error += 1
        if any(i.isdigit() for i in first_name_entry.get()):
            register_screen.geometry("1000x550")
            Label(register_screen, text="Please enter your given first name.").grid(row=2, column=4)
            logging.info("Digit in first name. Invalid input.")
            first_name_entry.delete(0, END)
            error += 1
        if first_name_entry.get() == " ":
            register_screen.geometry("1000x550")
            Label(register_screen, text="Please enter your given first name.").grid(row=2, column=4)
            logging.info("Space given as first name.")
            first_name_entry.delete(0, END)
            error += 1
        if any(i.isdigit() for i in last_name_entry.get()):
            register_screen.geometry("1000x550")
            Label(register_screen, text="Please enter your given last name.").grid(row=4, column=4)
            logging.info("Digit in last name. Invalid input.")
            last_name_entry.delete(0, END)
            error += 1
        if last_name_entry.get() == " ":
            register_screen.geometry("1000x550")
            Label(register_screen, text="Please enter your given last name.").grid(row=4, column=4)
            logging.info("Space given as last name.")
            last_name_entry.delete(0, END)
            error += 1

        # checks gender option format
        if genders_options.get() not in genders_options["values"]:
            register_screen.geometry("1000x550")
            Label(register_screen, text="Please choose a valid option.").grid(row=6, column=4)
            logging.info("Invalid gender entered.")
            error += 1

        # checks the validity of date of birth
        try:
            datetime.date(int(year_options.get()), int(month_options.get()), int(day_options.get()))
        except ValueError:
            register_screen.geometry("1000x550")
            Label(register_screen, text="Invalid Date of Birth Entered.").grid(row=8, column=4)
            logging.info("Invalid date of birth entered.")
            error += 1

        # checks the format of telephone number
        try:
            int(phone_number_entry.get())
        except ValueError:
            register_screen.geometry("1000x550")
            Label(register_screen, text="Telephone number must be 11 digits.").grid(row=10, column=4)
            logging.info("Telephone number not integers.")
            phone_number_entry.delete(0, END)
            error += 1
        if len(str(phone_number_entry.get())) != 11:
            register_screen.geometry("1000x550")
            Label(register_screen, text="Telephone number must be 11 digits.").grid(row=10, column=4)
            logging.info("Telephone number not 11 digits.")
            phone_number_entry.delete(0, END)
            error += 1

        # checks the format of the NHS number
        try:
            int(nhs_number_entry.get())
        except ValueError:
            register_screen.geometry("1000x550")
            Label(register_screen, text="Invalid NHS number").grid(row=12, column=4)
            logging.info("NHS number input not integers.")
            nhs_number_entry.delete(0, END)
            error += 1
        if len(str(nhs_number_entry.get())) != 10:
            register_screen.geometry("1000x550")
            Label(register_screen, text="Invalid NHS number - Please enter 10 digits.").grid(row=12, column=4)
            logging.info("NHS number not 10 integers.")
            nhs_number_entry.delete(0, END)
            error += 1

        # checks if NHS number already in the database
        nhs_list = []
        for patient in database.keys():
            nhs_list.append(str(database[patient]['NHS_number']))
        if str(nhs_number_entry.get()) in nhs_list:
            register_screen.geometry("1000x550")
            Label(register_screen, text="Invalid NHS number - number already registered").grid(row=12, column=4)
            logging.warning("NHS number already in database.")
            nhs_number_entry.delete(0, END)
            error += 1
        json.dump(database, open("database.json", "w"))

        if error == 0:
            database = json.load(open('database.json'))
            database[username_entry.get()] = {"username": username_entry.get(),
                                              "password": password_entry.get(),
                                              "First Name": first_name_entry.get(),
                                              "Last Name": last_name_entry.get(),
                                              "gender": genders_options.get(),
                                              "DOB": day_options.get() + "/" + month_options.get() +
                                                     "/" + year_options.get(),
                                              "tel_number": phone_number_entry.get(),
                                              "regular_drugs": [],
                                              "prescriptions": [],
                                              "NHS_number": nhs_number_entry.get(),
                                              "assigned_gp": "",
                                              "Verified": False,
                                              "Feedback": [],
                                              "Notes": [],
                                              "Allergies": [],
                                              'Referral': ''}

            json.dump(database, open('database.json', 'w'))
            logger.info("New Patient Profile created: {}".format(username_entry.get()))
            register_screen.destroy()
            messagebox.showinfo("Registration", "Thank you for registering your details. These will be reviewed by a "
                                                "member of the admin team within 24 hours, who will then activate "
                                                "your account.")

    Button(register_screen, text="Register", command=register_button).grid(row=17, column=1, pady=10)
    
