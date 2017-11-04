# Back end File for CMPUT 291, Mini-Project 1 App
# Group members: Justin Daza, Klark Bliss, Siddhart Khanna
# This file contains GUI functions

import sqlite3
import tkinter as tk
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
