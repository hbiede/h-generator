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

# Generated by impute_forbid.py. Bans chords based on experiment to reduce search space.
def custom_forbid(G, G_D, s, n):
    pass # Setup for G_127 with abstraction
    # for i in range(len(n.G)):
    #     # Forbidden finger combinations
    #     s.add( And( Not(G_D[i] == 4095)))

# Generated by impute_forbid.py. Hardcodes some variables based on the abstraction from the previous run.
def custom_hardcode(G, s, n): # Setup for G_127 with abstraction
    s.add(G[n.G_index[' ']] == 2)
    s.add(G[n.G_index['THE']] == 16)
    s.add(G[n.G_index['Y']] == 256)
    s.add(G[n.G_index['S']] == 64)
    s.add(G[n.G_index['OF']] == 1280)
    s.add(G[n.G_index['E']] == 1024)
    s.add(G[n.G_index['A']] == 2048)
    s.add(G[n.G_index['T']] == 512)
    s.add(G[n.G_index['D']] == 130)
    s.add(G[n.G_index['IN']] == 1040)
    s.add(G[n.G_index['AND']] == 640)
    s.add(G[n.G_index['TO']] == 2064)
    s.add(G[n.G_index['W']] == 1152)
    s.add(G[n.G_index['P']] == 144)
    s.add(G[n.G_index['B']] == 272)
    s.add(G[n.G_index['F']] == 80)
    s.add(G[n.G_index['N']] == 32)
    s.add(G[n.G_index['ING']] == 1042)
    s.add(G[n.G_index['BE']] == 520)
    s.add(G[n.G_index['R']] == 128)
    s.add(G[n.G_index['ED']] == 1056)
    s.add(G[n.G_index['M']] == 258)
    s.add(G[n.G_index['G']] == 1088)
    s.add(G[n.G_index['AL']] == 1032)
    s.add(G[n.G_index['RE']] == 72)
    s.add(G[n.G_index['IS']] == 288)
    s.add(G[n.G_index['I']] == 528)
    s.add(G[n.G_index['NO']] == 136)
    s.add(G[n.G_index['FOR']] == 1296)
    s.add(G[n.G_index['ES']] == 274)
    s.add(G[n.G_index['ON']] == 2112)
    s.add(G[n.G_index['THAT']] == 544)
    s.add(G[n.G_index['L']] == 18)
    s.add(G[n.G_index['IT']] == 2056)
    s.add(G[n.G_index['AS']] == 784)
    s.add(G[n.G_index['LE']] == 1282)
    s.add(G[n.G_index['SE']] == 1104)
    s.add(G[n.G_index['DE']] == 2066)
    s.add(G[n.G_index['ST']] == 264)
    s.add(G[n.G_index['MA']] == 146)
    s.add(G[n.G_index['HA']] == 530)
    s.add(G[n.G_index['TION']] == 1090)
    s.add(G[n.G_index['HE']] == 2304)
    s.add(G[n.G_index['CA']] == 290)
    s.add(G[n.G_index['SO']] == 656)
    s.add(G[n.G_index['TH']] == 1168)
    s.add(G[n.G_index['WITH']] == 592)
    s.add(G[n.G_index['CON']] == 578)
    s.add(G[n.G_index['AN']] == 1058)
    s.add(G[n.G_index['CE']] == 2176)
    s.add(G[n.G_index['WAS']] == 2080)
    s.add(G[n.G_index['ME']] == 1154)
    s.add(G[n.G_index['C']] == 8)
    s.add(G[n.G_index['O']] == 514)
    s.add(G[n.G_index['H']] == 160)
    s.add(G[n.G_index['CO']] == 1160)
    s.add(G[n.G_index['K']] == 2050)
    s.add(G[n.G_index['DI']] == 162)
    s.add(G[n.G_index['OR']] == 800)
    s.add(G[n.G_index['PRO']] == 74)
    s.add(G[n.G_index['U']] == 1026)
    s.add(G[n.G_index['SH']] == 1096)
    s.add(G[n.G_index['LI']] == 2192)
    s.add(G[n.G_index['LL']] == 98)
    s.add(G[n.G_index['AT']] == 642)
    s.add(G[n.G_index['VE']] == 82)
    s.add(G[n.G_index['X']] == 10)
    s.add(G[n.G_index['CH']] == 2320)
    s.add(G[n.G_index['HIS']] == 2184)
    s.add(G[n.G_index['ARE']] == 546)
    s.add(G[n.G_index['COM']] == 1120)
    s.add(G[n.G_index['THIS']] == 584)
    s.add(G[n.G_index['NE']] == 648)
    s.add(G[n.G_index['LA']] == 1184)
    s.add(G[n.G_index['EN']] == 2128)
    s.add(G[n.G_index['V']] == 66)
    s.add(G[n.G_index['PE']] == 776)
    s.add(G[n.G_index['OU']] == 522)
    s.add(G[n.G_index['FROM']] == 2120)
    s.add(G[n.G_index['LO']] == 2208)
    s.add(G[n.G_index['ER']] == 672)
    s.add(G[n.G_index['UT']] == 770)
    s.add(G[n.G_index['HO']] == 1312)
    s.add(G[n.G_index['SA']] == 2178)
    s.add(G[n.G_index['Q']] == 96)
    s.add(G[n.G_index['SI']] == 1034)
    s.add(G[n.G_index['MENT']] == 266)
    s.add(G[n.G_index['TS']] == 138)
    s.add(G[n.G_index['TER']] == 1288)
    s.add(G[n.G_index['TR']] == 2336)
    s.add(G[n.G_index['WHICH']] == 2144)
    s.add(G[n.G_index['UN']] == 2306)
    s.add(G[n.G_index['J']] == 576)
    s.add(G[n.G_index['INT']] == 2114)
    s.add(G[n.G_index['TED']] == 608)
    s.add(G[n.G_index['Z']] == 34)

# Generated by impute_forbid.py based on the abstraction from the previous run.
def custom_chord_cost(raw_G_cost, G, s, n):
    for i in range(len(n.G)): # Setup for G_127 with abstraction
        s.add( Or( Not( G[i] == 2), raw_G_cost[i] == 5381))
        s.add( Or( Not( G[i] == 8), raw_G_cost[i] == 6742))
        s.add( Or( Not( G[i] == 10), raw_G_cost[i] == 9772))
        s.add( Or( Not( G[i] == 16), raw_G_cost[i] == 4651))
        s.add( Or( Not( G[i] == 18), raw_G_cost[i] == 7889))
        s.add( Or( Not( G[i] == 32), raw_G_cost[i] == 5941))
        s.add( Or( Not( G[i] == 34), raw_G_cost[i] == 8771))
        s.add( Or( Not( G[i] == 64), raw_G_cost[i] == 5370))
        s.add( Or( Not( G[i] == 66), raw_G_cost[i] == 8069))
        s.add( Or( Not( G[i] == 72), raw_G_cost[i] == 9769))
        s.add( Or( Not( G[i] == 74), raw_G_cost[i] == 11115))
        s.add( Or( Not( G[i] == 80), raw_G_cost[i] == 7875))
        s.add( Or( Not( G[i] == 82), raw_G_cost[i] == 9232))
        s.add( Or( Not( G[i] == 96), raw_G_cost[i] == 8768))
        s.add( Or( Not( G[i] == 98), raw_G_cost[i] == 10114))
        s.add( Or( Not( G[i] == 128), raw_G_cost[i] == 4706))
        s.add( Or( Not( G[i] == 130), raw_G_cost[i] == 7903))
        s.add( Or( Not( G[i] == 136), raw_G_cost[i] == 9603))
        s.add( Or( Not( G[i] == 138), raw_G_cost[i] == 10949))
        s.add( Or( Not( G[i] == 144), raw_G_cost[i] == 7045))
        s.add( Or( Not( G[i] == 146), raw_G_cost[i] == 9066))
        s.add( Or( Not( G[i] == 160), raw_G_cost[i] == 8602))
        s.add( Or( Not( G[i] == 162), raw_G_cost[i] == 9948))
        s.add( Or( Not( G[i] == 256), raw_G_cost[i] == 5217))
        s.add( Or( Not( G[i] == 258), raw_G_cost[i] == 8031))
        s.add( Or( Not( G[i] == 264), raw_G_cost[i] == 9731))
        s.add( Or( Not( G[i] == 266), raw_G_cost[i] == 11077))
        s.add( Or( Not( G[i] == 272), raw_G_cost[i] == 7685))
        s.add( Or( Not( G[i] == 274), raw_G_cost[i] == 9194))
        s.add( Or( Not( G[i] == 288), raw_G_cost[i] == 8730))
        s.add( Or( Not( G[i] == 290), raw_G_cost[i] == 10075))
        s.add( Or( Not( G[i] == 512), raw_G_cost[i] == 5268))
        s.add( Or( Not( G[i] == 514), raw_G_cost[i] == 8043))
        s.add( Or( Not( G[i] == 520), raw_G_cost[i] == 9744))
        s.add( Or( Not( G[i] == 522), raw_G_cost[i] == 11089))
        s.add( Or( Not( G[i] == 528), raw_G_cost[i] == 7747))
        s.add( Or( Not( G[i] == 530), raw_G_cost[i] == 9206))
        s.add( Or( Not( G[i] == 544), raw_G_cost[i] == 8743))
        s.add( Or( Not( G[i] == 546), raw_G_cost[i] == 10088))
        s.add( Or( Not( G[i] == 576), raw_G_cost[i] == 8029))
        s.add( Or( Not( G[i] == 578), raw_G_cost[i] == 9386))
        s.add( Or( Not( G[i] == 584), raw_G_cost[i] == 11086))
        s.add( Or( Not( G[i] == 592), raw_G_cost[i] == 9192))
        s.add( Or( Not( G[i] == 608), raw_G_cost[i] == 10085))
        s.add( Or( Not( G[i] == 640), raw_G_cost[i] == 7761))
        s.add( Or( Not( G[i] == 642), raw_G_cost[i] == 9220))
        s.add( Or( Not( G[i] == 648), raw_G_cost[i] == 10920))
        s.add( Or( Not( G[i] == 656), raw_G_cost[i] == 8924))
        s.add( Or( Not( G[i] == 672), raw_G_cost[i] == 9919))
        s.add( Or( Not( G[i] == 768), raw_G_cost[i] == 7889))
        s.add( Or( Not( G[i] == 770), raw_G_cost[i] == 9348))
        s.add( Or( Not( G[i] == 776), raw_G_cost[i] == 11048))
        s.add( Or( Not( G[i] == 784), raw_G_cost[i] == 9052))
        s.add( Or( Not( G[i] == 800), raw_G_cost[i] == 10047))
        s.add( Or( Not( G[i] == 1024), raw_G_cost[i] == 4528))
        s.add( Or( Not( G[i] == 1026), raw_G_cost[i] == 7859))
        s.add( Or( Not( G[i] == 1032), raw_G_cost[i] == 9559))
        s.add( Or( Not( G[i] == 1034), raw_G_cost[i] == 10904))
        s.add( Or( Not( G[i] == 1040), raw_G_cost[i] == 6946))
        s.add( Or( Not( G[i] == 1042), raw_G_cost[i] == 9021))
        s.add( Or( Not( G[i] == 1056), raw_G_cost[i] == 8558))
        s.add( Or( Not( G[i] == 1058), raw_G_cost[i] == 9903))
        s.add( Or( Not( G[i] == 1088), raw_G_cost[i] == 7845))
        s.add( Or( Not( G[i] == 1090), raw_G_cost[i] == 9201))
        s.add( Or( Not( G[i] == 1096), raw_G_cost[i] == 10902))
        s.add( Or( Not( G[i] == 1104), raw_G_cost[i] == 9007))
        s.add( Or( Not( G[i] == 1120), raw_G_cost[i] == 9900))
        s.add( Or( Not( G[i] == 1152), raw_G_cost[i] == 7014))
        s.add( Or( Not( G[i] == 1154), raw_G_cost[i] == 9035))
        s.add( Or( Not( G[i] == 1160), raw_G_cost[i] == 10736))
        s.add( Or( Not( G[i] == 1168), raw_G_cost[i] == 8177))
        s.add( Or( Not( G[i] == 1184), raw_G_cost[i] == 9734))
        s.add( Or( Not( G[i] == 1280), raw_G_cost[i] == 7654))
        s.add( Or( Not( G[i] == 1282), raw_G_cost[i] == 9163))
        s.add( Or( Not( G[i] == 1288), raw_G_cost[i] == 10863))
        s.add( Or( Not( G[i] == 1296), raw_G_cost[i] == 8817))
        s.add( Or( Not( G[i] == 1312), raw_G_cost[i] == 9862))
        s.add( Or( Not( G[i] == 2048), raw_G_cost[i] == 5607))
        s.add( Or( Not( G[i] == 2050), raw_G_cost[i] == 8355))
        s.add( Or( Not( G[i] == 2056), raw_G_cost[i] == 9829))
        s.add( Or( Not( G[i] == 2058), raw_G_cost[i] == 11174))
        s.add( Or( Not( G[i] == 2064), raw_G_cost[i] == 8172))
        s.add( Or( Not( G[i] == 2066), raw_G_cost[i] == 9517))
        s.add( Or( Not( G[i] == 2080), raw_G_cost[i] == 8828))
        s.add( Or( Not( G[i] == 2082), raw_G_cost[i] == 10173))
        s.add( Or( Not( G[i] == 2112), raw_G_cost[i] == 8352))
        s.add( Or( Not( G[i] == 2114), raw_G_cost[i] == 9697))
        s.add( Or( Not( G[i] == 2120), raw_G_cost[i] == 11171))
        s.add( Or( Not( G[i] == 2128), raw_G_cost[i] == 9515))
        s.add( Or( Not( G[i] == 2144), raw_G_cost[i] == 10170))
        s.add( Or( Not( G[i] == 2176), raw_G_cost[i] == 8186))
        s.add( Or( Not( G[i] == 2178), raw_G_cost[i] == 9531))
        s.add( Or( Not( G[i] == 2184), raw_G_cost[i] == 11005))
        s.add( Or( Not( G[i] == 2192), raw_G_cost[i] == 9349))
        s.add( Or( Not( G[i] == 2208), raw_G_cost[i] == 10004))
        s.add( Or( Not( G[i] == 2304), raw_G_cost[i] == 8314))
        s.add( Or( Not( G[i] == 2306), raw_G_cost[i] == 9659))
        s.add( Or( Not( G[i] == 2312), raw_G_cost[i] == 11133))
        s.add( Or( Not( G[i] == 2320), raw_G_cost[i] == 9476))
        s.add( Or( Not( G[i] == 2336), raw_G_cost[i] == 10132))
        s.add( Or( Not( G[i] == 1170), raw_G_cost[i] == 10198))
        s.add( Or( Not( G[i] == 1298), raw_G_cost[i] == 10326))
        s.add( Or( Not( G[i] == 1106), raw_G_cost[i] == 10364))
        s.add( Or( Not( G[i] == 658), raw_G_cost[i] == 10383))
        s.add( Or( Not( G[i] == 786), raw_G_cost[i] == 10511))
        s.add( Or( Not( G[i] == 594), raw_G_cost[i] == 10549))
        s.add( Or( Not( G[i] == 2194), raw_G_cost[i] == 10694))
        s.add( Or( Not( G[i] == 2322), raw_G_cost[i] == 10822))
        s.add( Or( Not( G[i] == 2130), raw_G_cost[i] == 10860))
        s.add( Or( Not( G[i] == 1186), raw_G_cost[i] == 11080))
        s.add( Or( Not( G[i] == 1314), raw_G_cost[i] == 11207))
        s.add( Or( Not( G[i] == 1122), raw_G_cost[i] == 11246))
        s.add( Or( Not( G[i] == 674), raw_G_cost[i] == 11264))
        s.add( Or( Not( G[i] == 2210), raw_G_cost[i] == 11349))
        s.add( Or( Not( G[i] == 802), raw_G_cost[i] == 11392))
        s.add( Or( Not( G[i] == 610), raw_G_cost[i] == 11430))
        s.add( Or( Not( G[i] == 2338), raw_G_cost[i] == 11477))
        s.add( Or( Not( G[i] == 2146), raw_G_cost[i] == 11515))
        s.add( Or( Not( G[i] == 1162), raw_G_cost[i] == 12081))
        s.add( Or( Not( G[i] == 1290), raw_G_cost[i] == 12209))
        s.add( Or( Not( G[i] == 1098), raw_G_cost[i] == 12247))
        s.add( Or( Not( G[i] == 650), raw_G_cost[i] == 12266))
        s.add( Or( Not( G[i] == 2186), raw_G_cost[i] == 12351))
        s.add( Or( Not( G[i] == 778), raw_G_cost[i] == 12394))
        s.add( Or( Not( G[i] == 586), raw_G_cost[i] == 12432))
        s.add( Or( Not( G[i] == 2314), raw_G_cost[i] == 12478))
        s.add( Or( Not( G[i] == 2122), raw_G_cost[i] == 12517))

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
    custom_forbid(G, G_D, s, n)
    custom_hardcode(G, s, n)

    # The raw cost of pressing each g.
    raw_G_cost = [ Int('rc%s' % i) for i in range(len(n.G)) ]
    all_diff(raw_G_cost, s, n)
    custom_chord_cost(raw_G_cost, G, s, n)

    G_count = [ Int('g_cnt%s' % i) for i in range(len(n.G)) ]
    stride_stutter_count(G_count, G, G_D, s, n, p)

    total_cost = Int('total_cost')
    combine_chord_cost_with_count(total_cost, G_count, raw_G_cost, s, n)

    return Buttons(total_cost=total_cost, G=G, G_D=G_D)
