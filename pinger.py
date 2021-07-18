import json
import random
import requests
import string
import time

from copy import deepcopy
from signal import signal, SIGINT
from sys import exit
from typing import Dict, Mapping


with open('configuration.template.json', 'r') as f:
    jconfig = json.load(f)


lst_wbhook = [hook for dct in jconfig['webhook'] for hook in dct.values()]
lst_users = [usr for usr in jconfig['user']]
lst_users += ['Dummy1', 'Dummy2']


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)


class DiscordMessenger:
    def __init__(self) -> None:
        with open('discord_template.json', 'r') as f:
            self.template = json.load(f)

    @property
    def simple_template(self) -> Mapping[str, str]:
        """
        Return a simplified copy of the message template
        """
        tp_simple = deepcopy(self.template)
        tp_simple.pop('avatar_url')
        tp_simple.pop('embeds')

        return tp_simple

    def create_simple_message(self, 
        username: str, content: str) -> Mapping[str, str]:
        """
        Create a message from the simple template
        """
        msg = self.simple_template
        msg['username'] = username
        msg['content'] = content

        return msg


class DiscordClient:
    def __init__(self) -> None:
        self.messenger = DiscordMessenger()

    def send(self, 
        webhook: str, username: str, message: str) -> Mapping[str, str]:
        """
        POST a message to the webhook
        """
        payload = self.messenger.create_simple_message(username, message)
        resp = requests.post(webhook, json=payload)

        return resp


def main() -> None:
    """
    Spam #pokespam
    """
    dclient = DiscordClient()
    while True:
        message = ''.join(random.sample(
            string.ascii_lowercase + 
            string.ascii_uppercase + 
            ' ' + string.digits, 
            random.randrange(1, 5)))
        thishook = random.choice(lst_wbhook)
        thisuser = random.choice(lst_users)

        resp = dclient.send(thishook, thisuser, message)

        print(resp)
        if resp == '<Response [429]>':
            time.sleep(5)
        else:
            time.sleep(random.random() * random.randint(0, 3))


if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)

    main()
