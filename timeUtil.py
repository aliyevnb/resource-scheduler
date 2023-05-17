import awsenv
import datetime
from datetime import time

def startTime():
    localStartTime = time.fromisoformat(awsenv.setStart())
    localHour = localStartTime.strftime("%H")
    localMinute = localStartTime.strftime("%M")
    localDate = datetime.datetime(2023,5,15,int(localHour),int(localMinute))
    utcDate = localDate.astimezone(datetime.timezone.utc)
    return utcDate.strftime("%H"), utcDate.strftime("%M")

def stopTime():
    localStartTime = time.fromisoformat(awsenv.setStop())
    localHour = localStartTime.strftime("%H")
    localMinute = localStartTime.strftime("%M")
    localDate = datetime.datetime(2023,5,15,int(localHour),int(localMinute))
    utcDate = localDate.astimezone(datetime.timezone.utc)
    return utcDate.strftime("%H"), utcDate.strftime("%M")
