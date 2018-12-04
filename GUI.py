from tkinter import *
import tkinter.messagebox as tm

class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_username = Label(self, text="Username")
        self.label_url = Label(self, text="URL")
        self.label_password = Label(self, text="Master Password")

        self.entry_username = Entry(self)
        self.entry_url = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=0, sticky=E)
        self.label_url.grid(row=1, sticky=E)
        self.label_password.grid(row=2, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_url.grid(row=1, column=1)
        self.entry_password.grid(row=2, column=1)

        self.generate_password_btn = Button(self, text="Generate Password", command=self._generate_password_btn_clicked)
        self.generate_password_btn.grid(row=3, column=0)

        self.retrieve_password_btn = Button(self, text="Retrieve Password", command=self._retrieve_password_btn_clicked)
        self.retrieve_password_btn.grid(row=3, column=1)

        self.new_master_btn = Button(self, text="Create a new Master Password?", command=self._new_master_btn_clicked)
        self.new_master_btn.grid(row=4, columnspan = 2)

        self.pack()

    def _generate_password_btn_clicked(self):

        username = self.entry_username.get()
        url = self.entry_username.get()
        masterPassword = self.entry_password.get()

        # LAUNCH CODE FOR GENERATE PASSWORD

        masterPassword = None

    def _retrieve_password_btn_clicked(self):

        username = self.entry_username.get()
        url = self.entry_username.get()
        masterPassword = self.entry_password.get()

        # LAUNCH CODE FOR RETRIEVE PASSWORD

        masterPassword = None

    def _set_master_password(newMaster):
        print(newMaster)
        # NEED TO LAUNCH PASSWORD CHANGE FROM HERE
        newMaster = None

    def _reset_password_btn_clicked(top, newMaster):
        _set_master_password(newMaster)
        top.destroy()

    def _new_master_btn_clicked(self):

        top = Toplevel()

        label_instructions = Label(top, text="If creating a Master Password for the first time, leave the 'Current Password' field blank")
        label_instructions.grid(row=0, columnspan=2)

        label_old = Label(top, text="Current Master Password")
        label_old.grid(row=1, sticky=E)

        label_new = Label(top, text="New Master Password")
        label_new.grid(row=2, sticky=E)

        entry_old = Entry(top, show="*")
        entry_old.grid(row=1, column=1)

        entry_new = Entry(top, show="*")
        entry_new.grid(row=2, column=1)

        submit_button = Button(top, text="Submit", command=top.destroy) ## PASS newMaster here
        submit_button.grid(row=3, columnspan=2)
        top.pack()

root = Tk()
lf = LoginFrame(root)
root.mainloop()
