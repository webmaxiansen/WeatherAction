from datetime import datetime, date, timedelta
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import string  # 需要导入 string 模块


# 检查所有相关环境变量的值
variables = ['START_DATE', 'CITY', 'BIRTHDAY', 'APP_ID', 'APP_SECRET', 'USER_ID', 'TEMPLATE_ID', 'PERIOD_DATE']
for var in variables:
    print(f"{var}: {os.environ.get(var)}")
    
# 获取当前日期
today = datetime.now()

# 环境变量
start_date = os.environ.get('START_DATE')
city = os.environ.get('CITY')
birthday = os.environ.get('BIRTHDAY')
app_id = os.environ.get("APP_ID")
app_secret = os.environ.get("APP_SECRET")
user_id = os.environ.get("USER_ID")
xiaoma_user_id = os.environ.get("XM_USER_ID")
template_id = os.environ.get("TEMPLATE_ID")
# 检查姨妈日期是否设置
period_date = os.environ.get("PERIOD_DATE","19")
key = os.environ.get("WEATHER_KEY")

if period_date is None:
    raise ValueError("请确保环境变量 'PERIOD_DATE' 已设置")

# 获取天气信息
def get_weather():
    url = "https://restapi.amap.com/v3/weather/weatherInfo?city=410527&key=" + key
    res = requests.get(url).json()
    
    # 检查返回结果的状态码是否为成功
    if res.get("status") == "1" and res.get("lives"):
        # 提取天气数据
        weather_data = res['lives'][0]
        weather = weather_data['weather']  # 天气类型，例如“霾”
        temperature = int(weather_data['temperature'])  # 当前温度
        return weather, temperature
    else:
        raise Exception("Failed to fetch weather data.")

# 计算恋爱天数
def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days

# # 计算距离下一个姨妈到来的天数
# def get_period_days():
#     next_period = datetime.strptime(str(date.today().year) + "-" + period_date, "%Y-%m-%d")
#     if next_period < datetime.now():
#         next_period = next_period.replace(year=next_period.year + 1)
#     return (next_period - today).days

def get_period_days():
    today = date.today()
    
    # 构造下个月的姨妈周期日期
    next_period = datetime(today.year, today.month, period_day)
    
    # 如果当前日期已过了本月的姨妈周期，则下一个姨妈周期是在下个月
    if today > next_period.date():
        if today.month == 12:
            # 如果当前是12月，则下一个周期在明年1月
            next_period = datetime(today.year + 1, 1, period_day)
        else:
            # 否则，下一个周期在下个月
            next_period = datetime(today.year, today.month + 1, period_day)
    
    # 计算并返回天数差
    return (next_period - today).days

# 输出距离下一个姨妈到来的天数
print("距离姨妈到来剩余：{get_period_days()}")

# 计算距离下一个生日的天数
def get_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days

# 获取每日一句话
def get_words():
    words = requests.get("https://api.vvhan.com/api/text/love?type=json")
    
    # 如果请求不成功，重新调用
    if words.status_code != 200:
        return get_words()
    
    # 获取返回的内容
    content = words.json()['data']['content']
    
    # 判断内容的长度是否大于20，且是否包含标点符号
    if len(content) > 20 or any(char in string.punctuation for char in content):
        return get_words()  # 如果不符合要求，则重新获取
    
    return content

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

# 发送模板消息1
res = wm.send_template(user_id, template_id, data)
print(res)

# 发送模板消息2
res = wm.send_template(xiaoma_user_id, template_id, data)
print(res)

