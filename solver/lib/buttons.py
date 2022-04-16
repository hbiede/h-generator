from z3 import *
from dataclasses import dataclass, field
import lib

@dataclass
class Buttons:
    total_cost: ArithRef
    G: list = field(default_factory=lambda: [])
    G_D: list = field(default_factory=lambda: [])

def reserve_chords_for_numbers_and_symbols(G, s, n, p):
    # Reserve chords for numbers and symbols. Choose either Index or Pinky constraints:
    if p.reserved_finger == "index":
        # Index Constraint - Forbid use of L or R by the index finger.
        s.add([ Extract(11, 11, G[i]) == 0  for i in range(len(n.G)) ]) # Index L
        s.add([ Extract(9 , 9 , G[i]) == 0  for i in range(len(n.G)) ]) # Index R
    
    elif p.reserved_finger == "pinky":
        # Pinky Constraint - Forbid use of L or R by the pinky finger.
        s.add([ Extract(2 , 2 , G[i]) == 0  for i in range(len(n.G)) ]) # Pinky L
        s.add([ Extract(0 , 0 , G[i]) == 0  for i in range(len(n.G)) ]) # Pinky R

    else:
        print(f"reserved_finger must be set to either \"pinky\" or \"index\", but was set to: {p.reserved_finger}")
        assert 2 + 2 == 5

def one_button_per_finger(G, s, n):
    # For any finger the combination (LR) or (LMR) is illegal,
    #   because it is too hard to do in practice.
    # And
    # We reserve chords with (LM) or (MR) for user-defined chords.
    s.add([ Not(And(Extract(11, 11, G[i]) == 1, Extract(10, 10, G[i]) == 1))  for i in range(len(n.G)) ]) # index_con
    s.add([ Not(And(Extract(11, 11, G[i]) == 1, Extract(9 , 9 , G[i]) == 1))  for i in range(len(n.G)) ])
    s.add([ Not(And(Extract(10, 10, G[i]) == 1, Extract(9 , 9 , G[i]) == 1))  for i in range(len(n.G)) ])
    s.add([ Not(And(Extract(8 , 8 , G[i]) == 1, Extract(7 , 7 , G[i]) == 1))  for i in range(len(n.G)) ]) # middle_con
    s.add([ Not(And(Extract(8 , 8 , G[i]) == 1, Extract(6 , 6 , G[i]) == 1))  for i in range(len(n.G)) ])
    s.add([ Not(And(Extract(7 , 7 , G[i]) == 1, Extract(6 , 6 , G[i]) == 1))  for i in range(len(n.G)) ])
    s.add([ Not(And(Extract(5 , 5 , G[i]) == 1, Extract(4 , 4 , G[i]) == 1))  for i in range(len(n.G)) ]) # ring_con
    s.add([ Not(And(Extract(5 , 5 , G[i]) == 1, Extract(3 , 3 , G[i]) == 1))  for i in range(len(n.G)) ])
    s.add([ Not(And(Extract(4 , 4 , G[i]) == 1, Extract(3 , 3 , G[i]) == 1))  for i in range(len(n.G)) ])
    s.add([ Not(And(Extract(2 , 2 , G[i]) == 1, Extract(1 , 1 , G[i]) == 1))  for i in range(len(n.G)) ]) # pinky_con
    s.add([ Not(And(Extract(2 , 2 , G[i]) == 1, Extract(0 , 0 , G[i]) == 1))  for i in range(len(n.G)) ])
    s.add([ Not(And(Extract(1 , 1 , G[i]) == 1, Extract(0 , 0 , G[i]) == 1))  for i in range(len(n.G)) ])

def all_diff(G, s, n):
    # No two strings can have the same combo
    s.add( Distinct( [G[i] for i in range(len(n.G)) ] ))
    # for i in range(len(n.G) - 1):
    #     s.add( [ G[i] != G[j] for j in range(i + 1, len(n.G)) ] )

def no_null(G, s, n):
    # Every string must be assigned to a chord.
    s.add( [ G[i] != 0 for i in range(len(n.G)) ] )

def finger_bit_vector_act_as_triplets(G_D, s, n):
    # If a finger is used then the entire triplet of bits is 1, else entire triplet is 0.
    s.add([ Extract(11, 11, G_D[i]) == Extract(10, 10, G_D[i])  for i in range(len(n.G)) ]) # index_con
    s.add([ Extract(11, 11, G_D[i]) == Extract(9 , 9 , G_D[i])  for i in range(len(n.G)) ])
    s.add([ Extract(8,  8,  G_D[i]) == Extract(7,  7,  G_D[i])  for i in range(len(n.G)) ]) # middle_con
    s.add([ Extract(8,  8,  G_D[i]) == Extract(6,  6,  G_D[i])  for i in range(len(n.G)) ])
    s.add([ Extract(5,  5,  G_D[i]) == Extract(4,  4,  G_D[i])  for i in range(len(n.G)) ]) # ring_con
    s.add([ Extract(5,  5,  G_D[i]) == Extract(3,  3,  G_D[i])  for i in range(len(n.G)) ])
    s.add([ Extract(2,  2,  G_D[i]) == Extract(1,  1,  G_D[i])  for i in range(len(n.G)) ]) # pinky_con
    s.add([ Extract(2,  2,  G_D[i]) == Extract(0,  0,  G_D[i])  for i in range(len(n.G)) ])

def finger_used_when_single_button_on_finger_used(G_D, G, s, n):
    # If a single button from that finger is used then the finger is used.
    s.add([ Or(
                And(    Extract(9, 9, G_D[i]) == 1,       Or(Extract(11, 11, G[i]) == 1, Extract(10, 10, G[i]) == 1, Extract(9, 9, G[i]) == 1)),
                And(Not(Extract(9, 9, G_D[i]) == 1),  Not(Or(Extract(11, 11, G[i]) == 1, Extract(10, 10, G[i]) == 1, Extract(9, 9, G[i]) == 1))),
            )  for i in range(len(n.G)) ]) # index_con
    s.add([ Or(
                And(    Extract(6, 6, G_D[i]) == 1,       Or(Extract(8,  8,  G[i]) == 1, Extract(7,  7,  G[i]) == 1, Extract(6, 6, G[i]) == 1)),
                And(Not(Extract(6, 6, G_D[i]) == 1),  Not(Or(Extract(8,  8,  G[i]) == 1, Extract(7,  7,  G[i]) == 1, Extract(6, 6, G[i]) == 1))),
            )  for i in range(len(n.G)) ]) # middle_con
    s.add([ Or(
                And(    Extract(3, 3, G_D[i]) == 1,       Or(Extract(5,  5,  G[i]) == 1, Extract(4,  4,  G[i]) == 1, Extract(3, 3, G[i]) == 1)),
                And(Not(Extract(3, 3, G_D[i]) == 1),  Not(Or(Extract(5,  5,  G[i]) == 1, Extract(4,  4,  G[i]) == 1, Extract(3, 3, G[i]) == 1))),
            )  for i in range(len(n.G)) ]) # ring_con
    s.add([ Or(
                And(    Extract(0, 0, G_D[i]) == 1,       Or(Extract(2,  2,  G[i]) == 1, Extract(1,  1,  G[i]) == 1, Extract(0, 0, G[i]) == 1)),
                And(Not(Extract(0, 0, G_D[i]) == 1),  Not(Or(Extract(2,  2,  G[i]) == 1, Extract(1,  1,  G[i]) == 1, Extract(0, 0, G[i]) == 1))),
            )  for i in range(len(n.G)) ]) # pinky_con


def chord_cost(raw_G_cost, G, s, n):
    # **********************************************
    # Cost constraints
    #  - Estimate and minimize cost of configuration 
    # **********************************************
    for i in range(len(n.G)):
        s.add( Or(raw_G_cost[i] == 5381, raw_G_cost[i] == 6741, raw_G_cost[i] == 9772, raw_G_cost[i] == 4651, raw_G_cost[i] == 7889, raw_G_cost[i] == 5940, raw_G_cost[i] == 8771, raw_G_cost[i] == 5370, raw_G_cost[i] == 8068, raw_G_cost[i] == 9769, raw_G_cost[i] == 11114, raw_G_cost[i] == 7875, raw_G_cost[i] == 9231, raw_G_cost[i] == 8768, raw_G_cost[i] == 10113, raw_G_cost[i] == 4705, raw_G_cost[i] == 7902, raw_G_cost[i] == 9603, raw_G_cost[i] == 10948, raw_G_cost[i] == 7045, raw_G_cost[i] == 9065, raw_G_cost[i] == 8602, raw_G_cost[i] == 9947, raw_G_cost[i] == 5217, raw_G_cost[i] == 8030, raw_G_cost[i] == 9731, raw_G_cost[i] == 11076, raw_G_cost[i] == 7684, raw_G_cost[i] == 9193, raw_G_cost[i] == 8730, raw_G_cost[i] == 10075, raw_G_cost[i] == 5267, raw_G_cost[i] == 8043, raw_G_cost[i] == 9743, raw_G_cost[i] == 11089, raw_G_cost[i] == 7747, raw_G_cost[i] == 9206, raw_G_cost[i] == 8742, raw_G_cost[i] == 10087, raw_G_cost[i] == 8029, raw_G_cost[i] == 9385, raw_G_cost[i] == 11086, raw_G_cost[i] == 12431, raw_G_cost[i] == 9192, raw_G_cost[i] == 10548, raw_G_cost[i] == 10085, raw_G_cost[i] == 11430, raw_G_cost[i] == 7760, raw_G_cost[i] == 9219, raw_G_cost[i] == 10920, raw_G_cost[i] == 12265, raw_G_cost[i] == 8923, raw_G_cost[i] == 10382, raw_G_cost[i] == 9919, raw_G_cost[i] == 11264, raw_G_cost[i] == 7888, raw_G_cost[i] == 9347, raw_G_cost[i] == 11048, raw_G_cost[i] == 12393, raw_G_cost[i] == 9051, raw_G_cost[i] == 10510, raw_G_cost[i] == 10046, raw_G_cost[i] == 11392, raw_G_cost[i] == 4528, raw_G_cost[i] == 7858, raw_G_cost[i] == 9559, raw_G_cost[i] == 10904, raw_G_cost[i] == 6946, raw_G_cost[i] == 9021, raw_G_cost[i] == 8557, raw_G_cost[i] == 9903, raw_G_cost[i] == 7844, raw_G_cost[i] == 9201, raw_G_cost[i] == 10901, raw_G_cost[i] == 12246, raw_G_cost[i] == 9007, raw_G_cost[i] == 10363, raw_G_cost[i] == 9900, raw_G_cost[i] == 11245, raw_G_cost[i] == 7014, raw_G_cost[i] == 9035, raw_G_cost[i] == 10735, raw_G_cost[i] == 12080, raw_G_cost[i] == 8177, raw_G_cost[i] == 10197, raw_G_cost[i] == 9734, raw_G_cost[i] == 11079, raw_G_cost[i] == 7653, raw_G_cost[i] == 9162, raw_G_cost[i] == 10863, raw_G_cost[i] == 12208, raw_G_cost[i] == 8816, raw_G_cost[i] == 10325, raw_G_cost[i] == 9862, raw_G_cost[i] == 11207, raw_G_cost[i] == 5607, raw_G_cost[i] == 8354, raw_G_cost[i] == 9828, raw_G_cost[i] == 11174, raw_G_cost[i] == 8172, raw_G_cost[i] == 9517, raw_G_cost[i] == 8827, raw_G_cost[i] == 10172, raw_G_cost[i] == 8351, raw_G_cost[i] == 9697, raw_G_cost[i] == 11171, raw_G_cost[i] == 12516, raw_G_cost[i] == 9514, raw_G_cost[i] == 10859, raw_G_cost[i] == 10170, raw_G_cost[i] == 11515, raw_G_cost[i] == 8185, raw_G_cost[i] == 9531, raw_G_cost[i] == 11005, raw_G_cost[i] == 12350, raw_G_cost[i] == 9348, raw_G_cost[i] == 10693, raw_G_cost[i] == 10004, raw_G_cost[i] == 11349, raw_G_cost[i] == 8313, raw_G_cost[i] == 9658, raw_G_cost[i] == 11133, raw_G_cost[i] == 12478, raw_G_cost[i] == 9476, raw_G_cost[i] == 10821, raw_G_cost[i] == 10131, raw_G_cost[i] == 11477))
        s.add( Or( Not( G[i] == 2),    raw_G_cost[i] == 5381))
        s.add( Or( Not( G[i] == 8),    raw_G_cost[i] == 6741))
        s.add( Or( Not( G[i] == 10),   raw_G_cost[i] == 9772))
        s.add( Or( Not( G[i] == 16),   raw_G_cost[i] == 4651))
        s.add( Or( Not( G[i] == 18),   raw_G_cost[i] == 7889))
        s.add( Or( Not( G[i] == 32),   raw_G_cost[i] == 5940))
        s.add( Or( Not( G[i] == 34),   raw_G_cost[i] == 8771))
        s.add( Or( Not( G[i] == 64),   raw_G_cost[i] == 5370))
        s.add( Or( Not( G[i] == 66),   raw_G_cost[i] == 8068))
        s.add( Or( Not( G[i] == 72),   raw_G_cost[i] == 9769))
        s.add( Or( Not( G[i] == 74),   raw_G_cost[i] == 11114))
        s.add( Or( Not( G[i] == 80),   raw_G_cost[i] == 7875))
        s.add( Or( Not( G[i] == 82),   raw_G_cost[i] == 9231))
        s.add( Or( Not( G[i] == 96),   raw_G_cost[i] == 8768))
        s.add( Or( Not( G[i] == 98),   raw_G_cost[i] == 10113))
        s.add( Or( Not( G[i] == 128),  raw_G_cost[i] == 4705))
        s.add( Or( Not( G[i] == 130),  raw_G_cost[i] == 7902))
        s.add( Or( Not( G[i] == 136),  raw_G_cost[i] == 9603))
        s.add( Or( Not( G[i] == 138),  raw_G_cost[i] == 10948))
        s.add( Or( Not( G[i] == 144),  raw_G_cost[i] == 7045))
        s.add( Or( Not( G[i] == 146),  raw_G_cost[i] == 9065))
        s.add( Or( Not( G[i] == 160),  raw_G_cost[i] == 8602))
        s.add( Or( Not( G[i] == 162),  raw_G_cost[i] == 9947))
        s.add( Or( Not( G[i] == 256),  raw_G_cost[i] == 5217))
        s.add( Or( Not( G[i] == 258),  raw_G_cost[i] == 8030))
        s.add( Or( Not( G[i] == 264),  raw_G_cost[i] == 9731))
        s.add( Or( Not( G[i] == 266),  raw_G_cost[i] == 11076))
        s.add( Or( Not( G[i] == 272),  raw_G_cost[i] == 7684))
        s.add( Or( Not( G[i] == 274),  raw_G_cost[i] == 9193))
        s.add( Or( Not( G[i] == 288),  raw_G_cost[i] == 8730))
        s.add( Or( Not( G[i] == 290),  raw_G_cost[i] == 10075))
        s.add( Or( Not( G[i] == 512),  raw_G_cost[i] == 5267))
        s.add( Or( Not( G[i] == 514),  raw_G_cost[i] == 8043))
        s.add( Or( Not( G[i] == 520),  raw_G_cost[i] == 9743))
        s.add( Or( Not( G[i] == 522),  raw_G_cost[i] == 11089))
        s.add( Or( Not( G[i] == 528),  raw_G_cost[i] == 7747))
        s.add( Or( Not( G[i] == 530),  raw_G_cost[i] == 9206))
        s.add( Or( Not( G[i] == 544),  raw_G_cost[i] == 8742))
        s.add( Or( Not( G[i] == 546),  raw_G_cost[i] == 10087))
        s.add( Or( Not( G[i] == 576),  raw_G_cost[i] == 8029))
        s.add( Or( Not( G[i] == 578),  raw_G_cost[i] == 9385))
        s.add( Or( Not( G[i] == 584),  raw_G_cost[i] == 11086))
        s.add( Or( Not( G[i] == 586),  raw_G_cost[i] == 12431))
        s.add( Or( Not( G[i] == 592),  raw_G_cost[i] == 9192))
        s.add( Or( Not( G[i] == 594),  raw_G_cost[i] == 10548))
        s.add( Or( Not( G[i] == 608),  raw_G_cost[i] == 10085))
        s.add( Or( Not( G[i] == 610),  raw_G_cost[i] == 11430))
        s.add( Or( Not( G[i] == 640),  raw_G_cost[i] == 7760))
        s.add( Or( Not( G[i] == 642),  raw_G_cost[i] == 9219))
        s.add( Or( Not( G[i] == 648),  raw_G_cost[i] == 10920))
        s.add( Or( Not( G[i] == 650),  raw_G_cost[i] == 12265))
        s.add( Or( Not( G[i] == 656),  raw_G_cost[i] == 8923))
        s.add( Or( Not( G[i] == 658),  raw_G_cost[i] == 10382))
        s.add( Or( Not( G[i] == 672),  raw_G_cost[i] == 9919))
        s.add( Or( Not( G[i] == 674),  raw_G_cost[i] == 11264))
        s.add( Or( Not( G[i] == 768),  raw_G_cost[i] == 7888))
        s.add( Or( Not( G[i] == 770),  raw_G_cost[i] == 9347))
        s.add( Or( Not( G[i] == 776),  raw_G_cost[i] == 11048))
        s.add( Or( Not( G[i] == 778),  raw_G_cost[i] == 12393))
        s.add( Or( Not( G[i] == 784),  raw_G_cost[i] == 9051))
        s.add( Or( Not( G[i] == 786),  raw_G_cost[i] == 10510))
        s.add( Or( Not( G[i] == 800),  raw_G_cost[i] == 10046))
        s.add( Or( Not( G[i] == 802),  raw_G_cost[i] == 11392))
        s.add( Or( Not( G[i] == 1024), raw_G_cost[i] == 4528))
        s.add( Or( Not( G[i] == 1026), raw_G_cost[i] == 7858))
        s.add( Or( Not( G[i] == 1032), raw_G_cost[i] == 9559))
        s.add( Or( Not( G[i] == 1034), raw_G_cost[i] == 10904))
        s.add( Or( Not( G[i] == 1040), raw_G_cost[i] == 6946))
        s.add( Or( Not( G[i] == 1042), raw_G_cost[i] == 9021))
        s.add( Or( Not( G[i] == 1056), raw_G_cost[i] == 8557))
        s.add( Or( Not( G[i] == 1058), raw_G_cost[i] == 9903))
        s.add( Or( Not( G[i] == 1088), raw_G_cost[i] == 7844))
        s.add( Or( Not( G[i] == 1090), raw_G_cost[i] == 9201))
        s.add( Or( Not( G[i] == 1096), raw_G_cost[i] == 10901))
        s.add( Or( Not( G[i] == 1098), raw_G_cost[i] == 12246))
        s.add( Or( Not( G[i] == 1104), raw_G_cost[i] == 9007))
        s.add( Or( Not( G[i] == 1106), raw_G_cost[i] == 10363))
        s.add( Or( Not( G[i] == 1120), raw_G_cost[i] == 9900))
        s.add( Or( Not( G[i] == 1122), raw_G_cost[i] == 11245))
        s.add( Or( Not( G[i] == 1152), raw_G_cost[i] == 7014))
        s.add( Or( Not( G[i] == 1154), raw_G_cost[i] == 9035))
        s.add( Or( Not( G[i] == 1160), raw_G_cost[i] == 10735))
        s.add( Or( Not( G[i] == 1162), raw_G_cost[i] == 12080))
        s.add( Or( Not( G[i] == 1168), raw_G_cost[i] == 8177))
        s.add( Or( Not( G[i] == 1170), raw_G_cost[i] == 10197))
        s.add( Or( Not( G[i] == 1184), raw_G_cost[i] == 9734))
        s.add( Or( Not( G[i] == 1186), raw_G_cost[i] == 11079))
        s.add( Or( Not( G[i] == 1280), raw_G_cost[i] == 7653))
        s.add( Or( Not( G[i] == 1282), raw_G_cost[i] == 9162))
        s.add( Or( Not( G[i] == 1288), raw_G_cost[i] == 10863))
        s.add( Or( Not( G[i] == 1290), raw_G_cost[i] == 12208))
        s.add( Or( Not( G[i] == 1296), raw_G_cost[i] == 8816))
        s.add( Or( Not( G[i] == 1298), raw_G_cost[i] == 10325))
        s.add( Or( Not( G[i] == 1312), raw_G_cost[i] == 9862))
        s.add( Or( Not( G[i] == 1314), raw_G_cost[i] == 11207))
        s.add( Or( Not( G[i] == 2048), raw_G_cost[i] == 5607))
        s.add( Or( Not( G[i] == 2050), raw_G_cost[i] == 8354))
        s.add( Or( Not( G[i] == 2056), raw_G_cost[i] == 9828))
        s.add( Or( Not( G[i] == 2058), raw_G_cost[i] == 11174))
        s.add( Or( Not( G[i] == 2064), raw_G_cost[i] == 8172))
        s.add( Or( Not( G[i] == 2066), raw_G_cost[i] == 9517))
        s.add( Or( Not( G[i] == 2080), raw_G_cost[i] == 8827))
        s.add( Or( Not( G[i] == 2082), raw_G_cost[i] == 10172))
        s.add( Or( Not( G[i] == 2112), raw_G_cost[i] == 8351))
        s.add( Or( Not( G[i] == 2114), raw_G_cost[i] == 9697))
        s.add( Or( Not( G[i] == 2120), raw_G_cost[i] == 11171))
        s.add( Or( Not( G[i] == 2122), raw_G_cost[i] == 12516))
        s.add( Or( Not( G[i] == 2128), raw_G_cost[i] == 9514))
        s.add( Or( Not( G[i] == 2130), raw_G_cost[i] == 10859))
        s.add( Or( Not( G[i] == 2144), raw_G_cost[i] == 10170))
        s.add( Or( Not( G[i] == 2146), raw_G_cost[i] == 11515))
        s.add( Or( Not( G[i] == 2176), raw_G_cost[i] == 8185))
        s.add( Or( Not( G[i] == 2178), raw_G_cost[i] == 9531))
        s.add( Or( Not( G[i] == 2184), raw_G_cost[i] == 11005))
        s.add( Or( Not( G[i] == 2186), raw_G_cost[i] == 12350))
        s.add( Or( Not( G[i] == 2192), raw_G_cost[i] == 9348))
        s.add( Or( Not( G[i] == 2194), raw_G_cost[i] == 10693))
        s.add( Or( Not( G[i] == 2208), raw_G_cost[i] == 10004))
        s.add( Or( Not( G[i] == 2210), raw_G_cost[i] == 11349))
        s.add( Or( Not( G[i] == 2304), raw_G_cost[i] == 8313))
        s.add( Or( Not( G[i] == 2306), raw_G_cost[i] == 9658))
        s.add( Or( Not( G[i] == 2312), raw_G_cost[i] == 11133))
        s.add( Or( Not( G[i] == 2314), raw_G_cost[i] == 12478))
        s.add( Or( Not( G[i] == 2320), raw_G_cost[i] == 9476))
        s.add( Or( Not( G[i] == 2322), raw_G_cost[i] == 10821))
        s.add( Or( Not( G[i] == 2336), raw_G_cost[i] == 10131))
        s.add( Or( Not( G[i] == 2338), raw_G_cost[i] == 11477))

def stride_stutter_count(G_count, G, G_D, s, n, p):
    identical_found = False
    for g_index in range(len(n.G)):
        discounted_H_freq = []
        for h_index in range(len(n.H)):
            if n.G[g_index] == n.H2[h_index]:
                g_index_of_h1 = n.G_index[n.H1[h_index]]
                g_index_of_h2 = n.G_index[n.H2[h_index]]

                if g_index_of_h1 == g_index_of_h2: # Identical strings are always in stride.
                    assert n.H1[h_index] == n.H2[h_index]
                    identical_found = True
                    discounted_H_freq.append( int( p.stride * n.HF[h_index]) )
                else:
                    assert n.H1[h_index] != n.H2[h_index]
                    discounted_H_freq.append(
                        If(G_D[g_index_of_h1] & G_D[g_index_of_h2] == 0, int( p.stride * n.HF[h_index]), # Stride discount
                        If(G_D[g_index_of_h1] & G[g_index_of_h2] == G[g_index_of_h1] & G_D[g_index_of_h2], int( p.stutter * n.HF[h_index]), # Stutter discount
                        n.HF[h_index])))
        
        s.add( G_count[g_index] == Sum( discounted_H_freq ) )

    assert identical_found # We expect that this should happen at least once.

def stride_stutter_discount(raw_H2_cost, discounted_H_cost, G, G_D, s, n, p):
    identical_found = False
    for i in range(len(n.H)):
        h1_index = n.G_index[n.H1[i]]
        h2_index = n.G_index[n.H2[i]]
        if h1_index == h2_index: # Identical strings are always in stride.
            assert n.H1[i] == n.H2[i]
            identical_found = True
            s.add (discounted_H_cost[i] == p.stride * raw_H2_cost[i] * n.HF[i])
        else:
            assert n.H1[i] != n.H2[i]
            s.add( discounted_H_cost[i] == \
                If(G_D[h1_index] & G_D[h2_index] == 0, p.stride, # Stride discount
                If(G_D[h1_index] & G[h2_index] == G[h1_index] & G_D[h2_index], p.stutter, # Stutter discount
                1.0)) * # No stride or stutter discount
                raw_H2_cost[i] * n.HF[i]
            )
    assert identical_found # We expect that this should happen at least once.

def combine_chord_cost_with_count(total_cost, G_count, raw_G_cost, s, n):

    s.add( total_cost == Sum( [ G_count[i] * raw_G_cost[i] for i in range(len(n.G)) ] ) )

# ***************************************
# Problem Definition and hard constraints
#  -Hard constraints cannot be violated
# ***************************************
def problem_def(s, n, p):
    # Let the bit-vector represent a button combo with this correspondance:
    # Index(LMR) Middle(LMR) Ring(LMR) Pinky(LMR)
    #       000         000       000        000
    G = [ BitVec('g%s' % i, 12) for i in range(len(n.G))]
    reserve_chords_for_numbers_and_symbols(G, s, n, p)
    one_button_per_finger(G, s, n)
    all_diff(G, s, n)
    no_null(G, s, n)

    # Let the bit-vector represent finger use with this correspondance:
    # Index(---) Middle(---) Ring(---) Pinky(---)
    #       000         000       000        000
    G_D = [ BitVec('f%s' % i, 12) for i in range(len(n.G))]
    finger_bit_vector_act_as_triplets(G_D, s, n)
    finger_used_when_single_button_on_finger_used(G_D, G, s, n)

    # The raw cost of pressing each g.
    raw_G_cost = [ Int('rc%s' % i) for i in range(len(n.G)) ]
    all_diff(raw_G_cost, s, n)
    chord_cost(raw_G_cost, G, s, n)

    G_count = [ Int('g_cnt%s' % i) for i in range(len(n.G)) ]
    stride_stutter_count(G_count, G, G_D, s, n, p)

    total_cost = Int('total_cost')
    combine_chord_cost_with_count(total_cost, G_count, raw_G_cost, s, n)

    return Buttons(total_cost=total_cost, G=G, G_D=G_D)
