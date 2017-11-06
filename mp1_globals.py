# File contains global variables for mp1_app

__DBNAME__ = None
__USERID__ = None
def initDB(name):
    global __DBNAME__  # add this line!
    if __DBNAME__ is None: # see notes below; explicit test for None
        __DBNAME__ = name
    else:
        raise RuntimeError("Database name has already been set.")


def initUSER(name):
    global __USERID__  # add this line!
    if __USERID__ is None: # see notes below; explicit test for None
        __USERID__ = name
    else:
        raise RuntimeError("Database name has already been set.")