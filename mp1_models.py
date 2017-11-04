# Back end File for CMPUT 291, Mini-Project 1 App
# Group members: Justin Daza, Klark Bliss, Siddhart Khanna
# File contains back-end functions and Models for the data schema

import sqlite3
import tkinter as tk
from tkinter import messagebox
from mp1 import *
import uuid
import datetime

DATABASE = 'mp1.db'
########################################################################################################################
# FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# General back-end function to return # of rows in a table
def getTableSize(table):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    query = {'deliveries':" SELECT COUNT(*) FROM deliveries",
        'agents': " SELECT COUNT(*) FROM agents",
        'stores':" SELECT COUNT(*) FROM stores",
        'categories': " SELECT COUNT(*) FROM categories",
        'products': " SELECT COUNT(*) FROM products",
        'carries':" SELECT COUNT(*) FROM carries",
        'customers':" SELECT COUNT(*) FROM customers",
        'orders':" SELECT COUNT(*) FROM orders",
        'olines':" SELECT COUNT(*) FROM olines",
         }[table]
    c.execute(query)
    result = c.fetchone()
    conn.commit()
    conn.close()
    return result[0]


########################################################################################################################
# CLASSES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Model Classes for database tables

class Delivery():
    trackingNumList =[] # Used to identify if tracking number is unique
    def __init__(self,pickupTime = None, orders= []):
        self.orders = orders
        self.trackingNum = self.generateTrackNumber()
        self.pickUpTime = pickupTime
        self.dropOffTime = None

    def generateTrackNumber(self): # generates a unique tracking number
        i = True
        while i:
            num = uuid.uuid4().int & (1<<12)-1
            if num not in self.trackingNumList:
                i = False
        return num

    def getTrackingNum(self):
        return self.trackingNum

    def addOrders(self, newOrders): # add set of oids to the delivery orders and add new rows to the database
        self.orders += newOrders
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        for oid in newOrders:
            # Insert a row for each Order
            c.execute("""INSERT INTO deliveries(trackingNo, oid, pickUpTime, dropOffTime) VALUES(?, ?, ?, ?) """,
                      (self.trackingNum,oid,self.pickUpTime, self.dropOffTime))
        conn.commit()
        conn.close()

    def getOrders(self):    #return list of orders associated to the current trackingNum
        return self.orders

    def saveDelivery(self):   # for every order added to this delivery, insert new row into data table
        # TODO: CHECK IF ORDER ID IS VALID
        try:
            if self.trackingNum not in self.trackingNumList:
                self.trackingNumList.append(self.trackingNum)
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            for oid in self.orders:
                c.execute("""INSERT INTO deliveries(trackingNo, oid, pickUpTime, dropOffTime) VALUES(?, ?, ?, ?) """,
                          (self.trackingNum, oid, self.pickUpTime, self.dropOffTime))
            conn.commit()
            conn.close()
        except Exception as ex:
            conn.rollback()
            conn.commit()
            conn.close()
            print("Error saving new delivery")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def updateTimes(self, trackingNum, oID, pickUpTime, dropOffTime):   #Updates pickUp
        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("UPDATE deliveries SET pickUpTime = :pt, dropOffTime = :dt WHERE trackingNo = :tn AND oID = :id",
                      {"pt":pickUpTime,"dt":dropOffTime,"tn":trackingNum,"id":oID})
            conn.commit()
            conn.close()
        except Exception as ex:
            conn.rollback()
            conn.commit()
            conn.close()
            print("Error updating delivery times")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def getDelivery(self, trackingNum):  # Function retrieves data related to trackingNum
        try:
            self.trackingNum = trackingNum
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("SELECT pickUpTime, dropOffTime FROM deliveries WHERE trackingNo = :id", {"id": trackingNum})
            result = c.fetchone()
            self.pickUpTime = result[0]
            self.dropOffTime = result[1]

            orderlist = []
            c.execute("SELECT oid FROM deliveries WHERE trackingNo = :id",{"id": trackingNum})
            result = c.fetchall()
            for i in result:
                orderlist.append(i)
            self.orders = orderlist
            conn.commit()
            conn.close()

        except Exception as ex: #TODO: Print message saying trackingNum does not exist
            conn.rollback()
            conn.commit()
            conn.close()
            print("ERROR getting deliveries")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def removeOrder(self,oID):
        try:
            self.orders.remove(oID)
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("DELETE FROM deliveries WHERE trackingNo = :tn AND oid = :id",
                      {"tn":self.trackingNum, "id":oID})
            conn.commit()
            conn.close()

        except Exception as ex:
            conn.rollback()
            conn.commit()
            conn.close()
            print("ERROR removing orders")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)


class Oline():
    def __init__(self, oID,sID,pID,qty=0,uprice=0):
        self.oID = oID
        self.sID = sID
        self.pID = pID
        self.qty = qty
        self.uprice = uprice

    def updateUprice(self, value):
        try:
            self.uprice = value
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("UPDATE onlines SET uprice = :up WHERE oid = :od AND pid = :pd AND sid = :sd",
                          {"vl":value,"od":self.oID,"pd":self.pID,"sd":self.sID})
            conn.commit()
            conn.close()
        except Exception as ex:
            conn.rollback()
            conn.commit()
            conn.close()
            print("ERROR updating uprice")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def updateQty(self, value):
        try:
            self.uprice = value
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("UPDATE onlines SET qty = :vl WHERE oid = :od AND pid = :pd AND sid = :sd",
                          {"uvl":value,"od":self.oID,"pd":self.pID,"sd":self.sID})
            conn.commit()
            conn.close()
        except Exception as ex:
            conn.rollback()
            conn.commit()
            conn.close()
            print("ERROR updating qty")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def getOlineInfo(self,oid,pid,sid):
        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("SELECT oid, sid, pid, qty, uprice FROM olines WHERE oid=:od AND sid=:sd AND pID =:pd",
                      { "od": oid, "pd": pid, "sd": sid})
            result = c.fetchone()
            self.oID = result[0]
            self.sID = result[1]
            self.pID = result[2]
            self.qty = result[3]
            self.uprice = result[4]
            conn.commit()
            conn.close()
        except Exception as ex:
            conn.rollback()
            conn.commit()
            conn.close()
            print("ERROR getting oline info")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def saveOlineInfo(self):
        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("""INSERT INTO olines(oid, sid, pid, qty, uprice) VALUES(?, ?, ?, ?, ?) """,
                          (self.oID, self.sID, self.pID, self.qty, self.uprice))
            conn.commit()
            conn.close()
        except Exception as ex:
            conn.rollback()
            conn.commit()
            conn.close()
            print("Error saving oline")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def removeOline(self, oid, sid, pid):
        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("DELETE FROM olines WHERE oid=:od AND sid=:sd AND pID =:pd",
                      {"od": oid, "pd": pid, "sd": sid})
            conn.commit()
            conn.close()
        except Exception as ex:
            conn.rollback()
            conn.commit()
            conn.close()
            print("Error removing")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def getUprice(self):
        return self.uprice

    def getQty(self):
        return self.qty


class Order(): # oid, cid, odate, address
    __ID = getTableSize("orders") + 1
    def __init(self,cid,address):
        self.oID = self.__ID
        self.cID = cid
        self.address = address
        self.date = datetime.now()

    def saveOrder(self): #TODO: Error where order id may not be unique --> Make recursive call to saveorder with orderId +1
        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("""INSERT INTO orders(oid, cid, address, odate) VALUES(?, ?, ?, ?) """,
                      (self.oID, self.cID, self.address, self.date))
            conn.commit()
            conn.close()
        except Exception as ex:
            conn.rollback()
            conn.commit()
            conn.close()
            print("Error saving oline")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def getOrderInfo(self, ID):   # Update all self values to match the one from the database and return OID
        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("SELECT oid, cid, address, odate FROM orders WHERE oid = :id", {"id": ID})
            result = c.fetchone()
            self.oID = result[0]
            self.cID = result[1]
            self.address = result[2]
            self.date = result[3]
            conn.commit()
            conn.close()

        except Exception as ex: #TODO: Print message saying order id does not exist
            conn.rollback()
            conn.commit()
            conn.close()
            print("ERROR with retrieveOrder")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def updateAddress(self, newAddress):    #Update address of current Order
        self.address = newAddress
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        try:
            c.execute("UPDATE orders SET address = :ad WHERE oid = :id",{"ad":newAddress,"id":self.oID})
            conn.commit()
            conn.close()
        except Exception as ex:
            conn.rollback()
            conn.commit()
            conn.close()
            print("Error updating order address")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def getOID(self):
        return self.oID

    def getCID(self):   # Return customer ID of current order
        return self.cID

    def getAddress(self): # Return address of current order
        return self.address

    def getOrderDate(self): # Return date current order was made
        return self.date


class Customer():
    def __init__(self,cid, name, address, pwd):
        self.cid = cid
        self.name = name
        self. address = address
        self.pwd = pwd


class Product():
    def __init__(self, pid, name, unit, cat):
        self.pid = pid
        self.name = name
        self.unit = unit
        self.cat = cat


class Store():
    def __init__(self,sid,name,phone,address):
        self.sid = sid
        self.name = name
        self.phone = phone
        self.address = address


class Agent():
    def __init__(self, aid, name, pwd):
        self.aid = aid
        self.name = name
        self.pwd = pwd

    def getAgentInfo(self,ID):
        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("SELECT aid, name, pwd FROM agents WHERE aid=:ad",
                      { "od": ID})
            result = c.fetchone()
            self.aID = result[0]
            self.name = result[1]
            self.pwd = result[2]
            conn.commit()
            conn.close()
        except Exception as ex:
            conn.rollback()
            conn.commit()
            conn.close()
            print("ERROR getting agent info")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)



class Carry():
    def __init__(self,sid,pid,qty,uprice):
        self.sid = sid
        self.pid = pid
        self.qty = qty
        self.uprice = uprice



class Category():
    def __init__(self,cat, name):
        self.cat = cat
        self.name = name


