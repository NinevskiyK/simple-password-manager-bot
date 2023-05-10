#!/usr/bin/env python3

from telebot.async_telebot import AsyncTeleBot
import asyncio
import os
import helpers

collection = helpers.get_user_collection()
ttd = 30 # time to delete in seconds
tg_token = os.environ['TG_TOKEN']
bot = AsyncTeleBot(tg_token)

@bot.message_handler(commands=['start'])
async def hello(message):
    try:
        await bot.send_message(message.chat.id, "Hello! I can help you with managing your passwords!\n"+
                                "Type /set <service> <login> <password> to store it, /del <name> to delete it and /get <name> to get it!")
    except Exception as e:
        print(f'caught {type(e)}: {e}')

@bot.message_handler(commands=['set'])
async def hello(message):
    try:
        if not await helpers.post_password(collection, message.from_user.id, message.text.split()[1], (message.text.split()[2], message.text.split()[3])):
            await bot.send_message(message.chat.id, "Something wrong. Maybe you've already added this login?")
            return
        await bot.send_message(message.chat.id, "I've saved it! Will delete it soon not to exposure it!")
        await asyncio.sleep(ttd)
        await bot.delete_message(message.chat.id, message.message_id)
    except IndexError as e:
        await bot.send_message(message.chat.id, "You should give me 3 strings: name(of service), login and password. For example: /set vk my_login my_password")
    except Exception as e:
        print(f'caught {type(e)}: {e}')


@bot.message_handler(commands=['del'])
async def hello(message):
    try:
        if not await helpers.delete_password(collection, message.from_user.id, message.text.split()[1]):
            await bot.send_message(message.chat.id, "Something wrong. Maybe you don't have such login info?")
            return
        await bot.send_message(message.chat.id, "Have deleted it!")
    except Exception as e:
        print(f'caught {type(e)}: {e}')

@bot.message_handler(commands=['get'])
async def hello(message):
    try:
        info = await helpers.get_info(collection, message.from_user.id, message.text.split()[1])
        if info is None:
            await bot.send_message(message.chat.id, "Something wrong. Maybe you don't have such login info?")
            return
        sent_message = await bot.send_message(message.chat.id, 'Here is the login and password:\n{}\n{}\nWill delete it soon(in {} seconds)'.format(info[0], info[1], ttd))
        await asyncio.sleep(ttd)
        await bot.delete_message(sent_message.chat.id, sent_message.message_id)
    except Exception as e:
        print(f'caught {type(e)}: {e}')

if __name__ == '__main__':
    asyncio.run(bot.polling(none_stop=True))
