from z3 import Or

# ***************************************
# Design principles as hard constraints
# ***************************************

# Multi-character chords shold be made up of combination of single character chords
# -This is taken from TabSpace philosophy: https://rhodesmill.org/brandon/projects/tabspace-guide.pdf
def mcc_from_scc(s, n, b):
    for i in range(n.alphabet_size, len(n.grams)):
        assert len(n.grams[i]) > 1
        # Either
        #   n_gram must be union of letters that make up the n_gram
        # Or
        #   n_gram must have null assignment.
        if len(n.grams[i]) == 2:
            s.add(Or(b.G[n.index[n.grams[i][0]]] | b.G[n.index[n.grams[i][1]]] == b.G[i], b.G[i] == 0))
        elif len(n.grams[i]) == 3:
            s.add(Or(b.G[n.index[n.grams[i][0]]] | b.G[n.index[n.grams[i][1]]] |
                b.G[n.index[n.grams[i][2]]] == b.G[i], b.G[i] == 0))
        elif len(n.grams[i]) == 4:
            s.add(Or(b.G[n.index[n.grams[i][0]]] | b.G[n.index[n.grams[i][1]]] |
                b.G[n.index[n.grams[i][2]]] | b.G[n.index[n.grams[i][3]]] == b.G[i], b.G[i] == 0))
        elif len(n.grams[i]) == 5:
            s.add(Or(b.G[n.index[n.grams[i][0]]] | b.G[n.index[n.grams[i][1]]] |
                b.G[n.index[n.grams[i][2]]] | b.G[n.index[n.grams[i][3]]] |
                b.G[n.index[n.grams[i][4]]] == b.G[i], b.G[i] == 0))

