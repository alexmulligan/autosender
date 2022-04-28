from typing import List, Dict
import time
from datetime import datetime, timedelta, date

from service import *
from target import *
from sender import *

#AM_TIME_OF_DAY = timedelta(hours=21, minutes=45)   # debug
#PM_TIME_OF_DAY = timedelta(hours=21, minutes=48)   # debug
AM_TIME_OF_DAY = timedelta(hours=9, minutes=30)  # production
PM_TIME_OF_DAY = timedelta(hours=17, minutes=30) # production


def send_all_am_messages(targets: List[Target], creds: Dict[str, str]):
    for target in targets:
        send_am_messages(target, creds)


def send_all_pm_messages(targets: List[Target], creds: Dict[str, str]):
    for target in targets:
        send_pm_messages(target, creds)


def mainloop():
    print(f"Starting autosender @ {datetime.now().strftime('%H:%M:%S, %m/%d/%y')}")
    creds = get_creds_from_file('creds.yaml')
    print("Successfully got creds")
    targets = load_targets_from_file('targets.yaml')
    print("Successfully got targets\n\n")

    sent_am = False
    sent_pm = False

    last_time = datetime.now()
    while True:
        today = datetime(year=date.today().year, month=date.today().month, day=date.today().day)
        am_time = today + AM_TIME_OF_DAY
        pm_time = today + PM_TIME_OF_DAY
        current_time = datetime.now()

        if not sent_am:
            print(f"{LOG_PREFIX()}Comparing to AM Time - current: ({current_time.strftime('%H:%M:%S')});  am: ({am_time.strftime('%H:%M:%S')})  -  {current_time > am_time}")
            if current_time > am_time:
                send_all_am_messages(targets, creds)
                sent_am = True
                last_time = current_time

        if not sent_pm:
            print(f"{LOG_PREFIX()}Comparing to PM Time - current: ({current_time.strftime('%H:%M:%S')});  pm: ({pm_time.strftime('%H:%M:%S')})  -  {current_time > pm_time}")
            if current_time > pm_time:
                send_all_pm_messages(targets, creds)
                sent_pm = True
                last_time = current_time
        
        if sent_am and sent_pm:
            print(f"{LOG_PREFIX()}Both AM and PM sent for the day. Doing nothing")
        
        # if it is new day, reset am and pm sent status
        if current_time.day > last_time.day or current_time.month > last_time.month:
            print(f"{LOG_PREFIX()}Resetting sent flags")
            sent_am = False
            sent_pm = False

        print(f"{LOG_PREFIX()}Sleeping for 5 minutes")
        time.sleep(300) # sleep for 5 minutes
        print(f"{LOG_PREFIX()}Waking up from sleep")
    

if __name__ == '__main__':
    mainloop()
