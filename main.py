import requests
import os, sys
import json 
import base64
import time
import string
import random
import threading
import argparse

class GuildedGenerator:
    def __init__(self, username, invite, password, threads):
        self.username = username
        self.password = password
        self.invite = invite
        self.threads = threads
        
        self.created = 0
        self.proxies = [_ for _ in open('data/proxies.txt').read().rsplit('\n')]
        self.session = requests.Session()

    def proxy(self):
        return {'https' : 'http://%s' % random.choice(self.proxies), 
                'http' : 'http://%s' % random.choice(self.proxies)}

    def start(self):
        for index in range(self.threads):
            email = ''.join(random.choice(string.ascii_letters) 
                         for _ in range(7)) + '@gmail.com'
            threading.Thread(target=self.thread_task, args=(email,)).start()

    def thread_task(self, email):
        self.create_account(email)

    def create_account(self, email):
        global COUNT
        try:
            headers = {
                'authority'           : 'www.guilded.gg',
                'method'              : 'POST',
                'path'                : '/api/users?type=email',
                'scheme'              : 'https',
                'accept'              : 'application/json, text/javascript, */*; q=0.01',
                'accept-encoding'     : 'gzip, deflate, br',
                'accept-language'     : 'en-US,en;q=0.9',
                'content-type'        : 'application/json',
                'origin'              : 'https://www.guilded.gg',
                'sec-ch-ua'           : 'Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96',
                'sec-ch-ua-mobile'    : '?0',
                'sec-ch-ua-platform'  : 'Windows',
                'sec-fetch-dest'      : 'empty',
                'sec-fetch-mode'      : 'cors',
                'sec-fetch-site'      : 'same-origin',
                'user-agent'          : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
                'x-requested-with'    : 'XMLHttpRequest',
                'guilded-client-id'   : 'f1a162c9-8992-468c-afdd-de50fd3fd428',
                'guilded-stag'        : '90156f8d1cc4886a65e92aded2861869',
                'guilded-device-id'   : '537b5c96c662685a3c6a9cf97b15fafe68ca4eb5141254ac908d08f4460218cc',
            }

            payload = {
                'extraInfo' : {'platform' : 'desktop'},
                'email'     : email,
                'fullName'  : self.username,
                'name'      : self.username,
                'password'  : self.password
            }

            response = self.session.post('https://www.guilded.gg/api/users', params='type=email', 
                                          headers=headers, proxies=self.proxy(), json=payload)
            if response.status_code in (200, 201, 203, 204):
                self.created += 1
                os.system('title Guilded Generator - Created: %s' % self.created)
                print('[$] Created Account: %s' % response.json()['user']['name'])

                payload = {'getMe' : True, 'email' : email, 'password' : self.password}
                login = self.session.post('https://www.guilded.gg/api/login', json=payload, proxies=self.proxy())

                if login.status_code in (200, 201, 203, 204):
                    cookie = login.cookies['hmac_signed_session']
                    print('[$] Fetched Cookie: %s' % cookie[:50] + '...')
                    open('data/cookies.txt', 'a').write(cookie+'\n')

                    headers = {'cookie' : f'hmac_signed_session={cookie}'}
                    invite = self.session.put(f'https://www.guilded.gg/api/invites/{self.invite}', headers=headers, proxies=self.proxy())

                    if invite.status_code in (200, 201, 203, 204): 
                        print(f'[$] Joined Server: {cookie[:50]}...')

                    else: print('[$] Error Joining Server')
                elif response.status_code in (400, 401, 403, 404): print('[$] Error Fetching Cookie / Logging in')
            elif response.status_code in (400, 401, 403, 404): print('[$] Error Creating Account')
        except requests.exceptions.RequestException as e: 
            print('[$] Request Exception Occured: %s' % str(e)[:30])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', metavar='', required=True, type=str, help='Generated account usernames')
    parser.add_argument('-p', '--password', metavar='', required=False, type=str, help='Generated account passwords')
    parser.add_argument('-i', '--invite', metavar='', required=True, type=str, help='Invite to guilded.gg server the bots will join')
    parser.add_argument('-t', '--threads', metavar='', required=True, type=int, help='Amount of threading while creating accounts')
    args = parser.parse_args()

    if args.password == None:
        args.password = ''.join(random.choice(string.ascii_letters) 
                               for _ in range(10))

    generator = GuildedGenerator(
        username=args.username,
        password=args.password,
        invite=args.invite,
        threads=args.threads
    )
    generator.start()
    
