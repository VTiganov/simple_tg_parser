from dotenv import load_dotenv
import os
from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv

load_dotenv() # create your .env file 
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

client = TelegramClient('session_name', api_id, api_hash)

async def save_messages_to_csv():
    
    me = await client.get_me()
    my_id = me.id
    
    with open('all_messages.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(['Chat Name', 'Message ID', 'Sender ID', 'Date', 'Message'])

        async for dialog in client.iter_dialogs():
            chat_name = dialog.name

            if chat_name in ["AI котята", "Евгений Понасенков"]:
                print(f"Чат '{chat_name}' пропущен.")
                continue

            print(f"Getting messages from: {chat_name}")

            async for message in client.iter_messages(dialog.id):
                if message.sender_id == my_id:
                    writer.writerow([
                        chat_name,
                        message.id,
                        message.sender_id,
                        message.date,
                        message.text or ''
                    ])
    print("Messages succesfully saved to all_messages.csv")


async def main():
    await save_messages_to_csv()


with client:
    client.loop.run_until_complete(main())

