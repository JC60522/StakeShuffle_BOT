import tweepy
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from apscheduler.schedulers.blocking import BlockingScheduler

auth = tweepy.OAuthHandler('####################', '########################################')
auth.set_access_token('####################-####################', '####################')
api = tweepy.API(auth, wait_on_rate_limit=True)


def tweet_date():
    x = api.user_timeline(count=1, tweet_mode='extended')
    tweet_body = [tweet.full_text for tweet in x]
    tweet_body = tweet_body[0]
    tweet_string = tweet_body.split(' ')
    return tweet_string[0]


def main_b():
    url = 'https://dcrdata.decred.org'
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = bs(html, "html.parser")
    reward = soup.find_all(class_="int")
    reward_decimals = soup.find_all(class_="decimal")

    pow_reward = reward[-4]
    pow_reward_dec = reward_decimals[-4]
    pow_reward = [str(i) for i in str(pow_reward)]
    pow_reward_dec = [str(i) for i in str(pow_reward_dec)]
    pow_reward = pow_reward[18:-7]
    pow_reward_dec = pow_reward_dec[22:-7]
    pow_reward = str(''.join(pow_reward))
    pow_reward_dec = str(''.join(pow_reward_dec))
    pow_reward = pow_reward + pow_reward_dec

    treasury_reward = reward[-1]
    treasury_reward_dec = reward_decimals[-2]
    treasury_reward = [str(i) for i in str(treasury_reward)]
    treasury_reward_dec = [str(i) for i in str(treasury_reward_dec)]
    treasury_reward = treasury_reward[18:-7]
    treasury_reward_dec = treasury_reward_dec[22:-7]
    treasury_reward = str(''.join(treasury_reward))
    treasury_reward_dec = str(''.join(treasury_reward_dec))
    treasury_reward = treasury_reward + treasury_reward_dec

    vote_reward = reward[-8]
    vote_reward_dec = reward_decimals[-8]
    vote_reward = [str(i) for i in str(vote_reward)]
    vote_reward_dec = [str(i) for i in str(vote_reward_dec)]
    vote_reward = vote_reward[18:-7]
    vote_reward_dec = vote_reward_dec[22:-7]
    vote_reward = str(''.join(vote_reward))
    vote_reward_dec = str(''.join(vote_reward_dec))
    vote_reward = vote_reward + vote_reward_dec
    total_reward = round(float(pow_reward) + float(vote_reward) + float(treasury_reward), 3)

    with open('reward.txt', 'r+') as f:
        data = f.read()
        data = data.split('\n')
        rew_on_rec = float(data[-2])
    if total_reward < rew_on_rec:
        print("Block reward reduction detected.")
        with open('reward.txt', 'a') as f:
            f.write(str(total_reward))
            f.write('\n')
        total_reward = round(total_reward, 3)
        vote_reward = round(float(vote_reward), 3)
        pow_reward = round(float(pow_reward), 3)
        treasury_reward = round(float(treasury_reward), 3)
        new_reward = "{:,}".format(total_reward)
        vote = "{:,}".format(vote_reward)
        pow_ = "{:,}".format(pow_reward)
        treasury = "{:,}".format(treasury_reward)

        tweet = f'''{tweet_date()} #Decred Block Reward Reduced to $DCR {new_reward} per Block. New Block Reward allocation: ~ Miners: $DCR {pow_} ~
        Voters: $DCR {vote} ~ Treasury: $DCR {treasury} '''
        print(tweet)
        api.update_status(status=tweet)


def scheduler():
    sched = BlockingScheduler()
    sched.add_job(main_b, 'cron', month='1-12', day_of_week='mon-sun', hour='0-23', minute='*/25')
    sched.start()


if __name__ == '__main__':
    scheduler()
