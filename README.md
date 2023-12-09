# RHDV Team
## Инструмент, который объединяет новостные данные с техническими стратегиями. Наш бэктестер торговых стратегий учитывает тональность новостей, относящихся к конкретным активам на рынке, и использует их в качестве поддержки для решений о покупке или продаже. Мы также учли различные типы инвесторов, разделив тикеры на категории для долгосрочных, среднесрочных и краткосрочных инвесторов. Система включает парсеры для извлечения новостей, тегирование их по соответствующим тикерам, а затем анализ тональности с использованием BERT. Уникальность заключается в том, что эта оценка тональности новостей дополняется историческими данными котировок с биржи. Цель - понять, как тональность новостей может влиять на рыночное поведение, помогая техническим стратегиям принимать более обоснованные решения о покупке или продаже активов. Такая интеграция фундаментального анализа (через новостные данные) с техническими стратегиями предоставляет инвесторам более полную информацию для принятия решений.

## Презентация - https://drive.google.com/file/d/1pfpswsxlkFnBhNnEXMO_ScZkpxRQg1kw/view?usp=sharing
## Фронтенд демо - https://youtu.be/nD-5NSasORo?si=J6oTExz-qZoe6raK

# Установка и настройка проекта
## 1. Клонируйте репозиторий на свой локальный компьютер.
```.sh
git clone <https://.git>
```
## 2. Создайте ``` .env ```
```.env
# Redis
RESID_HOST=192.168.128.2
REDIS_PORT=6379

#PostgreSQL

DB_HOST=pgdb
DB_PORT=5432
DB_NAME=root
USERNAME=root
PASSWORD=root
PGADMIN_DEFAULT_EMAIL=root@root.com
PGADMIN_DEFAULT_PASSWORD=root

# Server
SERVER_PROTOCOL=http
SERVER_PORT=8080
SERVER_HOST=
ENABLE_LOGGING=true
```

## 3. Отдельно установить ta-lib
* ### Для Linux:
```.sh
❯ chmod +x talib.sh
❯ ./talib.sh
```
* ### Для Windows:
1. Скачать и установить библиотеку  ta-lib  ZIP-файлом по ссылке: https://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/ta-lib-0.4.0-msvc.zip/download?use_mirror=deac-fra
2. Разархивировать архив в диск С: по пути: ``` C:\ta-lib ```
3. Скачать и установить Visual Studio Community (2015 и позже)- при установке VSC обязательно поставить галочку рядом с  "Разработка на С++" и "Мобильная разработка на С++" 
4. Запустить из панели "Пуск" Native Tools Command Prompt for VS...
5. Прописать путь:``` C:\ta-lib\c\make\cdr\win32\msvc ```
6. Прописать команду ``` nmake ```
7. В терминале PyCharm прописать команду ``` pip install ta-lib ``` (для проверки)

## 4. Установите необходимые зависимости, запустив команду и настройте PYTHONPATH:
```.sh
❯ python -m venv venv
❯ soruce venv/bin/activate
❯ pip install -r requirements.txt
or
❯ poetry install

// PYTHONPATH
❯ export PYTHONPATH=$PYTHONPATH:$(pwd)
```

## 5. Docker start
```.sh
# clear docker cache
❯ sudo docker stop $(sudo docker ps -a -q)
❯ sudo docker rm $(sudo docker ps -a -q)
# Up postgresql database in docker
❯ docker-compose -f docker-compose.yaml build
❯ docker-compose -f docker-compose.yaml up
``` 

## 6. Database setup

1. Alembic init
```.shell
❯ cd Database
❯ rm alembic.ini
❯ rm -rf migrations/
❯ alembic init migrations
```

2. Изменить sqlalchemy.url в alembic.ini
```shell
❯ docker inspect pgdb | grep IPAddress
            "SecondaryIPAddresses": null,
            "IPAddress": "",
                    "IPAddress": "172.22.0.2",

// alembic.ini                
sqlalchemy.url = postgresql://root:root@172.22.0.2:5432/root
//or
sqlalchemy.url = postgresql://root:root@pgdb:5432/root
```

3. Изменить target_metadata в migrations/env.py
```.python
from Database.Models import Base
target_metadata = Base.metadata
```

4. Создать миграцию
```.shell
❯ alembic revision --autogenerate -m 'init'
```

5. Залить миграцию
```.shell
❯ alembic upgrade heads
```

## 7. Frontend setup
In the WebUI project directory, you can run:

### `npm install`

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

## Что делать если pyrogram заблокировался: database locked
```.shell
❯ cd Scrapping/sessions/
❯ fuser session.session
/home/donqhomo/Desktop/hackatons/MOEX-ALGO/Scrapping/sessions/session.session:  8167

❯ kill -9 8167
```

## API EndPoints

### MOEX TimePeriods
```.python
class MOEXTimePeriods(Enum):
    ONE_MINUTE = '1m'
    TEN_MINUTES = '10m'
    ONE_HOUR = '1h'
    ONE_DAY = 'D'
    ONE_WEEK = 'W'
    ONE_MONTH = 'M'
    ONE_QUARTER = 'Q'
```

### 1. GetCandles - получение катировок тикера с/по указанную дату с указанным тайм-периодом свечи
#### Route ```POST http://0.0.0.0:9878/api/ticker/get_candles ```
#### Body
```.json
{
    "ticker": "SBER",
    "from_date": "2023-10-10",
    "to_date": "2023-10-18",
    "time_period": "D"
}
```
#### Response
```.json
{
    "candles": [
        {
            "Open": 264.89,
            "Close": 263.0,
            "High": 265.18,
            "Low": 257.0,
            "Value": 8962447421.9,
            "Volume": 34001290.0,
            "Begin": "2023-10-10T00:00:00",
            "End": "2023-10-10T23:59:59"
        },
        {
            "Open": 263.3,
            "Close": 260.21,
            "High": 263.99,
            "Low": 259.5,
            "Value": 7743000723.4,
            "Volume": 29495790.0,
            "Begin": "2023-10-11T00:00:00",
            "End": "2023-10-11T23:59:59"
        },
        
        etc...
    ]
}
```

### 2. TickerList - получение списка тикеров доступных на MOEX
#### Route - ```GET http://0.0.0.0:9878/api/ticker/ticker_list```
#### Response
```.json
{
    "tickers": [
        "ABIO",
        "ABRD",
        "ACKO",
        "AFKS",
        "AFLT",
        "AGRO",
        "AKRN",
        "ALRS",
        "AMEZ",
        "APTK",
        "AQUA",
        "ARSA",
        "ASSB",
        "ASTR",
        "AVAN",
        "BANE",
        "BANEP",
        "BELU",
        "BISVP"
        
        etc...
    ]
}
```

### 3. TickersClustering - получение списка кластеризованных тикеров, под тип инвестирования
#### Route - ```GET http://0.0.0.0:9878/api/clustering/cluster_tickers```
#### Response
```.json
{
    "long_term": [
        "ELTZ",
        "HIMCP",
        "MRSB",
        "RTGZ",
        "SAGO",
        "VGSBP",
        
        etc...
    ],
    "mid_term": [
        "ABRD",
        "AFKS",
        "AFLT",
        "AGRO",
        
        etc...
    ],
    "short_term": [
        "ARSA",
        "ASSB",
        "BISVP",
        "BRZL",
        "BSPBP",
        "CHKZ",
        "DIOD",
        "DZRD",
        
        etc...
    ]
}
```

### 4. BackTest DualSMA - бэктестинг DualSMA
#### Route ```POST http://0.0.0.0:9878/api/backtest/dualsma```
#### Body
```.json
{
    "ticker": "SBER",
    "from_date": "2022-10-10",
    "to_date": "2023-10-18",
    "time_period": "1h",
    "fast_period": 10,
    "long_period": 50,
    "risk": 1,
    "reward_ratio": 3,
    "stop_loss_ratio": 2,
    "take_profit_ratio": 5,
    "start_balance": 10000
}
```
#### Response
```.json
{
    "strategy_name": "DualSMA",
    "max_day_loss": -9.136693666848537,
    "max_day_profitability": 16.278003781584825,
    "final_balance": 10003.077771604878,
    "start_balance": 10000,
    "overall_profit": 0.03077771604877853,
    "total_trades": 109,
    "profitable_trades": 26,
    "candles": [
    {
            "Open": 135.7,
            "Close": 135.7,
            "High": 135.7,
            "Low": 135.7,
            "Value": 5829672.0,
            "Volume": 42960.0,
            "Begin": "2022-11-23T09:00:00",
            "End": "2022-11-23T09:59:59",
            "SMA 10": 135.48799999999974,
            "SMA 50": 135.4202,
            "BUY": 135.7,
            "SELL": "Null",
            "POSITION": "long"
        },
        
        etc...
     ]
  }
```

### 5. BackTest MACD Signal - бэктестинг MACD
#### Route ```POST http://0.0.0.0:9878/api/backtest/macd```
#### Body
```.json
{
    "ticker": "SBER",
    "from_date": "2022-10-10",
    "to_date": "2023-10-18",
    "time_period": "1h",
    "fast_period": 12,
    "slow_period": 26,
    "signal_period": 9,
    "risk": 1,
    "reward_ratio": 3,
    "stop_loss_ratio": 2,
    "take_profit_ratio": 5,
    "start_balance": 10000
}
```
#### Response
```.json
{
   "strategy_name": "MACD signal",
    "max_day_loss": -9.235735546891377,
    "max_day_profitability": 13.64752927734932,
    "final_balance": 10037.700630849275,
    "start_balance": 10000,
    "overall_profit": 0.377006308492746,
    "total_trades": 270,
    "profitable_trades": 61,
    "candles": [
    {
            "Open": 159.42,
            "Close": 158.1,
            "High": 159.43,
            "Low": 158.03,
            "Value": 1771644862.6,
            "Volume": 11172830.0,
            "Begin": "2023-02-20T10:00:00",
            "End": "2023-02-20T10:59:59",
            "MACD 12 26 9": 0.12295354066145592,
            "MACD signal 12 26 9": 0.13214260259363245,
            "MACD hist 12 26 9": -0.009189061932176529,
            "BUY": "Null",
            "SELL": 158.1,
            "POSITION": "closed"
        },
        
        etc...
     ]
  }
```


### 6. AddIndicator - добавляет в датафрейм любые тех индикаторы и patter-recognition к котировкам, доступных в TA-Lib
#### Route ```POST http://0.0.0.0:9878/api/ticker/add_indicators```
#### Body
```.json
{
    "ticker": "SBER",
    "from_date": "2023-10-10",
    "to_date": "2023-10-18",
    "time_period": "10m",
    "selected_indicators": [
        {
            "indicator": "HT_DCPERIOD",
            "params": {}
        },
        {
            "indicator": "HT_DCPHASE",
            "params": {}
        },
        {
            "indicator": "HT_PHASOR",
            "params": {}
        },
        {
            "indicator": "HT_SINE",
            "params": {}
        },
        {
            "indicator": "ACOS",
            "params": {}
        },
        {
            "indicator": "ASIN",
            "params": {}
        },
        {
            "indicator": "ATAN",
            "params": {}
        },
        {
            "indicator": "CEIL",
            "params": {}
        },
        {
            "indicator": "COS",
            "params": {}
        },
        {
            "indicator": "COSH",
            "params": {}
        },
        {
            "indicator": "EXP",
            "params": {}
        },
        {
            "indicator": "FLOOR",
            "params": {}
        },
        {
            "indicator": "LN",
            "params": {}
        },
        {
            "indicator": "LOG10",
            "params": {}
        },
        {
            "indicator": "SIN",
            "params": {}
        },
        {
            "indicator": "SINH",
            "params": {}
        },
        {
            "indicator": "SQRT",
            "params": {}
        },
        {
            "indicator": "TAN",
            "params": {}
        },
        {
            "indicator": "TANH",
            "params": {}
        },
        {
            "indicator": "ADD",
            "params": {}
        },
        {
            "indicator": "DIV",
            "params": {}
        },
        {
            "indicator": "MAX",
            "params": {
                "timeperiod": 10
            }
        },
        {
            "indicator": "MAXINDEX",
            "params": {
                "timeperiod": 10
            }
        },
        {
            "indicator": "MAXINDEX",
            "params": {
                "timeperiod": 10
            }
        },
        {
            "indicator": "MIN",
            "params": {
                "timeperiod": 10
            }
        },
        {
            "indicator": "MININDEX",
            "params": {
                "timeperiod": 10
            }
        },
        {
            "indicator": "MINMAX",
            "params": {
                "timeperiod": 10
            }
        },
        {
            "indicator": "MINMAXINDEX",
            "params": {
                "timeperiod": 10
            }
        },
        {
            "indicator": "MULT",
            "params": {}
        },
        {
            "indicator": "SUB",
            "params": {}
        },
        {
            "indicator": "SUM",
            "params": {
                "timeperiod": 10
            }
        },
        {
            "indicator": "ADX",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "ADXR",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "AROON",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "AROONOSC",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "CCI",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "CMO",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "DX",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "MFI",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "MINUS_DI",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "MINUS_DM",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "MOM",
            "params": {
                "timeperiod": 10
            }
        },
        {
            "indicator": "PLUS_DI",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "PLUS_DM",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "ROC",
            "params": {
                "timeperiod": 10
            }
        },
        {
            "indicator": "ROCR",
            "params": {
                "timeperiod": 10
            }
        },
        {
            "indicator": "ROCR100",
            "params": {
                "timeperiod": 10
            }
        },
        {
            "indicator": "RSI",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "TRIX",
            "params": {
                "timeperiod": 30
            }
        },
        {
            "indicator": "WILLR",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "BOP",
            "params": {}
        },
        {
            "indicator": "MACDFIX",
            "params": {
                "signalperiod": 9
            }
        },
        {
            "indicator": "MACD",
            "params": {
                "fastperiod": 12,
                "slowperiod": 26,
                "signalperiod": 9
            }
        },
        {
            "indicator": "MACDEXT",
            "params": {
                "fastperiod": 12,
                "fastmatype": 0,
                "slowperiod": 26,
                "slowmatype": 0,
                "signalperiod": 9,
                "signalmatype": 0

            }
        },
        {
            "indicator": "PPO",
            "params": {
                "fastperiod": 12,
                "slowperiod": 26,
                "matype": 0
            }
        },
        {
            "indicator": "STOCH",
            "params": {
                "fastk_period": 5,
                "slowk_period": 3,
                "slowk_matype": 0,
                "slowd_period": 3,
                "slowd_matype": 0
            }
        },
        {
            "indicator": "STOCHF",
            "params": {
                "fastk_period": 5,
                "fastd_period": 3,
                "fastd_matype": 0
            }
        },
        {
            "indicator": "STOCHRSI",
            "params": {
                "timeperiod": 14,
                "fastk_period": 5,
                "fastd_period": 3,
                "fastd_matype": 0
            }
        },
        {
            "indicator": "ULTOSC",
            "params": {
                "timeperiod1": 7,
                "timeperiod2": 14,
                "timeperiod3": 28
            }
        },
        {
            "indicator": "BBANDS",
            "params": {
                "timeperiod": 5,
                "nbdevup": 2,
                "nbdevdn": 2,
                "matype": 0
            }
        },
        {
            "indicator": "DEMA",
            "params": {
                "timeperiod": 30
            }
        },
        {
            "indicator": "EMA",
            "params": {
                "timeperiod": 30
            }
        },
        {
            "indicator": "HT_TRENDLINE",
            "params": {}
        },
        {
            "indicator": "KAMA",
            "params": {
                "timeperiod": 30
            }
        },
        {
            "indicator": "MA",
            "params": {
                "timeperiod": 30,
                "matype": 0
            }
        },
        {
            "indicator": "MAMA",
            "params": {
                "fastlimit": 0.5,
                "slowlimit": 0.05
            }
        },
        {
            "indicator": "MIDPOINT",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "MIDPRICE",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "SAR",
            "params": {
                "acceleration": 0.02,
                "maximum": 0.2
            }
        },
        {
            "indicator": "SAREXT",
            "params": {
                "startvalue": 0,
                "offsetonreverse": 0,
                "accelerationinitlong": 0.02,
                "accelerationlong": 0.02,
                "accelerationmaxlong": 0.2,
                "accelerationinitshort": 0.02,
                "accelerationshort": 0.02,
                "accelerationmaxshort": 0.2
            }
        },
        {
            "indicator": "SMA",
            "params": {
                "timeperiod": 30
            }
        },

        {
            "indicator": "T3",
            "params": {
                "timeperiod": 5,
                "vfactor": 0.7
            }
        },
        {
            "indicator": "TEMA",
            "params": {
                "timeperiod": 30
            }
        },
        {
            "indicator": "TRIMA",
            "params": {
                "timeperiod": 30
            }
        },
        {
            "indicator": "WMA",
            "params": {
                "timeperiod": 30
            }
        },
        {
            "indicator": "AVGPRICE",
            "params": {}
        },
        {
            "indicator": "MEDPRICE",
            "params": {}
        },
        {
            "indicator": "TYPPRICE",
            "params": {}
        },
        {
            "indicator": "WCLPRICE",
            "params": {}
        },
        {
            "indicator": "ATR",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "NATR",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "TRANGE",
            "params": {}
        },
        {
            "indicator": "AD",
            "params": {}
        },
        {
            "indicator": "OBV",
            "params": {}
        },
        {
            "indicator": "ADOSC",
            "params": {
                "fastperiod": 3,
                "slowperiod": 10
            }
        },
        {
            "indicator": "BETA",
            "params": {
                "timeperiod": 5
            }
        },
        {
            "indicator": "CORREL",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "LINEARREG",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "LINEARREG_ANGLE",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "LINEARREG_INTERCEPT",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "LINEARREG_SLOPE",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "TSF",
            "params": {
                "timeperiod": 14
            }
        },
        {
            "indicator": "STDDEV",
            "params": {
                "timeperiod": 5,
                "nbdev": 1
            }
        },
        {
            "indicator": "VAR",
            "params": {
                "timeperiod": 5,
                "nbdev": 1
            }
        },
        {
            "indicator": "CDL2CROWS",
            "params": {}
        },
        {
            "indicator": "CDL3BLACKCROWS",
            "params": {}
        },
        {
            "indicator": "CDL3INSIDE",
            "params": {}
        },
        {
            "indicator": "CDL3LINESTRIKE",
            "params": {}
        },
        {
            "indicator": "CDL3OUTSIDE",
            "params": {}
        },
        {
            "indicator": "CDL3STARSINSOUTH",
            "params": {}
        },
        {
            "indicator": "CDL3WHITESOLDIERS",
            "params": {}
        },
        {
            "indicator": "CDLABANDONEDBABY",
            "params": {
                "penetration": 0.3
            }
        },
        {
            "indicator": "CDLADVANCEBLOCK",
            "params": {}
        },
        {
            "indicator": "CDLBELTHOLD",
            "params": {}
        },
        {
            "indicator": "CDLBREAKAWAY",
            "params": {}
        },
        {
            "indicator": "CDLCLOSINGMARUBOZU",
            "params": {}
        },
        {
            "indicator": "CDLCONCEALBABYSWALL",
            "params": {}
        },
        {
            "indicator": "CDLCOUNTERATTACK",
            "params": {}
        },
        {
            "indicator": "CDLDARKCLOUDCOVER",
            "params": {
                "penetration": 0.5
            }
        },
        {
            "indicator": "CDLDOJI",
            "params": {}
        },
        {
            "indicator": "CDLDOJISTAR",
            "params": {}
        },
        {
            "indicator": "CDLENGULFING",
            "params": {}
        },
        {
            "indicator": "CDLDRAGONFLYDOJI",
            "params": {}
        },
        {
            "indicator": "CDLEVENINGDOJISTAR",
            "params": {
                "penetration": 0.5
            }
        },
        {
            "indicator": "CDLEVENINGSTAR",
            "params": {
                "penetration": 0.5
            }
        },
        {
            "indicator": "CDLGAPSIDESIDEWHITE",
            "params": {}
        },
        {
            "indicator": "CDLGRAVESTONEDOJI",
            "params": {}
        },
        {
            "indicator": "CDLHAMMER",
            "params": {}
        },
        {
            "indicator": "CDLHANGINGMAN",
            "params": {}
        },
        {
            "indicator": "CDLHARAMI",
            "params": {}
        },
        {
            "indicator": "CDLHARAMICROSS",
            "params": {}
        },
        {
            "indicator": "CDLHIGHWAVE",
            "params": {}
        },
        {
            "indicator": "CDLHIKKAKE",
            "params": {}
        },
        {
            "indicator": "CDLHIKKAKEMOD",
            "params": {}
        },
        {
            "indicator": "CDLHOMINGPIGEON",
            "params": {}
        },
        {
            "indicator": "CDLIDENTICAL3CROWS",
            "params": {}
        },
        {
            "indicator": "CDLINNECK",
            "params": {}
        },
        {
            "indicator": "CDLINVERTEDHAMMER",
            "params": {}
        },
        {
            "indicator": "CDLKICKING",
            "params": {}
        },
        {
            "indicator": "CDLKICKINGBYLENGTH",
            "params": {}
        },
        {
            "indicator": "CDLLADDERBOTTOM",
            "params": {}
        },
        {
            "indicator": "CDLLONGLEGGEDDOJI",
            "params": {}
        },
        {
            "indicator": "CDLLONGLINE",
            "params": {}
        },
        {
            "indicator": "CDLMARUBOZU",
            "params": {}
        },
        {
            "indicator": "CDLMATCHINGLOW",
            "params": {}
        },
        {
            "indicator": "CDLMATHOLD",
            "params": {
                "penetration": 0.5
            }
        },
        {
            "indicator": "CDLMORNINGDOJISTAR",
            "params": {
                "penetration": 0.5
            }
        },
        {
            "indicator": "CDLMORNINGSTAR",
            "params": {
                "penetration": 0.5
            }
        },
        {
            "indicator": "CDLONNECK",
            "params": {}
        },
        {
            "indicator": "CDLPIERCING",
            "params": {}
        },
        {
            "indicator": "CDLRICKSHAWMAN",
            "params": {}
        },
        {
            "indicator": "CDLRISEFALL3METHODS",
            "params": {}
        },
        {
            "indicator": "CDLSEPARATINGLINES",
            "params": {}
        },
        {
            "indicator": "CDLSHOOTINGSTAR",
            "params": {}
        },
        {
            "indicator": "CDLSHORTLINE",
            "params": {}
        },
        {
            "indicator": "CDLSPINNINGTOP",
            "params": {}
        },
        {
            "indicator": "CDLSTALLEDPATTERN",
            "params": {}
        },
        {
            "indicator": "CDLSTICKSANDWICH",
            "params": {}
        },
        {
            "indicator": "CDLTAKURI",
            "params": {}
        },
        {
            "indicator": "CDLTASUKIGAP",
            "params": {}
        },
        {
            "indicator": "CDLTHRUSTING",
            "params": {}
        },
        {
            "indicator": "CDLTRISTAR",
            "params": {}
        },
        {
            "indicator": "CDLUNIQUE3RIVER",
            "params": {}
        },
        {
            "indicator": "CDLUPSIDEGAP2CROWS",
            "params": {}
        },
        {
            "indicator": "CDLXSIDEGAP3METHODS",
            "params": {}
        }
        
    ]
}

```
#### Response
```.json
{
    "candles": [
            "Open": 263.69,
            "Close": 263.6,
            "High": 263.86,
            "Low": 263.59,
            "Value": 55411517.79999999,
            "Volume": 210120.0,
            "Begin": "2023-10-13T19:20:00",
            "End": "2023-10-13T19:29:59",
            "HT_DCPERIOD": 19.229355778199547,
            "HT_DCPHASE": 293.65487732825574,
            "HT_PHASOR_inphase": 0.08345556145117587,
            "HT_PHASOR_quadrature": 0.3773597449957829,
            "HT_SINE_sine": -0.9159788589777965,
            "HT_SINE_leadsine": -0.36398486110365513,
            "ACOS": "Null",
            "ASIN": "Null",
            "ATAN": 1.5670027182863981,
            "CEIL": 264.0,
            "COS": 0.95715529258761,
            "COSH": 1.510064277979035e+114,
            "EXP": 3.02012855595807e+114,
            "FLOOR": 263.0,
            "LN": 5.574432802628352,
            "LOG10": 2.420945405921972,
            "SIN": -0.28957511265909347,
            "SINH": 1.510064277979035e+114,
            "SQRT": 16.235762994081924,
            "TAN": -0.30253723183857145,
            "TANH": 1.0,
            "ADD": 527.45,
            "DIV": 1.0010243180697296,
            "MAX 10": 263.7,
            "MAXINDEX 10": 302,
            "MIN 10": 263.25,
            "MININDEX 10": 298,
            "MINMAX_min": 263.25,
            "MINMAX_max": 263.7,
            "MINMAXINDEX_minidx": 298,
            "MINMAXINDEX_maxidx": 302,
            "MULT": 69550.8574,
            "SUB": 0.27000000000003865,
            "SUM": 2635.0899999999983,
            "ADX 14": 10.006134649378707,
            "ADRX 14": 12.778206334827658,
            "AROON_down 14": 50.0,
            "AROON_up 14": 21.42857142857143,
            "AROONOSC 14": -28.571428571428573,
            "CCI 14": 67.949454336601,
            "CMO 14": 1.4081706601936208,
            "DX 14": 4.949855991560166,
            "MFI 14": 66.37253486851306,
            "MINUS_DI 14": 24.857532435919826,
            "MINUS_DM 14": 1.0256368735617325,
            "MOM 10": 0.040000000000020464,
            "PLUS_DI 14": 22.51277065038229,
            "PLUS_DM 14": 0.9288905793281732,
            "ROC 10": 0.015176809834582805,
            "ROCR 10": 1.0001517680983458,
            "ROCR100 10": 100.01517680983459,
            "RSI 14": 50.70408533009682,
            "TRIX 30": 0.00016228028456577448,
            "WILLR 14": -37.804878048778455,
            "BOP": -0.333333333333193,
            "MACDEXT_macd 9": -0.008873761536733582,
            "MACDEXT_macdsignal 9": -0.018089633315928735,
            "MACDEXT_macdhist 9": 0.009215871779195153,
            "MACD 12 26 9": -0.009107316235997587,
            "MACD signal 12 26 9": -0.019060560450615535,
            "MACD hist 12 26 9": 0.009953244214617948,
            "MACDEXT_macd 12 26 9": -0.09083333333370547,
            "MACDEXT_macdsignal 12 26 9": -0.11507122507163735,
            "MACDEXT_macdhist 12 26 9": 0.02423789173793188,
            "PPO 12 26": -0.03445616164693448,
            "STOCH_slowk 5 3 3": 49.78623188405815,
            "STOCH_slowd 5 3 3": 64.3947224500955,
            "STOCHF_fastk 5 3": 48.00000000000182,
            "STOCHF_fastd 5 3": 49.78623188405815,
            "STOCHRSI_fastk 14 5 3": 52.18029972353461,
            "ULTOSC 7 14 28": 51.77990966700617,
            "BBANDS_upperband 5 2 2 0": 263.8189259956496,
            "BBANDS_middleband 5 2 2 0": 263.59600000000034,
            "BBANDS_lowerband 5 2 2 0": 263.3730740043511,
            "DEMA": 263.55626420612003,
            "EMA 30": 263.57185874036384,
            "HT_TRENDLINE": 263.5424486215539,
            "KAMA 30": 263.5365656860121,
            "MA 30 0": 263.6456666666668,
            "MAMA_mama 0.5 0.05": 263.55509559869915,
            "MAMA_fama 0.5 0.05": 263.531743923266,
            "MIDPOINT 14": 263.53,
            "MIDPRICE 14": 263.5,
            "SAR": 263.10926864925017,
            "SAREXT": 263.10926864925017,
            "SMA 30": 263.6456666666668,
            "T3 5": 263.55857632560446,
            "TEMA 30": 263.5344674460792,
            "TRIMA 30": 263.6098333333338,
            "WMA 30": 263.5793763440876,
            "AVGPRICE": 263.685,
            "MEDPRICE": 263.725,
            "TYPPRICE": 263.68333333333334,
            "WCLPRICE": 263.6625,
            "ATR 14": 0.2947186205055612,
            "NATR 14": 0.1118052429839003,
            "TRANGE": 0.27000000000003865,
            "AD": 8022564.116112176,
            "OBV": -13269280.0,
            "ADOSC 3 10": 19118.692237510346,
            "BETA 5": 1.1141923009422625,
            "BETA 14": 0.49340671288976434,
            "LINEARREG 14": 263.50828571428576,
            "LINEARREG_ANGLE 14": -0.49990873102051253,
            "LINEARREG_INTERCEPT 14": 263.62171428571423,
            "LINEARREG_SLOPE 14": -0.008725274725268146,
            "TSF 14": 263.49956043956047,
            "STDDEV 5": 0.11146299782461178,
            "VAR 5": 0.012423999884049408,
            "CDL2CROWS": 0,
            "CDL3BLACKCROWS": 0,
            "CDL3INSIDE": 0,
            "CDL3LINESTRIKE": 0,
            "CDL3OUTSIDE": 0,
            "CDL3STARSINSOUTH": 0,
            "CDL3WHITESOLDIERS": 0,
            "CDLABANDONEDBABY": 0,
            "CDLADVANCEBLOCK": 0,
            "CDLBELTHOLD": 0,
            "CDLBREAKAWAY": 0,
            "CDLCLOSINGMARUBOZU": 0,
            "CDLCONCEALBABYSWALL": 0,
            "CDLCOUNTERATTACK": 0,
            "CDLDARKCLOUDCOVER": 0,
            "CDLDOJI": 0,
            "CDLDOJISTAR": 0,
            "CDLENGULFING": 0,
            "CDLDRAGONFLYDOJI": 0,
            "CDLEVENINGDOJISTAR": 0,
            "CDLEVENINGSTAR": 0,
            "CDLGAPSIDESIDEWHITE": 0,
            "CDLGRAVESTONEDOJI": 0,
            "CDLHAMMER": 0,
            "CDLHANGINGMAN": 0,
            "CDLHARAMI": 0,
            "CDLHARAMICROSS": 0,
            "CDLHIGHWAVE": 0,
            "CDLHIKKAKE": 0,
            "CDLHIKKAKEMOD": 0,
            "CDLHOMINGPIGEON": 0,
            "CDLIDENTICAL3CROWS": 0,
            "CDLINNECK": 0,
            "CDLINVERTEDHAMMER": 0,
            "CDLKICKING": 0,
            "CDLKICKINGBYLENGTH": 0,
            "CDLLADDERBOTTOM": 0,
            "CDLLONGLEGGEDDOJI": 0,
            "CDLLONGLINE": 0,
            "CDLMARUBOZU": 0,
            "CDLMATCHINGLOW": 0,
            "CDLMATHOLD": 0,
            "CDLMORNINGDOJISTAR": 0,
            "CDLMORNINGSTAR": 0,
            "CDLONNECK": 0,
            "CDLPIERCING": 0,
            "CDLRICKSHAWMAN": 0,
            "CDLRISEFALL3METHODS": 0,
            "CDLSEPARATINGLINES": 0,
            "CDLSHOOTINGSTAR": 0,
            "CDLSHORTLINE": 0,
            "CDLSPINNINGTOP": 0,
            "CDLSTALLEDPATTERN": 0,
            "CDLSTICKSANDWICH": 0,
            "CDLTAKURI": 0,
            "CDLTASUKIGAP": 0,
            "CDLTHRUSTING": 0,
            "CDLTRISTAR": 0,
            "CDLUNIQUE3RIVER": 0,
            "CDLUPSIDEGAP2CROWS": 0,
            "CDLXSIDEGAP3METHODS": 0
        },
        
        etc...
        
    ]
}
```

### 7. GetAllNews - получение всех новостей отсортированных по дате
#### Route - ```GET http://0.0.0.0:9878/api/news/get_all_news```
#### Response
```.json
[
    {
        "link": "https://quote.ru/news/article/657029b79a7947174eda92cd",
        "text": "Портфель средств физических лиц в «Сбере» за год вырос на ₽4,5 трлн. В банке ожидают, что по итогам года он превысит ₽22 трлн. Об этом сообщил первый зампред правления Сбербанка Кирилл Царев на Дне инвестора, пишет Frank Media.\nПо словам топ-менеджера, доля срочных вкладов увеличилась на 5 п.п. и составляет 53%, средний чек депозита вырос на 15 п.п. и равен ₽673 тыс. При этом объем вкладов в валюте недружественных стран упал на 9 п.п., но выросла доля юаня до 13%.\nСбербанк повысил доходность по премиальному продукту «Лучший % Лидер» до 15% годовых, минимальная сумма вклада составляет ₽100 тыс., остальным клиентам предлагаются три вклада с максимальным процентом до 14% годовых.\nПо прогнозам Frank RG, объем срочных вкладов и текущих счетов всех банков к концу 2023 года может достигнуть ₽44 трлн:\nВ третьем квартале портфель срочных вкладов достиг ₽23,6 трлн. Остатки на текущих счетах и вкладах до востребования также выросли до ₽16 трлн.\nУвеличение портфеля аналитики связывают с повышением ключевой ставки (с 7,5% до 15%) и, соответственно, доходности вкладов.\nНа 6 декабря средняя ставка в 80 крупнейших банках по вкладам сроком на один год на сумму от ₽100 тыс. составляет 10,64% годовых, по данным ежедневного индекса FRG100. Это максимальное значение индекса за все время наблюдений с апреля 2017 года.\nПо статистике Банка России, объем средств физических лиц к концу третьего квартала 2023 года составил ₽40,8 трлн. Из них доля срочных вкладов — ₽25,8 трлн, денежные средства на счетах — ₽15 трлн.",
        "date": "2023-12-06T22:14:57.576258",
        "source": "rbc",
        "rating": null
    },
        
        etc...
]
```

### 8. GetNewsByTicker - получение всех новостей по тикеру отсортированных по дате
#### Route ```POST http://0.0.0.0:9878/api/news/get_news_by_ticker```
#### Body
```.json
{
    "ticker": "IMOEX"
}
```

#### Response
```.json
[
    {
        "link": "https://quote.ru/news/article/656d7cdd9a794796b6a2f3a8",
        "text": "Индекс Мосбиржи снизился на 1,47%, до 3096,33 пункта, свидетельствуют данные торгов по состоянию на 10:11 мск. Ниже отметки 3100 пунктов значение индикатора упало впервые с 28 сентября.\nК 10:19 мск индекс Мосбиржи скорректировался до 3104,66 пункта (-1,2%). Одновременно с этим долларовый индекс РТС потерял 1,49% и достиг отметки 1078,99 пункта.\n«Негативный общерыночный сентимент связан как со снижением нефтяных цен, так и с общим ожиданием дальнейшего ужесточения ДКП. На следующем заседании 15 декабря ЦБ РФ может вновь повысить ставку с текущего уровня 15%», — отметили в «БКС Мир инвестиций».\n\n\nЛидерами роста в составе индекса Мосбиржи по состоянию на 10:11 мск были бумаги «Полиметалла» (+2,33%), «Полюса» (+1,14%) и «Русала» (+0,07%). Наибольшее снижение демонстрировали расписки «Русагро» (-3,6%) и X5 Group (-3,3%), обыкновенные акции «Группы Позитив» (-3,13%), «Сургутнефтегаза» (-2,4%) и ГК «ПИК» (-2,31%).\nАкции «Полюса» и «Полиметалла» выглядят лучше рынка из-за роста стоимости золота до нового максимума за всю историю. Утром в понедельник, 4 декабря, котировки впервые поднялись выше $2100 за тройскую унцию. По мнению главного аналитика ПСБ Алексея Головинова, на фоне сильного роста цен на золото и общей безыдейности на российском рынке в качестве идей для покупки стоит рассматривать лишь бумаги золотодобытчиков.\nУправляющий директор департамента по работе с акциями УК «Система Капитал» Константин Асатуров ранее заявил «РБК Инвестициям», что в текущих условиях инвесторам все же лучше отдавать предпочтение консервативным инструментам, а на акции выделить лишь небольшую часть портфеля (менее 15%) в моменте.\n«Помимо роста ставки, что станет естественным образом стимулировать перетоки вложений в депозиты, фонды денежного рынка, облигации или другие консервативные инструменты, недавнее укрепление рубля будет также оказывать давление на российский рынок акций, который по большей части состоит из компаний-экспортеров», — отмечал эксперт.",
        "date": "2023-12-05T19:13:21.379963",
        "source": "rbc",
        "rating": null
    },
        
        etc...
]
```


## Настройка pre-committer
```.sh
$ pre-commit migrate-config
Configuration has been migrated.
$ pre-commit run flake8 --all-files
flake8...................................................................Passed
```
