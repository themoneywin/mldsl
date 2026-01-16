import random


def encrypt(text: str, key: int = 1):
    unicodeMax = 55295

    res = ""
    for symold in text:
        symnew = chr((int(ord(symold) )+ int(key)) % unicodeMax)
        res += symnew

    indexes = [ord(i) for i in res]

    srednee = 0

    for num in indexes:
        srednee += num
    srednee = round(srednee/len(indexes))
    print("sred", srednee)

    key_sym = ''
    key_sym_index = srednee + key
    print(key_sym_index)
    if key_sym_index >= unicodeMax:
        key_sym_index = key_sym_index - unicodeMax
        print(ord(key_sym_index))
        key_sym += '`'
    key_sym += chr(key_sym_index)

    res += key_sym

    return res

def decrypt(text: str, key: int = 0):
    unicodeMax = 55295

    key_symbol = text[-1:]
    source_text = text[:-1].replace('`', '')

    indexes = [ord(i) for i in source_text]
    srednee = 0

    for num in indexes:
        srednee += num
    srednee = round(srednee / len(indexes))

    key = ord(key_symbol) - srednee

    if text.__contains__('`'):
        key += unicodeMax

    if key < 0:
        key *= -1

    res = ''
    for sym in source_text:
        res += chr(ord(sym) - key)

    return res

# if __name__ == "__main__":
#     val = "привет! рад тебя видеть\nйооу"#input()
#     key = random.randint(1, 5000)#input()
#     print(encrypt(val, key))

