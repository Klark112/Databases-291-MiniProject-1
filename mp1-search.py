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


from itertools import chain
DATABASE = 'mp1.db'

"""
SAMPLE SEARCH QUERY if input 'milk', '4', 'cat' --> tested and works

SELECT pname , sname, count(*) as matches
FROM(
    SELECT pr.name as pname, st.name as sname
    FROM products pr 
    INNER JOIN carries ca ON pr.pid = ca.pid 
    INNER JOIN stores st  ON ca.sid = st.sid 
    WHERE pr.name LIKE ('%' ||'milk'|| '%')
    UNION ALL
    SELECT pr.name as pname, st.name as snams
    FROM products pr 
    INNER JOIN carries ca ON pr.pid = ca.pid 
    INNER JOIN stores st  ON ca.sid = st.sid 
    WHERE pr.name LIKE ('%' ||'4'|| '%')
    UNION ALL
    SELECT pr.name as pname, st.name as sname
    FROM products pr 
    INNER JOIN carries ca ON pr.pid = ca.pid 
    INNER JOIN stores st  ON ca.sid = st.sid 
    WHERE pr.name LIKE ('%' ||'cat'|| '%')
    )
GROUP BY pname, sname
ORDER BY matches DESC
"""

def search_Items(search_terms):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    #get search terms

    search_terms_list=search_terms.split()
    term_matches=[]
    print(search_terms_list)
    query = 'SELECT pname , sname, count(*) as matches FROM('
    for key in search_terms_list:
        print(key)
        query +=" SELECT pr.name as pname, st.name as sname FROM products pr INNER JOIN carries ca ON pr.pid = ca.pid INNER JOIN stores st  ON ca.sid = st.sid WHERE pr.name LIKE ('%' ||'" + key + "'|| '%') UNION ALL"

    query = query[:-9] + ')GROUP BY pname, sname ORDER BY  matches DESC, sname DESC'
    print(query)
    c.execute(query)
    res = c.fetchall()
    for i in res:
        print(i)
    conn.commit()
    conn.close()
"""
        c.execute('''
           SELECT pr.name, st.name
           FROM products pr, stores st, carries ca
           WHERE pr.name LIKE ('%' || ? || '%') and 
           pr.pid=ca.pid and 
           st.sid=ca.sid
           ''', (key,))
        res = c.fetchall()
        print(res)
        for i in res:
            sub_res = [i,1]
            if i in chain.from_iterable(term_matches):
                term_matches.append(sub_res)
            else:
                term_matches[term_matches.index(i)][1] += 1

"""


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



if __name__ == "__main__":
    search_terms=input("key words: ")
    search_Items(search_terms)