import enum
from typing import Union, Callable
from pathlib import Path
import os
from urllib.request import urlretrieve
import requests

class ServiceType(enum.Enum):
    TXT = 1
    IMG = 2

class Service:
    name: str
    service_type: ServiceType
    res_path: Path
    url: str
    _run_func: Union[Callable[[str], str], Callable[[str, Path], bool]]


    def __init__(self, new_name: str, new_service_type: ServiceType, new_res_path: str, new_url: str, new_run_func):
        self.name = new_name.lower()
        self.service_type = new_service_type
        if new_res_path:
            self.res_path = Path(new_res_path)
        else:
            self.res_path = None
        self.url = new_url
        self.run_func = new_run_func


    def run(self) -> str:
        # Call run_func but only pass in res_path if service_type is IMG
        if self.service_type == ServiceType.TXT:
            return self.run_func(self.url)
        else:
            return self.run_func(self.url, self.res_path)
    

    def cleanup(self):
        if self.res_path and self.res_path.exists():
            os.remove(self.res_path)


def run_meowfacts(src_url: str) -> str:
    res = requests.get(src_url)
    if res.status_code == 200:
        return res.json()["data"][0]
    else:
        return None


def run_cataas(src_url: str, dest_path: Path) -> str:
    res = urlretrieve(src_url, dest_path)
    return res[0]

services = {
    "meowfacts": Service("meowfacts", ServiceType.TXT, '', 'https://meowfacts.herokuapp.com', run_meowfacts),
    "cataas": Service("cataas", ServiceType.IMG, 'res/cataas.jpg', 'https://cataas.com/cat', run_cataas),
}


def test_meowfacts():
    text = services["meowfacts"].run()
    print(f"meowfacts: {text}")
    input('...')
    services["meowfacts"].cleanup() # NOTE: this should not do anything; it's called only to test that it causes no error when executing with a TXT service

def test_cataas():
    import sys, subprocess

    path = services["cataas"].run()
    print(f"cataas: {path}")
    
    # open image file in defualt application (multi-platform support)
    # TODO: make this work
#    if sys.platform.startswith('win'):
#        subprocess.call(path)
#    elif sys.platform.startswith('linux'):
#        subprocess.call(['xdg-open','filename'])

    input('...')
    services["cataas"].cleanup()

if __name__ == '__main__':
    test_meowfacts()
    test_cataas()
