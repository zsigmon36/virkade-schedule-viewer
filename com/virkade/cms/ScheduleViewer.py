'''
Created on Jun 24, 2020

@author: sigmo
'''
import time

from gql import gql
from gql.client import Client
from gql.transport.requests import RequestsHTTPTransport

width = 80
height = 30


def startApp():
    msg = "__main__.startApp()"
    for step in range(int(width / 2 - len(msg) / 2)):
        print(" ", end="")
    print(msg)
    time.sleep(0.500)
    msg = "::::Application Boot Request::::"
    for step in range(int(width / 2 - len(msg) / 2)):
        print(" ", end="")
    print(msg)
    time.sleep(1)
    for step in range(int(height)):
        print("\n", end="")
        time.sleep(0.100)
    while True:
        msg = "::::Welcome to the VirKade::::"
        for step in range(int(width / 2 - len(msg) / 2)):
            print(" ", end="")
        print(msg)
        print("\n", end="")
        
        msg = "loading..."
        for step in range(int(width / 2 - len(msg) / 2)):
            print(" ", end="")
        print(msg)
        for step in range(int(height/2) - 2):
            print("\n", end="")
            time.sleep(0.100)
        
        time.sleep(0.250)
            
        respArray = fetchSessions()
        for step in range(int(height/2) + 2):
            print("\n", end="")
            time.sleep(0.100)
        
        msg = "[ we got fun and games ]"
        for step in range(int(width / 2 - len(msg) / 2)):
            print(" ", end="")
        print(msg)
        print("\n", end="")
        
        for step in range(int(height)):
            print("\n", end="")
            time.sleep(0.100)
        
        msg = "::::Welcome to the VirKade::::"
        for step in range(int(width / 2 - len(msg) / 2)):
            print(" ", end="")
        print(msg)
        
        curtime = time.localtime();
        curHour = str(curtime.tm_hour)
        if len(curHour) == 1:
            curHour = "0" + curHour
        curMin = str(curtime.tm_min)
        if len(curMin) == 1:
            curMin = "0" + curMin
        msg = "[ current time = " + curHour + ":" + curMin + " ]"
        for step in range(int(width / 2 - len(msg) / 2)):
            print(" ", end="")
        print(msg)
        
        displaySessions(respArray)
        time.sleep(30)
        
        msg = "::::Refresh::::"
        for step in range(int(width / 2 - len(msg) / 2)):
            print(" ", end="")
        print(msg)
        time.sleep(0.250)
        
        for step in range(int(height)):
            print("\n", end="")
            time.sleep(0.100)


def displaySessions(resArray):
    loops = 0;
    # first row
    for step in range(int(width - 1)):
        print("=", end="")
    print("=")
    time.sleep(0.100)
        
    # second row
    print("|", end="")
    headers = " start "
    print(headers, end="")
    for step in range(int((width / 8) - (len(headers) + 2))):
        print(" ", end="")
    print("|", end="")
       
    headers = " end "
    print(headers, end="")
    for step in range(int((width / 8) - (len(headers) + 2))):
        print(" ", end="")
    print("|", end="")
    
    headers = " customer name "
    print(headers, end="")
    for step in range(int((width / 2) - (len(headers) + 0))):
        print(" ", end="")
    print("|", end="")
        
    headers = " activity details "
    print(headers, end="")
    for step in range(int((width / 4) - (len(headers) + 1))):
        print(" ", end="")
    print("|")
    time.sleep(0.100)
    
    # new row
    for step in range(int(width - 1)):
        print("=", end="")
    print("=")
    time.sleep(0.100)    
    
    for cur in resArray:
        border = "-"
        loops = loops + 1
        if loops > 12:
            return
        
        # new row
        print("|", end="")
        
        startDate = cur["startDate"].split(" ")[1]
        startDateHour = startDate.split(":")[0]
        startDateMin = startDate.split(":")[1]
        startDate = " " + startDateHour + ":" + startDateMin
        print(startDate, end="")
        for step in range(int((width / 8) - (len(startDate) + 2))):
            print(" ", end="")
        print("|", end="")
        
        endDate = cur["endDate"].split(" ")[1]
        endDateHour = endDate.split(":")[0]
        endDateMin = endDate.split(":")[1]
        endDate = " " + endDateHour + ":" + endDateMin
        print(endDate, end="")
        for step in range(int((width / 8) - (len(endDate) + 2))):
            print(" ", end="")
        print("|", end="")
        
        name = " " + cur["lastName"] + ", " + cur["firstName"]
        print(name, end="")
        for step in range(int((width / 2) - (len(name) + 0))):
            print(" ", end="")
        print("|", end="")
        
        sessionDetail = " " + cur["activity"]["name"]
        print(sessionDetail, end="")
        for step in range(int((width / 4) - (len(sessionDetail) + 1))):
            print(" ", end="")
        print("|")
        time.sleep(0.100)
        
        # new row
        for step in range(int(width - 1)):
            print(border, end="")
        print(border)
        time.sleep(0.100)
    
    if loops == 0:
        print("\n")
        msg = ":::no pending sessions:::"
        for step in range(int(width / 2 - len(msg) / 2)):
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
            '''{ getPendingSessions{
                    startDate
                    endDate
                    firstName
                    lastName
                    username
                    location {
                        name
                    }
                    activity {
                        name
                    }
                }
            }'''
        )
        res = client.execute(query)
    except Exception as e:
        print(":::session fetch failed [" + str(e.args[0].reason) + "]:::")
        return dict()
    resultsArray = res["getPendingSessions"]
    return resultsArray


if __name__ == '__main__':
    startApp()
