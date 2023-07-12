from translatepy import Translator, Language
from translatepy.translators.yandex import YandexTranslate
from translatepy.translators.google import GoogleTranslate
from translatepy.translators.bing import BingTranslate
import datetime
import pytz
import json
import os
import typing 
path_to_speech_dir = os.path.abspath(os.getcwd()).replace(
    'handlers', "speech_files_directory")



def inline_translater(message: str, lang='eng'):
    ytranslate = BingTranslate()
    try:
        if message.strip().find(' ') == -1:

            if lang != 'eng':
                message = ytranslate.translate(message.strip(), 'eng').result
                # ?Deafault word like Wheel, Ace, Mouse
                if message.strip().find(' ') == -1:

                    output_translate = ytranslate.dictionary(message, lang)
                    options = "<b>" + f'{output_translate.result[0]}, </b>'.capitalize() + ", ".join(output_translate.result[1::])
                    one_option = "<b>" + f'{output_translate.result[0]}</b>'.capitalize()
                    return options if len(output_translate.result) > 1 else one_option
                # ? 2 Words but using only together in grammar like: This is, There are
                else:
                    output_translate = ytranslate.translate(message, lang)
                    return "<b>" + f'{output_translate.result}</b>'.capitalize()
                
        output_translate = ytranslate.translate(message, lang)       
        return output_translate.result
    except:
        raise
# /usr/local/lib/python3.10/site-packages/translatepy/translators/bing.py

def text_to_speech(translate: typing.Union[str, list]):
    gtranslate = GoogleTranslate()

    speech_file = gtranslate.text_to_speech(text=translate)
    # speech_file.write_to_file(
    #     f"{path_to_speech_dir}/translator-tgbot/speech_files_directory/mp{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp3"
    # )
    return speech_file.result
def take_user_timezone(time, recieveMessageTime: datetime):
    zones = [
        'Etc/GMT', 'Etc/GMT+0', 'Etc/GMT+1', 'Etc/GMT+10', 'Etc/GMT+11',
        'Etc/GMT+12', 'Etc/GMT+2', 'Etc/GMT+3', 'Etc/GMT+4', 'Etc/GMT+5',
        'Etc/GMT+6', 'Etc/GMT+7', 'Etc/GMT+8', 'Etc/GMT+9', 'Etc/GMT-0',
        'Etc/GMT-1', 'Etc/GMT-10', 'Etc/GMT-11', 'Etc/GMT-12', 'Etc/GMT-13',
        'Etc/GMT-14', 'Etc/GMT-2', 'Etc/GMT-3', 'Etc/GMT-4', 'Etc/GMT-5',
        'Etc/GMT-6', 'Etc/GMT-7', 'Etc/GMT-8', 'Etc/GMT-9', 'Etc/GMT0',
        'Etc/Greenwich', 'Etc/UCT', 'Etc/UTC', 'Etc/Universal', 'Etc/Zulu'
    ]

    for zone in zones:
        find_zone = pytz.timezone(zone)
        time_in_zone = datetime.datetime.now(find_zone)
        currentTimeInZone = time_in_zone.strftime("%H:%M")
        
        if time == currentTimeInZone:
            return {
                "IsActive": True,
                "timeInZone": str(find_zone),
                "settedTimeByUser": recieveMessageTime.strftime("%H:%M")
            }