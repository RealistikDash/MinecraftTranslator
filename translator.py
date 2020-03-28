from googletrans import Translator
from colorama import Fore, init, Back
import json
import datetime
from os import path
import time
from random import choice

init() #initialises colorama

#languages that the text will be translated between
Languages = ["ru", "ja", "su", "th", "ig", "lt", "nl", "sv", "gd", "ur", "mt", "zh-TW", "zh-CN", "af", "ar", "ny", "lb", "ku", "az", "ro", "sn", "fa", "hi", "da"]

Translate = Translator()

class JsonFile:
    @classmethod
    def SaveDict(self, Dict, File="config.json"):
        """Saves a dict as a file"""
        with open(File, 'w+') as json_file:
            json.dump(Dict, json_file, indent=4)

    @classmethod
    def GetDict(self, File="config.json"):
        """Returns a dict from file name"""
        if not path.exists(File):
            return {}
        else:
            with open(File) as f:
                data = json.load(f)
            return data

class TextFormat:
    intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

    @classmethod
    def DisplayTime(self, seconds, DisplayHowMuch=2):
        """Converts seconds to nicely formatted time."""
        result = []

        for name, count in self.intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(value, name))
        return ', '.join(result[:DisplayHowMuch])

def TimestampConverter(timestamp, NoDate=1):
    """Converts timestamps into readable time."""
    date = datetime.datetime.fromtimestamp(int(timestamp)) #converting into datetime object
    if NoDate == 1:
        #return f"{hour}:{minute}"
        return date.strftime("%H:%M")
    if NoDate == 2:
        return date.strftime("%H:%M %d/%m/%Y")

def TranslateText(Text: str, Repeat:int=20):
    """This is the all in one translate function that covers the language randomisation, repetition and translation."""
    while Repeat != 0:
        Lang = choice(Languages)
        Result = Translate.translate(Text, dest=Lang)
        Text = Result.text
        Repeat -= 1
    return Text

def WorkOutMean(List:list):
    """Works out list from given mean."""
    ListLenght = len(List)
    Total = 0
    for x in List:
        Total += x
    return Total / ListLenght

#reading the MC json
LanguageJson = JsonFile.GetDict("en_us.json")

#Notifying the user
print(f"{Fore.BLUE}Minecraft Google Translator\nby RealistikDash{Fore.RESET}")
if LanguageJson == {}:
    print(f"{Back.RED}{Fore.BLACK}The language file could not be loaded! The program cannot continue! Closing...{Fore.RESET}{Back.RESET}")
    time.sleep(3)
    exit()
print(f"{Back.BLUE}{Fore.BLACK}This process can take a VERY long time (around 3 hours)! Are you sure you want to continue?{Fore.RESET}{Back.RESET}")
Response = input("(y/N/restore) ").lower()
if Response != "y":
    exit()
if Response == "restore":
    JsonFile.GetDict("en-us-gtransated.json")

#eta prerequisites
TextToDo = len(list(LanguageJson.keys()))
AllTimes = []

#start the translation
FinalJson = {}
for key in list(LanguageJson.keys()):
    StartTime = round(time.time())
    print(f"{Fore.BLACK}{Back.BLUE}[{TimestampConverter(round(time.time()))}] Beginning to translate {key}!{Fore.RESET}{Back.RESET}")
    Text = LanguageJson[key]
    try:
        Translated = TranslateText(Text)
    except json.decoder.JSONDecodeError:
        print(f"{Back.RED}{Fore.BLACK}Look like Google doesnt like you... Saving results!{Fore.RESET}{Back.RESET}")
        break
    FinalJson[key] = Translated
    EndTime = round(time.time())
    print(f"{Fore.BLACK}{Back.GREEN}[{TimestampConverter(round(time.time()))}] Key {key} translated!{Fore.RESET}{Back.RESET}")
    TextToDo -= 1
    TimeTaken = EndTime - StartTime
    AllTimes.append(TimeTaken)
    ETA = TextFormat.DisplayTime(WorkOutMean(AllTimes) * TextToDo) #Works out ETA and puts it in a readable format
    print(f"{Fore.BLUE}Time taken: {TimeTaken}s   |   ETA: {ETA}{Fore.RESET}")

#saves the new json
JsonFile.SaveDict(FinalJson, "en-us-gtransated.json")
print(f"{Back.BLUE}{Fore.BLACK}Translation finished! The translated json can be found as en-us-gtransated.json!\nHave fun!{Fore.RESET}{Back.RESET}")
time.sleep(5)
exit()