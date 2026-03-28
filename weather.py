import os
import requests
from datetime import datetime

# Mapping ไอคอนเบื้องต้น
ICON_MAP = {
    "Sunny": "☀️",
    "Mostly sunny": "🌤️",
    "Partly sunny": "⛅",
    "Intermittent clouds": "☁️",
    "Cloudy": "☁️",
    "Rain": "🌧️",
    "Showers": "🌦️",
    "Mostly cloudy": "☁️"
}

# ข้อมูลเมืองที่คุณต้องการทดสอบ
CITIES = [
    {"name": "Dali", "key": "2580103"},
    {"name": "Lijiang", "key": "2333576"},
    {"name": "Xianggelila", "key": "2333561"},
    {"name": "Kunming", "key": "106812"}
]

# ดึง API Key จาก Environment Variable (สำหรับ GitHub Actions)
# หากรันในคอมตัวเองให้เปลี่ยนเป็น API_KEY = "รหัสของคุณ"
API_KEY = os.getenv('ACCUWEATHER_API_KEY')

def get_5day_forecast(city_name, location_key):
    url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}?apikey={API_KEY}&metric=true&language=th-th"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            forecast_text = f"### 📍 พยากรณ์อากาศเมือง: {city_name}\n"
            forecast_text += "| วันที่ | สภาพอากาศ | ต่ำสุด (°C) | สูงสุด (°C) |\n"
            forecast_text += "| :--- | :--- | :---: | :---: |\n"
            
            # วนลูปดึงข้อมูลทั้ง 5 วันจาก API
            for day in data['DailyForecasts']:
                date_str = datetime.fromisoformat(day['Date']).strftime('%d/%m/%Y')
                temp_min = day['Temperature']['Minimum']['Value']
                temp_max = day['Temperature']['Maximum']['Value']
                condition = day['Day']['IconPhrase']
                icon = ICON_MAP.get(condition, "🌡️") # ถ้าไม่มีใน Map ให้ใช้ปรอท
                
                forecast_text += f"| {date_str} | {icon} <br> {condition} | {temp_min} | {temp_max} |\n"
            
            return forecast_text + "\n"
        else:
            return f"❌ ไม่สามารถดึงข้อมูลของ {city_name} ได้ (Status: {response.status_code})\n\n"
    except Exception as e:
        return f"⚠️ เกิดข้อผิดพลาดกับเมือง {city_name}: {str(e)}\n\n"

# สร้างเนื้อหาหลัก
content = "# 🌦️ ทดสอบระบบพยากรณ์อากาศยูนนาน (5 วันล่วงหน้า)\n\n"
content += f"อัปเดตล่าสุดเมื่อ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (เวลา Server)\n\n"

for city in CITIES:
    content += get_5day_forecast(city['name'], city['key'])

# เขียนลงไฟล์ README.md
with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ อัปเดตข้อมูลพยากรณ์ 5 วันลงใน README.md เรียบร้อยแล้ว")
