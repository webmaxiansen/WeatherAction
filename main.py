from datetime import datetime, date
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
period_date = int(os.environ.get("PERIOD_DATE","19"))
key = os.environ.get("WEATHER_KEY")

if period_date is None:
    raise ValueError("请确保环境变量 'PERIOD_DATE' 已设置")


# Define a list of random User-Agent headers
headers_list = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"},
    {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/602.1"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/602.1"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15"},
    {"User-Agent": "Mozilla/5.0 (Linux; U; Android 9; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 9.0; Win64; x64) AppleWebKit/583.3 (KHTML, like Gecko) Chrome/107.0.4739.36 Safari/529.20"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/526.24 (KHTML, like Gecko) Chrome/101.0.4912.15 Safari/594.20"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 9; SM-G973F) AppleWebKit/510.41 (KHTML, like Gecko) Chrome/101.0.4876.72 Mobile Safari/515.4"},
    {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/76.0"},
    {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/671.1.9 (KHTML, like Gecko) Version/12.0 Mobile/15E101 Safari/657.1.46"},
    {"User-Agent": "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/659.1.43 (KHTML, like Gecko) Version/14.0 Mobile/15E164 Safari/686.1.50"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 9.0; Win64; x64) AppleWebKit/583.3 (KHTML, like Gecko) Chrome/107.0.4739.36 Safari/529.20"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/526.24 (KHTML, like Gecko) Chrome/101.0.4912.15 Safari/594.20"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 9; SM-G973F) AppleWebKit/510.41 (KHTML, like Gecko) Chrome/101.0.4876.72 Mobile Safari/515.4"},
    {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/76.0"},
    {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/671.1.9 (KHTML, like Gecko) Version/12.0 Mobile/15E101 Safari/657.1.46"},
    {"User-Agent": "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/659.1.43 (KHTML, like Gecko) Version/14.0 Mobile/15E164 Safari/686.1.50"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 9.0; Win64; x64) AppleWebKit/583.3 (KHTML, like Gecko) Chrome/107.0.4739.36 Safari/529.20"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/526.24 (KHTML, like Gecko) Chrome/101.0.4912.15 Safari/594.20"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 9; SM-G973F) AppleWebKit/510.41 (KHTML, like Gecko) Chrome/101.0.4876.72 Mobile Safari/515.4"},
    {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/76.0"},
    {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/671.1.9 (KHTML, like Gecko) Version/12.0 Mobile/15E101 Safari/657.1.46"},
    {"User-Agent": "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/659.1.43 (KHTML, like Gecko) Version/14.0 Mobile/15E164 Safari/686.1.50"}
]


# Randomly select one header
random_header = random.choice(headers_list)

print(f"请求头信息为：{random_header}")

# 获取天气信息
def get_weather():
    url = "https://restapi.amap.com/v3/weather/weatherInfo?city=410527&key=" + key
    res = requests.get(url,headers=random_header).json()
    
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
    print(f"今天的日期: {today}")  # 打印今天的日期
    
    # 确保 period_date 是整数类型
    # period_date = int(period_date)  # 转换为整数类型
    
    # 构造下个月的姨妈周期日期
    next_period = datetime(today.year, today.month, period_date)
    print(f"本月的姨妈周期日期: {next_period.date()}")  # 打印本月的姨妈周期日期
    
    # 如果当前日期已过了本月的姨妈周期，则下一个姨妈周期是在下个月
    if today > next_period.date():
        if today.month == 12:
            # 如果当前是12月，则下一个周期在明年1月
            next_period = datetime(today.year + 1, 1, period_date)
        else:
            # 否则，下一个周期在下个月
            next_period = datetime(today.year, today.month + 1, period_date)
        
        print(f"因为今天已经过了本月的周期，所以下一个姨妈周期日期是: {next_period.date()}")
    
    # 将 today 转换为 datetime 类型，默认为 00:00:00
    today_datetime = datetime(today.year, today.month, today.day)
    
    # 计算并返回天数差
    days_until_next_period = (next_period - today_datetime).days
    print(f"距离下一个姨妈周期还有 {days_until_next_period} 天")
    
    return days_until_next_period

# 调用函数并输出日志
print(f"距离姨妈到来剩余：{get_period_days()}")

# 计算距离下一个生日的天数
def get_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days

# 获取每日一句话
def get_words():
    words = requests.get("https://api.vvhan.com/api/text/love?type=json",headers=random_header)
    
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

