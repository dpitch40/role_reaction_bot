import requests
import re

URL = 'https://unicode.org/Public/emoji/13.1/emoji-test.txt'
_EMOJI = None
EMOJI_LINE_RE = \
    re.compile(r'^([\dA-F ]+)\s+; (component|fully-qualified|unqualified|minimally-qualified)\s+# ([^ ]+)',
    flags=re.MULTILINE)

def load_emoji():
    global _EMOJI

    if _EMOJI is None:
        resp = requests.get(URL)
        text = resp.text
        emoji = set()
        for m in EMOJI_LINE_RE.finditer(text):
            emoji.add(m.group(3))
        _EMOJI = emoji

    return _EMOJI

def main():
    emoji = load_emoji()
    print(f'{len(emoji)} emoji loaded.')
    print(emoji)

if __name__ == '__main__':
    main()