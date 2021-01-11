import pybithumb
import time
import math
import telegram
import datetime

##### telebot #####
telgm_token = ''
bot = telegram.Bot(token = telgm_token)
chat = ""

###### key #####
con_key = ""
sec_key = ""

##### object ######
bithumb = pybithumb.Bithumb(con_key, sec_key)


clist = ["BTC", "ETH", "XLM"]

##### 잔고출력 #####
print('_________ 나의 잔고 현황 _________' )

for c in clist:
    balance = bithumb.get_balance(c)
    print('#', c,':', balance[0]) 

###### 현재가 #####
print('_________ 현재가 _________' )
# for ticker in pybithumb.get_tickers():
total_value = 0
for c in clist:
    price = pybithumb.get_current_price(c)
    balance = bithumb.get_balance(c)
    print('#', c, ':', price, '                     # 보유가치 : ', price*balance[0])
    total_value = total_value + price*balance[0]


print('\n'+'# KRW :', math.floor(bithumb.get_balance("BTC")[2]), '원')
print('# 총 보유가치 : ',  total_value)
print(' 총 보유금액 : ',  total_value+math.floor(bithumb.get_balance("BTC")[2]))

##### 가격상승 코인 단위 10분 #####
print('_________ 가격상승 _________' )
golist = pybithumb.get_tickers()
godict = {}

for go in golist:
    godict[go]= pybithumb.get_current_price(go)
print(godict)    

while True:
    for go in golist:
        try_count = 0
        while True:
            try:        
                prev_price = godict[go]
                now_price = pybithumb.get_current_price(go)
                percent = (float(now_price)/float(prev_price))-1

                print(go, '이전가: {} / 현재가: {}'.format(prev_price, now_price))
                if (percent>=0.05):
                    bot.sendMessage(chat, '{} / {} 가격 상승 {}'.format(time.strftime('%H:%M:%S'), go, percent)) # telegram (가격 5% 상승시)
                    bot.sendMessage(chat, '이전가: {} 현재가 : {}'.format(prev_price, now_price)) # telegram (가격 5% 상승시)
                    print('\n'+'# {} / {} 가격 상승 5%'.format(time.strftime('%H:%M:%S'), go)) # telegram (가격 5% 상승시)
                    print('# 이전가: {} 현재가 : {}'.format(prev_price, now_price)) # telegram (가격 5% 상승시)
                
                godict[go]= now_price
            except Exception as e:
                print(e)
                try_count = try_count + 1
                if(try_count == 3):
                    break

                continue
            
            break

    print("# 5분 대기중..")
    print("# 5분 대기중..")
    print("# 5분 대기중..")
    time.sleep(300) # 5분마다 반복




