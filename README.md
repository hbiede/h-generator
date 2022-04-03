[![Test and Lint](https://github.com/hbiede/Ranked-Choice-Voting/actions/workflows/test.yaml/badge.svg)](https://github.com/hbiede/Ranked-Choice-Voting/actions/workflows/test.yaml)
[![codecov](https://codecov.io/gh/hbiede/Ranked-Choice-Voting/graph/badge.svg)](https://codecov.io/gh/hbiede/Ranked-Choice-Voting)
[![Ruby Style Guide](https://img.shields.io/badge/code_style-rubocop-brightgreen.svg)](https://github.com/rubocop/rubocop)

# H-Generator
A script to generate H for a research class

## Usage

```bash
ruby gen_h.rb -g alphabet.txt, -f freqs.txt
```

## Options and Inputs

### Alphabet File

Flag: `-g, --alphabet`

Expected format is a list of words, one per line, all unique, with sufficient range so as to be allow users to type all
possible words (thereby requiring all english characters and the space character)

Example:

```
a
b
c
...
the
ation
st
```

### Frequency File

Flag: `-f, --frequencies`

Expected format is a list of words, space separated from their frequency counts, one per line, in descending order.

Example:
```
THE  12345677
HELLO  134567
EXAMPLE 123342
```

Recommended file: http://norvig.com/google-books-common-words.txt

### Output File

Flag: `-o, --output`

The file to write the result to

### Words to Parse (Optional)

Flag: `-n, --words-to-parse`

The number of words to parse from the frequency file. Defaults to 10000
