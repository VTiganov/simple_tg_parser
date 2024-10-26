import pandas as pd
from collections import Counter
import re


def load_data(file_path="all_messages_all.csv"):
    """Loads data from CSV file."""
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print("Error: File not found. Check the path and try again.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty or corrupted.")
        return None

def group_by_chat_name(file_path="all_messages_all.csv"):
    df = load_data(file_path)
    if df is not None:
        return df.groupby("Chat Name")


def analyze_chat(chat_name, chat_data, num_words):
    """Analyzes the selected chat and outputs word frequency statistics."""

    my_message_count = chat_data.shape[0]

    all_text = " ".join(chat_data["Message"].dropna())
    cleaned_text = re.sub(r"[^\w\s]", "", all_text.lower())

    stop_words = set(["у","и", "в", "на", "с", "что", "это", "как", "я", "а", "не", "по", "да", "ну", "там", "так", "но", "вот", "же", "за", "уже", "для"])
    words = [word for word in cleaned_text.split() if word not in stop_words]

    word_counts = Counter(words)
    total_words = sum(word_counts.values())

    most_common_words = word_counts.most_common(num_words)
    least_common_words = sorted(word_counts.items(), key=lambda x: x[1])[:num_words]

    most_common_percentage = [(word, count, count / total_words * 100) for word, count in most_common_words]
    least_common_percentage = [(word, count, count / total_words * 100) for word, count in least_common_words]

    print(f"\nChat analysis: {chat_name}")
    print(f"Total messages: {my_message_count}")

    if most_common_percentage:
        print(f"Top {num_words} frequently used words and their frequency (%):")
        for word, count, percentage in most_common_percentage:
            print(f"{word}: {count} times ({percentage:.2f}%)")
    else:
        print("Not enough words for analyzing most common words.")

    if least_common_percentage:
        print(f"\nTop {num_words} rarely used words and their frequency (%):")
        for word, count, percentage in least_common_percentage:
            print(f"{word}: {count} times ({percentage:.2f}%)")
    else:
        print("Not enough words for analyzing rarest words.")

def overall_stats(file_path="all_messages_all.csv"):

    df = load_data(file_path)
    if df is None:
        return
    
    total_messages = df.shape[0]
    total_chats = df["Chat Name"].nunique()

    all_text = ' '.join(df["Message"].dropna())
    cleaned_text = re.sub(r"[^\w\s]", "", all_text.lower())

    stop_words = set(["у","и", "в", "на", "с", "что", "это", "как", "я", "а", "не", "по", "да", "ну", "там", "так", "но", "вот", "же", "за", "уже", "для"])
    words = [word for word in cleaned_text.split() if word not in stop_words]

    word_counts = Counter(words)
    total_words = sum(word_counts.values())

    most_common_words = word_counts.most_common(10)  # Top 10 common words
    least_common_words = sorted(word_counts.items(), key=lambda x: x[1])[:10]  # Bottom 10 common words


    # Print overall stats
    print("\nOverall Chat Statistics:")
    print(f"Total number of messages: {total_messages}")
    print(f"Total number of chats: {total_chats}")

    if most_common_words:
        print("\nTop 10 frequently used words across all chats:")
        for word, count in most_common_words:
            print(f"{word}: {count} times ({count / total_words * 100:.2f}%)")
    
    if least_common_words:
        print("\nTop 10 rarely used words across all chats:")
        for word, count in least_common_words:
            print(f"{word}: {count} times ({count / total_words * 100:.2f}%)")



    
def main():
    chats = load_data()
    if chats is None:
        return
    chats_grouped_by_name = group_by_chat_name(file_path="all_messages_all.csv")

    while True:
        print("\nOptions:")
        print("1. Analyze a specific chat")
        print("2. Show overall stats for all chats")
        print("3. Exit")
        
        option = input("\nEnter your choice: ")
        
        if option == "1":
            chat_names = list(chats_grouped_by_name.groups.keys())
            print("Available chats:")
            for idx, chat_name in enumerate(chat_names, start=1):
                print(f"{idx}. {chat_name}")

            try:
                chat_index = int(input("\nEnter the chat number to analyze: ")) - 1
                if 0 <= chat_index < len(chat_names):
                    selected_chat = chat_names[chat_index]
                    chat_data = chats_grouped_by_name.get_group(selected_chat)

                    num_words = int(input("Enter the number of words to display for most and least common words: "))
                    if num_words > 0:
                        analyze_chat(selected_chat, chat_data, num_words)
                    else:
                        print("Error: Number of words must be positive.")
                else:
                    print("Error: Invalid chat number selected.")
            except ValueError:
                print("Error: Please enter valid numbers.")

        elif option == "2":
            overall_stats(file_path="all_messages_all.csv")
        
        elif option == "3":
            print("Exiting the program.")
            break
        
        else:
            print("Error: Invalid option selected.")


if __name__ == "__main__":
    main()
