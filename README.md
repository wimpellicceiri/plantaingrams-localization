# plantaingrams-localization
Support for other languages within https://plantaingrams.app

## Contributing
You may contribute your own language and I will attempt to integrate the language into https://plantaingrams.app

### Step 1 - Add language code folder, if necessary
If it does not exist already, add a folder beneath `lang` to indicate the language code you are supporting.

### Step 2 - Add valid words
Within the appropriate language code folder, e.g. `en`, add a `words` folder with json files that include an array containing valid words. The name of the file does not matter, but I would prefer to use the same structure that `en` uses so that the words are organized and distributed (better for caching).

### Step 3 - Add valid tile counts
Also within the appropriate language code folder, e.g. `en`, add two files representing the tile count for single player games and multiplayer games. This should be a JSON object with a letter and corresponding count for that letter.

#### NOTE
There is a Python script that is available to help with generating the words located [here](lang/pt/script.py). Thank you to @eduardohenriquearnold for contributing this.
