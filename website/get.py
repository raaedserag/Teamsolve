import pyperclip
import json

if __name__ == '__main__':
    # index = json.load(open("index.json", "r"))

    problems = json.load(open("problems.json", "r"))
    max = 0
    for i in range(len(problems)):
        if len(problems[i] )> max:
            max = len(problems[i])
    print(max)
    # temp = ""
    # for i in range(3):
    #     temp += "https://codeforces.com/problemset/problem/" + problems[index]
    #     temp += "\n"
    #     index += 1

    # pyperclip.copy(temp)

    # json.dump(index, open("index.json", "w"))