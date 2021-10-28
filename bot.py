#!/usr/bin/env python

from pycoingecko import CoinGeckoAPI
from telegram import ReplyKeyboardMarkup

import time , datetime , pytz
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import  Update
from persiantools.jdatetime import JalaliDate




def topcoins(x):

    cg = CoinGeckoAPI()
    data_list = cg.get_coins_markets(vs_currency='usd')
    data_list = data_list[0:20]

    for i in range (x):

        new_data_list = []

        symbol_list = []
        current_price_list = []
        p_c_p_list = []
        state_list = []
        number_list = []

        number = 0
        state = ''

        for i in data_list:
            int_p_c_p = float(i['price_change_percentage_24h'])

            symbol = i['symbol'].upper()
            current_price = ("$" + '{0:000,.2f}'.format(i['current_price']))
            p_c_p = ("" +"("+'{0:0,.2f}'.format(i['price_change_percentage_24h']) + "%)")

            if (int_p_c_p < 1 and int_p_c_p > 0):
                state = "🟡"
            elif (int_p_c_p > -1 and int_p_c_p < 0):
                state = "🟠"
            elif (int_p_c_p > 1):
                state = "🟢"
            elif (int_p_c_p < -1):
                state = "🔴"

            number+=1
            number2 = ("{:02d}".format(number))
            number_list.append(str(number2))

            symbol_list.append(symbol)
            current_price_list.append(current_price)
            p_c_p_list.append(p_c_p)
            state_list.append(state)


        new_data_list = [' '.join(x) for x in zip(number_list,state_list,symbol_list,current_price_list,p_c_p_list)]
        my_result = ' \n '.join(new_data_list)

    return my_result


def time():


    nyc_datetimeUS = datetime.datetime.now(pytz.timezone('US/Eastern'))

    now_yearUS = nyc_datetimeUS.year
    now_monthUS = nyc_datetimeUS.month
    now_dayUS = nyc_datetimeUS.day
    now_hourUS = nyc_datetimeUS.hour
    now_hourUS = ("{:02d}".format(now_hourUS))
    now_minuteUS = nyc_datetimeUS.minute
    now_minuteUS = ("{:02d}".format(now_minuteUS))
    now_secondUS = nyc_datetimeUS.second
    now_secondUS = ("{:02d}".format(now_secondUS))

    now_time_string_US = '{}-{}-{} {}:{}:{}'.format(now_yearUS,now_monthUS,now_dayUS,now_hourUS,now_minuteUS,now_secondUS)



    nyc_datetimeIR = datetime.datetime.now(pytz.timezone('Asia/Tehran'))

    now_yearIR = nyc_datetimeIR.year
    now_monthIR = nyc_datetimeIR.month
    now_dayIR = nyc_datetimeIR.day
    now_hourIR = nyc_datetimeIR.time().hour
    now_hourIR = ("{:02d}".format(now_hourIR))
    now_minuteIR = nyc_datetimeIR.time().minute
    now_minuteIR = ("{:02d}".format(now_minuteIR))
    now_secondIR = nyc_datetimeIR.time().second
    now_secondIR = ("{:02d}".format(now_secondIR))

    date_fa = JalaliDate(datetime.date(now_yearIR, now_monthIR, now_dayIR))
    now_time_string_IR = '{}:{}:{}'.format(now_hourIR, now_minuteIR, now_secondIR)




    UStime=(f'🇺🇸 {now_time_string_US}')
    IRtime=(f'🇮🇷 {date_fa} {now_time_string_IR}')
    ftime = (f' {UStime}\n {IRtime}')

    return ftime

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user


    menu_keyboard = [["Top Coins 🔝", "Help ❗️"]]
    menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()} \! Welcome to "My Coin Price" bot', reply_markup=menu_markup)


    idu = update.effective_chat.id

    def ex_id(id):
        result = False
        file = open('user.txt','r')
        for line in file:
            if line.strip()==id:
                result = True
        file.close()
        return result

    f = open('user.txt','a')
    if (not ex_id(str(idu))):
        f.write("{}\n".format(idu))
        f.close



def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Click to get started /Start')


def trunk_command(update: Update, context: CallbackContext) -> None:


    if (update.message.text == "Top Coins 🔝"):

        oscillation = topcoins(20)
        ftime = time()

        update.message.reply_markdown_v2(f'```\ {oscillation} \n\n{ftime}```\n\n@MyCoinPriceBot')


    elif(update.message.text == "Help ❗️"):
        update.message.reply_text('Click to get started /Start')


def test_command(update: Update, context: CallbackContext) -> None:

    update.message.reply_markdown_v2(f'```\ test```')


def main() -> None:
    updater = Updater("API")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("test", test_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, trunk_command))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
