'''
Created on Jun 24, 2020

@author: sigmo
'''
import time

from gql import gql
from gql.client import Client
from gql.transport.requests import RequestsHTTPTransport


width = 76
height = 18


def startApp():
    msg = "__main__.startApp()"
    for step in range(int(width/2  - len(msg)/2)):
        print(" ", end="")
    print(msg)
    time.sleep(0.500)
    msg="::::Application Boot Request::::"
    for step in range(int(width/2 - len(msg)/2)):
        print(" ", end="")
    print(msg)
    time.sleep(1)
    for step in range(int(height)):
        print("\n")
    while True:
        msg="::::Welcome to the VirKade::::"
        for step in range(int(width/2 - len(msg)/2)):
            print(" ", end="")
        print(msg)
        print("")
        msg="loading..."
        for step in range(int(width/2 - len(msg)/2)):
            print(" ", end="")
        print(msg)
        for step in range(int((height/2)-2)):
            print("\n")
        time.sleep(0.500)
        respArray = fetchSessions()
        msg="::::Welcome to the VirKade::::"
        for step in range(int(width/2 - len(msg)/2)):
            print(" ", end="")
        print(msg)
        displaySessions(respArray)
        time.sleep(60)
        msg="::::Refresh::::"
        for step in range(int(width/2 - len(msg)/2)):
            print(" ", end="")
        print(msg)
        time.sleep(0.250)
        for step in range(int(height)):
            print("\n")


def displaySessions(resArray):
    loops = 0;
    for cur in resArray:
        border = "-"
        if not loops % 2 == 0:
            border= "="
        loops = loops + 1
        if loops > 4:
            return
        
        # first row
        for step in range(int(width-2)):
            print(border, end="")
        print("-")
        # second row
        print("|", end="")
        startDate = "    start time: " + cur["startDate"] 
        print(startDate, end="")
        for step in range(int(width - (len(startDate)-2))):
            print(" ", end="")
        print("|")
        
        # third row
        print("|", end="")
        name = "    customer name: " + cur["lastName"] + ", " + cur["firstName"]
        print(name, end="")
        for step in range(int(width - (len(name)-2))):
            print(" ", end="")
        print("|")
        
        # fourth row
        print("|", end="")
        username = "    username: " + cur["username"]
        print(username, end="")
        for step in range(int(width - (len(username)-2))):
            print(" ", end="")
        print("|")
        
        # fifth row
        print("|", end="")
        sessionDetail = "    session details: " + cur["location"]["name"] + "[["
        activities = cur["activities"]
        for activity in activities:
            sessionDetail = sessionDetail + activity["name"] + ", "
        sessionDetail = sessionDetail + "]]"
        print(sessionDetail, end="")
        for step in range(int(width - (len(sessionDetail)-2))):
            print(" ", end="")
        print("|")
        
        # six row
        print("|", end="")
        endDate = "    end time: " + cur["endDate"] 
        print(endDate, end="")
        for step in range(int(width - (len(endDate)-2))):
            print(" ", end="")
        print("|")
        
        # last row
        for step in range(int(width-2)):
            print(border, end="")
        print(border)
    
    if loops == 0:
        msg=":::no pending sessions:::"
        for step in range(int(width/2 - len(msg)/2)):
            print(" ", end="")
        print(msg)

def fetchSessions():
    try:
        requestConfig = RequestsHTTPTransport(
            url="http://192.168.1.7:136/service/",
            use_json=True,
            headers={'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ScheduleViewer',
                'UserName': 'Virkade Experience'
            },
            verify=False,
            retries=2
        )
        
        client = Client(
            transport=requestConfig,
            fetch_schema_from_transport=True,
            )
        query = gql(
            '''{ getPendingSessions(
                    locationName:"VirKade Prime",
                    activityName:"Viveport"
                    ){
                    startDate
                    endDate
                    firstName
                    lastName
                    username
                    location {
                        name
                    }
                    activities {
                        name
                    }
                }
            }'''
        )
        res = client.execute(query)
    except Exception as e:
        print(":::session fetch failed ["+str(e.args[0].reason)+"]:::")
        return dict()
    resultsArray = res["getPendingSessions"]
    return resultsArray

if __name__ == '__main__':
    startApp()
