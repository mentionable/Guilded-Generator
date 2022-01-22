import multiprocessing
import os, sys
import ctypes
import requests
import itertools 
import string
import random
import threading 
from lib import arguments


class GuildedGenerator:
    def __init__(self, arguments):
        self.args = arguments
        self.created = 0
        self.session = requests.Session()
        self.proxies = itertools.cycle(
            [_ for _ in open("data/proxies.txt").read().rsplit()]
        )

    def proxy(self) -> dict:
        proxy_dict = {"http" : f"http://{next(self.proxies)}", "https" : f"http://{next(self.proxies)}"}
        return None if self.args.proxies.lower() == "n" else proxy_dict

    def randomstr(self, amount: int) -> str:
        _string = "".join(random.choice(string.ascii_letters) for _ in range(amount))
        return _string

    def headers(self) -> dict:
        return {
            "guilded-client-id" : "f1a162c9-8992-468c-afdd-de50fd3fd428",
            "guilded-stag" :      "90156f8d1cc4886a65e92aded2861869",
            "guilded-device-id" : "537b5c96c662685a3c6a9cf97b15fafe68ca4eb5141254ac908d08f4460218cc"
        }

    def update_title(self):
        while self.created != 0:
            if os.name == "nt":
                ctypes.windll.kernel32.SetConsoleTitleW(f"Total Created: {self.created}")
            elif os.name == "posix":
                print(f"\x1b]2;Total Created: {self.created}\x07")


    def joinserver(self, invite, cookie):
        try:
            proxies = self.proxy()
            headers = self.headers()
            headers["cookie"] = f"hmac_signed_session={cookie}"

            response = self.session.put(f"https://www.guilded.gg/api/invites/{invite}", headers=headers, proxies=proxies)

            if response.status_code in (200, 203, 204):
                print("[anti.sh] Joined Server!")
            elif response.status_code in (400, 403, 404):
                print("[anti.sh] Error Joining Server.")

        except requests.exceptions.RequestException:
            print("[anti.sh] Request Error!")


    def login(self, email, password):
        try:
            headers = self.headers()
            proxies = self.proxy()
            payload = {"getMe" : True, "email" : email, "password" : password}
            
            response = self.session.post("https://www.guilded.gg/api/login", json=payload, headers=None, proxies=proxies)

            if response.status_code in (200, 203, 204):
                cookie = response.cookies['hmac_signed_session']

                print(f"[anti.sh] Fetched Cookie: {cookie[:100]}...")
                open("data/cookies.txt", "a").write(cookie+'\n')
                self.joinserver(self.args.invite, cookie)

            elif response.status_code in (400, 403, 404):
                print("[anti.sh] Error logging into account: ", end="")
                print(response.json())
                
        except requests.exceptions.RequestException:
            print("[anti.sh] Request Error!")


    def register(self, username, password, email):
        try:
            headers = self.headers()
            proxies = self.proxy()

            payload = {
                "extraInfo" : {"platform" : "desktop"},
                "name"      : username,
                "fullName"  : username,
                "password"  : password,
                "email"     : email
            }

            response = self.session.post("https://www.guilded.gg/api/users", params="type=email", headers=headers, proxies=proxies, json=payload)

            if response.status_code in (200, 203, 204):
                print("[anti.sh] Account Created!")
                self.created += 1
                self.login(email, password)

            elif response.status_code in (400, 403, 404):
                print("[anti.sh] Error Creating Account.")

        except requests.exceptions.RequestException:
            print("[anti.sh] Request Error!")

    
    def worker_thread(self, username, password, email):
        threads = [
            threading.Thread(
                target=self.register,
                args=(username, password, email)
            )
        for index in range(self.args.threads)]
        for thread in threads: thread.start()

    def start(self):
        threading.Thread(target=self.update_title).start()

        workers = [
            multiprocessing.Process(
                target=self.worker_thread,
                args=(self.args.username, 
                      self.args.password,
                      self.randomstr(amount=15) + "@gmail.com")
            )
        for index in range(self.args.workers)]
        for worker in workers: worker.start()


if __name__ == "__main__":
    generator = GuildedGenerator(
        arguments.arg_parser()
        )
    generator.start()
