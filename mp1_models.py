# Back end File for CMPUT 291, Mini-Project 1 App
# Group members: Justin Daza, Klark Bliss, Siddhart Khanna
# File contains funtions that support actions that Agents can take

import sqlite3
import tkinter as tk
from tkinter import messagebox
from mp1 import *
import uuid
import datetime

class Delivery():
    #__trackingNumList ={} # Used to identify if tracking number is unique?
    __ID = getTableSize("deliveries") + 1
    def __init__(self,pickupTime = None, orders= []):
        self.id =self.__ID
        self.__class__.__ID += 1
        self.orders = orders
        self.trackingNum = uuid.uuid4().int & (1<<12)-1
        self.pickUpTime = pickupTime
        self.dropOffTIme = None

    def addOrders(self, newOrders):
        self.orders+=newOrders
        return

    def getOrders(self):
        return

    def setDelivery(self):
        return

    def updateDelivery(self,trackingNum):
        return

    def getDelivery(self, ID):
        return

class Oline():
    def __init__(self, oID,sID,pID,qty=0,uprice=0):
        self.oID = oID
        self.sID = sID
        self.pID = pID
        self.qty = qty
        self.uprice = uprice

    def updatePID(self, value):
        return

    def updateUprice(self, value):
        return

    def getOID(self):
        return self.oID

    def getSID(self):
        return self.sID

    def getPID(self):
        return self.pID

    def getUprice(self):
        return self.uprice

    def getQty(self):
        return self.qty

class Order():
    __ID = getTableSize("orders") + 1
    def __init(self,cid,address):
        self.oID = self.__ID
        self.cID = cid
        self.address = address
        self.date = datetime.now()

    def getOID(self):
        return self.oID

    def getCID(self):
        return self.cID

    def getAddress(self):
        return self.address

    def getOrderDate(self):
        return self.date

    def updateAddress(self, newAddress):
        self.address = newAddress


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

    

# Global function to returns size of specified db
def getTableSize(table):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(" SELECT COUNT(*) FROM :tb ",
              {"tb":table})
    return c.fetchone()