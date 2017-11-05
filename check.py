import sqlite3
import time

conn = sqlite3.connect('./mp1.db')  
c = conn.cursor()

userID = "c1"
listBasket = [[1, 'p1', 4],[2, 'p4', 4],[1, 'p1', 5], [1, 'p2', 9]] #sid, pid, qty

#Checking if the qty is large
for n in range(len(listBasket)):
   c.execute("""SELECT c1.qty FROM carries c1 WHERE c1.sid =:sd AND c1.pid=:pd""",
             {"sd":listBasket[n][0], "pd":listBasket[n][1]})
   conn.commit()
   res = c.fetchall()
   
   if(listBasket[n][2]>res[0][0]):
      print("too high quantity")
   else:
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
      
      #update the table after placing an order
      c.execute("""UPDATE carries SET qty = qty - :qt WHERE sid=:sd AND pid=:pd""",
                {"qt":listBasket[n][2], "sd":listBasket[n][0], "pd":listBasket[n][1]})
      conn.commit()