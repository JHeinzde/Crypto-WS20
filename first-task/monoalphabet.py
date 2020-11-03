'''
Author: Jonathan Heinz WS 2020
'''
import re


def read_file():
    with open('./01-3.txt') as f:
        return f.read()


def count_chars(string: str):
    map_count = {}
    for c in string:
        map_count.setdefault(c, 0)
        map_count[c] += 1
    return map_count


def absolute_char_count(chars):
    result = 0
    for char in chars:
        result += char[1]
    return result


def main():
    string = read_file()
    item_set = count_chars(string).items()
    filtered_list = list(filter(lambda x: re.match(r'[A-Z]', x[0]), item_set))
    filtered_list.sort(key=lambda x: x[1], reverse=True)
    abs_count = absolute_char_count(filtered_list)
    print('Frequency table:')
    print('Letter | Frequency (absolute) | Frequency (percentage)')
    for letter in filtered_list:
        print(letter[0] + ' | ' + str(letter[1]) + ' | ' + str(letter[1] / abs_count))

    replacement_table = {
        'T': 'E',
        'X': 'T',
        'D': 'A',
        'F': 'O',
        'K': 'H',
        'J': 'D',
        'G': 'S',
        'I': 'Y',
        'Y': 'I',
        'R': 'C',
        'H': 'R',
        'W': 'P',
        'E': 'L',
        'P': 'B',
        'A': 'U',
        'M': 'W',
        'C': 'G',
        'Q': 'F',
        'U': 'M',
        'O': 'K',
        'S': 'Y',
        'B': 'Z',
        'V': 'V'
    }
    print(string.translate(str.maketrans(replacement_table)))


if __name__ == '__main__':
    main()
