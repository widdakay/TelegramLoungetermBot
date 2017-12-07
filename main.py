#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Bot to reply to Telegram messages.

This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
import logging
import telegram, os
from telegram.error import NetworkError, Unauthorized
from time import sleep
from subprocess import Popen

update_id = None


def main():
    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot('508556794:AAEoXkUd4D0W8UqH9DReFdDlz7rU00x2j3U')

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1



def echo(bot):
    """Echo the message the user sent."""
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message and len(update.message.text) > 2 and update.message.text[0] == "/":  # your bot can receive updates without messages
            # Reply to the message
            text = update.message.text[1:]

            print "command: '"+text+"'"
            params = ""
            command = text[:text.find(" ")]
            if text.find(" "):
                params = text[text.find(" ")+1:]

            if command == "yt":
                update.message.reply_text("Playing youtube video '" + params + "'")
            elif command == "ct":
                update.message.reply_text("closing tab")
            elif command == "vd":
                update.message.reply_text("decreasing volume")
            elif command == "vu":
                update.message.reply_text("increasing volume")
            else:
                update.message.reply_text("executing: '" + text + "'")
            #print(["ssh", "-i", "/Users/erik/.ssh/id_rsa", "east@ea.st.hmc.edu", "bash", "-l", "'/home/east/bin/" + command + params + "'"])
            #command = ["/usr/bin/ssh", "-i", "/Users/erik/.ssh/id_rsa", "east@ea.st.hmc.edu", "bash", "-l", "'/home/east/bin/" + command, + params + "'"]
            commandarr = ["/home/east/bin/" + command, params]
            print command
            print "executing command"
            Popen(commandarr)
            #commandstr = "ssh -i /Users/erik/.ssh/id_rsa east@ea.st.hmc.edu bash -l '/home/east/bin/" + command + " " + params + "'"
            #print commandstr
            os.system(commandstr)
            print "done"

            #update.message.reply_text(update.message.text)


if __name__ == '__main__':
    main()