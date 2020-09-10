import asyncio
import discord
import datetime
import emoji
import os
import sys
import requests
from pprint import pprint

client = discord.Client()

token = "NzA5NTcwMjU1NjcyMDQ5Njc0.Xrn0zA.OOmxQYYJ9zeeA5GFJPR-Cd41UZw"

imgmod = False
chsmod = False
att = []
clock = []

client_id = "buG_X9Dd9ZHoOGM5GB5b"
client_secret = "833AKK0Ivs"

def get_translate1(text,start, last):
    data = {'text' : text,
            'source' : start,
            'target': last}

    url = "https://openapi.naver.com/v1/papago/n2mt"

    header = {"X-Naver-Client-Id":client_id,
              "X-Naver-Client-Secret":client_secret}

    response = requests.post(url, headers=header, data= data)
    rescode = response.status_code

    if(rescode==200):
        t_data = response.json()
        pprint(t_data['message']['result']['translatedText'])
        return t_data['message']['result']['translatedText']
    else:
       print("Error Code:" , rescode)

@client.event
async def on_ready():
    print("Logged in as ")  # 화면에 봇의 아이디, 닉네임이 출력됩니다.
    print(client.user.name)
    print(client.user.id)
    print(discord.__version__)
    print("===========")
    # 디스코드에는 현재 본인이 어떤 게임을 플레이하는지 보여주는 기능이 있습니다.
    # 이 기능을 사용하여 봇의 상태를 간단하게 출력해줄 수 있습니다.
    game = discord.Game("명령 대기")
    await client.change_presence(status=discord.Status.online, activity=game)


# 봇이 새로운 메시지를 수신했을때 동작되는 코드입니다.


@client.event
async def on_message(message):
    global imgmod
    global chsmod
    if message.author.bot:
        return None

    id = message.author.id
    channel = message.channel
    a = str(message.content)

    def check(m):
        return m.channel.id == message.channel.id and m.author == message.author

    if imgmod is True and message.content.startswith("=끝"):
        await message.channel.send("번역 모드 비활성화")
        game = discord.Game("명령 대기")
        await client.change_presence(status=discord.Status.online, activity=game)
        imgmod = False
    elif message.content.startswith('=시작'):
        await message.channel.send("한글 -> 영어 번역 모드 활성화")
        game = discord.Game("영잘알 모드")
        await client.change_presence(status=discord.Status.online, activity=game)
        imgmod = True
    elif imgmod:
        if "\u200b" in message.content:
            await message.channel.send("하지말라.")
        else:
            c = str(get_translate1(message.content, "ko", "en"))
            print(c)
            await message.channel.send(c)

    elif message.content.startswith("일어날 기"):
        now = datetime.datetime.now()
        f = open("출석부.txt", "a+")

        s = "{}년{}월{}일{}시{}분".format(now.year, now.month, now.day, now.hour, now.minute)
        t = str(message.author)
        f.write("\n" + str(t) + " " + str(s) + "\n")
        if t in att:
            await message.channel.send("이미 일어날 기를 외치셨습니다. 시간 : "+clock[att.index(t)])
        else:
            msg = "{}년{}월{}일{}시{}분 기상이 인증되었습니다.".format(now.year, now.month, now.day, now.hour, now.minute)
            att.append(t)
            clock.append(s)
            await message.channel.send(msg)
    elif message.content.startswith("일어날기근황 근"):
        now = datetime.datetime.now()
        for i in range(len(att)):
            if i == 0 :
                title = "<{}월 {}일 일어날 기 근황>".format(now.month,now.day)
                await message.channel.send(title)
            msg = att[i] + " : " + clock[i][10:]+"에 일어남."
            await message.channel.send(msg)

client.run(token)

