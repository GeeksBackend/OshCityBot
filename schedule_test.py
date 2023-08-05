import schedule
import requests

def hello_world():
    print("Hello World")

def get_btc_price():
    url = "https://api.binance.com/api/v3/avgPrice?symbol=BTCUSDT"
    response = requests.get(url).json()
    print(f"Текущий курс биткоина: {response['price']}")

# schedule.every(3).seconds.do(hello_world)
# schedule.every(1).minutes.do(hello_world)
# schedule.every(1).hours.do(hello_world)
# schedule.every().day.at("19:25").do(hello_world)
# schedule.every().saturday.at('19:29').do(hello_world)
# schedule.every().minute.at(":31").do(hello_world)
schedule.every(1).seconds.do(get_btc_price)

while True:
    schedule.run_pending()