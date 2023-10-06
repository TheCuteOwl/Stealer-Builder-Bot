Designed to be used with Trap Stealer


This script utilizes a Discord bot to build a virus. Only authorized key users are able to generate the virus
To use the Virus-Builder-Bot, you have to first obtain a key from the administrator. Once you have the key, you can proceed to set up the bot. Follow the instructions carefully to ensure the bot is set up properly:

~ How to install it?
Clone the repository from GitHub.

Install the required dependencies by running pip install -r requirements.txt.

Set up a new Discord Bot application in the Discord Developer Portal.

Add the bot to your Discord server using the OAuth2 link generated in the Developer Portal, Enable every Privileged Gateway Intents
Open the main.py in a text editor and replace:

```
Bot_token = 'Bot Token')
channelid = ID # The channel where the builder will work
admin = ID # The admin ID (He can generate key for user)
```
Run the ```py main.py``` file using Python.

as it is intended for educational purposes only. It is not meant to be used for any malicious intents or purposes.
