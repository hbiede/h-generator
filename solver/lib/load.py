from dataclasses import dataclass, field
import lib

# Load strings to assign to chords.
def load_G(G_file):
    G_size = 0
    G = list()
    with open(G_file) as f:
        for line in f:
            # Remove trailing newline.
            # Must be sure to not remove intentional white space.
            line = line[:-1]
            G.append(line)
            G_size += 1
    return G, G_size

# Load strings and frequencies used to calculate costs:
def load_H(H_file , sep=','):
    H_size = 0
    H = list()
    H1 = list()
    H2 = list()
    HF = list()
    with open(H_file) as f:
        for line in f:
            str, sub_str_1, sub_str_2, freq = line.split(sep)
            freq = int(freq)
            H.append(str)
            H1.append(sub_str_1)
            H2.append(sub_str_2)
            HF.append(freq)
            H_size += 1
    return H, H1, H2, HF, H_size

def create_dict(my_list):
    # We create a dictionary to quickly lookup the index of all my_list
    index = {}
    for i in range(len(my_list)):
        index[my_list[i]] = i
    return index

@dataclass
class NGrams:
    G_size: int = 0
    G: list = field(default_factory=lambda: [])
    G_index: dict = field(default_factory=lambda : {})
    H_size: int = 0
    H: list = field(default_factory=lambda: [])
    H1: list = field(default_factory=lambda: [])
    H2: list = field(default_factory=lambda: [])
    HF: list = field(default_factory=lambda: [])
    H_index: dict = field(default_factory=lambda : {})

    def load_G_H(p):
        G, G_size = load_G(p.G_file)
        G_index = create_dict(G)
        assert len(G) == G_size
        H, H1, H2, HF, H_size = load_H(p.H_file)
        H_index = create_dict(H)
        assert len(H) == len(H1) == len(H2) == len(HF) == H_size

        return NGrams(G_size = G_size, G = G, G_index = G_index, H_size = H_size, H = H, H1 = H1, H2 = H2, HF = HF, H_index = H_index)