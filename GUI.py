from tkinter import *
import tkinter.messagebox as tm

import subprocess
from subprocess import PIPE, Popen

class LoginFrame(Frame):
    P = None

    def launch_master_password_program(self):
        cmd = 'master_password.py'
        # it will execute script which runs only `function1`
        P = Popen(["python", cmd], stdin=PIPE, stdout=PIPE, bufsize=1)
        text = p.stdout.readline()
        self.toplevel_launch(text)
        #toplevel_launch(output.strip())

    def toplevel_launch(self, msg):
        top = Toplevel()

        label = Message(top, text=msg)
        label.pack()

        button = Button(top, text="Dismiss", command=top.destroy)
        button.pack()


    def __init__(self, master):
        super().__init__(master)

        # main UI work #
        self.password_prompt = Label(self, text="Generate or Retrieve a Password?")
        self.password_prompt.grid(row=0, columnspan = 2)

        self.label_username = Label(self, text="Username")
        self.label_url = Label(self, text="URL")
        self.label_password = Label(self, text="Master Password")

        self.entry_username = Entry(self)
        self.entry_url = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=1, sticky=E)
        self.label_url.grid(row=2, sticky=E)
        self.label_password.grid(row=3, sticky=E)
        self.entry_username.grid(row=1, column=1)
        self.entry_url.grid(row=2, column=1)
        self.entry_password.grid(row=3, column=1)

        self.generate_password_btn = Button(self, text="Generate Password", command=self._generate_password_btn_clicked)
        self.generate_password_btn.grid(row=4, column=0)

        self.retrieve_password_btn = Button(self, text="Retrieve Password", command=self._retrieve_password_btn_clicked)
        self.retrieve_password_btn.grid(row=4, column=1)

        self.new_master_prompt = Label(self, text="Create a New Master Password?")
        self.new_master_prompt.grid(row=5, columnspan = 2)

        self.label_instructions = Label(self, text="If creating a Master Password for the first time, leave the 'Current Password' field blank")
        self.label_instructions.grid(row=6, columnspan=2)

        self.label_old = Label(self, text="Current Master Password")
        self.label_old.grid(row=7, sticky=E)

        self.label_new = Label(self, text="New Master Password")
        self.label_new.grid(row=8, sticky=E)

        self.entry_old = Entry(self, show="*")
        self.entry_old.grid(row=7, column=1)

        self.entry_new = Entry(self, show="*")
        self.entry_new.grid(row=8, column=1)

        self.submit_button = Button(self, text="Submit", command=self._reset_password_btn_clicked) ## PASS newMaster here
        self.submit_button.grid(row=9, columnspan=2)

        self.pack()

        self.launch_master_password_program()


    def _generate_password_btn_clicked(self):

        username = self.entry_username.get()
        url = self.entry_username.get()
        masterPassword = self.entry_password.get()

        # LAUNCH CODE FOR GENERATE PASSWORD
        self.toplevel_launch(username)

        masterPassword = None

    def _retrieve_password_btn_clicked(self):

        username = self.entry_username.get()
        url = self.entry_username.get()
        masterPassword = self.entry_password.get()

        # LAUNCH CODE FOR RETRIEVE PASSWORD

        masterPassword = None

    def _reset_password_btn_clicked(self):
        newMaster = self.entry_new.get();

root = Tk()
lf = LoginFrame(root)
root.mainloop()
