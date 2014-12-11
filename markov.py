from collections import defaultdict
from random import randrange

def choice(weighted_set):
    """Return one random object from a list with weights."""
    total = sum(v for _, v in weighted_set)
    if total <= 0:
        return None
    choice = randrange(total)
    for item, weight in weighted_set:
        choice -= weight
        if choice < 0:
            return item

def get_paragraphs(text):
    paragraph = ""
    for line in text:
        if line.strip() == "":
            if paragraph:
                yield paragraph
            paragraph = ""
        else:
            paragraph += " " + line

def clause_parts(token):
    if "--" in token:
        parts = token.split("--")
        return " -- ".join(parts).split()
    for symbol in ":;!,.":
        if token.endswith(symbol):
            return [token.strip(symbol), symbol]
    return [token]

def simplify(word):
    return word.strip('"')

def tokenize(line):
    for token in line.split():
        for word in clause_parts(token):
            yield simplify(word)

def join(words):
    phrase = ""
    for word in words:
        if word in ":;!,.":
            phrase += word
        else:
            phrase += " " + word
    return phrase

class MarkovChain:
    """Keep a statistical model of input text and produce output on demand.
    """
    def __init__(self, order=3):
        self.order = order
        self.table = defaultdict(lambda: defaultdict(int))

    def process_input(self, source):
        for paragraph in get_paragraphs(text):
            prefix = [None] * self.order
            for word in tokenize(paragraph):
                self.table[tuple(prefix)][word] += 1
                prefix = prefix[1:] + [word]

    def get(self, prefix):
        """Get the next (random) word following the prefix."""
        return choice(self.table[tuple(prefix)].items())

    def output(self, length):
        prefix = [None] * self.order
        result = []
        while len(result) < length:
            word = self.get(prefix)
            if word is None:
                return join(result) + "\n\n" + self.output(length-len(result))
            result.append(word)
            prefix = prefix[1:] + [word]
        return join(result)


mc = MarkovChain(3)

with open("source-text/lovecraft_collected_stories.txt", encoding="utf-8") as text:
    mc.process_input(text)
for i in range(3):
    with open("source-text/thus_spake_zarathustra.txt", encoding="utf-8") as text:
        mc.process_input(text)

print(mc.output(5000))
print()
