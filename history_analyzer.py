
import datetime
import csv
import sys

import matplotlib.pyplot as plt

arguments = sys.argv
if len(arguments) != 2:
    print("Invalid arguments.")
    sys.exit()

history_csv_filename = arguments[1]

with open(history_csv_filename, newline='') as csvfile:
    history_reader = csv.reader(csvfile, delimiter='\t', quotechar='"')

    next(history_reader, None)
    full_message_list = list()
    for message in history_reader:
        date = datetime.datetime.fromtimestamp(int(message[0]))
        source = message[1]
        destination = message[2]
        text = message[3]
        full_message_list.append({
            "date": date,
            "source": source,
            "destination": destination,
            "text": text
        })

    day_to_messages_map = dict()
    for message in full_message_list:
        parsed_datetime = message["date"]
        year = parsed_datetime.year
        month = parsed_datetime.month
        day = parsed_datetime.day
        hour = parsed_datetime.hour
        minute = parsed_datetime.minute
        second = parsed_datetime.second

        date_string = parsed_datetime.strftime('%Y/%m/%d')
        if date_string not in day_to_messages_map:
            day_to_messages_map[date_string] = 0
        day_to_messages_map[date_string] += 1

        #print(str(date) + ": " + source + " -> " + destination + " : " + text)

    date_list = sorted(day_to_messages_map.keys())
    date_count_list = list()
    for date in date_list:
        date_count_list.append(day_to_messages_map[date])

    date_count = len(date_list)
    plt.bar(range(date_count), date_count_list)
    plt.xticks(range(date_count), date_list, size='small', rotation='vertical')
    #plt.show()

    sender_to_message_map = dict()
    for message in full_message_list:
        source = message["source"]
        if source not in sender_to_message_map:
            sender_to_message_map[source] = list()
        sender_to_message_map[source].append(message)

    for sender, message_list in sender_to_message_map.items():
        message_count = len(message_list)
        message_chars = sum([len(message) for message in message_list])
        print(sender + ", Count: " + str(message_count) + ", Chars: " + str(message_chars))
