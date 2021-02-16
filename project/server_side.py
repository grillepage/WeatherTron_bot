import config
import requests
import json
import icons_imgs as img

def today_weather(city):
    with open('today.json', 'w', encoding='utf-8') as json_save:
        req = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric' + '&lang=ru' +'&appid=' + config.weather_key
        response = requests.get(req)
        source = (response.json())
        json_save.write(json.dumps(source, ensure_ascii=False))
    return today_weather_decode(city)


def today_weather_decode(city):
    with open('today.json', 'r', encoding='utf-8') as json_load:
        source = json.load(json_load)
        description = str((source['weather'][0]['description']).upper())
        temp_now = str(int((source['main']['temp']) // 1)) + '°С'
        weather_icon_source = str(source['weather'][0]['icon'])
        weather_icon = img.icons.get(weather_icon_source)
        feels_like = str(int((source['main']['feels_like']) // 1)) + '°С'
        final_text = 'Погода в городе ' + city + ' сейчас:' + '\n' + temp_now + '\n' + description + ' ' + weather_icon + '\n' + '(Ощущается как: ' + feels_like + ')'
    return final_text

def tomorrow_weather(city):
    with open('tomorrow.json', 'w', encoding='utf-8') as json_save:
        req = 'https://api.openweathermap.org/data/2.5/forecast?q=' + city + '&units=metric' + '&lang=ru' +'&appid=' + config.weather_key
        response = requests.get(req)
        source = response.json()
        json_save.write(json.dumps(source["list"][1], ensure_ascii=False))
    # return json.dumps(source["list"][1], ensure_ascii=False)
    return tomorrow_weather_decode(city)

def tomorrow_weather_decode(city):
    with open('tomorrow.json', 'r', encoding='utf-8') as json_load:
        source = json.load(json_load)
        description = str((source['weather'][0]['description']).upper())
        temp_tomorrow = str(int((source['main']['temp']) // 1)) + '°С'
        weather_icon_source = str(source['weather'][0]['icon'])
        weather_icon = img.icons.get(weather_icon_source)
        feels_like = str(int((source['main']['feels_like']) // 1)) + '°С'
        final_text = 'Погода в городе ' + city + ' завтра:' + '\n' + temp_tomorrow + '\n' + description + ' ' + weather_icon + '\n' + '(Ощущается как: ' + feels_like + ')'
    return final_text