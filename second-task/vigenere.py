'''
Author: Jonathan Heinz WS 2020
'''

import re
from functools import reduce
from typing import Dict, List, Tuple

letter_frequencies = {
    'E': 0.1202,
    'T': 0.0910,
    'A': 0.0812,
    'O': 0.0768,
    'I': 0.0731,
    'N': 0.0695,
    'S': 0.0628,
    'R': 0.0602,
    'H': 0.0592,
    'D': 0.0432,
    'L': 0.0398,
    'U': 0.0288,
    'C': 0.0271,
    'M': 0.0261,
    'F': 0.0230,
    'Y': 0.0211,
    'W': 0.0209,
    'G': 0.0203,
    'P': 0.0182,
    'B': 0.0149,
    'V': 0.0111,
    'K': 0.0069,
    'X': 0.0017,
    'Q': 0.0011,
    'J': 0.0010,
    'Z': 0.0007,
}


def read_file() -> str:
    with open('02-1.txt') as f:
        return f.read()


def sanitize_text(string: str) -> str:
    return re.sub(r'\s|\n|,|\.|\-|:|@|\'|[0-9]', '', string)


def tokenize_into_groups(group_size: int, string: str):
    groups = []
    for i in range(0, len(string), group_size):
        if i + group_size < len(string):
            groups.append(string[i:i + group_size])
        else:
            groups.append(string[i:len(string)])
    return groups


def count_frequency_in_cipher_texts(ciphers_text_groups, group_size: int):
    result = [{} for i in range(group_size)]
    for group in ciphers_text_groups:
        for i in range(len(group)):
            result[i].setdefault(group[i], 0)
            result[i][group[i]] += 1
    return result


def get_absolute_count(map_of_letters: Dict[str, int]):
    items = list(map_of_letters.items())
    items = map(lambda x: x[1], items)
    return reduce(lambda x, y: x + y, items)


def map_calc_frequencies(map_of_letters: Dict[str, str], absolute_count_for_map):
    percent = map(lambda x: (x[0], x[1] / absolute_count_for_map), map_of_letters.items())
    percent = map(lambda x: x[1], percent)
    percent = map(lambda x: x * x, percent)
    percent = reduce(lambda x, y: x + y, percent)
    return percent


def shift_cipher_text(offset_a: int, letter_distribution: Dict[str, int]) -> List[Tuple[str, int]]:
    new_letter_distribution = []
    for letter in letter_distribution.items():
        new_letter_distribution.append((shift_letter(letter, offset_a), letter[1]))
    return new_letter_distribution


def shift_letter(letter, offset_a: int):
    ascii_code = ord(letter[0])
    ascii_code = ascii_code - 65  # Normalize to the range of 0, 25
    ascii_code = ascii_code - offset_a  # Subtract offset from the letter number
    ascii_code = ascii_code % 26  # Rectify any possible overflows
    ascii_code = ascii_code + 65  # denormalize to be able to reconvert into a char
    return chr(ascii_code)


def calc_coincidence_index(map_of_letters_items, absolute_count_for_map):
    percent = map(lambda x: (x[0], x[1] / absolute_count_for_map), map_of_letters_items)
    percent = map(lambda x: (letter_frequencies[x[0]], x[1]), percent)
    percent = map(lambda x: x[0] * x[1], percent)
    return reduce(lambda x, y: x + y, percent)


def main():
    string = read_file()
    s_string = sanitize_text(string)
    for i in range(1, 11):
        frequency_count = count_frequency_in_cipher_texts(tokenize_into_groups(i, s_string), i)
        abs_count = get_absolute_count(frequency_count[0])
        print('Possible key length', i)
        print(map_calc_frequencies(frequency_count[0], abs_count))
    ### 6 is the group_number with the closest coincidence index to 0.065 ###
    all_counts = count_frequency_in_cipher_texts(tokenize_into_groups(6, s_string), 6)

    for count in all_counts:
        print('-----')
        for i in range(26):
            shifted_letters = shift_cipher_text(i, count)
            print(chr(i + 65), calc_coincidence_index(shifted_letters, get_absolute_count(count)))
        print('-----')
    # Key is GEHEIM.


if __name__ == '__main__':
    main()

#docker run --rm -it --privileged -u $(id -u):$(id -g) -v `pwd`:/documents asciidoctor/docker-asciidoctor \
#asciidoctor-pdf -a stem -r asciidoctor-mathematical writeup.adoc
