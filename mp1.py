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

def processOrder(basketItemList, userID):   #Function handles the data changes
    DATABASE = mp1_globals.__DBNAME__

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute("""SELECT MAX(oid) FROM orders""")
        conn.commit()
        result = c.fetchall()
        high = result[0]
        newOid = high[0] + 1

        for item in basketItemList:
            # updating the Carries Table with the values of listBasket
            c.execute("""UPDATE carries SET qty = qty - :qt WHERE sid=:sd AND pid=:pd""",
                      {"qt": item[2], "sd": item[0], "pd": item[1]})
            conn.commit()

            # Getting the uprice for the specific product of specific store
            c.execute("""SELECT uprice FROM carries WHERE sid=:si AND pid=:pi""",
                      {"si": item[0], "pi": item[1]})
            res = c.fetchall()

            # Inserting into olines these products to be ordered
            c.execute("""INSERT INTO olines(oid, sid, pid, qty, uprice) VALUES (:od, :sd, :pd, :qy, :upr)""",
                      {"od": newOid, "sd": item[0], "pd": item[1], "qy": item[2],
                       "upr": res[0][0]})


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
        messagebox.showinfo("Order Placed", "Your order has been placed. \n Order ID: "+str(newOid))

    except Exception as ex:
        conn.rollback()
        conn.commit()
        conn.close()
        messagebox.showinfo("Error", "Something went wrong processing your order")
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)


def list_orders(username):
    DATABASE = mp1_globals.__DBNAME__
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT ol.oid, od.odate, ol.qty, ol.uprice from olines ol,orders od where ol.oid=od.oid and od.cid=:un",
              {"un": username})
    list_oo = c.fetchall()
    #print(list_oo)
    list_total = []
    list_order_tuple = [0, '', 0, 0]  # order id, order date, the number of products ordered and the total price
    total_qty = 0
    current_oid = -1
    for i in list_oo:
        #print(i)
        if (i[0] != current_oid):
            list_total.append(list_order_tuple[:])
            list_order_tuple[0] = i[0]
            list_order_tuple[1] = i[1]
            list_order_tuple[2] = 0
            list_order_tuple[3] = 0
            current_oid = i[0]

        if (i[0] == current_oid):
            list_order_tuple[2] += i[2]
            list_order_tuple[3] += i[2] * i[3]

    list_total.append(list_order_tuple[:])
    conn.commit()
    conn.close()
    list2 = []
    for t in list_total[1:]:
        list2.append(t)
        
    #print(list2)
    return list2

def show_details(username, order_id):  # get oid from list_objects[0]
    DATABASE = mp1_globals.__DBNAME__
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
   SELECT de.trackingno, de.pickUpTime, de.dropOffTime, od.address
   FROM deliveries de, orders od
   WHERE de.oid=od.oid and od.cid=:un and od.oid=:oi
   ''', {"un": username, "oi": order_id})
    list_delivery = c.fetchall()
    c.execute('''
   SELECT ol.sid, st.name, ol.pid, pr.name, ol.qty, pr.unit ,ol.uprice
   FROM olines ol, stores st, products pr
   WHERE ol.sid=st.sid and ol.pid=pr.pid and ol.oid=:oi''', {"oi": order_id})
    list_details = c.fetchall()
    list_delivery.append(list_details)
    conn.commit()
    conn.close()
    return list_delivery
