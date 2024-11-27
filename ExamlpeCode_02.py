import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
import os
import pandas as pd

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_console()

# Убираю ограничения по количеству строк в таблице
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

bool_isPrint = True # Будут ли печататься сообщения в консоль, во время выполнения алгоритма реферирования
bool_isPrint_ScoreOfWords = True # Будут ли печататься сообщения в консоль, во время выполнения алгоритма реферирования

def Summarize(text, n):
    global bool_isPrint

    if(bool_isPrint): print()
    if(bool_isPrint): print(">- Токенизация текста на предложения")
    # Токенизация текста на предложения
    sentences = sent_tokenize(text)    

    if(bool_isPrint): print(">- Создание таблицы частотности слов в тексте")
    # Создание таблицы частотности слов в тексте
    freq_table = defaultdict(int)
    for sentence in sentences:
        words = word_tokenize(sentence)
        for word in words:
            if word.lower() not in stopwords.words('russian'):
                freq_table[word.lower()] += 1

    if(bool_isPrint): print(">- Присвоение оценки каждому предложению на основе частотности его слов")
    # Присвоение оценки каждому предложению на основе частотности его слов
    sentence_scores = defaultdict(int)
    for sentence in sentences:
        words = word_tokenize(sentence)
        for word in words:
            if word.lower() in freq_table:
                sentence_scores[sentence] += freq_table[word.lower()]
    
    if(bool_isPrint_ScoreOfWords): # Вывожу все предложения, и присвоенные им веса:
        print()
        print("Все предложения, и присвоенные им веса:")
        df = pd.DataFrame.from_dict(sentence_scores, orient='index', columns=['Score'])    
        df = df.sort_values(by='Score', ascending=False)
        print(df)
        print()

    if(bool_isPrint): print(">- Сортировка предложений по оценке и выбор топ n")
    # Сортировка предложений по оценке и выбор топ n
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:n]

    if(bool_isPrint): print(">- Объединение выбранных предложений в краткое содержание")
    # Объединение выбранных предложений в краткое содержание
    summary = ' '.join(summary_sentences)

    return summary

def set_n(text, percentage=5): # Задаю число n как 5% от общего количества предложений в тексте
    sentences = nltk.sent_tokenize(text)
    total_sentences = len(sentences)
    print("Общее количество предложений: " + str(total_sentences))
    n = int(total_sentences * percentage / 100)
    print("Количеств предложений в реферате (5%): " + str(n))
    
    return n

print("Запускаем алгоритм автореферирования ACSI-Matic:")
print()

text = "" # Переменная, в которой хранится полный текст из загруженного файла

# Чтение файла input-text.txt
with open('input-text.txt', 'r', encoding='utf-8') as file:
    text = file.read()

n = set_n(text)

# Реферирование текста
summary = Summarize(text, n)

print()
print("Результат реферирования: ")
print(summary)

# Запись результата в файл outpu-text.txt
with open('outpu-text.txt', 'w') as file:
    file.write(summary)

print()