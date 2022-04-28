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
    for i in range(len(n.G)): # Setup for G_16 with ab
        # Forbidden finger combinations
        s.add( And( Not(G_D[i] == 4095), Not(G_D[i] == 4088), Not(G_D[i] == 4039), Not(G_D[i] == 3647), Not(G_D[i] == 511)))

        # Forbidden chord combinations
        s.add( And( Not(G[i] == 10), Not(G[i] == 66), Not(G[i] == 80), Not(G[i] == 160), Not(G[i] == 288), Not(G[i] == 96), Not(G[i] == 136), Not(G[i] == 264), Not(G[i] == 72), Not(G[i] == 2050), Not(G[i] == 2064), Not(G[i] == 1056), Not(G[i] == 544), Not(G[i] == 2080), Not(G[i] == 1032), Not(G[i] == 520), Not(G[i] == 2056), Not(G[i] == 640), Not(G[i] == 1088), Not(G[i] == 768), Not(G[i] == 576), Not(G[i] == 2176), Not(G[i] == 2304), Not(G[i] == 2112)))

# Generated by impute_forbid.py. Hardcodes some variables based on the abstraction from the previous run.
def custom_hardcode(G, s, n): # Setup for G_16 with ab
    s.add(G[n.G_index[' ']] == 16)
    s.add(G[n.G_index['THE']] == 2)
    s.add(G[n.G_index['E']] == 1024)
    s.add(G[n.G_index['T']] == 8)
    s.add(G[n.G_index['A']] == 512)
    s.add(G[n.G_index['S']] == 64)
    s.add(G[n.G_index['Y']] == 18)
    s.add(G[n.G_index['W']] == 256)
    s.add(G[n.G_index['R']] == 32)
    s.add(G[n.G_index['OF']] == 2048)
    s.add(G[n.G_index['C']] == 130)
    s.add(G[n.G_index['N']] == 128)

# Generated by impute_forbid.py based on the abstraction from the previous run.
def custom_chord_cost(raw_G_cost, G, s, n):
    for i in range(len(n.G)): # Setup for G_16 with ab
        s.add( Or( Not( G[i] == 2), raw_G_cost[i] == 5381))
        s.add( Or( Not( G[i] == 8), raw_G_cost[i] == 6742))
        s.add( Or( Not( G[i] == 16), raw_G_cost[i] == 4651))
        s.add( Or( Not( G[i] == 32), raw_G_cost[i] == 5941))
        s.add( Or( Not( G[i] == 64), raw_G_cost[i] == 5370))
        s.add( Or( Not( G[i] == 128), raw_G_cost[i] == 4706))
        s.add( Or( Not( G[i] == 256), raw_G_cost[i] == 5217))
        s.add( Or( Not( G[i] == 512), raw_G_cost[i] == 5268))
        s.add( Or( Not( G[i] == 1024), raw_G_cost[i] == 4528))
        s.add( Or( Not( G[i] == 2048), raw_G_cost[i] == 5607))
        s.add( Or( Not( G[i] == 18), raw_G_cost[i] == 7889))
        s.add( Or( Not( G[i] == 34), raw_G_cost[i] == 8771))
        s.add( Or( Not( G[i] == 130), raw_G_cost[i] == 7903))
        s.add( Or( Not( G[i] == 258), raw_G_cost[i] == 8031))
        s.add( Or( Not( G[i] == 144), raw_G_cost[i] == 7045))
        s.add( Or( Not( G[i] == 272), raw_G_cost[i] == 7685))
        s.add( Or( Not( G[i] == 1026), raw_G_cost[i] == 7859))
        s.add( Or( Not( G[i] == 514), raw_G_cost[i] == 8043))
        s.add( Or( Not( G[i] == 1040), raw_G_cost[i] == 6946))
        s.add( Or( Not( G[i] == 528), raw_G_cost[i] == 7747))
        s.add( Or( Not( G[i] == 1152), raw_G_cost[i] == 7014))
        s.add( Or( Not( G[i] == 1280), raw_G_cost[i] == 7654))

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
