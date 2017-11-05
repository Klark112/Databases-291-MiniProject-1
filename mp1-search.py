from collections import defaultdict
#agents(aid, name, pwd)
#stores(sid, name, phone, address)
#categories(cat, name)
#products(pid, name, unit, cat)
#carries(sid, pid, qty, uprice)
#customers(cid, name, address, pwd)
#orders(oid, cid, odate, address)
#olines(oid, sid, pid, qty, uprice)
#deliveries(trackingno, oid, pickUpTime, dropOffTime)

#sid, pid, qty [[sid,pid,qty],[...],...,[...]] for sid's question 2
#
#The input I use to test this function is: 4l milk
#
import sqlite3
DATABASE = 'mp1.db'

def search_Items(search_terms):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    #get search terms

    search_terms_list=search_terms.split()
    found_terms={}
    print(search_terms_list)

    for i in search_terms_list:
        print(i)



"""
    where_clause = ''
    for i in search_terms_list:
        where_clause += " pr.name LIKE ('%' ||'"+i+"'|| '%') OR"

    #print(where_clause[:-2])
    query = "SELECT pr.name, st.name, count(*) as matches FROM products pr INNER JOIN carries ca ON pr.pid = ca.pid INNER JOIN stores st  ON ca.sid = st.sid WHERE" +where_clause[:-2] +"GROUP BY pr.name, st.name ORDER BY matches DESC"
    print(query)
    c.execute(query)
    res = c.fetchall()

    for i in res:
        found_terms.append(i)
    print(found_terms)
    found_terms.sort()
"""

    conn.commit()
    conn.close()


if __name__ == "__main__":
    search_terms=input("key words: ")
    search_Items(search_terms)