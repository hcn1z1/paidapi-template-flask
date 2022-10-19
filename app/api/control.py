import json,random,string
from array import array
from datetime import datetime
from threading import Lock
from app.api.syntax import errorsHandling

class DatabaseControler:
    def __init__(self,database,cursor:object) -> None:
        """
            control sqlite3 cursor ! 
            database: sqlite3.connect object
            cursor: database.cursor object
        """
        self.lock = Lock()
        self.database = database
        self.cursor = cursor
        self.commands = {
            "check" : "SELECT * FROM {0} WHERE {1}",
            "update" : "UPDATE {0} SET {2} WHERE {1}",
            "insert" : "INSERT INTO {0} VALUES {1}"
        }
        self.balanceCut = 0.001 # price of each api call

    def response(self,name:str,key:str,value:str):
        """
            :return: a 200 response message with addition of some data provided by module app.api.function
        """
        data = self.cursor.execute(self.commands["check"].format("APIS",f"name='{name}'")).fetchone()
        self.database.commit()
        return {
            "name":data[0],
            "balance":data[4],
            key:value
        }

    def __checkAPI(self,name:str,apiKey:str) -> int:
        data = self.cursor.execute(self.commands["check"].format("APIS",f"name='{name}'")).fetchone()
        print(data)
        self.database.commit()
        if bool(data) and data[1] == apiKey:
            return True
        else:
            return False

    def __checkBalance(self,name:str) -> bool:
        data = self.cursor.execute(self.commands["check"].format("APIS",f"name='{name}'")).fetchone()
        self.database.commit()
        if bool(data) and data[4] - self.balanceCut >= 0 :
            return True
        else:
            return False

    def updateBalance(self,name:str) -> None:
        """
            remove balanceCut value from account balance 
        """
        data = self.cursor.execute(self.commands["check"].format("APIS",f"name='{name}'")).fetchone()
        self.database.commit()
        newBalance = data[4] - self.balanceCut
        self.cursor.execute(self.commands["update"].format("APIS",f"NAME = '{name}'",f"BALANCE={newBalance}"))
        self.database.commit()

    def paidAPIRequest(self,name:str,apiKey:str) -> int:
        """
            :return: error code {
                406 insufficient funds
                401 unknown credential
                200 Ok 
            }
        """
        if self.__checkAPI(name,apiKey):
            if self.__checkBalance(name):return (200,{"message":"Ok"})
            else:return (406,errorsHandling(406))
        else:
            return (401,errorsHandling(401))

class ControlLogsFile(DatabaseControler):
    def __init__(self,database,cursor) -> None:
        """
            control json logs file ! 
            :cursor: sqlite3.connect.cursor object
            inherit object DatabaseControler to use some functionalities
        """
        DatabaseControler.__init__(self,database,cursor)
    
    def getPath(self,name:str) -> str:
        return self.cursor.execute(self.commands["check"].format("APIS",f"name='{name}'")).fetchone()[2]
        self.database.commit()

    def getLogs(self,name:str,apiKey:str) -> array:
        """
            :return: array (code:integer,logs:dict) {
                code = an https return code
                logs = informations about api usage for this api key
            }
        """
        if self.__checkAPI(name,apiKey):
            file = open(self.getPath(name),"r")
            content = file.read()
            file.close()
            return (200,json.loads(content))
        else:
            return (401,errorsHandling(401))
    
    def embeddingLog(self,name:str,apiKey:str,log:dict) -> None:
        timeNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S %f")
        jsonPath = self.getPath(name)
        file =  open(jsonPath,"r")
        content = file.read()
        file.close()
        jsonDict = json.loads(content)
        jsonDict[timeNow] = log
        self.lock.acquire()
        open(jsonPath,"w+").write(json.dumps(jsonDict,indent=4))
        self.lock.release()
    
    def createLog(self,name:str,apiKey:str,location:str):
        generatedString = "".join(random.choice(string.ascii_uppercase + string.digits) for i in range(16))
        jsonPath = f"logs/logs-[{generatedString}].txt"
        file = open(jsonPath,"w+")
        file.write(json.dumps({"name":name,"creation":{"time" : datetime.now().strftime("%Y-%m-%d"),"location":location}},indent=4))
        return jsonPath