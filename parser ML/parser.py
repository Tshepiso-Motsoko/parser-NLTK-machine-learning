import nltk
from nltk.tokenize import word_tokenize
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S
NP -> N | Det N | Det AdjP N | NP P NP
VP -> V | V NP | V NP PP | V PP | VP Adv | Adv VP
PP -> P NP
AdjP -> Adj | Adj AdjP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)

def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    tokens = word_tokenize(sentence)
    return [token.lower() for token in tokens if any(char.isalpha() for char in token)]

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunks = []

    for subtree in tree.subtrees():
        if subtree.label() == 'NP':
            contains_np = False
            for subsubtree in subtree:
                if isinstance(subsubtree, nltk.Tree) and subsubtree.label() == 'NP':
                    contains_np = True
                    break
            if not contains_np:
                np_chunks.append(subtree)

    return np_chunks

def main():
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()
    else:
        s = input("Sentence: ")

    s = preprocess(s)

    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return

    if not trees:
        print("Could not parse sentence.")
        return

    for tree in trees:
        tree.pretty_print()
        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))

if __name__ == "__main__":
    main()
