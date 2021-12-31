import tweepy, json
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from datetime import date
import time


auth = tweepy.OAuthHandler('#############', '########################################')
auth.set_access_token('################-###############', '########################################')
api = tweepy.API(auth, wait_on_rate_limit=True)


def tweet_date():
    x = api.user_timeline(count=1, tweet_mode='extended')
    tweet_body = [tweet.full_text for tweet in x]
    tweet_body = tweet_body[0]
    tweet_string = tweet_body.split(' ')
    return tweet_string[0]


def config():
    with open('attack_params.txt') as f:
        data = json.load(f)
        global elec
        elec = (data['elec_cost'])
        miner_capacity = (data['miner_capacity'])
        miner_cost = (data['miner_cost'])
        miner_input = (data['miner_watts'])
        facility_cost = float((data['facility_est'])) / 100
    return elec, miner_capacity, miner_cost, miner_input, facility_cost


def capex(hash_rate, usd_rate, staked):
    global cost_of_miners
    cost_of_miners = (round(hash_rate / float(config()[1]) * 1000)) * float(config()[2])
    cost_of_tickets = round(float(staked) * usd_rate)
    global capex_
    capex_ = cost_of_miners + cost_of_tickets


def opex(hash_rate):
    cost_of_elec = (round(hash_rate / float(config()[1]) * float(config()[3]))) * float(config()[0])
    facility_cost = cost_of_miners * config()[4]
    global opex_
    opex_ = cost_of_elec + facility_cost


def construct(supply, staked, usd_value, hash_rate):
    if supply < staked * 2:
        attack_viability = "Attack not possible."
    else:
        attack_viability = "Attack unlikely."

    staked_display = "{:,}".format(staked)
    capex_display = "{:,}".format(capex_)
    opex_display = "{:,}".format(opex_)

    body = f"""{tweet_date()} At {usd_value} USD/DCR & electricity cost of {elec} USD/KW with DCR5 miners you'll need to add #rate of {hash_rate} Ph/s and stake $DCR {staked_display} to attack the #Decred network for 1 hour. Attack cost~ Capex: {capex_display} USD | Opex: {opex_display} USD ~{attack_viability} #btc"""
    api.update_status(status=body)

    
def main_a():
    url = 'https://explorer.dcrdata.org'
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = bs(html, "html.parser")
    rate_tag = soup.get_text('Exchange Rate')
    usd_rate = rate_tag.split('\n')
    usd_rate = usd_rate[-27]
    usd_value = usd_rate.lower()
    usd_list = usd_value.split('e')
    usd_value = float(usd_list[3])
    hash_ = soup.find_all(class_="int")

    supply = hash_[-2]
    supply_list = [str(i) for i in str(supply)]
    supply_slice = supply_list[18:-7]
    supply = ''.join(supply_slice)
    supply = supply.replace(',', '')

    staked = hash_[-7]
    staked_list = [str(i) for i in str(staked)]
    staked_slice = staked_list[18:-7]
    staked = ''.join(staked_slice)
    staked = staked.replace(',', '')

    hash_tag = hash_[-5]
    hash_list = [str(i) for i in str(hash_tag)]
    hash_rate = hash_list[18:-7]
    hash_rate = ''.join(hash_rate)
    capex(float(hash_rate), usd_value, staked)
    opex(float(hash_rate))
    construct(float(supply), float(staked), usd_value, hash_rate)


if __name__ == '__main__':
    if date.today().weekday() == 2:
        main_a()
        time.sleep(5)
        exit("exiting process...")


