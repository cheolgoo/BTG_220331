import time
import pyupbit
import datetime
import numpy as np


access = "BgyVpvO8MOEmDg7j1XocJq4xcrSWYoShtAvlteJ2"
secret = "zlYA1hl4Dxguqei2xRXEf2eDEglibSitxcu5oxun"


# 로그인
upbit = pyupbit.Upbit(access, secret)


# 파라미터 ( BTG 3minute )

buy_count   = 0 
buy_vol     = 0 
buy_price   = 0 
buy_num     = 0


sum_n       = 8
sum_perc    = 1.2/100
up          = 1.16/100
num_limit   = 7* 60 /3 


# time check 초기화
OHLCV_temp  = pyupbit.get_ohlcv(ticker="KRW-BTG", interval='minute3', count=sum_n+2, to=None, period=0.1)
time_prev   = np.array( [OHLCV_temp.index[-2], OHLCV_temp.index[-1]] ) # [0] : 과거, [1] : 최근

# autotrade start
while True:
    
    time.sleep(2)
  
    try :

        OHLCV_temp  = pyupbit.get_ohlcv(ticker="KRW-BTG", interval='minute3', count=sum_n+2, to=None, period=0.1)
        time_new    = np.array( [OHLCV_temp.index[-2], OHLCV_temp.index[-1]] )
     


        if ( time_prev[0] != time_new[0] ) :

            # time count
            if ( buy_count != 0 ) :
                buy_num  =  buy_num + 1
               

           
            # get open, close, delta
            time_prev   = time_new
            OHLCV       = OHLCV_temp.to_numpy()
            open        = OHLCV[0:-1,0]
            close       = OHLCV[0:-1,3]
            delta       = close - open
    

            sum_check = np.sum( delta ) 

            if (sum_check < -open[-1]*sum_perc)  & (buy_count == 0) :  

                    balance     = upbit.get_balance("KRW")

                    buy_price    = pyupbit.get_current_price("KRW-BTG")
                    buy_vol      = balance / pyupbit.get_current_price("KRW-BTG")
                    upbit.buy_market_order("KRW-BTG", balance*0.999 )

                    buy_count    = 1 
                    buy_num      = 1 
                    
                      


            # sell (실제buy_market한 것과 get_current한 값의 차이가 있을 수도 있는데, 약간의 BTG를 사놓으면 문제 없을듯함)

        if ( buy_count != 0 ) :

            if ( pyupbit.get_current_price("KRW-BTG") > buy_price * (1 + up) )  or  ( buy_num >= num_limit  ) :


                BTG_balance  = upbit.get_balance("KRW-BTG") 
                upbit.sell_market_order("KRW-BTG", BTG_balance*0.999)
                    

                buy_count    = 0 
                buy_num      = 0 
                buy_vol      = 0

                if (  upbit.get_balance("KRW-BTG") > 1) :
                    left = upbit.get_balance("KRW-BTG")
                    upbit.sell_market_order("KRW-BTG", left * 0.99)

                time.sleep(3*60)


    except :
        print("error!")
        time.sleep(3) # n 초 동안 작동 안함
        
