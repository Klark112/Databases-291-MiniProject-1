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
DATABASE = 'mp1a.db'
conn = sqlite3.connect(DATABASE)
c = conn.cursor()

#get search terms
search_terms=input() 
search_terms_list=search_terms.split()
found_terms=[]
print(search_terms_list)
username="c1"
order_id=1

#look for order by terms
for search_term in search_terms_list:
    print(search_term)
    c.execute('''
    SELECT pr.name, st.name
    FROM products pr, stores st, carries ca
    WHERE pr.name LIKE ('%' || ? || '%') and 
    pr.pid=ca.pid and 
    st.sid=ca.sid
    ''', (search_term,))
    found_terms.append(c.fetchall())
print(found_terms)

#flatten terms into a 1D list
flat_list=[]
for sublist in found_terms:
    for item in sublist:
        flat_list.append(item)
print(flat_list)

#count most frequent matching term
term_count=defaultdict(int)
for term in flat_list:
        term_count[term]+=1
print(term_count)

#list most common match first
flat_list=sorted(flat_list, key=term_count.get, reverse=True)
print(flat_list)

#seperate into lists based on matching terms
ordered_list=[]
ordered_list2=[]
placeholder=''
for i in flat_list:
    if i[0]!=placeholder:
        ordered_list.append(ordered_list2)
        ordered_list2=[]
        placeholder=i[0]
    if i[0]==placeholder:
        ordered_list2.append(i)
ordered_list.append(ordered_list2)
ordered_list=ordered_list[1:]
print(ordered_list)

#order each list based on store name z->a
for matching_list in ordered_list:
    matching_list.sort(key=lambda x: x[1], reverse=True)
print(ordered_list)

#flatten into 1D list again to be used as order by
flat_list=[]
for sublist in ordered_list:
    for item in sublist:
        flat_list.append(item)
print(flat_list)

#For each matching product, list the product id, name, unit, the number of stores that have it in stock, 
#the minimum price among the stores that have the product in stock, and the number of orders within the past 7 days. 
# the number of stores that carry it, the minimum price among the stores that carry it,

#currently from the specification this function returns the product id, name, unit, the number of stores that have it in stock, 
#the minimum price among the stores that have the product in stock, and the number of orders within the past 7 days.
#it does not return the number of stores that carry it( i.e. they can list but have 0 in stock) 
# and it does not return the minimum unit price for each product of that store
# finally the query does not stay ordered according the final flat list (see the flat_list just before the comment block)
#PS. sorry to offload this onto you and good luck.
found_terms=[]
print(found_terms)
for search_term in search_terms_list:
    for names in flat_list:
        c.execute('''
        SELECT pr.pid, pr.name, pr.unit, count(ca.sid), min(ca.uprice), count(od.oid)
        FROM products pr, stores st, carries ca, orders od
        WHERE pr.name=? and 
        pr.pid=ca.pid and 
        st.sid=ca.sid and
        pr.name=? and
        st.name=? and
        ca.qty>0 and
        odate> datetime('now','-7 days')
        ''', (names[0],names[0],names[1]))
        found_terms.append(c.fetchall())
print(found_terms)

conn.commit()
conn.close()