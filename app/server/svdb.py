import random,string
from app.api.control import ControlLogsFile


class Svdb:
    """
        Svdb (Server database)
        this module used to create new members and add balance to them only
        well, this is not very pratical but still works fine rn.
        YOU have to add more secure layers no cap.
    """
    def __init__(self,database,cursor:object) -> None:
        """
            database: sqlite3.connect object
            cursor: database.cursor object
        """
        self.cursor = cursor
        self.database = database
        self.controlLog = ControlLogsFile(database=database,cursor=cursor)
        self.commands = {
            "check" : "SELECT * FROM {0} WHERE {1}",
            "update" : "UPDATE {0} SET {2} WHERE {1}",
            "insert" : "INSERT INTO {0} VALUES {1}"
        }

    def generateApiKey(self) -> str:
        generatedApi = "".join(random.choice(string.ascii_uppercase + string.digits) for i in range(16))
        print(generatedApi)
        while bool(self.cursor.execute(self.commands["check"].format("APIS",f"APIKEY='{generatedApi}'")).fetchone()):
            self.database.commit()
            generatedApi = "".join(random.choice(string.ascii_uppercase + string.digits) for i in range(16))
        self.database.commit()
        print(generatedApi)
        return generatedApi

    def newMember(self,username:str,ipAddr:str) -> None:
        newapi = self.generateApiKey()
        print(newapi)
        values = f"('{username}','{newapi}','{self.controlLog.createLog(username,newapi,ipAddr)}',1000,0.0)"
        print(values)
        self.cursor.execute(self.commands["insert"].format("APIS",values))
        self.database.commit()
    
    def addBalance(self,name:str,newpaiement:float) -> None:
        print(self.cursor.execute(self.commands["check"].format("APIS",f"name='{name}'")).fetchone()[4])
        balance = self.cursor.execute(self.commands["check"].format("APIS",f"name='{name}'")).fetchone()[4]
        newbalance = balance + newpaiement
        print(self.commands["update"].format("APIS",f"NAME ='{name}'",f"BALANCE = {float(newbalance)}"))
        self.cursor.execute(self.commands["update"].format("APIS",f"NAME='{name}'",f"BALANCE={str(float(newbalance))}"))
        self.database.commit()
