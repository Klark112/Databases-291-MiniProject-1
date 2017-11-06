# Back end File for CMPUT 291, Mini-Project 1 App
# Group members: Justin Daza, Klark Bliss, Siddhart Khanna
# This file contains GUI functions

import sqlite3
import tkinter as tk
import time
from tkinter import messagebox
from mp1_app import *
from mp1_models import *

import mp1_globals
# global variable for backend to keep track of user


def log_in(username,password): #NOTE: username and password are currently blank
    DATABASE = mp1_globals.__DBNAME__
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
    DATABASE = mp1_globals.__DBNAME__
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
    DATABASE = mp1_globals.__DBNAME__
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
    DATABASE = mp1_globals.__DBNAME__
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute("SELECT sid, pid FROM carries WHERE sid=:sd AND pid=:pd", 
              {"sd": sid, "pd": pid})
    storeID = c.fetchone()
    
    if(storeID is None):
        c.execute("SELECT sid FROM stores WHERE sid =:sd",{"sd":sid})
        storePIDN = c.fetchone()
        if(storePIDN is None):
            return False                        
        else:    
            conn.commit()
            default = None
            qty = 0
            c.execute("""SELECT pid FROM products WHERE pid=:pd""", {"pd":pid})
            conn.commit()
            result2 = c.fetchone()
            if(result2 is None):
                return False
            else:
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
    DATABASE = mp1_globals.__DBNAME__
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute("""UPDATE carries SET qty= qty + :qt WHERE sid=:sd AND pid=:pd""",
              {"qt":qty, "sd":sid, "pd":pid})
    conn.commit()
    conn.close()          
    
def StockPrice(sid, pid, price):
    DATABASE = mp1_globals.__DBNAME__
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("""UPDATE carries SET uprice =:pr WHERE sid=:sd AND pid=:pd""",
              {"pr":price, "sd":sid, "pd":pid})
    conn.commit()
    conn.close()    

def processOrder(basketItemList):
    DATABASE = mp1_globals.__DBNAME__
    userID = globalUserID
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        # updating the Carries Table with the values of listBasket
        for n in range(len(basketItemList)):
            c.execute("""UPDATE carries SET qty = qty - :qt WHERE sid=:sd AND pid=:pd""",
                      {"qt": basketItemList[n][2], "sd": basketItemList[n][0], "pd": basketItemList[n][1]})
            conn.commit()

            # Adding to olines
            c.execute("""SELECT MAX(oid) FROM olines""")
            conn.commit()
            result = c.fetchall()

            high = result[0]
            newOidOlines = high[0] + 1

            # Getting the uprice for the specific product of specific store
            c.execute("""SELECT uprice FROM carries WHERE sid=:si AND pid=:pi""",
                      {"si": basketItemList[n][0], "pi": basketItemList[n][1]})
            res = c.fetchall()

            # Inserting into olines these products to be ordered
            c.execute("""INSERT INTO olines VALUES (:od, :sd, :pd, :qy, :upr)""",
                      {"od": newOidOlines, "sd": basketItemList[n][0], "pd": basketItemList[n][1], "qy": basketItemList[n][2],
                       "upr": res[0][0]})

            # creating a new order for all these products
        c.execute("""SELECT MAX(oid) FROM orders""")
        conn.commit()
        result = c.fetchall()
        high = result[0]
        newOid = high[0] + 1

        # for getting the users address
        c.execute("""SELECT c1.address FROM customers c1 WHERE c1.cid =:useID""", {"useID": userID})
        conn.commit()
        resultAddress2 = c.fetchone()

        # for creating the dates
        dates2 = time.strftime("%Y/%m/%d")

        # generating a new order
        c.execute("""INSERT INTO orders VALUES (:od, :cd, :date, :adr)""",
                  {"od": newOid, "cd": userID, "date": dates2, "adr": resultAddress2[0]})
        conn.commit()
        conn.close()
        messagebox.showinfo("Order Placed", "Your order has been placed")

    except Exception as ex:
        conn.rollback()
        conn.commit()
        conn.close()
        messagebox.showinfo("Error", "Something went wrong processing your order")
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)



# def listItems(self, userID, listBasket):
# DATABASE = mp1_globals.__DBNAME__
# conn = sqlite3.connect(DATABASE)
# c = conn.cursor()
# for n in range(len(listBasket)):
#     #getting the quantity of the products that are; that specific sid and pid
#     c.execute("""SELECT c1.qty FROM carries c1 WHERE c1.sid =:sd AND c1.pid=:pd""",
#               {"sd":listBasket[n][0], "pd":listBasket[n][1]})
#     conn.commit()
#     k = []
#     res = c.fetchone()
#     #if the qty ordered higher than the one the store has:
#     if(listBasket[n][2]>res[0]):
#         i = 1
#         mylabel = Label(self, text = "Quantity too High.\nChange Quantity or Delete"+"", font = ("Verdana", 8))
#         mylabel.pack()
#         k.append(n)
#         #upInfo = Entry(self)
#         #upInfo.pack()
#         #updateButton = ttk.Button(self, text="Update", command=lambda: updateListBasket(self, userID, listBasket, n, upInfo.get()))
#         #updateButton.pack()
#         #deleteButton = ttk.Button(self, text="Delete", command=lambda: deleteListBasket(self, userID, listBasket, n))
#         #deleteButton.pack()
#     else:
#         mylabel2 = Label(self, text = "In Process", font = ("Verdana", 8))
#         mylabel2.pack()
#         #if(i==0 & n == (len(listBasket)-1)):
#         #if(n == (len(listBasket)-1)):
#         #print("Passing to the end")
#             #finalOrder(self, userID, listBasket)
#     #n = n + 1
# contButton = ttk.Button(self, text="Fix Qty", command=lambda: cont(self, listBasket, k, userID))
# contButton.pack()
#
# def cont(self, listBasket, k, userID):
# #If position [1,3] are incorrect and want to fix there quantity
# # the for loop just iterates through the list without caring if value was added
# for t in range(len(k)):
#     upInfo = Entry(self)
#     upInfo.pack()
#     updateButton = ttk.Button(self, text="Update", command=lambda: updateListBasket(self, userID, listBasket, t, upInfo.get(), k))
#     updateButton.pack()
#     deleteButton = ttk.Button(self, text="Delete", command=lambda: deleteListBasket(self, userID, listBasket, t, k))
#     deleteButton.pack()
# finalizeButton = ttk.Button(self, text="Finish", command=lambda: finalOrder(self, userID, listBasket))
# finalizeButton.pack()

# def finalOrder(self, userID, listBasket):
#     DATABASE = mp1_globals.__DBNAME__
#     conn = sqlite3.connect(DATABASE)
#     c = conn.cursor()
#     #updating the Carries Table with the values of listBasket
#     for n in range(len(listBasket)):
#         c.execute("""UPDATE carries SET qty = qty - :qt WHERE sid=:sd AND pid=:pd""",
#                   {"qt":listBasket[n][2], "sd":listBasket[n][0], "pd":listBasket[n][1]})
#         conn.commit()
#
#         #Adding to olines
#         c.execute("""SELECT MAX(oid) FROM olines""")
#         conn.commit()
#         result = c.fetchall()
#
#         high = result[0]
#         newOidOlines = high[0]+1
#
#         #Getting the uprice for the specific product of specific store
#         c.execute("""SELECT uprice FROM carries WHERE sid=:si AND pid=:pi""",
#                   {"si":listBasket[n][0], "pi":listBasket[n][1]})
#         res = c.fetchall()
#
#         #Inserting into olines these products to be ordered
#         c.execute("""INSERT INTO olines VALUES (:od, :sd, :pd, :qy, :upr)""",
#                   {"od":newOidOlines, "sd":listBasket[n][0], "pd":listBasket[n][1], "qy":listBasket[n][2], "upr":res[0][0]})
#
#     #creating a new order for all these products
#     c.execute("""SELECT MAX(oid) FROM orders""")
#     conn.commit()
#     result = c.fetchall()
#     high = result[0]
#     newOid = high[0] + 1
#
#
#     #for getting the users address
#     c.execute("""SELECT c1.address FROM customers c1 WHERE c1.cid =:useID""",{"useID":userID})
#     conn.commit()
#     resultAddress2 = c.fetchone()
#
#     #for creating the dates
#     dates2 = time.strftime("%Y/%m/%d")
#
#     #generating a new order
#     c.execute("""INSERT INTO orders VALUES (:od, :cd, :date, :adr)""",
#               {"od":newOid, "cd":userID, "date":dates2, "adr":resultAddress2[0]})
#     conn.commit()
#
#
#     mylabel = Label(self, text = "Order Placed", font = ("Verdana", 8))
#     mylabel.pack()
#def listItems(self, userID, listBasket, n):
    #conn = sqlite3.connect(DATABASE)
    #c = conn.cursor()
    
    #NextButton = ttk.Button(self, text="NextOrder", command=lambda: itemInList(self, userID,listBasket, n))
    #NextButton.pack()
    
#def itemInList(self, userID, listBasket, n):
    #conn = sqlite3.connect(DATABASE)
    #c = conn.cursor()    
    #if(n<len(listBasket)):
        ##print(listBasket[n:n+1])
        #product = listBasket[n:n+1]
        #c.execute("""SELECT c1.qty FROM carries c1 WHERE c1.sid =:sd AND c1.pid=:pd""",
                    #{"sd":product[n][0], "pd":product[n][1]})
        #conn.commit()
        #res = c.fetchone()
        #print(product[0][2])
        #print(res[0])
        #if(product[0][2]>res[0]):
            #mylabel = Label(self, text = "Quantity too High. Enter quantity or del to delete", font = ("Verdana", 8))
            #mylabel.pack()
            #upInfo = Entry(self)
            #upInfo.pack()
            #if(upInfo.get() != 'del'):
                #listBasket[n][2] = upInfo.get()
                #updateButton = ttk.Button(self, text="Update", command=lambda: listItems(self, userID, listBasket, n))
                #updateButton.pack()                
                
            #else:
                #listBasket.remove(n)
                #deleteButton = ttk.Button(self, text="Delete", command=lambda: listItems(self, userID, listBasket, n))
                #deleteButton.pack()                 
                
        #else:
            #mylabel = Label(self, text = "Placed in Order", font = ("Verdana", 8))
            #mylabel.pack()        
        
    #else:
        #mylabel = Label(self, text = "No more products", font = ("Verdana", 8))
        #mylabel.pack()
    #n= n +1
