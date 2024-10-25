import pandas as pd
from collections import Counter
import re
import os
os.environ['TCL_LIBRARY'] = r'C:\Users\Admin\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Admin\AppData\Local\Programs\Python\Python313\tcl\tk8.6'

# Загружаем данные
df = pd.read_csv('all_messages.csv')

# Группируем данные по чатам
chats = df.groupby('Chat Name')

# Выводим список названий всех чатов
chat_names = list(chats.groups.keys())
print("Доступные чаты:")
for idx, chat_name in enumerate(chat_names, start=1):
    print(f"{idx}. {chat_name}")

# Запрашиваем у пользователя название чата
selected_chat = input("\nВведите название чата для анализа: ")

# Проверяем, существует ли введенный чат
if selected_chat not in chat_names:
    print("Ошибка: выбранный чат не найден. Пожалуйста, проверьте название и попробуйте снова.")
else:
    # Получаем данные для выбранного чата
    chat_data = chats.get_group(selected_chat)
    
    my_message_count = chat_data.shape[0]
    all_text = ' '.join(chat_data['Message'].dropna())
    cleaned_text = re.sub(r'[^\w\s]', '', all_text.lower())

    stop_words = set(['и', 'в', 'на', 'с', 'что', 'это', 'как', 'я', 'а', 'не', 'по', 'да'])
    words = [word for word in cleaned_text.split() if word not in stop_words]
    
    word_counts = Counter(words)
    total_words = sum(word_counts.values())
    
    # Находим 15 самых частых и 15 самых редких слов
    most_common_words = word_counts.most_common(15)
    least_common_words = sorted(word_counts.items(), key=lambda x: x[1])[:15]

    # Рассчитываем процентное соотношение для частых и редких слов
    most_common_percentage = [(word, count, count / total_words * 100) for word, count in most_common_words]
    least_common_percentage = [(word, count, count / total_words * 100) for word, count in least_common_words]

    # Вывод анализа для выбранного чата
    print(f"\nАнализ чата: {selected_chat}")
    print(f"Всего сообщений: {my_message_count}")
    
    # Вывод самых частых слов
    if most_common_percentage:
        print("Топ-15 часто используемых слов и их частота (%):")
        for word, count, percentage in most_common_percentage:
            print(f"{word}: {count} раз ({percentage:.2f}%)")
    else:
        print("Нет достаточного количества слов для анализа самых частых слов.")

    # Вывод самых редких слов
    if least_common_percentage:
        print("\nТоп-15 редко используемых слов и их частота (%):")
        for word, count, percentage in least_common_percentage:
            print(f"{word}: {count} раз ({percentage:.2f}%)")
    else:
        print("Нет достаточного количества слов для анализа самых редких слов.")
