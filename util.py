import json

def VerifyLogin(username, password):
    with open('./static/resources/logindata.json', 'r') as file:
        droneData = json.load(file)
        
    for data in droneData:
        if data["username"].lower() == username.lower() and data["password"] == password:
            return True
    return False

def GetPicture():
    