import time
import tweepy
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

auth = tweepy.OAuthHandler('################', '#################################################')
auth.set_access_token('#######################-###################', '####################################')
api = tweepy.API(auth)

def inboxCheck():
    global senderId
    global senderText
    senderId = []
    senderText = []
    messages = api.list_direct_messages(count=50)
    for i in reversed(messages):
        senderId.append(i.message_create['sender_id'])
        senderText.append(i.message_create['message_data']['text'])

def editAndRewrite(newTxs):
    with open('txList.csv', 'r+') as f:
        f.truncate(0)
        f.seek(0)
        for n in updatedCsv:
            f.write(str(n))
            f.write("\n")
    with open('blackList.csv', 'a') as f:
        f.write(str(newTxs))
        f.write("\n")

def newEntryCheck(newEntry, entry):
    newEntryList = []
    for i in newEntry:
        if i not in entry:
            newEntryList.append(i)
    return newEntryList

def reset():
    time.sleep(180)
    inboxCheck()
    ticketVote(senderId, senderText)

def ticketVote(senderId, senderText):
    newEntry = []
    for i in senderText:
        if len(i) == 64:
            print('Transaction ID sensed')
            tx_index = senderText.index(i)
            newEntry.append(senderId[tx_index] + ',' + str(i))   
    with open('txList.csv', 'r+') as f: 
        entry = f.read() 
        entry = entry.split('\n')                                  
    with open('blackList.csv', 'r+') as f: 
        old = f.read() 
        old = old.split('\n')                                     
        rmDuplicates = set(old)
        old = list(rmDuplicates)
        
    try:
        vettedEntries = newEntryCheck(newEntry, old)
        print(vettedEntries)
        for i in vettedEntries:    
            with open('txList.csv', 'a') as f:
                f.write(i)
                f.write("\n")
        with open('txList.csv', 'r+') as f:
            entryNew = f.read() 
            global updatedCsv
            updatedCsv = entryNew.split('\n')
        for i in updatedCsv:
            if updatedCsv[-1] == '':
                updatedCsv.pop()
        rmDup = set(updatedCsv)
        updatedCsv = list(rmDup)
        print(updatedCsv)
        for newTxs in updatedCsv:
            try:
                commaIndex = newTxs.index(',')
                tx1 = newTxs[commaIndex +1:]
                url = 'https://dcrdata.decred.org/tx/' + str(tx1)
                votedIndex = updatedCsv.index(newTxs)
                id1 = newTxs[:commaIndex]
                ticketRoute = 'https://dcrdata.decred.org/tx/' + str(tx1)
                try:
                    page = urlopen(url)
                    html = page.read().decode("utf-8")
                    soup = bs(html, "html.parser")

                    try:
                        status = soup.find_all("td", class_="text-left py-1 text-secondary")
                        tags = str(status).split(',')
                        new = []
                        for i in tags:
                            i.replace(' ', '').replace('\n', '')
                            e_index = str(i[::-1]).index('=')
                            if i[-e_index:-e_index+14] == '"tx.statusMsg"':
                                new.append(i[-e_index+14:])
                                break
                        ticketStatus = str(new).replace(' ', '').replace('\\n', '').replace('</td>', '').replace('>', '')[2:-2]
                        if ticketStatus == 'Voted':
                            print(id1 + ' Ticket ' + tx1 + ' voted')
                            api.send_direct_message(id1, f'Ticket {ticketRoute} has Voted.')
                            updatedCsv.pop(votedIndex)
                            editAndRewrite(newTxs)
                    except Exception as e:
                        print(e)
                    status2 = soup.find_all(class_="h5 d-inline-block pl-1")
                    status2 = [str(x) for x in str(status2)]
                    smallerThanIndex = status2.index('<')
                    status2.pop(smallerThanIndex)
                    s_t_index = status2.index('<')
                    b_t_index = status2.index('>')
                    revokedStatus = status2[b_t_index+1:s_t_index]
                    revokedStatus = str(''.join(revokedStatus))

                    time.sleep(5)
                    if revokedStatus == 'Vote':
                        print(id1 + ' Ticket ' + tx1 + ' has been Voted')
                        api.send_direct_message(id1, f'Ticket {ticketRoute} has Voted.')
                        updatedCsv.pop(votedIndex)
                        editAndRewrite(newTxs)
                    elif revokedStatus == 'Revocation':
                        print(id1 + ' Ticket ' + tx1 + ' has been Revoked')
                        api.send_direct_message(id1, f'Ticket {ticketRoute} has been Revoked.')
                        updatedCsv.pop(votedIndex)
                        editAndRewrite(newTxs)
                except:
                    badEntry = updatedCsv.index(newTxs)
                    updatedCsv.pop(badEntry)
                    commaIndex = newTxs.index(',')
                    id1 = newTxs[:commaIndex]
                    tx1 = newTxs[commaIndex +1:]
                    ticketRoute = 'https://dcrdata.decred.org/tx/' + str(tx1)
                    api.send_direct_message(id1, f'Transaction id {ticketRoute} invalid/not found.')
                    editAndRewrite(newTxs)
                    reset()
            except:
                reset()
        reset()
    except:
        print('Seems like there are no new valid ticket queries in the inbox..')
        reset()

if __name__ == '__main__':
    inboxCheck()
    ticketVote(senderId, senderText)   
                                     
            
        
        
        
        




