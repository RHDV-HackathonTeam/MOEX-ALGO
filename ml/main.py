import json
from fuzzywuzzy import fuzz

# set_of_tickers = set()

# for ticker in tickers:
#     set_of_tickers.add(ticker)

json_file_path3 = 'output.json'
json_file_path = 'chats_with_rating.json'
json_file_path2 = 'rbc.json'



def process_json_file(json_input, json_tickers):
    try:
        with open(json_input, 'r', encoding='utf-8') as file:
            data = json.load(file)
        with open(json_tickers, 'r', encoding='utf-8') as file:
            tickers = json.load(file)
            for entry in data:
                # if type( entry['text']) == None:
                #     print('alksdjflkajsf')
                if entry['text'] != None:
                    upper_case_string = entry['text'].upper()
                    for ticker in tickers:
                        if ticker in upper_case_string:
                            print(f"{ticker}: text id{entry['id']}")


    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON в файле {file_path}.")


process_json_file(json_file_path, json_file_path3)





# Пример сравнения двух строк
# string1 = "hello world"
# string2 = "hell world abobalksdjf lalksdjflkasj l;kfja;sldjkf asdfasdf "

# Оценка сходства строк (по умолчанию используется алгоритм Levenshtein)
# similarity_score = fuzz.ratio(string1, string2)

# print(f"Сходство строк: {similarity_score}%")

