import requests
import time
import json
import os
from dotenv import load_dotenv
from argparse import ArgumentParser
from random import randint
from urllib import parse, request
from re import search

parser = ArgumentParser(
    prog='Bot',
    description='Runs a groupme bot'
)

parser.add_argument('-s', '--sender', help='the (integer) id of the sender to whom the bot will exclusively respond.\
                    if none is provided then Anh\'s sender id is used.')
parser.add_argument('--debug', action='store_true')

args = parser.parse_args()

load_dotenv()

BOT_ID = os.getenv("BOT_ID")
GROUP_ID = os.getenv("GROUP_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
LAST_MESSAGE_ID = None


def send_message(text, attachments=None):
    """Send a message to the group using the bot."""
    post_url = "https://api.groupme.com/v3/bots/post"
    data = {"bot_id": BOT_ID, "text": text, "attachments": attachments or []}
    response = requests.post(post_url, json=data)
    return response.status_code == 202


def get_group_messages(since_id=None):
    """Retrieve recent messages from the group."""
    params = {"token": ACCESS_TOKEN}
    if since_id:
        params["since_id"] = since_id

    get_url = f"https://api.groupme.com/v3/groups/{GROUP_ID}/messages"
    response = requests.get(get_url, params=params)
    
    if response.status_code == 200:
        # this shows how to use the .get() method to get specifically the messages but there is more you can do (hint: sample.json)
        return response.json().get("response", {}).get("messages", [])
    return []


def process_message(message):
    """Process and respond to a message."""
    global LAST_MESSAGE_ID

    text = None

    if message['text']:
        text = message['text'].lower()

    if args.debug:
            print(f'Processing message {message}')

    # i.e. responding to a specific message (note that this checks if "hello bot" is anywhere in the message, not just the beginning)
    if not LAST_MESSAGE_ID:
        send_message('Active')
    elif text == 'good morning' and message['sender_type'] == 'user':
        send_message('good morning ' + message['name'])
    elif text == 'good night' and message['sender_type'] == 'user':
        send_message('good night ' + message['name'])
    elif message['sender_id'] == (args.sender if args.sender else '103115108'):
        m = search('^(\\d+) cat gifs$', text)
        if m and 0 < int(m.group(1)) < 5000:

            params = parse.urlencode({
                "api_key":"xnrKQz4Cx39sRUtdk4wbVBgL7MmhtH5F",
                "q":"cats",
                "limit":m.group(1),
                "offset":randint(0, 4999 - int(m.group(1)))
            })

            with request.urlopen("".join(("http://api.giphy.com/v1/gifs/search?", params))) as response:
                if response.getcode() == 200:
                    gifs = json.loads(response.read())
                    send_message("Here are the gifs!")
                    for gif in gifs['data']:
                        send_message(gif['url'])
                elif args.debug:
                    print(f'A response status code of 200 was expected but encountered {response.status.code}\n')
        elif text == 'bye bot':
            send_message('bye')
            exit(0)
        elif text == 'hi bot':
            send_message("hi")
    
    LAST_MESSAGE_ID = message["id"]


def main():
    global LAST_MESSAGE_ID
    # this is an infinite loop that will try to read (potentially) new messages every 1 seconds, but you can change this to run only once or whatever you want
    while True:
        messages = get_group_messages(LAST_MESSAGE_ID)
        for message in messages:
            if not LAST_MESSAGE_ID:
                process_message(message)
                break
            else:
                process_message(message)
        time.sleep(1)

if __name__ == "__main__":
    main()