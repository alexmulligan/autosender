from typing import Union, List, Dict
from pathlib import Path
import yaml

from service import *


class Target:
    name: str
    number: str
    am_services: List[Service]
    pm_services: List[Service]

    def __init__(self, new_name: str, new_number: str, new_am_services: List[Service]=None, new_pm_services: List[Service]=None):
        self.name = new_name.strip()
        self.number = new_number.strip()
        self.am_services = []
        if new_am_services:
            self.am_services.extend(new_am_services)
        self.pm_services = []
        if new_pm_services:
            self.pm_services.extend(new_pm_services)

    def add_am_service(self, new_service: Service):
        self.am_services.append(new_service)

    def add_pm_service(self, new_service: Service):
        self.pm_services.append(new_service)

    def __str__(self):
        return f"{self.name} - {self.number}\n\tAM: {', '.join([service.name for service in self.am_services])}\n\tPM: {', '.join([service.name for service in self.pm_services])}"


def load_targets_from_file(filepath: Union[Path, str]) -> Dict:
    yaml_text = ""
    with open(filepath, 'r') as target_file:
        for line in target_file:
            yaml_text += line

    targets_data = yaml.load_all(yaml_text, Loader=yaml.Loader)
    targets = []

    for data in targets_data:
        new_target = Target(data["name"], data["number"])
        for target_service_name in data["am_services"]:
            for service in services:
                if service.name == target_service_name:
                    new_target.add_am_service(service)

        for target_service_name in data["pm_services"]:
            for service in services:
                if service.name == target_service_name:
                    new_target.add_pm_service(service)

        targets.append(new_target)
    
    return targets


if __name__ == '__main__':
    targets = load_targets_from_file('targets.yaml')
    for target in targets:
        print(target)
