from z3 import *
from dataclasses import dataclass, field
import lib

@dataclass
class Buttons:
    G: list = field(default_factory=lambda: [])
    G_D: list = field(default_factory=lambda: [])
    raw_H2_cost: list = field(default_factory=lambda: [])
    discounted_H_cost: list = field(default_factory=lambda: [])
    cumulative_cost: list = field(default_factory=lambda: [])

def reserve_chords_for_numbers_and_symbols(G, s, n, p):
    # Reserve chords for numbers and symbols. Choose either Index or Pinky constraints:
    if p.reserved_finger == "pinky":
        # Reserve chords for numbers and symbols. Choose either Index or Pinky constraints:
        # Index Constraint - Forbid use of L or R by the index finger.
        s.add([ Extract(11, 11, G[i]) == 0  for i in range(len(n.G)) ]) # Index L
        s.add([ Extract(9 , 9 , G[i]) == 0  for i in range(len(n.G)) ]) # Index R
    
    elif p.reserved_finger == "index":
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
    for i in range(len(n.G) - 1):
        s.add( [ G[i] != G[j] for j in range(i + 1, len(n.G)) ] )

def no_null(G, s, n):
    # Every string must be assigned to a chord.
    s.add( [ G[i] != 0 for i in range(n.G) ] )

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


def chord_cost(raw_H2_cost, s, n):
    # **********************************************
    # Cost constraints
    #  - Estimate and minimize cost of configuration 
    # **********************************************

    # Finding the cost of every possible chord is too much work
    #   Num_chords > 5^4!
    # Instead we approximate the cost of the chord as the most expensive
    #   one/two finger press of that cord. Ex: Suppose the chord
    #   L0MR, we then pick the most expensive of all two finger
    #   presses {L0M0, L00R, 00MR}
    # Requires 5*5*6+5*4 = 170 known costs for chords.
    # Single finger chords have a one-to-one correspondance with
    #   single finger preferences.
    # A chord involving more than two fingers cannot be approximated by
    #   the cost of a single finger press.

    # Raw cost is the cost of entering a n_gram a single time regardless of frequency.
    # "Generate Cost Function.xlsx" will generate this.
    # Note: Doesn't this giant if-then-else block look ugly? Keep in mind that we are required
    #   to express this problem in 1st-order logic for the SMT solver to accept it. The ITE block
    #   will be converted to a SAT expression.
    # 2nd Note: Unintuitively the masking is faster in this instance then using extract as in
    #   the constraint blocking same finger (LR) presses above.

    null_assignment = 100
    for i in range(len(n.H)):
        h2_index = n.G_index[n.H2[i]]
        s.add( raw_H2_cost[i] == \
            If(And(Extract(4, 4, G[h2_index]) == 1, Extract(3, 3, G[h2_index]) == 1),  1.53846153846154, #  000 000 011 000
            If(And(Extract(5, 5, G[h2_index]) == 1, Extract(4, 4, G[h2_index]) == 1),  1.53846153846154, #  000 000 110 000
            If(And(Extract(1, 1, G[h2_index]) == 1, Extract(0, 0, G[h2_index]) == 1),  1.53846153846154, #  000 000 000 011
            If(And(Extract(2, 2, G[h2_index]) == 1, Extract(1, 1, G[h2_index]) == 1),  1.53846153846154, #  000 000 000 110
            If(And(Extract(11, 11, G[h2_index]) == 1, Extract(10, 10, G[h2_index]) == 1),  1.27659574468085, #  110 000 000 000
            If(And(Extract(8, 8, G[h2_index]) == 1, Extract(7, 7, G[h2_index]) == 1),  1.2, #  000 110 000 000
            If(And(Extract(7, 7, G[h2_index]) == 1, Extract(6, 6, G[h2_index]) == 1),  1.11111111111111, #  000 011 000 000
            If(And(Extract(10, 10, G[h2_index]) == 1, Extract(9, 9, G[h2_index]) == 1),  1.09090909090909, #  011 000 000 000
            If(Extract(2, 2, G[h2_index]) == 1,  0.689655172413793, #  000 000 000 100
            If(Extract(5, 5, G[h2_index]) == 1,  0.674157303370786, #  000 000 100 000
            If(Extract(0, 0, G[h2_index]) == 1,  0.625, #  000 000 000 001
            If(Extract(3, 3, G[h2_index]) == 1,  0.594059405940594, #  000 000 001 000
            If(Extract(9, 9, G[h2_index]) == 1,  0.560747663551402, #  001 000 000 000
            If(Extract(1, 1, G[h2_index]) == 1,  0.538116591928251, #  000 000 000 010
            If(Extract(11, 11, G[h2_index]) == 1,  0.530973451327434, #  100 000 000 000
            If(Extract(8, 8, G[h2_index]) == 1,  0.530973451327434, #  000 100 000 000
            If(Extract(6, 6, G[h2_index]) == 1,  0.521739130434783, #  000 001 000 000
            If(Extract(7, 7, G[h2_index]) == 1,  0.470588235294118, #  000 010 000 000
            If(Extract(4, 4, G[h2_index]) == 1,  0.465116279069767, #  000 000 010 000
            If(Extract(10, 10, G[h2_index]) == 1,  0.452830188679245, #  010 000 000 000

            #  This can only be reached if the n-gram has a null assignment, this should be unreachable.
            null_assignment)))))))))))))))))))))

def stride_stutter_discount(raw_H2_cost, discounted_H_cost, G, G_D, s, n, p):
    identical_found = false
    for i in range(len(n.H)):
        h1_index = n.G_index[n.H1[i]]
        h2_index = n.G_index[n.H2[i]]
        if h1_index == h2_index: # Identical strings are always in stride.
            assert n.H1[i] == n.H2[i]
            identical_found = true
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

def add_up_cumulative_cost(cumulative_cost, discounted_H_cost, s, n):
    print(f"G Size: {len(n.G)} H Size: {len(n.H)}")
    # This is a round about way of summing up the total cost of the
    #   whole problem. Keep in mind that we are limited to 1st-order logic
    s.add(cumulative_cost[0] == discounted_H_cost[0])
    s.add( [ cumulative_cost[i] == cumulative_cost[i-1] + discounted_H_cost[i] \
                for i in range(1, len(n.H)) ] )

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

    # The raw cost of pressing each h2.
    raw_H2_cost = [ Real('rc%s' % i) for i in range(len(n.H)) ]

    # The cost of each H according to stride, stutter, and conflict, multiplied by frequency.
    discounted_H_cost = [ Real('rc%s' % i) for i in range(len(n.H)) ]
    stride_stutter_discount(raw_H2_cost, discounted_H_cost, G, G_D, s, n, p)
    
    cumulative_cost = [ Real('cc%s' % i) for i in range(len(n.H)) ]
    add_up_cumulative_cost(cumulative_cost, discounted_H_cost, s, n)

    return Buttons(G=G, G_D=G_D, discounted_H_cost=discounted_H_cost, cumulative_cost=cumulative_cost)
