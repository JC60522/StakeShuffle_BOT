import time, os, requests, json
import matplotlib.pyplot as plt
import numpy as np
import tweepy
import pandas as pd
import matplotlib.patches as mpatches
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from datetime import datetime, timezone
from itertools import accumulate


auth = tweepy.OAuthHandler('###################', '#############################################')
auth.set_access_token('#################-#################', '########################################')
api = tweepy.API(auth, wait_on_rate_limit=True)

def proposed_block_url():
    url = 'https://explorer.dcrdata.org'
    try:
        page = urlopen(url)
    except:
        logic()
    html = page.read().decode("utf-8")
    soup = bs(html, "html.parser")
    current_block = soup.find_all(class_="d-inline-block h3 position-relative")
    current_block = [str(x) for x in str(current_block)]
    first_smaller_than_index = current_block.index('<')
    current_block.pop(first_smaller_than_index)
    s_t_index = current_block.index('<')
    b_t_index = current_block.index('>')
    proposed_block = current_block[b_t_index+1:s_t_index]
    proposed_block = str(''.join(proposed_block))
    return proposed_block


def date_time(date):
    date = str(''.join(date))
    soup_main = bs(html_main, "html.parser")
    mixed_val = soup_main.find_all(class_="int")
    mixed_val = mixed_val[1]
    mix_int = [str(x) for x in str(mixed_val)]
    mix_int1 = mix_int[18:-7]
    mix_int2 = str("".join(mix_int1))

    total = soup_main.find_all(class_="int")
    total = list(total)
    total = total[0]
    total = [str(x) for x in str(total)]
    total.pop(0)
    first_index = total.index('>')
    second_index = total.index('<')
    total = total[first_index + 1:second_index]
    total_sent = str(''.join(total))
    total_sent = total_sent.replace(',', '')
    total_sent = round(float(total_sent))

    block = soup_main.find_all(class_="h5 d-inline-block pl-2")
    block = [str(x) for x in str(block)]
    block = str(block[2:])
    first_index = block.index('#')
    second_index = block.index('<')
    block = block[first_index + 3:second_index - 1]
    block = block[:-2]
    block_nr = str(''.join(block))
    block_nr  = block_nr.replace("'", '').replace(",", '').replace(" ", '')
    block_nr = int(block_nr)
    return mix_int2, date, total_sent, block_nr


def mixed_date_time(route):
    try:
        page = urlopen(route)
    except:
        logic()
    global html_main
    html_main = page.read().decode("utf-8")
    global soup_main
    soup_main = bs(html_main, "html.parser")
    date = soup_main.find_all(class_="fs18 font-weight-bold lh1rem d-inline-block pt-1")
    date = [str(x) for x in str(date)]
    date = date[-20:-8]
    try:
        if date[0] == '>':
            date.pop(0)
        mix_int2 = date_time(date)[0]
        total_sent = date_time(date)[2]
        block_nr = date_time(date)[3]
    except:
        mix_int2 = date_time(date)[0]
        total_sent = date_time(date)[2]
        block_nr = date_time(date)[3]
    date = date_time(date)[1]

    if len(mix_int2) >= 5:
        mix_int2 = mix_int2.replace(',','')
    if mix_int2 != '0':
        mixed_val2 = soup_main.find_all(class_="decimal")
        mixed_val2 = mixed_val2[3]
        mix_dec = [str(x) for x in str(mixed_val2)]
        mix_dec = mix_dec[22:-7]
        mix_dec = str("".join(mix_dec))
        mixed_in_block = float(str(mix_int2) + '.' + str(mix_dec))
    else:
        zero = 0
    try:
        return mixed_in_block, total_sent, block_nr, date
    except:
        return zero, total_sent, block_nr, date


def coin_supply():
    url = 'https://explorer.dcrdata.org'
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = bs(html, "html.parser")
    coin_supply = soup.find_all(class_="int")
    coin_supply = coin_supply[-2]
    coin_supply = [str(x) for x in str(coin_supply)]
    coin_supply = coin_supply[18:28]
    coin_supply = str("".join(coin_supply))
    coin_supply = coin_supply.replace(',','')
    coin_supply = float(coin_supply)
    return coin_supply


def usd_val(mixed_today):
    url = 'https://explorer.dcrdata.org'
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = bs(html, "html.parser")
    global usd_value
    usd_value = soup.get_text('Exchange Rate')
    usd_value = usd_value.split('\n')
    usd_value = usd_value[-27]
    usd_value = usd_value.lower()
    usd_value = usd_value.split('e')
    usd_value = float(usd_value[3])
    global USD
    USD = round((usd_value * mixed_today))


def twitter_data():
    api = tweepy.API(auth, wait_on_rate_limit=True)
    client_id = api.me()
    x = api.user_timeline(id = client_id, count = 1, tweet_mode='extended')
    tweet_body = [tweet.full_text for tweet in x]
    tweet_body = tweet_body[0]
    tweet_string = tweet_body.split(' ')
    prev_time_stamp = tweet_string[0]
    l_of_pts = prev_time_stamp.split('-')
    global latest_tweet_date
    latest_tweet_date = l_of_pts[2]
    global current_tw_dt
    current_tw_dt = datetime(int(l_of_pts[0]),int(l_of_pts[1]),int(l_of_pts[2])).timestamp()


def current_utc_time():
    now_utc = datetime.now(timezone.utc)
    global now_utc_list
    now_utc_list = str(now_utc)[11:16]
    current_time_list = str(now_utc).split(' ')
    cur_date = current_time_list[0]
    l_of_d = cur_date.split('-')
    current_timestamp = datetime(int(l_of_d[0]),int(l_of_d[1]),int(l_of_d[2])).timestamp()
    return current_timestamp


def record_helper(test_var):
    if test_var == True:
        data_values.pop()
    record_val = sorted(data_values)[-1]
    record_val2 = [int(x) for x in str(record_val)]

    if len(str(record_val)) == 14:
        record_val3 = record_val2[0:6]
    elif len(str(record_val)) == 15:
        record_val3 = record_val2[0:7]
    elif len(str(record_val)) == 16:
        record_val3 = record_val2[0:8]

    record_val4 = [str(i) for i in record_val3]
    global record_value
    record_value = int("".join(record_val4))
    return record_value


def record_check():
    url_2 = 'https://dcrdata.decred.org/api/chart/privacy-participation?axis=time&bin=day'
    response = requests.get(url_2)
    data = response.text
    parsed = json.loads(data)
    timestamp = parsed["t"]
    global data_values
    data_values = parsed["anonymitySet"]
    test_time = current_utc_time() - 86400
    ts_latest = timestamp[-1]
    test_var = False
    if ts_latest == test_time:
        test_var = True
        prev_rec = record_helper(test_var)
    else:
        prev_rec = record_helper(test_var)
    return prev_rec


def staked_in_usd():
    url = 'https://explorer.dcrdata.org'
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = bs(html, "html.parser")
    stake = soup.find_all(class_="int")
    stake = stake[5]
    staked_list = [str(x) for x in str(stake)]
    staked_list.pop(0)
    staked_list.pop(-1)
    stake_index1 = staked_list.index('>')
    stake_index2 = staked_list.index('<')
    global staked_val
    staked_val = staked_list[stake_index1 +1:stake_index2]
    staked_val = str("".join(staked_val))
    staked_val = staked_val.replace(',','')
    global stakedP
    stakedP = (round(int(staked_val) / coin_supply())) * 100
    staked_usd = round(int(staked_val) * usd_value)
    return staked_usd


def first_check():
    weight = 1
    while weight == 1:
        current_utc_time()
        if now_utc_list == '00:15':
            weight = 2
            logic()
        else:
            time.sleep(45)
            print('First time-based conditional not yet satisfied..')


def start_block1():
    with open('blocks_p1.csv', 'r') as f:
        data = f.read()
        data = data.split('\n')
    return int(data[-2])


def utcAndUsd():
    timeAndPrice = []
    currentTs = current_utc_time()
    prevDay = currentTs - 86400
    prevMonth = currentTs - 2678400
    global ts3
    global ts2
    ts3 = datetime.fromtimestamp(prevDay).strftime('%b %d %Y')
    ts2 = datetime.fromtimestamp(prevMonth).strftime('%b %d %Y')
    ts1 = ts3.split(' ')
    timeAndPrice.append(f"{ts1[0]} {ts1[1]}, {ts1[2]}', '${usd_value}")
    return timeAndPrice


def ticketPrice():
    url = 'https://explorer.dcrdata.org'
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = bs(html, "html.parser")
    ticket_ = soup.find_all(class_='int')
    global ticket
    ticket = ticket_[0]
    ticket = [str(x) for x in str(ticket)]
    index1 = ticket.index('>')
    index2 = ticket.index('/')
    ticket = ticket[index1 + 1:index2 - 1]
    ticket = ''.join(ticket)
    ticket = ticket.replace(',','')
    global ticketUsd
    ticketUsd = usd_value * float(ticket)
    return ticket


def txVol():
    df_data = pd.concat([df_dates, df_total], axis=1)
    df_agg2 = df_data.groupby(['Dates'], sort=False).sum()
    df_agg2 = df_agg2.tail(31)
    df_agg2 = df_agg2.reset_index()
    colNames = ['Closin prices']
    dfPrices = pd.read_csv('usd_price.csv', delimiter = '\n', names = colNames)
    dfPrices = dfPrices.tail(31)
    dfPrices = dfPrices.reset_index()
    df_agg2['Closin prices'] = dfPrices['Closin prices']
    dom = []
    day = []
    day2 = []
    price_list = []
    price = []
    cleaned_list = []
    p1 = df_agg2['Closin prices'].values.tolist()
    for i in p1:
        price_list.append(str(i).split(' '))
    for i in price_list:
        price.append(i[3])
    for i in price:
        indexOne = i.index('$')
        indexTwo = i.index(']')
        clean = i[indexOne + 1:indexTwo - 1]
        cleaned_list.append(clean)
    d2 = df_agg2['Dates'].values.tolist()
    for i in d2:
        dom.append(str(i).split(' '))
    for i in dom:
        day.append(i[1])
    for i in day:
        i2 = i[1:-2]
        day2.append(i2)

    df_agg2['day'] = pd.DataFrame(day2)
    df_agg2['clean'] = pd.DataFrame(cleaned_list).astype(float)
    df_agg2['USD-Val'] = df_agg2['clean'] * df_agg2['Total']
    dates = df_agg2['day'].values.tolist()
    N = len(dates)
    fig, ax1 = plt.subplots()
    t = np.arange(N)
    s1 = df_agg2['Total']
    ax1.plot(t, s1, 'mediumspringgreen')
    ax1.set_xlabel('Days')
    ax1.set_ylabel('DCR (Million)', color='black')
    ax1.tick_params('y', colors='black')
    ax1.tick_params('x', rotation=60)

    ax2 = ax1.twinx()
    s2 = df_agg2['USD-Val']
    ax2.plot(t, s2, 'dodgerblue')
    ax2.set_ylabel('USD (Million)', color='black')
    ax2.tick_params('y', colors='black')
    dcr = mpatches.Patch(color='mediumspringgreen', label='DCR')
    usd = mpatches.Patch(color='dodgerblue', label='USD')
    plt.legend(handles=[dcr, usd])
    plt.title(f'Decred on-chain TX volume {ts2} - {ts3}')
    plt.grid(True)
    plt.savefig('txVol.png')


def csv_prune(doc_name):
    with open(doc_name, 'r+') as f:
        data = f.read()
        data = data.split('\n')
        if len(data) > 36000:
            for i in range(0, 18000):
                data.reverse()
                data.pop()
                data.reverse()
            with open(doc_name, 'r+') as f:
                f.truncate(0)
                f.seek(0)
                for i in data:
                    f.write(str(i))
                    f.write("\n")
            print("csv prune completed.")
        else:
            print(f' {doc_name} file size still in bounds.')


def logic():
    mixed_list = []
    url_block = []
    list_of_300_urls = []
    mixed_by_block = []
    test_list = []
    new_total = []
    new_block = []
    new_date = []
    twitter_data()
    time_value = current_utc_time() - current_tw_dt

    if time_value == 172800:
        print('startup conditional satisfied')
        csv_prune('dates_p1.csv')
        csv_prune('mixed_p1.csv')
        csv_prune('blocks_p1.csv')
        csv_prune('total_p1.csv')
        proposed_block = proposed_block_url()
        start_block = start_block1()
        proposed_block = int(proposed_block) + 2


        for i in range(start_block, proposed_block):
            url_block.append(int(i) + 1)
        print('determined block range')
        for i in url_block:
            list_of_300_urls.append('https://explorer.dcrdata.org/block/' + str(i))
        print('appended urls to list complete. Scraping urls...est 40min remaining if no errors occur..')
        for route in list_of_300_urls:
            mixed_by_block.append(list(mixed_date_time(route)))
            time.sleep(5)
        print('mixed by block data appended to list, wrangling data')
        for i in mixed_by_block:
            mixed_by_block = str(mixed_by_block).replace(',','').replace('[','')
        mixed_by_block = mixed_by_block.split(']')
        mixed_by_block.pop()
        mixed_by_block.pop()

        day_after_tweet = current_tw_dt + 86400
        ts = datetime.fromtimestamp(day_after_tweet).strftime('%Y-%m-%d %I:%M:%S %p')
        ts_list = ts.split(' ')
        latest_date = ts_list[0]
        day_of_latest_date = latest_date.split('-')
        day_of_latest_data = day_of_latest_date[2]

        if day_of_latest_data[0] == '0':
            day_of_latest_data = day_of_latest_data[1]
        for i in mixed_by_block:
            test_list.append(str(i).split(' '))
        for i in test_list:
            if i[-2] == day_of_latest_data:
                mixed_list.append(i[-6])
                new_block.append(i[-4])
                new_total.append(i[-5])
                new_date.append(i[-3:])

        with open('dates_p1.csv', 'a') as f:
            for i in new_date:
                f.write(str(i))
                f.write("\n")

        with open('mixed_p1.csv', 'a') as f:
            for i in mixed_list:
                f.write(str(i))
                f.write("\n")

        with open('blocks_p1.csv', 'a') as f:
            for i in new_block:
                f.write(str(i))
                f.write("\n")

        with open('total_p1.csv', 'a') as f:
            for i in new_total:
                f.write(str(i))
                f.write("\n")


        global mixed_today
        mixed_today = 0
        for i in mixed_list:
            mixed_today += float(i)

        mixed_today = round(mixed_today)
        usd_val(mixed_today)
        mixed_by_supply = (mixed_today / coin_supply()) * 100
        mixed_by_supply = round((mixed_by_supply), 2)
        cspp_current = "{:,}".format(mixed_today)
        usd_display = "{:,}".format(USD)
        sup_display = "{:,}".format(mixed_by_supply)
        staked_display = "{:,}".format(staked_in_usd())

        url3 = 'https://explorer.dcrdata.org/market?chart=depth&xc=aggregated&bin=1h&stack=1'
        page3 = urlopen(url3)
        html3 = page3.read().decode("utf-8")
        soup3 = bs(html3, "html.parser")
        btc_value = soup3.find_all(class_="pl-3 fs16 py-2 text-right")
        btc_sliced_val = list(btc_value[-1])
        btc_sliced_val = [str(x) for x in str(btc_sliced_val)]
        prior_index = btc_sliced_val.index('0')
        post_index = prior_index + 7
        btc_val = btc_sliced_val[prior_index:post_index]
        btc_val_final = str(''.join(btc_val))

        if mixed_today > record_check():
            daily = f"""{latest_date} StakeShuffle transaction volume was: {cspp_current} $DCR / {usd_display} $USD
            {sup_display} % of Circulating Supply Mixed Yesterday *NEW ATH!! (1 DCR = {usd_value} USD / {btc_val_final} BTC)
             Total staked in USD: {staked_display} #dcr $dcr #DAO #Decred #bitcoin #btc #DCRDEX"""
        else:
            daily = f"""{latest_date} StakeShuffle transaction volume was: {cspp_current} $DCR / {usd_display} $USD
            {sup_display} % of Circulating Supply Mixed Yesterday (1 DCR = {usd_value} USD / {btc_val_final} BTC)
             Total staked in USD: {staked_display} #dcr $dcr #DAO #Decred #bitcoin #btc #DCRDEX"""

        global df_dates
        df_dates = pd.read_csv('dates_p1.csv', delimiter = '\n')
        df_mixed = pd.read_csv('mixed_p1.csv', delimiter = '\n')
        global df_total
        df_total = pd.read_csv('total_p1.csv', delimiter = '\n')
        df_total = df_total.div(1000000)

        df_mixed = df_mixed.astype(int)
        df_mixed = df_mixed.div(1000000)
        df_data = pd.concat([df_dates, df_mixed, df_total], axis=1)
        df_data['Total-Mixed'] = df_data['Total'] - df_data['Mixed']
        df_agg = df_data.groupby(['Dates'], sort=False).sum()
        df_agg = df_agg.tail(31)
        df_agg = df_agg.reset_index()
        df_agg['Dates'] = df_agg['Dates'].str.strip('[]')
        df_agg['Dates'] = df_agg['Dates'].str.strip('""')
        df_acc = list(accumulate(df_agg['Mixed']))

        m = df_agg['Mixed'].values.tolist()
        t = df_agg['Total-Mixed'].values.tolist()
        d2 = df_agg['Dates'].values.tolist()
        test_list2 = []
        day = []
        day2 = []
        year = []
        year2 = []
        month = []
        month2 = []

        for i in d2:
            test_list2.append(str(i).split(' '))
        for i in test_list2:
            day.append(i[1])
            month.append(i[0])
            year.append(i[2])
        for i in month:
            month2.append(i[1:-2])
        for i in day:
            day2.append(i[1:-2])
        for i in year:
            year2.append(i[1:-1])

        df_date = pd.DataFrame(columns=['day2', 'month2', 'year2'])
        df_date['day2'], df_date['month2'], df_date['year2'] = day2, month2, year2
        df_date = df_date.assign(Dates_new = df_date.day2.astype(str) + ' ' + df_date.month2.astype(str) + ' ' + df_date.year2.astype(str))
        df_date.drop('month2', axis=1, inplace=True)
        df_date.drop('year2', axis=1, inplace=True)
        df_final = pd.concat([df_agg, df_date], axis=1)
        df_final.drop('Dates', axis=1, inplace=True)
        df_final['day2'] = df_final['day2'].astype(int)
        print(df_final)

        dates_xaxis = df_final['day2'].values.tolist()
        dates_new = df_final['Dates_new'].values.tolist()
        f2 = dates_new[0]
        l2 = dates_new[-1]
        N = len(dates_new)
        xloc = np.arange(N)
        barWidth = 0.50
        p1 = plt.bar(xloc, m, width=barWidth, color='dodgerblue', edgecolor='black')
        p2 = plt.bar(xloc, t, bottom=m, width=barWidth, color='mediumspringgreen', edgecolor='black')
        p3 = plt.plot(xloc, df_acc)
        plt.ylabel('DCR (Million)')
        plt.xlabel('Day of Month')
        plt.xticks(rotation=60)
        plt.xticks(np.arange(len(dates_xaxis)), dates_xaxis)
        plt.title(f'{f2} - {l2}')
        plt.grid(True)
        plt.legend((p1[0], p2[0], p3[0]), ('mixed', 'normal', 'mixed(cumulative)'))
        plt.savefig('graph2.png')
        media = api.media_upload('graph2.png')

        f = new_block[0]
        l = new_block[-1]
        print(f'data scraped by range {f} - {l}')

        api.update_status(status = daily, media_ids=[media.media_id])
        os.remove("graph2.png")
        print('first batch data released.')
        time.sleep(10)
        tAp = utcAndUsd()
        with open('usd_price.csv', 'a') as f:
            f.write(str(tAp))
            f.write("\n")

        txVol()
        ticketPrice()
        ticketUSD = "{:,}".format(ticketUsd)
        stakedPerc = round((stakedP), 2)
        stakedPercentage = "{:,}".format(stakedPerc)
        stakedRound = round(float(staked_val))
        stakedValue = "{:,}".format(stakedRound)
        media = api.media_upload('txVol.png')
        daily2 = f"""{latest_date} Current Ticket Price: {ticket} $DCR / {ticketUSD} $USD  $$$
           {stakedPercentage}% of circulating supply staked ~ {stakedValue} $DCR  **New graph in beta**
        $dcr #DAO #Decred #eth #ethereum #bitcoin #btc #DCRDEX"""
        api.update_status(status = daily2, media_ids=[media.media_id])
        os.remove("txVol.png")
        print('second batch data released.')

    else:
        pass


if __name__ == '__main__':
    first_check()
