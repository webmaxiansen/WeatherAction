from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


# def get_weather():
#   url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
#   res = requests.get(url).json()
#   weather = res['data']['list'][0]
#   return weather['weather'], math.floor(weather['temp'])
def get_weather():
    url = "https://api.vvhan.com/api/weather?city=" + city
    res = requests.get(url).json()
    
    if res.get("success"):
        weather = res['data']['type']  # 天气类型，例如“多云”
        # 提取温度区间的最低温度和最高温度，这里我们取平均值作为当前温度
        low_temp = int(res['data']['low'].replace("°C", ""))
        high_temp = int(res['data']['high'].replace("°C", ""))
        temperature = (low_temp + high_temp) / 2  # 计算平均温度
        return weather, math.floor(temperature)
    else:
        raise Exception("Failed to fetch weather data.")
def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  # words = requests.get("https://api.shadiao.pro/chp")
  words = requests.get("https://api.vvhan.com/api/text/love?type=json")
  if words.status_code != 200:
    return get_words()
  # return words.json()['data']['text']
  return words.json()['data']['content']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()

# data = {
#     "weather": {"value": wea, "color": get_random_color()},
#     "temperature": {"value": temperature, "color": get_random_color()},
#     "love_days": {"value": get_count(), "color": get_random_color()},
#     "birthday_left": {"value": get_birthday(), "color": get_random_color()},
#     "words": {"value": get_words(), "color": get_random_color()}
# }
data = {
    "weather": {"value": wea},  # 无需颜色
    "temperature": {"value": temperature},  # 无需颜色
    "love_days": {"value": get_count()},  # 无需颜色
    "birthday_left": {"value": get_birthday()},  # 无需颜色
    "words": {"value": get_words(), "color": "#FF0000"}  # 仅给 words 设置颜色
}
res = wm.send_template(user_id, template_id, data)
print(res)
