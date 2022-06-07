import enum
from typing import Union, Callable
from pathlib import Path
import os
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
        self._run_func = new_run_func

    def run(self) -> str:
        # Call run_func but only pass in res_path if service_type is IMG
        if self.service_type == ServiceType.TXT:
            return self._run_func(self.url)
        else:
            return self._run_func(self.url, self.res_path)

    def cleanup(self):
        if self.res_path and self.res_path.exists():
            os.remove(self.res_path)

    def __str__(self):
        return f"{self.name} - {self.service_type}"


# TODO: figure out some way to cut down on code repetition for these functions; might not be possible for text services since we want to wrap the text in boilerplate text not from the apis
def run_generic_txt_service(src_url: str, format='text'):
    res = requests.get(src_url)
    if res.status_code != 200:
        return None

    if format == 'text':
        return res.text
    elif format == 'json':
        return res.json()
    else:
        return res


def run_generic_img_service(src_url: str, dest_path: Path) -> str:
    res = requests.get(src_url)
    if res.status_code != 200:
        return None

    with open(dest_path, 'wb') as f:
        f.write(res.content)
    return dest_path


def run_meowfacts(src_url: str) -> str:
    text = run_generic_txt_service(src_url, format='json')
    # extract what we want from json if `text` is defined, else return None
    return f"Did you know this about cats? - {text['data'][0]}" if text else None


def run_dogapi(src_url: str) -> str:
    text = run_generic_txt_service(src_url, format='json')
    # extract what we want from json if `text` is defined, else return None
    return f"Did you know this about dogs? - {text['facts'][0]}" if text else None


def run_funfacts(src_url: str) -> str:
    text = run_generic_txt_service(src_url, format='json')
    # extract what we want from json if `text` is defined, else return None
    return f"Fun Fact: \"{text[0]}\"" if text else None


def run_tronalddump(src_url: str) -> str:
    text = run_generic_txt_service(src_url, format='json')
    # extract what we want from json if `text` is defined, else return None
    return f"\"{text['value']}\" - Donald Trump" if text else None


def run_randomdog(src_url: str, dest_path: Path) -> str:
    url_res = requests.get(src_url)
    if url_res.status_code == 200:
        img_url = 'https://random.dog/' + url_res.text
    else:
        return None
    return run_generic_img_service(img_url, dest_path)


def run_randomfox(src_url: str, dest_path: Path) -> str:
    url_res = requests.get(src_url)
    if url_res.status_code == 200:
        img_url = url_res.json()["image"].replace('\\', '')
    else:
        return None
    return run_generic_img_service(img_url, dest_path)


def run_forzaapi(src_url: str, dest_path: Path) -> str:
    url_res = requests.get(src_url)
    if url_res.status_code == 200:
        img_url = url_res.json()["image"]
    else:
        return None
    return run_generic_img_service(img_url, dest_path)


def run_foodish(src_url: str, dest_path: Path) -> str:
    url_res = requests.get(src_url)
    if url_res.status_code == 200:
        img_url = url_res.json()["image"]
    else:
        return None
    return run_generic_img_service(img_url, dest_path)


services = [
    # text services
    Service("meowfacts", ServiceType.TXT, '',
            'https://meowfacts.herokuapp.com', run_meowfacts),
    Service("dogapi", ServiceType.TXT, '',
            'https://dog-api.kinduff.com/api/facts', run_dogapi),
    Service("funfacts", ServiceType.TXT, '',
            'http://api.aakhilv.me/fun/facts', run_funfacts),
    Service("tronalddump", ServiceType.TXT, '',
            'https://tronalddump.io/random/quote', run_tronalddump),

    # image services
    Service("cataas", ServiceType.IMG, 'res/cataas.jpg',
            'https://cataas.com/cat', run_generic_img_service),
    Service("randomdog", ServiceType.IMG, 'res/randomdog.jpg',
            'https://random.dog/woof?include=jpg', run_randomdog),
    Service('randomfox', ServiceType.IMG, 'res/randomfox.jpg',
            'http://randomfox.ca/floof/', run_randomfox),
    Service('randomduck', ServiceType.IMG, 'res/randomduck.jpg',
            'https://random-d.uk/api/v2/randomimg?type=jpg', run_generic_img_service),
    Service('forzaapi', ServiceType.IMG, 'res/forzaapi.jpg',
            'https://forza-api.tk', run_forzaapi),
    Service('coffeeapi', ServiceType.IMG, 'res/coffeeapi.jpg',
            'https://coffee.alexflipnote.dev/random', run_generic_img_service),
    Service('foodish', ServiceType.IMG, 'res/foodish.jpg',
            'https://foodish-api.herokuapp.com/api/', run_foodish),
]


def test_txt_service(s: Service):
    text = s.run()
    print(f"{s.name}: {text}")
    input('...')


def test_img_service(s: Service):
    path = s.run()
    print(f"{s.name}: {path}")
    _open_image_file(path)
    input('...')
    s.cleanup()


def _open_image_file(fp: Path):
    import sys
    import subprocess
    if sys.platform.startswith('win'):
        pass #subprocess.call(fp, shell=True) # TODO: make this work on Windows
    elif sys.platform.startswith('linux'):
        subprocess.call(['xdg-open', fp])


if __name__ == '__main__':
    for service in services:
        donottest_list = []
        if service.name in donottest_list:
            continue

        if service.service_type == ServiceType.TXT:
            test_txt_service(service)
        else:
            test_img_service(service)
