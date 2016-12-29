# telegram-history
Retrieve and analyze Telegram messenger history.

# Installation

* Create a folder where you are going to clone the repo of Telegram-CLI and this repo.

* Install the Telegram-CLI
  * https://github.com/vysheng/tg
  * `git clone --recursive https://github.com/vysheng/tg`
  * `cd tg`
  * `sudo apt-get install libreadline-dev libconfig-dev libssl-dev lua5.2 liblua5.2-dev libevent-dev libjansson-dev libpython-dev make`
  * `./configure`
  * `make`
  * `bin/telegram-cli -k tg-server.pub`
    * after waiting a few seconds, you will be asked for your phone number
    * after giving your phone number, you will be asked for a pass code, that you should receive as a message on your phone
    * after entering this pass code, you should have a working Telegram-CLI
    * messages that are sent and received appear in a feed
  * using the `contact_list` command of the Telegram-CLI
    * identify the contact from which you want to have the history.
    * write down the name in your notes for later

* Install the Python binding to Telegram-CLI
  * `sudo pip3 install pytg`

* Clone this repo
  * `git clone https://github.com/pwalch/telegram-history.git`
  * `cd telegram-history`
  * `./history_downloader.py ../tg/bin/telegram-cli ../tg/tg-server.pub Pierre --min_messages 550`
    * pay attention to the path to Telegram-CLI (`tg` folder).
