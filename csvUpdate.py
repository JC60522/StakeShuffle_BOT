import easygui as easygui
from easygui import *
from progress.bar import Bar
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import time


def ping():
    try:
        urlopen('https://www.google.com')
    except:
        exit('Internet connection seems unavailable. Connect.. relaunch program and try again....script terminated')


def main_menu():
    ping()
    msg = "Choose to update CSV files:"
    title = "Main Menu"
    choices = ["Update existing .CSV files", "Exit"]
    fieldValues = choicebox(msg,title, choices)
    global userInput
    userInput = fieldValues
    if (userInput == 'Update existing .CSV files'):
        control()
    else:
        exit('Script terminated')
    

def block():
    msg = "Enter CSV file names as saved on your system as well as the last block number of the intended broadcast date."
    title = "CSV Update"
    fieldNames = ["End Block:", "i.e: blocks.csv:", "i.e: mixed.csv:", "i.e: dates.csv:", "i.e: total.csv:"]
    fieldValues = fieldCheck(msg, title, fieldNames)
       
    if fieldValues != None:
        global endBlock
        endBlock = fieldValues[0]
        global blocks_csv
        blocks_csv = fieldValues[1]
        global mixed_csv
        mixed_csv = fieldValues[2]
        global dates_csv
        dates_csv = fieldValues[3]
        global total_csv
        total_csv = fieldValues[4]
    else:
        main_menu()


def fieldCheck(msg, title, fieldNames):
    fieldValues = multenterbox(msg, title, fieldNames)
    while 1:
        if fieldValues is None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg += ('"%s" is a required field.\n\n' % fieldNames[i])
        if errmsg == "":
            break 
        fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
    return fieldValues


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
    return int(proposed_block)



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
        update()
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


def checkBlock_input():
    start_block1()
    if int(endBlock) > int(proposed_block_url()):
        print('This block does not exist yet..try again')
        main_menu()
    elif int(endBlock) < int(data2):
        print(f'Block out of range. Choose a block in this range: {start_block1()} - {proposed_block_url()}')
        main_menu()
    elif int(endBlock) < start_block1():
        print(f'Block already logged in {blocks_csv}. Choose a block in this range: {start_block1()} - {proposed_block_url()}')
        main_menu()



def checkFile_input():
    try:
        with open(blocks_csv, 'r') as f:
            data = f.read()
    except:
        print(f'{blocks_csv} not detected, try again...')
        main_menu()
    try:
        with open(mixed_csv, 'r') as f:
            data = f.read()
    except:
        print(f'{mixed_csv} not detected, try again...')
        main_menu()
    try:
        with open(dates_csv, 'r') as f:
            data = f.read()
    except:
        print(f'{dates_csv} not detected, try again...')
        main_menu()
    try:
        with open(total_csv, 'r') as f:
            data = f.read()
    except:
        print(f'{total_csv} not detected, try again...')
        main_menu()


def start_block1():
    with open(blocks_csv, 'r') as f:
        data = f.read()
        data = data.split('\n')
        global data2
        data2 = data[1]
    return int(data[-2])


def update():
        start_block = start_block1()
        end_block = int(endBlock)
        N = end_block - start_block
        start_block = start_block1()
        end_block = int(endBlock)
        mixed_list = []
        url_block = []
        list_of_300_urls = []
        mixed_by_block = []
        test_list = []
        new_total = []
        new_block = []
        new_date = []
    
        for i in range(start_block, end_block):
            url_block.append(int(i) + 1)
        for i in url_block:
            list_of_300_urls.append('https://dcrdata.decred.org/block/' + str(i))
        
        with Bar('Updating....', max=N) as bar:
            for route in list_of_300_urls:
                mixed_by_block.append(list(mixed_date_time(route)))
                time.sleep(2)
                bar.next()
        
        for i in mixed_by_block:
            mixed_by_block = str(mixed_by_block).replace(',','').replace('[','')
        mixed_by_block = mixed_by_block.split(']')
        mixed_by_block.pop()
        mixed_by_block.pop()
        
        for i in mixed_by_block:
            test_list.append(str(i).split(' '))
        for i in test_list:            
            mixed_list.append(i[-6])
            new_block.append(i[-4])
            new_total.append(i[-5])
            new_date.append(i[-3:])

        with open(dates_csv, 'a') as f:
            for i in new_date:
                f.write(str(i))
                f.write("\n")

        with open(mixed_csv, 'a') as f:
            for i in mixed_list:
                f.write(str(i))
                f.write("\n")

        with open(blocks_csv, 'a') as f:
            for i in new_block:
                f.write(str(i))
                f.write("\n")

        with open(total_csv, 'a') as f:
            for i in new_total:
                f.write(str(i))
                f.write("\n")

        print(f'Data scraped by block range {start_block + 1} - {end_block}')        
        print('Update Successful.')
        exit('Script Terminated.')
    

def control():
    while userInput != ('Exit')or('None'):
        if userInput == 'Update existing .CSV files':
            block()
            checkFile_input()
            checkBlock_input()
            update()
            
    
if __name__ == '__main__':
    main_menu()
