import requests
from twilio.rest import Client

account_sid = 'Account SID from Twilio'
auth_token = 'Auth token from Twilio'
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
stock_api_key = 'stock api key from alpha vantage'
news_apiKey = 'news api key'
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = ("https://newsapi.org/v2/everything")

stock_params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': stock_api_key
}

response1 = requests.get(STOCK_ENDPOINT, params=stock_params)
stocks_data = response1.json()['Time Series (Daily)']
data_list = [value for (key, value) in stocks_data.items()]
yesterday_Data = data_list[0]
yesterday_closing_price = yesterday_Data["4. close"]

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "📈"
else:
    up_down = "📉"
diff_percent = round((difference / float(yesterday_closing_price)) * 100)

if abs(diff_percent) > 5:
    news_params = {
        'apiKey': news_apiKey,
        'qInTitle': COMPANY_NAME,
        'language': 'en'

    }
    response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = response.json()['articles']
    three_articles = articles[:3]

    formatted_articles = [
        f"{STOCK}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for
        article in three_articles]

    client = Client(account_sid, auth_token)
    for article in formatted_articles:
        message = client.messages \
            .create(
            body=article,
            from_='senders mobile number from Twilio',
            to='+receivers mobile number registered on Twilio'
        )


