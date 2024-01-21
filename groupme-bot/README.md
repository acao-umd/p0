# Bot Info

## Usage
To activate the bot, just run ```python3 bot.py```.

## Flags
There are three useful flags.

1. ```-h``` or ```--help``` brings up usage information, which is reflected here
2. ```-s SENDER``` or ```--sender SENDER``` will override the primary sender ID with SENDER (if this flag is not
    provided then it defaults to mine).
3. ```--debug``` runs the script in debug mode, which prints some additional information to the console
    in some cases.

## Features

1. When the script is ran, the bot will send the message ```Active```.

2. If the user with the primary sender ID (I am the default) sends the message ```hello bot```, the bot
    will reply with ```hi```.

3. If any user sends the message ```good morning```, the bot will reply with ```good morning```, followed by their
username. Same goes with ```good night```.

4. If the primary user sends the message ```<n> cat gifs```, where ```n``` is a natural number less than 5000, 
the bot will send ```n``` links to randomly selected (but contiguous) cat gifs from Giphy as seperate messages.
If ```n``` is invalid, no reply is sent.

5. If the primary user sends the message ```bye bot```, then the bot will reply with ```bye``` and the script 
will terminate.