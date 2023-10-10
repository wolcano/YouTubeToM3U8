#! /usr/bin/python3
import requests
import os
import unicodedata
from datetime import datetime, timedelta
from lxml import etree


channels = []

# From https://stackoverflow.com/questions/4324790/removing-control-characters-from-a-string-in-python
def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def build_xml_tv(streams: list) -> bytes:
    data = etree.Element("tv")
    data.set("generator-info-name", "youtube-live-epg")
    data.set("generator-info-url", "https://github.com/dp247/YouTubeToM3U8")

    for stream in streams:
        channel = etree.SubElement(data, "channel")
        channel.set("id", stream[1])
        name = etree.SubElement(channel, "display-name")
        name.set("lang", "en")
        name.text = stream[0]

    # TODO: Make this less static - i.e. generate the next 6 hour blocks from time run rather than midnight
    dt_format = '%Y%m%d%H%M%S %z'
    start_times = ["000000", "060000", "120000", "180000"]
    end_times = ["060000", "120000", "180000", "000000"]

    for i in range(4):
        programme = etree.SubElement(data, 'programme')
        start = datetime.combine(datetime.today().date(), datetime.strptime(start_times[i], "%H%M%S").time()).strftime(dt_format)
        if i < 3:
            end = datetime.combine(datetime.today().date(), datetime.strptime(end_times[i], "%H%M%S").time()).strftime(dt_format)
        else:
            end = datetime.combine((datetime.today() + timedelta(days=1)).date(), datetime.strptime(end_times[i], "%H%M%S").time()).strftime(dt_format)

        print("")

def grab(url):
    z = requests.get(url, timeout = 15)
    response = requests.get(url, timeout = 15).text
    if '.m3u8' not in response:
        print("https://www.youtube.com/watch?v=1oh9IEwBbFY")
        return
    end = response.find('.m3u8') + 5
    tuner = 100
    while True:
        if 'https://' in response[end - tuner : end]:
            link = response[end - tuner : end]
            start = link.find('https://')
            end = link.find('.m3u8') + 5
            break
        else:
            tuner += 5
    print(f"{link[start : end]}")

with open('./youtubeLink.txt', encoding='utf-8') as f:
    print("#EXTM3U")
    for line in f:
        line = line.strip()
        if not line or line.startswith('##'):
            continue
        if not line.startswith('https:'):
            line = line.split('||')
            channel_name = line[0].strip()
            channel_id = line[1].strip()
            category = line[2].strip().title()
            channels.append((channel_name, channel_id, category))
            print(f'\n#EXTINF:-1 tvg-id="{channel_id}" tvg-name="{channel_name}" group-title="{category}", {channel_name}')
        else:
            grab(line)

build_xml_tv(channels)
            
if 'temp.txt' in os.listdir():
    os.system('rm temp.txt')
    os.system('rm watch*')
