import tkinter as tk
from tkinter import ttk
from tkinter import *
from mp1 import *

LARGE_FONT = ("Veranda", 18)
SMALL_FONT = ("Veranda", 12)

def main():
    app = MiniProjectapp()
    app.geometry("270x480")
    app.mainloop()


class MiniProjectapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "291_MiniProject1")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # List of all pages 
        frame_list = [StartPage, DashBoard, Register, AgentLogin]
        for F in frame_list:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):  # function to move desired frame to the front
        frame = self.frames[cont]
        frame.tkraise()


# Initial Login Page
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Login", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        userLabel= ttk.Label(self, text="UserID")
        userLabel.pack()
        userInfo = Entry(self)
        userInfo.pack()
        passLabel = ttk.Label(self, text="Password")
        passLabel.pack()
        passInfo = Entry(self, show="*")
        passInfo.pack()

        loginButton = ttk.Button(self, text="Login",
                             command=lambda: self.LoginCheck(controller,userInfo.get(),passInfo.get()))
        loginButton.pack()

        registerButton = ttk.Button(self, text="Register",
                             command=lambda: controller.show_frame(Register))
        registerButton.pack()

        agentButton = ttk.Button(self, text="Agent?",
                             command=lambda: controller.show_frame(AgentLogin))
        agentButton.pack()

        quitButton = ttk.Button(self, text="Quit",
                             command= quit)
        quitButton.pack()

    def LoginCheck(self, controller,username, password):
        if(log_in(username, password) == True):
            controller.show_frame(DashBoard)


# User-Specific dashboard after successful login
class DashBoard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Dashboard", font=LARGE_FONT)

        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Logout",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()


# Registration Page for Regular Users
class Register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Register", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Cancel",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

# Login page for agents
class AgentLogin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Login", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        userLabel = ttk.Label(self, text="AgentID")
        userLabel.pack()
        userInfo = Entry(self)
        userInfo.pack()
        passLabel = ttk.Label(self, text="Password")
        passLabel.pack()
        passInfo = Entry(self, show="*")
        passInfo.pack()

        loginButton = ttk.Button(self, text="Login",
                                 command=lambda: self.AgentLoginCheck(controller, userInfo.get(), passInfo.get()))
        loginButton.pack()


        button1 = ttk.Button(self, text="Return",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

    def AgentLoginCheck(self, controller,username, password):
        if(agent_log_in(username, password) == True):
            controller.show_frame(DashBoard)


main()
