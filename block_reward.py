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
    url = 'https://explorer.dcrdata.org'
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = bs(html, "html.parser")
    reward = soup.find_all(class_="int")
    pow_reward = reward[-4]
    pow_reward = [str(i) for i in str(pow_reward)]
    pow_reward = pow_reward[18:-7]
    pow_reward = ''.join(pow_reward)
    treasury_reward = reward[-1]
    treasury_reward = [str(i) for i in str(treasury_reward)]
    treasury_reward = treasury_reward[18:-7]
    treasury_reward = ''.join(treasury_reward)
    vote_reward = reward[-8]
    vote_reward = [str(i) for i in str(vote_reward)]
    vote_reward = vote_reward[18:-7]
    vote_reward = ''.join(vote_reward)
    total_reward = float(pow_reward) + float(vote_reward) + float(treasury_reward)

    with open('reward.txt', 'r+') as f:
        data = f.read()
        data = data.split('\n')
        rew_on_rec = float(data[-2])
    if total_reward < rew_on_rec:
        print("Block reward reduction detected.")
        with open('reward.txt', 'a') as f:
            f.write(str(total_reward))
            f.write('\n')

        new_reward = "{:,}".format(float(total_reward))
        vote = "{:,}".format(float(vote_reward))
        pow_ = "{:,}".format(float(pow_reward))
        treasury = "{:,}".format(float(treasury_reward))

        tweet = f'''{tweet_date()} #Decred Block Reward Reduced to $DCR {new_reward} per Block. New Block Reward allocation: ~ Miners: $DCR {pow_} ~
        Voters: $DCR {vote} ~ Treasury: $DCR {treasury} ~ $dcr #DAO #Decred #eth #ethereum #bitcoin #btc #DCRDEX #Scarcity'''
        print(tweet)
        api.update_status(status=tweet)


def scheduler():
    sched = BlockingScheduler()
    sched.add_job(main_b, 'cron', month='1-12', day_of_week='mon-sun', hour='0-23', minute='*/25')
    sched.start()


if __name__ == '__main__':
    scheduler()
