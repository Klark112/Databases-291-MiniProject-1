import sqlite3
import tkinter as tk
from tkinter import messagebox

DATABASE = 'mp1.db'

def log_in(username,password): #NOTE: username and password are currently blank
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(" SELECT cid FROM customers WHERE customers.cid=:un",{"un":username})
    result = c.fetchone()
    try:
        if(result[0] == username):
            c.execute(" SELECT cid, pwd FROM customers WHERE customers.pwd=:pw AND customers.cid=:un", {"pw": password, "un": username})
            result = c.fetchone()
            print(result[1])
            if(result[1] == password):
                conn.commit()
                conn.close()
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
            print(result[1])
            if (result[1] == password):
                conn.commit()
                conn.close()
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


def sign_up(username,password): #customer(cid, name, address, pwd)
    i_cid=input("\nPlease enter a Username: ")
    i_name=input("\n Please enter your Full name: ")
    i_address=input("\n Please enter your address: ")
    i_pwd=input("\n Please enter your password: ") #TODO:have to hide this value while it is being typed

    conn= sqlite3.connect('./mp1.db')
    c=conn.cursor()    
    c.execute(" INSERT INTO customers(cid, name, address, pwd) VALUES (i_cid, i_name, i_address,i_pwd) ") #TODO: incomplete SQL INSERT
    return True

#used to check whether the user is an agent, returning customer, or new customer
#NOTE:login and sign up must guard against SQL injections
def login_screen(username,password): 
    print("Hello and Welcome to your online Grocer")
    lg_sgn=0                                    #A value used to check if the user is logging in or signing up or exiting
    while(lg_sgn!=1 or lg_sgn!=2):              #TODO:optimize condition later, as is it checks two conditions every loop
        print("\nPlease enter a listed number")
        lg_sgn=input("\n1. Login\n2. sign up\n3. exit\n")
        if(lg_sgn==1):                          #QUESTION:do we want to handle log in and sign up in different functions? For now I will implement these if conditionals with functions  
            success=log_in(username,password)
            break                                  
        elif(lg_sgn==2):
            success=sign_up(username,password)
            break
        elif(lg_sgn==3):
            print("Thank you for using our services, Goodbye")
            return('a','a') #NOTE: I returned two characters because they take up 1 byte of memory each
        

    return (username,password)

#def main():
#    username=""
#    password=""
#    lg_in=[]
#    lg_in.append(login_screen(username,password))
    
    #username=lg_in[0][0]
    #password=lg_in[0][1]    
    #print(username,password)
#    return 0

#main()