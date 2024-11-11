from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

# 获取当前日期
today = datetime.now()

# 环境变量
start_date = os.environ.get('START_DATE')
city = os.environ.get('CITY')
birthday = os.environ.get('BIRTHDAY')
app_id = os.environ.get("APP_ID")
app_secret = os.environ.get("APP_SECRET")
user_id = os.environ.get("USER_ID")
template_id = os.environ.get("TEMPLATE_ID")
# 检查姨妈日期是否设置
period_date = os.environ.get("PERIOD_DATE")
if period_date is None:
    raise ValueError("请确保环境变量 'PERIOD_DATE' 已设置")

# 获取天气信息
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

# 计算恋爱天数
def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days

# 计算距离下一个姨妈到来的天数
def get_period_days():
    next_period = datetime.strptime(str(date.today().year) + "-" + period_date, "%Y-%m-%d")
    if next_period < datetime.now():
        next_period = next_period.replace(year=next_period.year + 1)
    return (next_period - today).days

# 计算距离下一个生日的天数
def get_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days

# 获取每日一句话
def get_words():
    words = requests.get("https://api.vvhan.com/api/text/love?type=json")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['content']

# 随机生成颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)

# 微信客户端和模板
client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)

# 获取天气信息
wea, temperature = get_weather()

# 组织模板数据
data = {
    "weather": {"value": wea},  # 无需颜色
    "temperature": {"value": temperature},  # 无需颜色
    "love_days": {"value": get_count()},  # 无需颜色
    "birthday_left": {"value": get_birthday()},  # 无需颜色
    "period_days": {"value": get_period_days()},  # 新增的姨妈倒计时
    "words": {"value": get_words(), "color": "#FF0000"}  # 仅给 words 设置颜色
}

# 发送模板消息
res = wm.send_template(user_id, template_id, data)
print(res)
