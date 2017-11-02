#CMPUT 291 Mini Project 1
#Group Members: Justin Daza. Klark Bliss, Siddhart Khanna
#Project GUI main code to run our application

import tkinter as tk
from tkinter import ttk
from tkinter import *
from mp1 import *
from mp1_models import *

LARGE_FONT = ("Veranda", 18)
SMALL_FONT = ("Veranda", 9)


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
        frame_list = [StartPage, UserDashBoard, Register, AgentLogin, AgentDashBoard]
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

        userLabel= ttk.Label(self, text="UserID",font=SMALL_FONT)
        userLabel.pack()
        userInfo = Entry(self)
        userInfo.pack()
        passLabel = ttk.Label(self, text="Password",font=SMALL_FONT)
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
        if re.match("^[A-Za-z0-9_]*$", username) and re.match("^[A-Za-z0-9_]*$", password):
            if(log_in(username, password) == True):
                controller.show_frame(UserDashBoard)
        else:
            messagebox.showerror("Problem", "Invalid characters")

# User Dashboard after successful login
class UserDashBoard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Welcome", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        Button1 = ttk.Button(self, text="Search for products",
                             command=lambda: self.SearchForProducts())
        Button1.pack()
        Button2 = ttk.Button(self, text="Place an order",
                             command=lambda: self.PlaceAnOrder())
        Button2.pack()
        Button3 = ttk.Button(self, text="List orders",
                             command=lambda: self.ListOrders())
        Button3.pack()
        logoutButton = ttk.Button(self, text="Logout",
                             command=lambda: controller.show_frame(StartPage))
        logoutButton.pack()

    def SearchForProducts(self):
        print("1")
        return

    def PlaceAnOrder(self):
        print("2")
        return

    def ListOrders(self):
        print("3")
        return



# Registration Page for Regular Users
class Register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Register", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        uIDLabel = ttk.Label(self, text="Enter ID",font=SMALL_FONT)
        uIDLabel.pack()
        uIDInfo = Entry(self)
        uIDInfo.pack()
        nameLabel = ttk.Label(self, text="Enter name",font=SMALL_FONT)
        nameLabel.pack()
        nameInfo = Entry(self)
        nameInfo.pack()
        addressLabel = ttk.Label(self, text="Enter address",font=SMALL_FONT)
        addressLabel.pack()
        addressInfo = Entry(self)
        addressInfo.pack()
        passwordLabel = ttk.Label(self, text="Enter password",font=SMALL_FONT)
        passwordLabel.pack()
        passwordInfo = Entry(self, show='*')
        passwordInfo.pack()
        conpasswordLabel = ttk.Label(self, text="Confirm Password",font=SMALL_FONT)
        conpasswordLabel.pack()
        conpasswordInfo = Entry(self, show='*')
        conpasswordInfo.pack()

        registerButton =  ttk.Button(self, text="Register",
                             command=lambda: self.registerUser(controller,uIDInfo.get(),nameInfo.get(),addressInfo.get(),passwordInfo.get(),conpasswordInfo.get()))
        registerButton.pack()
        cancelButton = ttk.Button(self, text="Cancel",
                             command=lambda: controller.show_frame(StartPage))
        cancelButton.pack()

    def registerUser(self,controller, uID, name, address, password,conpass):
        if re.match("^[A-Za-z0-9_]*$", uID) and re.match("^[A-Za-z0-9_]*$", password):
            if(conpass == password):
                if (sign_up(uID, name, address, password) == True):
                    messagebox._show("Success","You have successfully registered your account!")
                    controller.show_frame(StartPage)
            else:
                messagebox.showerror("Different passwords","The passwords you entered must match.")
        else:
            messagebox.showerror("Invalid ID", "Username or Password contains invalid characters")



# Login page for agents
class AgentLogin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Login", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        userLabel = ttk.Label(self, text="AgentID",font=SMALL_FONT)
        userLabel.pack()
        userInfo = Entry(self)
        userInfo.pack()
        passLabel = ttk.Label(self, text="Password",font=SMALL_FONT)
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
        if re.match("^[A-Za-z0-9_]*$", username) and re.match("^[A-Za-z0-9_]*$", password):
            if(agent_log_in(username, password) == True):
                controller.show_frame(AgentDashBoard)
        else:
            messagebox.showerror("Invalid ID", "Username or Password contains invalid characters")

#Dashboard for agents, containing all the actions that agents can perform
class AgentDashBoard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="AgentDashboard", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        Button1 = ttk.Button(self, text="Setup Delivery",
                                 command=lambda: self.SetUpDelivery())
        Button1.pack()
        Button2 = ttk.Button(self, text="Update Delivery",
                             command=lambda: self.UpdateDelivery())
        Button2.pack()
        Button3 = ttk.Button(self, text="Add to Stocks",
                             command=lambda: self.AddToStock())
        Button3.pack()
        logoutButton = ttk.Button(self, text="Logout",
                             command=lambda: controller.show_frame(StartPage))
        logoutButton.pack()
    def SetUpDelivery(self):
        print("1")
        return

    def UpdateDelivery(self):
        print("2")
        return

    def AddToStock(self):
        #Do stuff here
        #When click this go to another page -> ask for sid, pid, qty to change
        
        #then update that
        #then display change
        print("3")
        return



if __name__ == "__main__":
    app = MiniProjectapp()
    app.geometry("270x480")
    app.mainloop()


