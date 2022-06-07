from typing import Union, List, Dict
from pathlib import Path
from datetime import timedelta
import yaml

from service import *


class ServiceEntry:
    text_service: Service
    img_service: Service
    run_time: timedelta

    def __init__(self, new_text_service: Service, new_img_service: Service, new_run_time: timedelta):
        self.text_service = new_text_service
        self.img_service = new_img_service
        self.run_time = new_run_time

    def __str__(self):
        return f"({self.text_service.name} + {self.img_service.name} @ {self.run_time})"


class Target:
    name: str
    email: str
    service_entries: List[ServiceEntry]

    def __init__(self, new_name: str, new_email: str, new_service_entries: List[ServiceEntry]):
        self.name = new_name.strip()
        self.email = new_email.strip()
        self.service_entries = new_service_entries

    def add_service_entry(self, new_service_entry: ServiceEntry):
        self.service_entries.append(new_service_entry)

    def __str__(self):
        return f"{self.name} - {self.email}\n\tService Entries: {', '.join([str(entry) for entry in self.service_entries])}"

"""
Example Target YAML:

Me:
  email: me@gmail.com
  service_entries:
  - meowfacts + randomcats @ 8:41AM
  - dogapi + randomdogs @ 9:21PM
"""
def load_targets_from_file(filepath: Union[Path, str]) -> Dict:
    yaml_text = ""
    with open(filepath, 'r') as target_file:
        for line in target_file:
            yaml_text += line

    targets_data = yaml.load_all(yaml_text, Loader=yaml.Loader)
    targets = []

    for data in targets_data:
        new_target = Target(data["name"], data["email"])
        for target_entry in data["service_entries"]:
            new_run_time = target_entry

        targets.append(new_target)
    
    return targets


if __name__ == '__main__':
    targets = load_targets_from_file('targets.yaml')
    for target in targets:
        print(target)
