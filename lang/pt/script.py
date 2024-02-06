import urllib.request
from pathlib import Path
from collections import defaultdict, Counter
from typing import Iterator
import json
from math import floor


def list_of_words(url: str) -> Iterator[str]:
    """Yields words from a file (downloaded from URL).
     Note:
      - assumes line breaks between words
      - ignores words starting with upper-case (proper nouns)
    """
    FILE_PATH = Path("./words.txt").resolve()

    # retrieve file from web if it doesn't exist
    if not FILE_PATH.exists():
        urllib.request.urlretrieve(url, FILE_PATH)

    with FILE_PATH.open("r") as f:
        for line in f:
            if not line[0].isupper():
                yield line.strip()


def int_to_en(num: int) -> str:
    """Given an int32 number, print it in English.
    Source: https://stackoverflow.com/a/32640407
    """
    d = {
        0: "zero",
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "ten",
        11: "eleven",
        12: "twelve",
        13: "thirteen",
        14: "fourteen",
        15: "fifteen",
        16: "sixteen",
        17: "seventeen",
        18: "eighteen",
        19: "nineteen",
        20: "twenty",
        30: "thirty",
        40: "forty",
        50: "fifty",
        60: "sixty",
        70: "seventy",
        80: "eighty",
        90: "ninety",
    }
    assert 0 <= num
    if num < 20:
        return d[num]
    if num < 100:
        if num % 10 == 0:
            return d[num]
        else:
            return d[num // 10 * 10] + d[num % 10]
    raise ValueError("Expected a number below 100")


def write_letter_distribution_json(
    words: defaultdict, multiplayer: bool, output_folder: Path
) -> None:
    """Letter distributions follows the distribution of letters over all words."""
    NUM_TILES = 144 if multiplayer else 72

    letter_counter = Counter()
    num_words, num_letters = 0, 0
    for length, words in words.items():
        num_words += len(words)
        num_letters += length * len(words)
        for word in words:
            letter_counter.update(word)

    filename = "tilesMultiplayer.json" if multiplayer else "tilesSinglePlayer.json"
    count = {
        k.upper(): max(2, floor(letter_counter[k] / num_letters * NUM_TILES))
        for k in sorted(letter_counter.keys())
    }
    with (output_folder / filename).open("w") as file:
        json.dump(count, file)


def generate_json(url: str, output_folder: Path) -> None:
    output_folder = Path(output_folder)
    output_folder_words = output_folder / "words"
    output_folder_words.mkdir(exist_ok=True, parents=True)

    # index words by length, and count letters
    words_by_size = defaultdict(list)
    for word in list_of_words(url=url):
        if (length := len(word)) > 1:
            words_by_size[length].append(word)

    # create a word JSON file per number of letters
    for length, words in words_by_size.items():
        output_file_path = output_folder_words / f"{int_to_en(length)}LetterWords.json"
        with output_file_path.open("w") as file:
            json.dump(words, file)

    # create letter distribution JSON
    write_letter_distribution_json(
        words=words_by_size, multiplayer=True, output_folder=output_folder
    )
    write_letter_distribution_json(
        words=words_by_size, multiplayer=False, output_folder=output_folder
    )


if __name__ == "__main__":
    # ASCII Brazilian-Portuguese words without diacritics
    WORDS_URL = "https://www.ime.usp.br/~pf/dicios/br-sem-acentos.txt"
    generate_json(WORDS_URL, Path("."))
