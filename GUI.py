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
        self.generate_password_btn.grid(row=3, sticky=E)

        self.retrieve_password_btn = Button(self, text="Retrieve Password", command=self._retrieve_password_btn_clicked)
        self.retrieve_password_btn.grid(row=3, column=1)

        self.pack()

    def _generate_password_btn_clicked(self):
        # print("Clicked")
        username = self.entry_username.get()
        url = self.entry_username.get()
        masterPassword = self.entry_password.get()

        #print(username, password)4

        if username == "" and url == "" and masterPassword == "":
            tm.showinfo("Login info", "Welcome Gabor, you are looking very wealthy today!!")
        else:
            tm.showerror("Password Fetch Error", "Incorrect Credentials")

    def _retrieve_password_btn_clicked(self):
        # print("Clicked")
        username = self.entry_username.get()
        url = self.entry_username.get()
        masterPassword = self.entry_password.get()

        #print(username, password)4

        if username == "" and url == "" and masterPassword == "":
            tm.showinfo("Login info", "Welcome Gabor, you are looking very wealthy today!!")
        else:
            tm.showerror("Password Fetch Error", "Incorrect Credentials")

root = Tk()
lf = LoginFrame(root)
root.mainloop()
