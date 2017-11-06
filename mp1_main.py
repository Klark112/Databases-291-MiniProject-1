
import mp1_globals
from mp1_app import MiniProjectapp
import sys

def main():
    Database_name = sys.argv[1]
    print("Databasename: " + Database_name)
    mp1_globals.initDB(Database_name)
    app = MiniProjectapp()
    app.geometry("270x480")
    app.mainloop()
    print(mp1_globals.__DBNAME__)

if __name__ == "__main__":
    main()
