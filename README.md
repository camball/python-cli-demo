# Python CLI Demo

Sample project used to demo refactoring a CLI tool for an elegant UX and improved DX and robustness.

See tag `unrefactored` for the bad, original version, and branch `main` for the refactored, improved version.

## Installation

```sh
# Clone
git clone https://github.com/camball/python-cli-demo
cd python-cli-demo/

# Install Globally
pip3 install .
echo "\n\nexport PATH=\"\$PATH:$HOME/Library/Python/3.12/bin\"" >> ~/.zshrc
```

## Usage

```sh
wordinfo define <words>... [--language <language_code>]
wordinfo plural <word>
wordinfo indefinite <noun>
wordinfo ordinal <number>
```

## Notes

Due to an upstream bug in the [Free Dictionary API](https://dictionaryapi.dev), the only language codes that work (when passed to `wordinfo define <word> --language <language code>`) are the following:

- `en`
- `en_US`
- `en_GB`

Technically there are [many other supported languages](https://github.com/meetDeveloper/freeDictionaryAPI/blob/4f274a853dd7a352aa2a349d1b92624ff18a36a8/modules/utils.js#L10-L27), but they don't seem to work.

## Credits

- The wonderful [`inflect`](https://github.com/jaraco/inflect) library
- The [Free Dictionary API](https://dictionaryapi.dev)
