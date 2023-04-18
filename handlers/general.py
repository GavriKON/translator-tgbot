from translatepy import Translator, Language
from translatepy.translators.bing import BingTranslate
import datetime
import pytz
import json

gtranslate = BingTranslate()


def inline_translater(message: str, lang='eng'):
    try:
        output_translate = gtranslate.translate(message, lang)
        return output_translate
    except:
        raise

def take_user_timezone(time, recieveMessageTime: datetime):            
    zones = ['Etc/GMT', 'Etc/GMT+0', 'Etc/GMT+1', 'Etc/GMT+10', 'Etc/GMT+11', 'Etc/GMT+12', 'Etc/GMT+2', 'Etc/GMT+3', 'Etc/GMT+4', 'Etc/GMT+5', 'Etc/GMT+6', 'Etc/GMT+7', 'Etc/GMT+8', 'Etc/GMT+9', 'Etc/GMT-0', 'Etc/GMT-1', 'Etc/GMT-10', 'Etc/GMT-11', 'Etc/GMT-12', 'Etc/GMT-13', 'Etc/GMT-14', 'Etc/GMT-2', 'Etc/GMT-3', 'Etc/GMT-4', 'Etc/GMT-5', 'Etc/GMT-6', 'Etc/GMT-7', 'Etc/GMT-8', 'Etc/GMT-9', 'Etc/GMT0', 'Etc/Greenwich', 'Etc/UCT', 'Etc/UTC', 'Etc/Universal', 'Etc/Zulu']
    for zone in zones:
        find_zone = pytz.timezone(zone) 
        time_in_zone = datetime.datetime.now(find_zone)
        currentTimeInZone = time_in_zone.strftime("%H:%M")
        if time == currentTimeInZone:
            return {"IsActive":True, "timeInZone":str(find_zone), "settedTimeByUser":recieveMessageTime.strftime("%H:%M")}
# exmpl = take_user_timezone('20:00', '17:00')
# print(datetime.datetime.strptime(exmpl['timeInZone'], '%H:%M') < datetime.datetime.strptime(exmpl['settedTimeByUser'], '%H:%M'))
