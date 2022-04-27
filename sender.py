from typing import Union, Dict
from pathlib import Path
from datetime import datetime
import yaml
import yagmail

from service import *
from target import *

LOG_PREFIX = f"[{datetime.now().strftime('%H:%M:%S, %m/%d/%y')}]\t"

SUBJECT = 'Look at this...'


def get_creds_from_file(filepath: Union[Path, str]) -> Dict[str, str]:
    yaml_text = ''
    with open(filepath, 'r') as creds_file:
        for line in creds_file:
            yaml_text += line
    
    return yaml.load(yaml_text, Loader=yaml.Loader)


def send_am_messages(target: Target, creds: Dict):
    yag = yagmail.SMTP(creds["email"], creds["password"])
    message_contents = []
    for service in target.am_services:
        message_contents.append(service.run())
    
    yag.send(target.email, SUBJECT, message_contents)
    print(f"{LOG_PREFIX}Sent AM Messages to {target.name} ({target.email})")


def send_pm_messages(target: Target, creds: Dict):
    yag = yagmail.SMTP(creds["email"], creds["password"])
    message_contents = []
    for service in target.pm_services:
        message_contents.append(service.run())
    
    yag.send(target.email, SUBJECT, message_contents)
    print(f"{LOG_PREFIX}Sent PM Messages to {target.name} ({target.email})")


if __name__ == '__main__':
    creds = get_creds_from_file('creds.yaml')
    targets = load_targets_from_file('targets.yaml')
    for target in targets:
        print(f"am: {send_am_messages(target, creds)}")
        print(f"pm: {send_pm_messages(target, creds)}")
