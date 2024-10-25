from dotenv import load_dotenv
import os
from telethon import TelegramClient
import csv
import asyncio

# Load environment variables from .env file
load_dotenv() 
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME", "session_name")

# Validate API keys
if not api_id or not api_hash:
    raise ValueError("API_ID and API_HASH must be specified in the .env file")

# Initialize the Telegram client
client = TelegramClient(session_name, int(api_id), api_hash)

async def save_messages_to_csv(excluded_chats=None):
    """Saves messages from all chats to a CSV, excluding specified chats."""
    
    # Default chats to exclude if none provided
    if excluded_chats is None:
        excluded_chats = []
    
    # Get the user's ID to filter messages sent by the user
    me = await client.get_me()
    my_id = me.id
    
    # Open CSV file for writing
    with open('all_messages.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Chat Name', 'Message ID', 'Sender ID', 'Date', 'Message'])

        # Iterate over all chats
        async for dialog in client.iter_dialogs():
            chat_name = dialog.name
            if chat_name in excluded_chats:
                print(f"Chat '{chat_name}' skipped.")
                continue

            print(f"Getting messages from: {chat_name}")

            # Iterate over messages within the current chat
            async for message in client.iter_messages(dialog.id):
                if message.sender_id == my_id:
                    # Write message data to CSV
                    writer.writerow([
                        chat_name,
                        message.id,
                        message.sender_id,
                        message.date,
                        message.text or ''
                    ])
    
    print("Messages successfully saved to all_messages.csv")

async def main():
    # Run the message saving function with error handling
    try:
        await save_messages_to_csv()
    except Exception as e:
        print(f"An error occurred: {e}")

# Start the client and run the main function
if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
