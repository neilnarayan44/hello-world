from tkinter import Toplevel, Label, Button, messagebox, CENTER, W, IntVar, Checkbutton
import tkinter.font as tkFont
import logging

# Create and configure logger
logging.basicConfig(filename="../uch_system/newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
logger = logging.getLogger()


def consultation_help(window):

    """

    Gives three options of Framingham heart failure risk, depression diagnostics and COVID-19 diagnostics.

    Arguments:
        window where the function roots
        entries in each function

    Returns:
        messagebox (COVID checker)
        label update (Framingham heart failure risk, depression diagnostics)

    """

    # sets up the window and fonts
    root = Toplevel(window)
    root.geometry("350x520")
    root.title('Consultation help tools')
    fontStyle2 = tkFont.Font(family="Lucida Grande", size=13)

    def f_calc():

        """
        Opens a window with 14 checkboxes for the symptoms, user chooses and then runs the calculate_hf_risk to return
        the label with positive/negative heart failure diagnosis

        Arguments:
            local scope variables: major1-major8, minor1-minor6 (integer 0/1 variables)

        Returns:
            label indicating positive/ negative HF diagnosis
        """

        # destroys the previous grid (instead of new window opening)
        f_calc_button.destroy()
        COVID_calc_button.destroy()
        depress_calc_button.destroy()

        # criteria saved as major, integer variables
        Label(root, text="Major Criteria", font=fontStyle2, pady=10).grid(row=0, column=0)
        major1 = IntVar()
        c = Checkbutton(root, text="Acute Pulmonary edema", variable=major1)
        c.grid(row=1, column=0, sticky=W)
        major2 = IntVar()
        c = Checkbutton(root, text="Cardiomegaly", variable=major2)
        c.grid(row=2, column=0, sticky=W)
        major3 = IntVar()
        c = Checkbutton(root, text="Hepatojugular reflux", variable=major3)
        c.grid(row=3, column=0, sticky=W)
        major4 = IntVar()
        c = Checkbutton(root, text="Neck vein distention", variable=major4)
        c.grid(row=4, column=0, sticky=W)
        major5 = IntVar()
        c = Checkbutton(root, text="Paroxysmal nocturnal dyspnea or orthopnea", variable=major5)
        c.grid(row=5, column=0, sticky=W)
        major6 = IntVar()
        c = Checkbutton(root, text="Pulmonary rales", variable=major6)
        c.grid(row=6, column=0, sticky=W)
        major7 = IntVar()
        c = Checkbutton(root, text="Third heart sound", variable=major7)
        c.grid(row=7, column=0, sticky=W)
        major8 = IntVar()
        c = Checkbutton(root, text="Weight loss >4.5kg in 5 days in response to treatment", variable=major8)
        c.grid(row=8, column=0, sticky=W)

        # criteria saved as minor, integer variables
        Label(root, text="Minor Criteria", font=fontStyle2, pady=10).grid(row=9, column=0)
        minor1 = IntVar()
        c = Checkbutton(root, text="Ankle Edema", variable=minor1)
        c.grid(row=10, column=0, sticky=W)
        minor2 = IntVar()
        c = Checkbutton(root, text="Dyspnea on exertion", variable=minor2)
        c.grid(row=11, column=0, sticky=W)
        minor3 = IntVar()
        c = Checkbutton(root, text="Hepatomegaly", variable=minor3)
        c.grid(row=12, column=0, sticky=W)
        minor4 = IntVar()
        c = Checkbutton(root, text="Nocturnal Cough", variable=minor4)
        c.grid(row=13, column=0, sticky=W)
        minor5 = IntVar()
        c = Checkbutton(root, text="Pleural effusion", variable=minor5)
        c.grid(row=14, column=0, sticky=W)
        minor6 = IntVar()
        c = Checkbutton(root, text="Tachycardia (HR>120)", variable=minor6)
        c.grid(row=15, column=0, sticky=W, pady=(0, 10))

        # submits the checkbox information (major + minor variables) into calculate_hf_risk function
        submit_button = Button(root, text="Evaluate heart failure diagnosis", command=lambda: calculate_hf_risk(minor1,
                                                                                                                minor2,
                                                                                                                minor3,
                                                                                                                minor4,
                                                                                                                minor5,
                                                                                                                minor6,
                                                                                                                major1,
                                                                                                                major2,
                                                                                                                major3,
                                                                                                                major4,
                                                                                                                major5,
                                                                                                                major6,
                                                                                                                major7,
                                                                                                                major8,
                                                                                                                major8))
        submit_button.grid(row=16, column=0)

        # returns back to the help tools selection
        return_button = Button(root, text='Return', command=lambda: (root.destroy(), consultation_help(window)))
        return_button.place(relx=0.9, rely=0.05, anchor=CENTER)

    # Takes IntVariables, converts into 0/1, sums up and calculates the full score, updates label with diagnosis
    def calculate_hf_risk(*args):
        minor = 0
        major = 0

        for i in range(6):
            minor += args[i].get()      # adds up the 0/1 to a final minor score
        for i in range(6, 14):
            major += args[i].get()      # adds up the 0/1 to a final major score

        if major >= 2 or (major == 1 and minor >= 2):       # criterion for positive diagnostics
            label = Label(root, text="Positive for Heart Failure", font=fontStyle2)
            label.grid(row=21, column=0)
            logger.info("HF diagnosis evaluated")
        else:
            label = Label(root, text="Negative for Heart Failure", font=fontStyle2)
            label.grid(row=21, column=0)
            logger.info("HF diagnosis evaluated")

    def depress_calc():

        """
        Opens a window with 8 checkboxes for the symptoms, user chooses and then runs the calculate_depressionrisk to
        return the label with positive/negative depression diagnosis

        Arguments:
            local scope variables: major1-major2, minor1-minor6 (integer 0/1 variables)

        Returns:
            label indicating positive/ negative depression diagnosis
        """

        root.geometry("320x370")

        # destroys the previous grid (instead of new window opening)
        f_calc_button.destroy()
        COVID_calc_button.destroy()
        depress_calc_button.destroy()

        # criteria saved as major, integer variables
        Label(root, text="Major criteria (past 2 weeks)", font=fontStyle2, pady=10).grid(row=0, column=0)
        major1 = IntVar()
        Checkbutton(root, text="Depressed mood most of the day", variable=major1).grid(row=1, column=0, sticky=W)
        major2 = IntVar()
        Checkbutton(root, text="Loss of interest or pleasure", variable=major2).grid(row=2, column=0, sticky=W)

        # criteria saved as minor, integer variables
        Label(root, text="Minor Criteria (past 2 weeks)", font=fontStyle2, pady=10).grid(row=9, column=0)
        minor1 = IntVar()
        Checkbutton(root, text="Significant weight loss/weight gain", variable=minor1).grid(row=10, column=0, sticky=W)
        minor2 = IntVar()
        Checkbutton(root, text="Slowing down of thought/physical movement", variable=minor2).grid(
            row=11, column=0, sticky=W)
        minor3 = IntVar()
        Checkbutton(root, text="Fatigue", variable=minor3).grid(row=12, column=0, sticky=W)
        minor4 = IntVar()
        Checkbutton(root, text="Feeling of worthlessness/guilt", variable=minor4).grid(row=13, column=0, sticky=W)
        minor5 = IntVar()
        Checkbutton(root, text="Diminished ability to think", variable=minor5).grid(row=14, column=0, sticky=W)
        minor6 = IntVar()
        Checkbutton(root, text="Suicidal ideation", variable=minor6).grid(row=15, column=0, sticky=W, pady=(0, 10))

        # submits the checkbox information (major + minor variables) into calculate_depressionrisk function
        Button(root, text="Evaluate depression diagnosis",
               command=lambda: calculate_depressrisk(minor1, minor2, minor3, minor4, minor5, minor6,
                                                     major1, major2)).grid(row=16, column=0)

        # returns back to the help tools selection
        return_button = Button(root, text='Return', command=lambda: (root.destroy(), consultation_help(window)))
        return_button.place(relx=0.9, rely=0.05, anchor=CENTER)

    # Takes IntVariables, converts into 0/1, sums up and calculates the full score, updates label with diagnosis
    def calculate_depressrisk(*args):
        minor = 0
        major = 0

        for i in range(6):
            minor += args[i].get()      # adds up the 0/1 to a final minor score
        for i in range(6, 8):
            major += args[i].get()      # adds up the 0/1 to a final minor score
        if ((major == 1) and (minor >= 4)) or ((major == 2) and (minor >= 3)):      # criteria for positive diagnosis
            Label(root, text="Positive diagnosis of clinical depression", font=fontStyle2).grid(row=21, column=0)
            logger.info("Depression diagnosis evaluated")
        else:
            Label(root, text="Negative diagnosis of clinical depression", font=fontStyle2).grid(row=21, column=0)
            logger.info("Depression diagnosis evaluated")

    def check_covid(root):

        """
        Opens a window with 5 checkboxes for the symptoms, user chooses and then runs the covid_submit to return the
        messagebox with COVID-19 positive or negative symptoms.

        Arguments:
            window where check_covid originates
            local scope variables: var1-var5 (integer 0/1 variables indicating presence of COVID symptoms)

        Returns:
            messagebox with recommendation to take a test/ stay alert
        """

        # sets up the window
        window = Toplevel(root)
        window.title('COVID symptoms')
        window.geometry('340x220')
        fontStyle2 = tkFont.Font(family="Lucida Grande", size=16)
        Label(window, text="Check what applies to the patient:", font=fontStyle2, pady=10).grid(row=0, column=0)

        # introduces the variables and checkboxes, IntVar = integer variable of 0/1 based on being checked/unchecked
        var1 = IntVar()
        c = Checkbutton(window, text="New persistent cough", variable=var1)
        c.grid(row=1, column=0, sticky=W)
        var2 = IntVar()
        c = Checkbutton(window, text="Loss of smell", variable=var2)
        c.grid(row=2, column=0, sticky=W)
        var3 = IntVar()
        c = Checkbutton(window, text="Loss of taste", variable=var3)
        c.grid(row=3, column=0, sticky=W)
        var4 = IntVar()
        c = Checkbutton(window, text="High temperature", variable=var4)
        c.grid(row=4, column=0, sticky=W)
        var5 = IntVar()
        c = Checkbutton(window, text="They had contact with COVID-19 positive person", variable=var5)
        c.grid(row=5, column=0, sticky=W, pady=(0, 10))

        # submit button that calls the covid_submit function with all the IntVariables above + destroys the window
        submit_button = Button(window, text="Submit",
                               command=lambda: (covid_submit(var1, var2, var3, var4, var5), window.destroy()))
        submit_button.grid(row=16, column=0)

        window.mainloop()

    # Takes IntVariables, converts into 0/1, sums up and calculates the full score, raises a messagebox of
    # symptom indication
    def covid_submit(*args):
        full_score = 0
        for i in range(5):
            full_score += args[i].get()     # adds up the 0/1 to a final score
        if full_score >= 1:     # checking any box indicates that the person should get tested
            messagebox.showinfo("COVID-19", "Patient is likely to have COVID-19. Please, sign them up for a test: "
                                            "https://www.gov.uk/get-coronavirus-test.")
            logger.info("COVID diagnosis evaluated")
        else:
            messagebox.showinfo("COVID-19", "At the moment they do not have indications of COVID-19.")
            logger.info("COVID diagnosis evaluated")

    # helper tools buttons selection
    f_calc_button = Button(root, text="Calculate Framingham score", command=f_calc)
    f_calc_button.place(relx=0.5, rely=0.4, anchor=CENTER)
    COVID_calc_button = Button(root, text='Check COVID symptoms', command=lambda: check_covid(root))
    COVID_calc_button.place(relx=0.5, rely=0.5, anchor=CENTER)
    depress_calc_button = depress_calc_button = Button(root, text="Check depression symptoms", command=depress_calc)
    depress_calc_button.place(relx=0.5, rely=0.6, anchor=CENTER)

    root.mainloop()
