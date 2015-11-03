#
# Script to download all Telegram history of a contact to a CSV file
# Usage: python3 history_downloader.py "Pierre" "history_pierre.csv"
#

from pytg import Telegram
from pytg.exceptions import IllegalResponseException

import csv
import sys
import time

arguments = sys.argv
if len(arguments) != 3:
    print("Invalid arguments.")
    sys.exit()

contact_name = arguments[1]
csv_output_filename = arguments[2]

tg = Telegram(
    telegram="./tg/bin/telegram-cli",
    pubkey_file="./tg-server.pub"
)
receiver = tg.receiver
sender = tg.sender

print("Performing mandatory call to dialog list")
dialog_list = sender.dialog_list()

# Parameters to retrieve 1'000'000 messages
chunk_message_count = 100
max_calls = 10000

history = list()
print("Starting to call API to retrieve history for contact: " + contact_name)
for i in range(0, max_calls):
    try:
        message_list = sender.history(contact_name, chunk_message_count,
                                      i * chunk_message_count)
        history.extend(message_list)
        time.sleep(1)
    except IllegalResponseException:
        print("Reached max offset, stopping API calls")
        break
    finally:
        print("Retrieved " + str(len(history)) + " messages")

print("Saving history to file: " + csv_output_filename)
with open(csv_output_filename, 'w', newline='') as csv_file:
    history_writer = csv.writer(csv_file, delimiter="\t", quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
    history_writer.writerow(["date", "from", "to", "text"])
    for message in history:
        date = message["date"]
        source = message["from"]["print_name"]
        destination = message["to"]["print_name"]
        text = message["text"] if "text" in message else ""
        history_writer.writerow([date, source, destination, text]);

    print("Saved history to file")
