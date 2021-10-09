import json
import tweepy
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from apscheduler.schedulers.blocking import BlockingScheduler

auth = tweepy.OAuthHandler('#####################', '#####################')
auth.set_access_token('#####################-#####################', '#####################')
api = tweepy.API(auth, wait_on_rate_limit=True)


def tweet_date():
    x = api.user_timeline(count=1, tweet_mode='extended')
    tweet_body = [tweet.full_text for tweet in x]
    tweet_body = tweet_body[0]
    tweet_string = tweet_body.split(' ')
    return tweet_string[0]


def get_current():
    with open('milestone.txt') as f:
        data = json.load(f)
        supply = (data['supply'])
        loot = (data['treasury'])
    return supply, loot


def wrangle(html_string):
    raw = [str(x) for x in str(html_string)]
    raw.pop(0)
    first_index = raw.index('>')
    second_index = raw.index('<')
    less_raw = raw[first_index + 1:second_index]
    refined = str(''.join(less_raw).replace(',', ''))
    return refined


def request_explorer():
    url = 'https://explorer.dcrdata.org'
    try:
        page = urlopen(url)
    except:
        scheduler()
    html = page.read().decode("utf-8")
    soup = bs(html, "html.parser")
    supply_data = soup.find_all(class_="int")
    lootRaw = supply_data[9]
    supplyRaw = supply_data[10]
    return wrangle(supplyRaw), wrangle(lootRaw)


def edit_config(treasury, mined):
    with open('milestone.txt', 'w+') as f:
        f.truncate(0)
        f.seek(0)
        f.write('{"treasury": "' + str(treasury) + '", ' + '"supply": "' + str(mined) + '"}')


def main_f():
    prev_mined = get_current()[0]
    prev_treasury = get_current()[1]
    prev_m_check = int(prev_mined) + 1000000
    next_m = prev_m_check + 1000000
    prev_t_check = int(prev_treasury) + 10000
    next_t = prev_t_check + 10000
    altered = False
    if int(request_explorer()[0]) >= prev_m_check:
        m_display = "{:,}".format(int(request_explorer()[0]))
        m_display_sights = "{:,}".format(next_m)
        tweet_mined = f'{tweet_date()} New $Decred Supply Milestone reached! A Total of {m_display} $DCR have been mined! -> Next Milestone in sight is {m_display_sights} $DCR    $dcr #DAO #Decred #eth #ethereum #bitcoin #btc #DCRDEX'
        print(tweet_mined)
        api.update_status(status=tweet_mined)
        edit_config(prev_treasury, prev_m_check)
        altered = True
    if int(request_explorer()[1]) >= prev_t_check:
        t_display = "{:,}".format(int(request_explorer()[1]))
        t_display_sights = "{:,}".format(next_t)
        tweet_treasury = f'{tweet_date()} New $Decred Supply Milestone reached! The #Decred treasury have just increased to {t_display} $DCR -> Next Milestone in sight is {t_display_sights} $DCR    $dcr #DAO #Decred #eth #ethereum #bitcoin #btc #DCRDEX'
        print(tweet_treasury)
        api.update_status(status=tweet_treasury)
        if altered:
            edit_config(prev_t_check, prev_m_check)
        else:
            edit_config(prev_t_check, prev_mined)


def scheduler():
    sched = BlockingScheduler()
    sched.add_job(main_f, 'cron', month='1-12', day_of_week='mon-sun', hour='0-23', minute='*/20')
    sched.start()


if __name__ == '__main__':
    scheduler()
