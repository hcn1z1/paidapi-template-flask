from array import array
import json

def __stringToDictionary(string:str) -> list:
    return json.loads(string)

def errorsHandling(errorcode:int):
    if errorcode == 400: return {"error":"bad payload data ! check documentation on {0}"}
    elif errorcode == 401: return {"error":"unknown credential"}
    elif errorcode == 406: return {"error":"Insufficent Funds"}

def checkPayloadData(data:str) -> array:
    data = __stringToDictionary(data)
    # this is only an example of twilio lookup api
    neededQueries = ["apikey","number"]
    # convert and sort the payload's queries into a list ! 
    # sort "needed queries" to check if all on "payload's queries"
    payloadQueries = list(data.keys())
    if set(neededQueries).issubset(set(payloadQueries)): return (200,data)
    else: return (401,errorsHandling(401))
    
def dataHandling(data:str) -> array:
    """
        :return: array  (code:int,_data:dict)
        code : A http status code
        _data : converted data from string to dictionary or a potentiel error
    """
    print("working")
    try:return checkPayloadData(data)
    except: return (400,errorsHandling(400))

def logsSyntax(number,provider):
    """
        :inputs: depends on your functionalities !
        :returns: a log dictionary to be saved as json on logs/
        PS: this is just an example !
    """
    return {
        "checked":number,
        "provider":provider
    }