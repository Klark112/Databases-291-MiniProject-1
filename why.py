#MP!_APP##############################
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

globalUserID = ""

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
        frame_list = [StartPage, UserDashBoard, Register, AgentLogin, AgentDashBoard, Stock, placeOrder]
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
        
        globalUserID = userInfo
        
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
                             command=lambda: controller.show_frame(placeOrder))
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
                             command=lambda: controller.show_frame(Stock))
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

class Stock(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)        
        userLabel4= ttk.Label(self, text="Enter Store ID(sid)",font=SMALL_FONT)
        userLabel4.pack()
        sidInfo = Entry(self)
        sidInfo.pack()    
        
        userLabel3= ttk.Label(self, text="Enter Product ID(pid)",font=SMALL_FONT)
        userLabel3.pack()
        pidInfo = Entry(self)
        pidInfo.pack()        
        
        CheckButton = ttk.Button(self, text="Check",
                             command=lambda: self.StockImplement(sidInfo.get(), pidInfo.get()))
        CheckButton.pack()
        
        buttonReturn = ttk.Button(self, text="Return",
                             command=lambda: controller.show_frame(AgentDashBoard))
        buttonReturn.pack()            
        
    def StockImplement(self, sid, pid):
        #display quantity button
        if(StockCheck(self, sid, pid)==True):
            userLabel= ttk.Label(self, text="Enter Qty",font=SMALL_FONT)
            userLabel.pack()
            qtyInfo = Entry(self)
            qtyInfo.pack()                
            qtyButton = ttk.Button(self, text="Add Quantity", command=lambda: StockQTY(sid,pid, qtyInfo.get()))
            qtyButton.pack()
        
            userLabel2= ttk.Label(self, text="Enter Price",font=SMALL_FONT)
            userLabel2.pack()
            priceInfo = Entry(self)
            priceInfo.pack()                
            priceButton = ttk.Button(self, text="Change Price", command=lambda: StockPrice(sid,pid, priceInfo.get()))
            priceButton.pack()         
            
        else:
            mylabel = Label(self, text = "Store Not Present", font = ("Verdana", 12))
            mylabel.pack()

class placeOrder(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)   
        basketItem = Label(self, text = "Items in Basket", font = ("Verdana", 12))
        basketItem.pack()
        
        listBasket = [[1, 'p1', 4],[2, 'p4', 4],[1, 'p1', 5], [1, 'p2', 9]] #sid, pid, qty
        checkQuantity = ttk.Button(self, text="Check Quantity", command=lambda: listItems(self, globalUserID, listBasket))
        checkQuantity.pack()        
        
        
        
if __name__ == "__main__":
    app = MiniProjectapp()
    app.geometry("270x480")
    app.mainloop()




#MP1#######################3
# Back end File for CMPUT 291, Mini-Project 1 App
# Group members: Justin Daza, Klark Bliss, Siddhart Khanna
# This file contains GUI functions

import sqlite3
import tkinter as tk
import time
from tkinter import messagebox
from mp1_app import *
from mp1_models import *

DATABASE = 'mp1.db'
# global variable for backend to keep track of user
USER = ""

def log_in(username,password): #NOTE: username and password are currently blank
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(" SELECT cid FROM customers WHERE customers.cid=:un",{"un":username})
    result = c.fetchone()
    try:
        if(result[0] == username):
            c.execute(" SELECT cid, pwd FROM customers WHERE customers.pwd=:pw AND customers.cid=:un", {"pw": password, "un": username})
            result = c.fetchone()
            # print(result[1])
            if(result[1] == password):
                conn.commit()
                conn.close()
                setUser(username)
                return True
            else:
                messagebox.showinfo("Invalid Login", "The username or password you entered is incorrect.")
                conn.commit()
                conn.close()
                return False
        else:
            messagebox.showinfo("Invalid Login", "The username or password you entered is incorrect.")
            conn.commit() #NOTE: I don't think we need this commit statement since we aren't changing anything
            conn.close()
            return False
    except TypeError:
        messagebox.showinfo("Invalid Login","The username or password you entered is incorrect." )

    return False


def agent_log_in(username, password):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(" SELECT aid FROM agents WHERE agents.aid=:un", {"un": username})
    result = c.fetchone() 
    
    try:
        if (result[0] == username):
            c.execute(" SELECT aid, pwd FROM agents WHERE agents.pwd=:pw AND agents.aid=:un",
                      {"pw": password, "un": username})
            result = c.fetchone()
            # print(result[1])
            if (result[1] == password):
                conn.commit()
                conn.close()
                setUser(username)
                return True
            else:
                messagebox.showinfo("Invalid Login", "The username or password you entered is incorrect.")
                conn.commit()
                conn.close()
                return False
        else:
            messagebox.showinfo("Invalid Login", "The username or password you entered is incorrect.")
            conn.commit()  # NOTE: I don't think we need this commit statement since we aren't changing anything
            conn.close()
            return False
    except TypeError:
        messagebox.showinfo("Invalid Login", "The username or password you entered is incorrect.")

    return False


def setUser(username):
    global USER
    USER = username

def getUser():
    global USER
    return USER

def sign_up(cid, name, address,pwd): #customer(cid, name, address, pwd)
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute(""" INSERT INTO customers(cid, name, address, pwd) VALUES (?, ?, ?, ?)""", (cid,name,address,pwd))
        conn.commit()
        conn.close()
        return(True)
    except sqlite3.IntegrityError:
        conn.rollback()
        conn.commit()
        conn.close()
        messagebox.showerror("Invalid ID", "Invalid Registration Info. ID may have already been taken")
    except Exception as ex:
        conn.rollback()
        conn.commit()
        conn.close()
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        messagebox.showerror("Signup error", message)


def StockCheck(self, sid, pid):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute("SELECT sid, pid FROM carries WHERE sid=:sd AND pid=:pd", 
              {"sd": sid, "pd": pid})
    storeID = c.fetchone()
    
    if(storeID is None):
        c.execute("SELECT sid FROM carries WHERE sid =:sd",{"sd":sid})
        storePIDN = c.fetchone()
        if(storePIDN is None):
            return False                        
        else:    
            conn.commit()
            default = None
            qty = 0
            mylabel = Label(self, text = "Product not present(Added to store)", font = ("Verdana", 8))
            mylabel.pack()            
            c.execute("""INSERT INTO carries VALUES(:sd, :pd, :qty, :def)""",
                      {"sd":sid, "pd":pid,"qty":qty, "def":default})
            conn.commit()   
            conn.close()            
            return True
    else:
        if((storeID[0])==int(sid)):
            if(storeID[1] == pid):
                conn.commit()
                conn.close()             
                return True
            
        else:
            conn.commit()
            conn.close()         
            return False    

def StockQTY(sid, pid, qty):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute("""UPDATE carries SET qty= qty + :qt WHERE sid=:sd AND pid=:pd""",
              {"qt":qty, "sd":sid, "pd":pid})
    conn.commit()
    conn.close()          
    
def StockPrice(sid, pid, price):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("""UPDATE carries SET uprice =:pr WHERE sid=:sd AND pid=:pd""",
              {"pr":price, "sd":sid, "pd":pid})
    conn.commit()
    conn.close()    
    
def listItems(self, userID, listBasket):
    for n in range(len(listBasket)):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()        
        c.execute("""SELECT c1.qty FROM carries c1 WHERE c1.sid =:sd AND c1.pid=:pd""",
                 {"sd":listBasket[n][0], "pd":listBasket[n][1]})
        conn.commit()
        res = c.fetchall()
       
        if(listBasket[n][2]>res[0][0]):
            mylabel = Label(self, text = "Quantity too High.\nEnter different quantity \nOr delete Item", font = ("Verdana", 8))
            mylabel.pack()
            myInfo = Entry(self)
            myInfo.pack()
            updateButton = ttk.Button(self, text="Update", command=lambda: updateList(self, myInfo.get(), n, listBasket))
            updateButton.pack()
            deleteButton = ttk.Button(self, text="Delete",command=lambda: deleteList(self, n, listBasket))
            deleteButton.pack()            
            
        else:
            mylabel2 = Label(self, text = "Order Placed", font = ("Verdana", 9))
            mylabel2.pack()             
            #update the table after placing an order
            c.execute("""UPDATE carries SET qty = qty - :qt WHERE sid=:sd AND pid=:pd""",
                      {"qt":listBasket[n][2], "sd":listBasket[n][0], "pd":listBasket[n][1]})
            conn.commit()
        
        #for generating the oid
        c.execute("""SELECT oid FROM orders""")
        conn.commit()
        result = c.fetchall()

        high = result[0]  
        for each in result:
            if high < each:
                high = each

        newOid = high[0] + 1  

        #for getting the users address
        c.execute("""SELECT c1.address FROM customers c1 WHERE c1.cid =:userID""",{"userID":userID})
        conn.commit()
        resultAddress = c.fetchone()
        #for creating the dates
        dates = time.strftime("%Y/%m/%d")
        #generating a new order
        c.execute("""INSERT INTO orders VALUES (:od, :cd, :date, :adr)""", 
                  {"od":newOid, "cd":userID, "date":dates, "adr":resultAddress[0]})
        conn.commit()
      
            
def updateList(self, valueQty, pos, listBasket):
    #print(pos)
    listBasket[pos][2] = valueQty
    listItems(self, listBasket)

def deleteList(self, pos, listBasket):
    listBasket.pop(pos)
    listItems(self, listBasket)