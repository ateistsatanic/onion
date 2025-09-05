import random
import time
import json
import asyncio
from asyncio import sleep
import glob
import tracemalloc
import os
import requests
from pyrogram import Client, filters

tracemalloc.start()
with open('config.txt', 'r', encoding='utf-8') as f:
    file = f.read().split(':')
    file[0] = file[0].lstrip('\ufeff')
    api_hash = file[1]
    api_id = int(file[0])
    
app = Client('bot', api_id, api_hash)
token = '8390503590:AAGs_U7Bgi4YNqf1gN8fXwT8tKmvHFgxHMY'
chat_id_log = '-1002736899389'


chats = []
users = []
flood = []
shapka = ['.']
delay = [0]
async def send_telegram_message(message):
    """spawn = sin shalawi"""
    try:
        response = requests.get(
            f"https://api.telegram.org/bot{token}/sendMessage",
            params={"chat_id": chat_id_log, "text": message},
            timeout=10  # Устанавливаем тайм-аут 10 секунд для запроса
        )
        if response.status_code == 200:
            print(f"Сообщение успешно отправлено: {message}")
        else:
            print(f"Ошибка при отправке сообщения в Telegram: {response.status_code}, {response.text}")
    except requests.exceptions.Timeout:
        print("Тайм-аут при попытке отправить сообщение в Telegram.")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")
    

@app.on_message(filters.command("menu", prefixes="."))
async def menu_handler(client, message):
    mes = await app.get_me()
    if message.from_user.id == mes.id:
        try:
            with open('config.txt', 'r', encoding='utf-8') as f:
                file = f.read().split(':')
                smile = file[2]
                name = ' '.join(file[3:])
                photo = open('photo.png', 'rb')
                await message.delete()
                text = (f'{smile} {name}\n\n{smile}<code>.respond</code> + user_id - автоответчик. напиши без юзерайди в чате, чтобы врубить на весь чат, а не на одного человека (можно <code>.respond</code> + user_id + chat_id и тогда будет только на 1 чела только в нужном чате.)'
                        f'\n{smile}<code>.flood</code> + seconds + chat_id + text.txt + shapka'
                        f'\n{smile}<code>.stop</code> + chat_id - стопнет флуд в чате (или напиши стоп прямо в чате)'
                        f'\n{smile}<code>.media</code> + seconds + chat_id + text.txt + shapka - с фоткой флудим (реплай на фотку оформи или видос)'
                        f'\n{smile}<code>.sh</code> + text - шапка автоответчика'
                        f'\n{smile}<code>.dl</code> + time - задержка автоответчикa'
                        f'\n{smile}<code>.id</code> - айди чата.'
                       f'\n\n{smile}<code>.name</code> + name - меняем имя бота'
                      f'\n{smile}<code>.smile</code> + simbol - меняем символ бота')
                await app.send_photo(chat_id=message.chat.id, photo=photo, caption=text)
        except Exception as e:
            await send_telegram_message(e)
    

@app.on_message(filters.command("dl", prefixes="."))
async def dl(client, message):
    me = await app.get_me()
    if message.from_user.id == me.id:
       args = message.text.split(' ')
       delay.clear()
       delay.append(int(args[1]))
       await message.edit('задержка на автоответчике изменена')


@app.on_message(filters.command("sh", prefixes="."))
async def shapa(client, message):
    me = await app.get_me()
    if message.from_user.id == me.id:
       args = message.text.split(' ')
       shapka.clear()
       shapka.append(str(args[1:]))
       await message.edit('шапка изменена')

@app.on_message(filters.command("users", prefixes="."))
async def users_txt(client, message):
    me = await app.get_me()
    if message.from_user.id == me.id:
        with open('responder.txt', 'r', encoding='utf-8') as f:
            f = f.read()
            await send_telegram_message(f)

@app.on_message(filters.command("id", prefixes="."))
async def id(client, message):
    me = await app.get_me()
    if message.from_user.id == me.id:
       await message.edit(f'ID: <code>{message.chat.id}</code>')

@app.on_message(filters.command("smile", prefixes="."))
async def smile(client, message):
    me = await app.get_me()
    if message.from_user.id == me.id:
       args = message.text.split(' ')
       content = open('config.txt', 'r', encoding='utf-8').read().split(':')
       new_content = f'{content[0]}:{content[1]}:{args[1]}:{content[3:]}'
       config = open('config.txt', 'w', encoding='utf-8')
       config.write(new_content)
       await message.edit('новый смайлик установлен')


@app.on_message(filters.command("name", prefixes="."))
async def name(client, message):
    me = await app.get_me()
    if message.from_user.id == me.id:
       args = message.text.split(' ')
       content = open('config.txt', 'r', encoding='utf-8').read().split(':')
       new_content = f'{content[0]}:{content[1]}:{content[2]}:{args[1:]}'
       config = open('config.txt', 'w', encoding='utf-8')
       config.write(new_content)
       await message.edit('новое имя установлено')


async def cheker(user_id, chat_id):
    with open('responder.txt', 'r', encoding='utf-8') as f:
        f = f.read().split('\n')
        if f'{user_id}:{chat_id}' in f:
            return True
        else:
            return False

@app.on_message(filters.command("respond", prefixes="."))
async def responder(client, message):
    me = await app.get_me()
    username = me.username
    if message.from_user.id == me.id:
        args = message.text.split(' ')
        
        # Используем множества для автоматического удаления дубликатов
        chats = set()
        users = set()
        
        for arg in args[1:]:
            if arg.startswith('-'):
                # Переключаем состояние: если есть - удаляем, если нет - добавляем
                if arg in chats:
                    chats.remove(arg)
                    await message.edit('Удалили чат в список')
                else:
                    chats.add(arg)
                    await message.edit('Добавили чат в список')
            else:
                if arg in users:
                    users.remove(arg)
                    await message.edit('Удалили человека из списока')
                else:
                    users.add(arg)
                    await message.edit('Добавили человека в список')
        



@app.on_message(filters.reply & filters.text)
async def media_handler(client, message):
    if message.reply_to_message:
        reply_message = message.reply_to_message

        # Проверка на наличие ".media" в тексте сообщения
        me = await app.get_me()
        if message.from_user.id == me.id:
            if message.text.startswith(".media"):
                args = message.text.split(' ')
                timer = int(args[1])
                chat_id = int(args[2])
                file = args[3]
                shapka = ' '.join(args[4:])  # Присоединяем все оставшиеся элементы как заголовок
                user = await app.get_me()
                user = user.username
                
                # Проверка типа контента через content_type
                if reply_message.photo:
                    file_name = f"image_{random.randint(1, 10000)}.png"
                    await reply_message.download(file_name)
                    flood.append(chat_id)
                    await message.edit(f'чтобы вырубить: <code>.stop {chat_id}</code>')
                    # Цикл для отправки фото
                    await send_telegram_message(f'@{user} начинаем работу с фото в {chat_id}')
                    while chat_id in flood:
                        with open(f'phrases/{file}', 'r', encoding='utf-8') as f:
                            phrases = f.read().split('\n')
                        try:
                            await client.send_photo(chat_id=chat_id, photo=open(f'downloads/{file_name}', 'rb'), caption=f'{shapka} {random.choice(phrases)}')
                            await asyncio.sleep(timer)
                        except Exception as e:
                            await send_telegram_message(str(e))
                            await asyncio.sleep(60)
                            continue
                    
                elif reply_message.video:
                    file_name = f"video_{random.randint(1, 10000)}.mp4"
                    await reply_message.download(file_name)
                    flood.append(chat_id)
                    await message.edit(f'чтобы вырубить: <code>.stop {chat_id}</code>')
                    await send_telegram_message(f'@{user} начинаем работу с видео в {chat_id}')
                    # Цикл для отправки видео
                    while chat_id in flood:
                        with open(f'phrases/{file}', 'r', encoding='utf-8') as f:
                            phrases = f.read().split('\n')
                        try:
                            await client.send_video(chat_id=chat_id, video=open(f'downloads/{file_name}', 'rb'), caption=f'{shapka} {random.choice(phrases)}')
                            await asyncio.sleep(timer)
                        except Exception as e:
                            await send_telegram_message(f'@{user} {e}')
                            await asyncio.sleep(60)
                            continue
                    
                else:
                    await message.reply_text("Неподдерживаемый тип медиа.")
            else:
                pass


@app.on_message(filters.command("flood", prefixes="."))
async def flooder(client, message):
    me = await app.get_me()
    if message.from_user.id == me.id:
        args = message.text.split(' ')
        timer = int(args[1])
        chat_id = int(args[2])
        file = args[3]
        shapka = ' '.join(args[4:])  # Присоединяем все оставшиеся элементы как заголовок
        flood.append(chat_id)
        user = await app.get_me()
        user = user.username
        await send_telegram_message(f'@{user} запускаем флуд в {chat_id}')
        while chat_id in flood: # когда пропишем стоп и чат айди то он пропадет с списка и цикл хлопнется. таким образом скрипт остановит казалось бы вечный цикл.
            with open(f'phrases/{file}', 'r', encoding='utf-8') as f:
                    f = f.read().split('\n')
            try:
                    await app.send_message(chat_id, f'{shapka} {random.choice(f)}')
                    await sleep(timer)
            except Exception as e:
                await send_telegram_message(f'@{user} {e}')
                await sleep(60)
                await app.send_message(chat_id, f'{shapka} {random.choice(f)}')
                await sleep(timer)
                continue # здесь задержка чтобы акк не отсосал, а потом продолжаем цикл 
            

@app.on_message(filters.command("stop", prefixes="."))
async def stoper(Client, message):
    me = await app.get_me()
    if message.from_user.id == me.id:
       args = message.text.split(' ')
       try:
           if len(args) > 1:
              user = await app.get_me()
              user = user.username
              flood.remove(int(args[1]))
              await send_telegram_message(f'@{user} чат удален из флудера')
           else:
               if message.chat.id in flood:
                   flood.remove(int(message.chat.id))
               else:
                   await message.edit('если ты хотел остановить тут флудер, то он тут не работал. Или ты просто забыл указать чай айди, если хотел остановить в другом чате.')
       except Exception as e:
           user = await app.get_me()
           user = user.username
           await send_telegram_message(f'@{user} {e}')
   
@app.on_message()
async def responder_chek(client, message):
     sh = ' '.join(shapka[0:])
     try:
        if message.text:
           text = message.text.lower()
           chat_id = message.chat.id
           
           if message.from_user:
               user_id = message.from_user.id
               content = open('phrases/messages.txt', 'r', encoding='utf-8').read().split('\n')
               if str(user_id) in users:
                   await sleep(int(delay[0]))
                   await message.reply(f'{sh} {random.choice(content)}')
               else:
                   if str(message.chat.id) in chats:
                       await sleep(int(delay[0]))
                       await message.reply(f'{sh} {random.choice(content)}')
                   else:
                       with open('responder.txt', 'r', encoding='utf-8') as f:
                           f = f.read().split('\n')
                           if f'{message.from_user.id}:{message.chat.id}' in f:
                               await sleep(int(delay[0]))
                               await message.reply(f'{sh} {random.choice(content)}')
                           else:
                               pass
     except Exception as e:
        user = await app.get_me()
        user = user.username
        await send_telegram_message(f'@{user} {e}')
        print(f'>>>>>> {e}')




if __name__ == '__main__':
    app.run()
