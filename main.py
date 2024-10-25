import pandas as pd
from collections import Counter
import re
import os

# Setting up environment paths if necessary for your system
os.environ['TCL_LIBRARY'] = r'C:\Users\Admin\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Admin\AppData\Local\Programs\Python\Python313\tcl\tk8.6'


def load_data(file_path='all_messages.csv'):
    """Loads data from CSV file and groups it by chat name."""
    try:
        df = pd.read_csv(file_path)
        return df.groupby('Chat Name')
    except FileNotFoundError:
        print("Error: File not found. Check the path and try again.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty or corrupted.")
        return None


def analyze_chat(chat_name, chat_data):
    """Analyzes the selected chat and outputs word frequency statistics."""
    # Count total messages
    my_message_count = chat_data.shape[0]
    # Combine all messages into a single text string, removing non-word characters and converting to lowercase
    all_text = ' '.join(chat_data['Message'].dropna())
    cleaned_text = re.sub(r'[^\w\s]', '', all_text.lower())

    # Define stop words to exclude from frequency count
    stop_words = set(['и', 'в', 'на', 'с', 'что', 'это', 'как', 'я', 'а', 'не', 'по', 'да'])
    words = [word for word in cleaned_text.split() if word not in stop_words]

    # Count word frequencies
    word_counts = Counter(words)
    total_words = sum(word_counts.values())

    # Find 15 most and least common words
    most_common_words = word_counts.most_common(15)
    least_common_words = sorted(word_counts.items(), key=lambda x: x[1])[:15]

    # Calculate percentage for each common and rare word
    most_common_percentage = [(word, count, count / total_words * 100) for word, count in most_common_words]
    least_common_percentage = [(word, count, count / total_words * 100) for word, count in least_common_words]

    # Output analysis results
    print(f"\nChat analysis: {chat_name}")
    print(f"Total messages: {my_message_count}")

    # Output most common words
    if most_common_percentage:
        print("Top 15 frequently used words and their frequency (%):")
        for word, count, percentage in most_common_percentage:
            print(f"{word}: {count} times ({percentage:.2f}%)")
    else:
        print("Not enough words for analyzing most common words.")

    # Output least common words
    if least_common_percentage:
        print("\nTop 15 rarely used words and their frequency (%):")
        for word, count, percentage in least_common_percentage:
            print(f"{word}: {count} times ({percentage:.2f}%)")
    else:
        print("Not enough words for analyzing rarest words.")


def main():
    # Load chat data
    chats = load_data()
    if chats is None:
        return

    # Display all available chat names
    chat_names = list(chats.groups.keys())
    print("Available chats:")
    for idx, chat_name in enumerate(chat_names, start=1):
        print(f"{idx}. {chat_name}")

    # Prompt user to select a chat
    try:
        chat_index = int(input("\nEnter the chat number to analyze: ")) - 1
        if 0 <= chat_index < len(chat_names):
            selected_chat = chat_names[chat_index]
            chat_data = chats.get_group(selected_chat)
            analyze_chat(selected_chat, chat_data)
        else:
            print("Error: Invalid chat number selected.")
    except ValueError:
        print("Error: Please enter a valid chat number.")


if __name__ == "__main__":
    main()
