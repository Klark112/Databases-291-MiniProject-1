import sqlite3

def log_in(username,password): #NOTE: username and password are currently blank    
    conn= sqlite3.connect('./mp1.db')      
    c=conn.cursor()
    
    check=c.execute(" SELECT cid FROM customer WHERE customer.name=:un",{"un":username})
    if(check!=username):
        print("Sorry but that user does not exist")
        conn.commit() #NOTE: I don't think we need this commit statement since we aren't changing anything
        conn.close()
        return False
    
    check=c.execute(" SELECT pwd FROM customer WHERE customer.pwd=:pw",{"pw":password})
    if(check!=password): #TODO: should probably change the message printed for security reasons
        print("Sorry but that password is incorrect")
        conn.commit()
        conn.close()        
        return False
    
    conn.commit()
    conn.close()    
    return True

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
    return 0

#main()