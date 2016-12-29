#!/usr/bin/python3

#
# Script to download all Telegram history of a contact to a CSV file
#

from pytg import Telegram
from pytg.exceptions import IllegalResponseException

import argparse
import csv
import time

MIN_MESSAGES = 1000000


def download_history(telegram_binary, telegram_key, contact_name,
                     csv_output_filename, max_messages):
    tg = Telegram(
        telegram=telegram_binary,
        pubkey_file=telegram_key
    )
    sender = tg.sender

    print("Performing mandatory call to dialog list")
    sender.dialog_list()

    # Parameters to retrieve 1'000'000 messages
    chunk_message_count = 100
    max_calls = int(max_messages / chunk_message_count) + 1
    if max_calls == 0:
        raise RuntimeError("Max calls is zero.")

    print("We are going to attempt to retrieve "
          "at least " + str(max_messages) + " messages.")

    history = list()
    print("Starting to call API to retrieve history "
          "for contact: " + contact_name)
    print("This operation may take a while.")
    for i in range(0, max_calls):
        try:
            message_list = sender.history(contact_name, chunk_message_count,
                                          i * chunk_message_count)
            history.extend(message_list)

            # Wait a second to avoid issuing too many calls
            wait_time_seconds = 1
            time.sleep(wait_time_seconds)
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
            history_writer.writerow([date, source, destination, text])

        print("Successfully saved history to file.")

parser = argparse.ArgumentParser(description="Extracts Telegram history.")
parser.add_argument("telegram_binary",
                    help="something like ../tg/bin/telegram-cli")
parser.add_argument("telegram_key",
                    help="something like ../tg/tg-server.pub")
parser.add_argument("contact_name")
parser.add_argument("--csv_output_filename",
                    help="CSV file where to save the messages",
                    default="history.csv")
parser.add_argument("--min_messages",
                    type=int,
                    help="Maximum number of messages to retrieve.",
                    default=MIN_MESSAGES)
args = parser.parse_args()

if __name__ == '__main__':
    download_history(
        args.telegram_binary, args.telegram_key,
        args.contact_name, args.csv_output_filename,
        args.min_messages
    )
