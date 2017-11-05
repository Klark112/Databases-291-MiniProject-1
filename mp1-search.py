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

class Search_products():
    def __init__(self, key_terms):
        self.key_terms = key_terms
        self.results = self.search_Items(key_terms)

    def list_product_details(self, pid):
        details = []
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''
                  SELECT pr.pid, pr.name, pr.unit, pr.cat
                  FROM products pr
                  WHERE pr.pid = ?
              ''',(pid,))
        res = c.fetchone()
        for i in res:
            details.append(i)
        print(details)
        c.execute('''
                 SELECT st.name, ca.uprice, ca.qty, sub.ordernum
                 FROM carries ca
                 INNER JOIN stores st ON ca.sid = st.sid
                 INNER JOIN products pr ON ca.pid = pr.pid
                 INNER JOIN (SELECT ol.sid as name, COUNT(*) as ordernum
                            FROM olines ol
                            INNER JOIN orders od ON ol.oid=od.oid
                            INNER JOIN products pr ON ol.pid=pr.pid
                            WHERE pr.pid = ?
                            and ((od.odate > DATETIME('now', '-7 days'))=1) GROUP BY ol.sid) sub ON ca.sid = sub.name
                 WHERE pr.pid = ?
                 ORDER BY ca.qty DESC, ca.uprice ASC
                 
             ''', (pid,pid))
        res = c.fetchall()
        details.append(res)
        print(details)

        conn.commit()
        conn.close()

    def list_details(self, result_item):
       # for search_term in search_terms_list:
       #      for names in flat_list:
        print(result_item)
        product_info = []
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''
                    SELECT pr.pid, pr.name, pr.unit, st.name
                    FROM carries ca
                    INNER JOIN products pr  ON ca.pid=pr.pid
                    INNER JOIN stores st ON ca.sid=st.sid
                    WHERE pr.name=? and
                    st.sid=ca.sid and
                    st.name=?
                    ''', (result_item[0], result_item[1]))
        res = c.fetchone()
        for i in res:
            product_info.append(i)

        c.execute('''
                    SELECT count(ca.pid), min(ca.uprice)
                    FROM carries ca
                    INNER JOIN products pr  ON ca.pid=pr.pid
                    INNER JOIN stores st ON ca.sid=st.sid
                    WHERE pr.name=?
                    ''', (result_item[0],))
        res = c.fetchone()
        for i in res:
            product_info.append(i)
        print(product_info)

        c.execute('''
                   SELECT count(ca.pid), min(ca.uprice)
                   FROM carries ca
                   INNER JOIN products pr  ON ca.pid=pr.pid
                   INNER JOIN stores st ON ca.sid=st.sid
                   WHERE pr.name=? and
                   ca.qty > 0
                   ''', (result_item[0],))
        res = c.fetchone()
        for i in res:
            product_info.append(i)
        print(product_info)

        c.execute('''
                SELECT count(od.odate)
                FROM orders od
                INNER JOIN olines ol  ON od.oid=ol.oid
                INNER JOIN products pr  ON ol.pid=pr.pid
                WHERE pr.name=? and
                ((od.odate > datetime('now',"-7 days"))=1)
                ''', (result_item[0],))
        res = c.fetchone()
        for i in res:
            product_info.append(i)
        print(product_info)
        conn.commit()
        conn.close()
        return(product_info)

    def search_Items(self, search_terms):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        search_terms_list=search_terms.split()
        #print(search_terms_list)
        query = 'SELECT pname , sname, count(*) as matches FROM('
        for key in search_terms_list:
            #print(key)
            query +=" SELECT pr.name as pname, st.name as sname FROM products pr INNER JOIN carries ca ON pr.pid = ca.pid INNER JOIN stores st  ON ca.sid = st.sid WHERE pr.name LIKE ('%' ||'" + key + "'|| '%') UNION ALL"

        query = query[:-9] + ')GROUP BY pname, sname ORDER BY  matches DESC, sname DESC'
        #print(query)
        c.execute(query)
        res = c.fetchall()
        result_list =[]
        for i in res:
            result_list.append(i)
        conn.commit()
        conn.close()
        return result_list



if __name__ == "__main__":
    newsearch = Search_products('milk cat lettuce')
    newsearch.list_product_details("p1")