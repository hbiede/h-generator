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
        # s.add( raw_H2_cost[i] == \
        #     If(And(Extract(4, 4, G[h2_index]) == 1, Extract(3, 3, G[h2_index]) == 1),  1.53846153846154, #  000 000 011 000
        #     If(And(Extract(5, 5, G[h2_index]) == 1, Extract(4, 4, G[h2_index]) == 1),  1.53846153846154, #  000 000 110 000
        #     If(And(Extract(1, 1, G[h2_index]) == 1, Extract(0, 0, G[h2_index]) == 1),  1.53846153846154, #  000 000 000 011
        #     If(And(Extract(2, 2, G[h2_index]) == 1, Extract(1, 1, G[h2_index]) == 1),  1.53846153846154, #  000 000 000 110
        #     If(And(Extract(11, 11, G[h2_index]) == 1, Extract(10, 10, G[h2_index]) == 1),  1.27659574468085, #  110 000 000 000
        #     If(And(Extract(8, 8, G[h2_index]) == 1, Extract(7, 7, G[h2_index]) == 1),  1.2, #  000 110 000 000
        #     If(And(Extract(7, 7, G[h2_index]) == 1, Extract(6, 6, G[h2_index]) == 1),  1.11111111111111, #  000 011 000 000
        #     If(And(Extract(10, 10, G[h2_index]) == 1, Extract(9, 9, G[h2_index]) == 1),  1.09090909090909, #  011 000 000 000
        #     If(Extract(2, 2, G[h2_index]) == 1,  0.689655172413793, #  000 000 000 100
        #     If(Extract(5, 5, G[h2_index]) == 1,  0.674157303370786, #  000 000 100 000
        #     If(Extract(0, 0, G[h2_index]) == 1,  0.625, #  000 000 000 001
        #     If(Extract(3, 3, G[h2_index]) == 1,  0.594059405940594, #  000 000 001 000
        #     If(Extract(9, 9, G[h2_index]) == 1,  0.560747663551402, #  001 000 000 000
        #     If(Extract(1, 1, G[h2_index]) == 1,  0.538116591928251, #  000 000 000 010
        #     If(Extract(11, 11, G[h2_index]) == 1,  0.530973451327434, #  100 000 000 000
        #     If(Extract(8, 8, G[h2_index]) == 1,  0.530973451327434, #  000 100 000 000
        #     If(Extract(6, 6, G[h2_index]) == 1,  0.521739130434783, #  000 001 000 000
        #     If(Extract(7, 7, G[h2_index]) == 1,  0.470588235294118, #  000 010 000 000
        #     If(Extract(4, 4, G[h2_index]) == 1,  0.465116279069767, #  000 000 010 000
        #     If(Extract(10, 10, G[h2_index]) == 1,  0.452830188679245, #  010 000 000 000

        #     #  This can only be reached if the n-gram has a null assignment, this should be unreachable.
        #     null_assignment)))))))))))))))))))))
        s.add( If(G[h2_index] == 1, raw_H2_cost[i] == 0.689655172))
        s.add( If(G[h2_index] == 2, raw_H2_cost[i] == 0.538116592))
        s.add( If(G[h2_index] == 4, raw_H2_cost[i] == 0.625))
        s.add( If(G[h2_index] == 8, raw_H2_cost[i] == 0.674157303))
        s.add( If(G[h2_index] == 9, raw_H2_cost[i] == 1.03060829075))
        s.add( If(G[h2_index] == 10, raw_H2_cost[i] == 0.97722577675))
        s.add( If(G[h2_index] == 12, raw_H2_cost[i] == 0.99894662875))
        s.add( If(G[h2_index] == 16, raw_H2_cost[i] == 0.465116279))
        s.add( If(G[h2_index] == 17, raw_H2_cost[i] == 0.97834803475))
        s.add( If(G[h2_index] == 18, raw_H2_cost[i] == 0.7889248097499999))
        s.add( If(G[h2_index] == 20, raw_H2_cost[i] == 0.89752906975))
        s.add( If(G[h2_index] == 32, raw_H2_cost[i] == 0.594059406))
        s.add( If(G[h2_index] == 33, raw_H2_cost[i] == 1.0105838165))
        s.add( If(G[h2_index] == 34, raw_H2_cost[i] == 0.8771034055))
        s.add( If(G[h2_index] == 36, raw_H2_cost[i] == 0.9297648515))
        s.add( If(G[h2_index] == 64, raw_H2_cost[i] == 0.537003738))
        s.add( If(G[h2_index] == 65, raw_H2_cost[i] == 0.9963198995))
        s.add( If(G[h2_index] == 66, raw_H2_cost[i] == 0.8068966744999999))
        s.add( If(G[h2_index] == 68, raw_H2_cost[i] == 0.9155009345))
        s.add( If(G[h2_index] == 72, raw_H2_cost[i] == 0.97694756325))
        s.add( If(G[h2_index] == 73, raw_H2_cost[i] == 1.16485922525))
        s.add( If(G[h2_index] == 74, raw_H2_cost[i] == 1.11147671125))
        s.add( If(G[h2_index] == 76, raw_H2_cost[i] == 1.13319756325))
        s.add( If(G[h2_index] == 80, raw_H2_cost[i] == 0.78753374225))
        s.add( If(G[h2_index] == 81, raw_H2_cost[i] == 1.11259896925))
        s.add( If(G[h2_index] == 82, raw_H2_cost[i] == 0.9231757442499999))
        s.add( If(G[h2_index] == 84, raw_H2_cost[i] == 1.0317800042499998))
        s.add( If(G[h2_index] == 96, raw_H2_cost[i] == 0.876825192))
        s.add( If(G[h2_index] == 97, raw_H2_cost[i] == 1.144834751))
        s.add( If(G[h2_index] == 98, raw_H2_cost[i] == 1.01135434))
        s.add( If(G[h2_index] == 100, raw_H2_cost[i] == 1.0640157860000001))
        s.add( If(G[h2_index] == 128, raw_H2_cost[i] == 0.470588235))
        s.add( If(G[h2_index] == 129, raw_H2_cost[i] == 0.97971602375))
        s.add( If(G[h2_index] == 130, raw_H2_cost[i] == 0.7902927987499999))
        s.add( If(G[h2_index] == 132, raw_H2_cost[i] == 0.89889705875))
        s.add( If(G[h2_index] == 136, raw_H2_cost[i] == 0.9603436875))
        s.add( If(G[h2_index] == 137, raw_H2_cost[i] == 1.1482553495))
        s.add( If(G[h2_index] == 138, raw_H2_cost[i] == 1.0948728355))
        s.add( If(G[h2_index] == 140, raw_H2_cost[i] == 1.1165936875))
        s.add( If(G[h2_index] == 144, raw_H2_cost[i] == 0.7045143635))
        s.add( If(G[h2_index] == 145, raw_H2_cost[i] == 1.0959950935))
        s.add( If(G[h2_index] == 146, raw_H2_cost[i] == 0.9065718684999999))
        s.add( If(G[h2_index] == 148, raw_H2_cost[i] == 1.0151761285))
        s.add( If(G[h2_index] == 160, raw_H2_cost[i] == 0.86022131625))
        s.add( If(G[h2_index] == 161, raw_H2_cost[i] == 1.12823087525))
        s.add( If(G[h2_index] == 162, raw_H2_cost[i] == 0.9947504642499999))
        s.add( If(G[h2_index] == 164, raw_H2_cost[i] == 1.0474119102500001))
        s.add( If(G[h2_index] == 256, raw_H2_cost[i] == 0.52173913))
        s.add( If(G[h2_index] == 257, raw_H2_cost[i] == 0.9925037475))
        s.add( If(G[h2_index] == 258, raw_H2_cost[i] == 0.8030805225))
        s.add( If(G[h2_index] == 260, raw_H2_cost[i] == 0.9116847825000001))
        s.add( If(G[h2_index] == 264, raw_H2_cost[i] == 0.97313141125))
        s.add( If(G[h2_index] == 265, raw_H2_cost[i] == 1.1610430732500001))
        s.add( If(G[h2_index] == 266, raw_H2_cost[i] == 1.10766055925))
        s.add( If(G[h2_index] == 268, raw_H2_cost[i] == 1.12938141125))
        s.add( If(G[h2_index] == 272, raw_H2_cost[i] == 0.7684529822500001))
        s.add( If(G[h2_index] == 273, raw_H2_cost[i] == 1.10878281725))
        s.add( If(G[h2_index] == 274, raw_H2_cost[i] == 0.91935959225))
        s.add( If(G[h2_index] == 276, raw_H2_cost[i] == 1.02796385225))
        s.add( If(G[h2_index] == 288, raw_H2_cost[i] == 0.8730090399999999))
        s.add( If(G[h2_index] == 289, raw_H2_cost[i] == 1.1410185990000001))
        s.add( If(G[h2_index] == 290, raw_H2_cost[i] == 1.0075381879999998))
        s.add( If(G[h2_index] == 292, raw_H2_cost[i] == 1.060199634))
        s.add( If(G[h2_index] == 512, raw_H2_cost[i] == 0.526762113))
        s.add( If(G[h2_index] == 513, raw_H2_cost[i] == 0.99375949325))
        s.add( If(G[h2_index] == 514, raw_H2_cost[i] == 0.8043362682499999))
        s.add( If(G[h2_index] == 516, raw_H2_cost[i] == 0.91294052825))
        s.add( If(G[h2_index] == 520, raw_H2_cost[i] == 0.974387157))
        s.add( If(G[h2_index] == 521, raw_H2_cost[i] == 1.162298819))
        s.add( If(G[h2_index] == 522, raw_H2_cost[i] == 1.108916305))
        s.add( If(G[h2_index] == 524, raw_H2_cost[i] == 1.130637157))
        s.add( If(G[h2_index] == 528, raw_H2_cost[i] == 0.774731711))
        s.add( If(G[h2_index] == 529, raw_H2_cost[i] == 1.110038563))
        s.add( If(G[h2_index] == 530, raw_H2_cost[i] == 0.920615338))
        s.add( If(G[h2_index] == 532, raw_H2_cost[i] == 1.029219598))
        s.add( If(G[h2_index] == 544, raw_H2_cost[i] == 0.8742647857499999))
        s.add( If(G[h2_index] == 545, raw_H2_cost[i] == 1.1422743447500001))
        s.add( If(G[h2_index] == 546, raw_H2_cost[i] == 1.0087939337499998))
        s.add( If(G[h2_index] == 548, raw_H2_cost[i] == 1.06145537975))
        s.add( If(G[h2_index] == 576, raw_H2_cost[i] == 0.80294520075))
        s.add( If(G[h2_index] == 577, raw_H2_cost[i] == 1.12801042775))
        s.add( If(G[h2_index] == 578, raw_H2_cost[i] == 0.93858720275))
        s.add( If(G[h2_index] == 580, raw_H2_cost[i] == 1.0471914627499999))
        s.add( If(G[h2_index] == 584, raw_H2_cost[i] == 1.1086380915))
        s.add( If(G[h2_index] == 585, raw_H2_cost[i] == 1.2965497535))
        s.add( If(G[h2_index] == 586, raw_H2_cost[i] == 1.2431672395))
        s.add( If(G[h2_index] == 588, raw_H2_cost[i] == 1.2648880915))
        s.add( If(G[h2_index] == 592, raw_H2_cost[i] == 0.9192242705))
        s.add( If(G[h2_index] == 593, raw_H2_cost[i] == 1.2442894975))
        s.add( If(G[h2_index] == 594, raw_H2_cost[i] == 1.0548662725))
        s.add( If(G[h2_index] == 596, raw_H2_cost[i] == 1.1634705324999999))
        s.add( If(G[h2_index] == 608, raw_H2_cost[i] == 1.00851572025))
        s.add( If(G[h2_index] == 609, raw_H2_cost[i] == 1.27652527925))
        s.add( If(G[h2_index] == 610, raw_H2_cost[i] == 1.1430448682499998))
        s.add( If(G[h2_index] == 612, raw_H2_cost[i] == 1.19570631425))
        s.add( If(G[h2_index] == 640, raw_H2_cost[i] == 0.7760997))
        s.add( If(G[h2_index] == 641, raw_H2_cost[i] == 1.111406552))
        s.add( If(G[h2_index] == 642, raw_H2_cost[i] == 0.921983327))
        s.add( If(G[h2_index] == 644, raw_H2_cost[i] == 1.0305875869999999))
        s.add( If(G[h2_index] == 648, raw_H2_cost[i] == 1.09203421575))
        s.add( If(G[h2_index] == 649, raw_H2_cost[i] == 1.27994587775))
        s.add( If(G[h2_index] == 650, raw_H2_cost[i] == 1.22656336375))
        s.add( If(G[h2_index] == 652, raw_H2_cost[i] == 1.24828421575))
        s.add( If(G[h2_index] == 656, raw_H2_cost[i] == 0.89237876975))
        s.add( If(G[h2_index] == 657, raw_H2_cost[i] == 1.22768562175))
        s.add( If(G[h2_index] == 658, raw_H2_cost[i] == 1.03826239675))
        s.add( If(G[h2_index] == 660, raw_H2_cost[i] == 1.1468666567499999))
        s.add( If(G[h2_index] == 672, raw_H2_cost[i] == 0.9919118444999999))
        s.add( If(G[h2_index] == 673, raw_H2_cost[i] == 1.2599214035))
        s.add( If(G[h2_index] == 674, raw_H2_cost[i] == 1.1264409924999998))
        s.add( If(G[h2_index] == 676, raw_H2_cost[i] == 1.1791024385))
        s.add( If(G[h2_index] == 768, raw_H2_cost[i] == 0.78888742375))
        s.add( If(G[h2_index] == 769, raw_H2_cost[i] == 1.12419427575))
        s.add( If(G[h2_index] == 770, raw_H2_cost[i] == 0.93477105075))
        s.add( If(G[h2_index] == 772, raw_H2_cost[i] == 1.0433753107500001))
        s.add( If(G[h2_index] == 776, raw_H2_cost[i] == 1.1048219394999998))
        s.add( If(G[h2_index] == 777, raw_H2_cost[i] == 1.2927336015000002))
        s.add( If(G[h2_index] == 778, raw_H2_cost[i] == 1.2393510874999998))
        s.add( If(G[h2_index] == 780, raw_H2_cost[i] == 1.2610719394999998))
        s.add( If(G[h2_index] == 784, raw_H2_cost[i] == 0.9051664935))
        s.add( If(G[h2_index] == 785, raw_H2_cost[i] == 1.2404733455))
        s.add( If(G[h2_index] == 786, raw_H2_cost[i] == 1.0510501205))
        s.add( If(G[h2_index] == 788, raw_H2_cost[i] == 1.1596543805000001))
        s.add( If(G[h2_index] == 800, raw_H2_cost[i] == 1.00469956825))
        s.add( If(G[h2_index] == 801, raw_H2_cost[i] == 1.2727091272500002))
        s.add( If(G[h2_index] == 802, raw_H2_cost[i] == 1.1392287162499999))
        s.add( If(G[h2_index] == 804, raw_H2_cost[i] == 1.19189016225))
        s.add( If(G[h2_index] == 1024, raw_H2_cost[i] == 0.452830189))
        s.add( If(G[h2_index] == 1025, raw_H2_cost[i] == 0.97527651225))
        s.add( If(G[h2_index] == 1026, raw_H2_cost[i] == 0.7858532872499999))
        s.add( If(G[h2_index] == 1028, raw_H2_cost[i] == 0.89445754725))
        s.add( If(G[h2_index] == 1032, raw_H2_cost[i] == 0.955904176))
        s.add( If(G[h2_index] == 1033, raw_H2_cost[i] == 1.143815838))
        s.add( If(G[h2_index] == 1034, raw_H2_cost[i] == 1.090433324))
        s.add( If(G[h2_index] == 1036, raw_H2_cost[i] == 1.112154176))
        s.add( If(G[h2_index] == 1040, raw_H2_cost[i] == 0.694602896))
        s.add( If(G[h2_index] == 1041, raw_H2_cost[i] == 1.091555582))
        s.add( If(G[h2_index] == 1042, raw_H2_cost[i] == 0.9021323569999999))
        s.add( If(G[h2_index] == 1044, raw_H2_cost[i] == 1.010736617))
        s.add( If(G[h2_index] == 1056, raw_H2_cost[i] == 0.8557818047499999))
        s.add( If(G[h2_index] == 1057, raw_H2_cost[i] == 1.12379136375))
        s.add( If(G[h2_index] == 1058, raw_H2_cost[i] == 0.9903109527499999))
        s.add( If(G[h2_index] == 1060, raw_H2_cost[i] == 1.04297239875))
        s.add( If(G[h2_index] == 1088, raw_H2_cost[i] == 0.78446221975))
        s.add( If(G[h2_index] == 1089, raw_H2_cost[i] == 1.10952744675))
        s.add( If(G[h2_index] == 1090, raw_H2_cost[i] == 0.92010422175))
        s.add( If(G[h2_index] == 1092, raw_H2_cost[i] == 1.02870848175))
        s.add( If(G[h2_index] == 1096, raw_H2_cost[i] == 1.0901551105))
        s.add( If(G[h2_index] == 1097, raw_H2_cost[i] == 1.2780667725000001))
        s.add( If(G[h2_index] == 1098, raw_H2_cost[i] == 1.2246842585))
        s.add( If(G[h2_index] == 1100, raw_H2_cost[i] == 1.2464051105))
        s.add( If(G[h2_index] == 1104, raw_H2_cost[i] == 0.9007412895))
        s.add( If(G[h2_index] == 1105, raw_H2_cost[i] == 1.2258065165))
        s.add( If(G[h2_index] == 1106, raw_H2_cost[i] == 1.0363832915))
        s.add( If(G[h2_index] == 1108, raw_H2_cost[i] == 1.1449875515))
        s.add( If(G[h2_index] == 1120, raw_H2_cost[i] == 0.9900327392499999))
        s.add( If(G[h2_index] == 1121, raw_H2_cost[i] == 1.25804229825))
        s.add( If(G[h2_index] == 1122, raw_H2_cost[i] == 1.12456188725))
        s.add( If(G[h2_index] == 1124, raw_H2_cost[i] == 1.17722333325))
        s.add( If(G[h2_index] == 1152, raw_H2_cost[i] == 0.701442841))
        s.add( If(G[h2_index] == 1153, raw_H2_cost[i] == 1.092923571))
        s.add( If(G[h2_index] == 1154, raw_H2_cost[i] == 0.903500346))
        s.add( If(G[h2_index] == 1156, raw_H2_cost[i] == 1.0121046059999999))
        s.add( If(G[h2_index] == 1160, raw_H2_cost[i] == 1.07355123475))
        s.add( If(G[h2_index] == 1161, raw_H2_cost[i] == 1.2614628967500001))
        s.add( If(G[h2_index] == 1162, raw_H2_cost[i] == 1.20808038275))
        s.add( If(G[h2_index] == 1164, raw_H2_cost[i] == 1.22980123475))
        s.add( If(G[h2_index] == 1168, raw_H2_cost[i] == 0.81772191075))
        s.add( If(G[h2_index] == 1169, raw_H2_cost[i] == 1.20920264075))
        s.add( If(G[h2_index] == 1170, raw_H2_cost[i] == 1.01977941575))
        s.add( If(G[h2_index] == 1172, raw_H2_cost[i] == 1.12838367575))
        s.add( If(G[h2_index] == 1184, raw_H2_cost[i] == 0.9734288634999999))
        s.add( If(G[h2_index] == 1185, raw_H2_cost[i] == 1.2414384225))
        s.add( If(G[h2_index] == 1186, raw_H2_cost[i] == 1.1079580115))
        s.add( If(G[h2_index] == 1188, raw_H2_cost[i] == 1.1606194575))
        s.add( If(G[h2_index] == 1280, raw_H2_cost[i] == 0.76538145975))
        s.add( If(G[h2_index] == 1281, raw_H2_cost[i] == 1.10571129475))
        s.add( If(G[h2_index] == 1282, raw_H2_cost[i] == 0.91628806975))
        s.add( If(G[h2_index] == 1284, raw_H2_cost[i] == 1.02489232975))
        s.add( If(G[h2_index] == 1288, raw_H2_cost[i] == 1.0863389584999998))
        s.add( If(G[h2_index] == 1289, raw_H2_cost[i] == 1.2742506205000002))
        s.add( If(G[h2_index] == 1290, raw_H2_cost[i] == 1.2208681064999998))
        s.add( If(G[h2_index] == 1292, raw_H2_cost[i] == 1.2425889584999998))
        s.add( If(G[h2_index] == 1296, raw_H2_cost[i] == 0.8816605295000001))
        s.add( If(G[h2_index] == 1297, raw_H2_cost[i] == 1.2219903645))
        s.add( If(G[h2_index] == 1298, raw_H2_cost[i] == 1.0325671395))
        s.add( If(G[h2_index] == 1300, raw_H2_cost[i] == 1.1411713995000001))
        s.add( If(G[h2_index] == 1312, raw_H2_cost[i] == 0.9862165872499999))
        s.add( If(G[h2_index] == 1313, raw_H2_cost[i] == 1.2542261462500002))
        s.add( If(G[h2_index] == 1314, raw_H2_cost[i] == 1.1207457352499999))
        s.add( If(G[h2_index] == 1316, raw_H2_cost[i] == 1.17340718125))
        s.add( If(G[h2_index] == 2048, raw_H2_cost[i] == 0.560747664))
        s.add( If(G[h2_index] == 2049, raw_H2_cost[i] == 1.002255881))
        s.add( If(G[h2_index] == 2050, raw_H2_cost[i] == 0.8354637279999999))
        s.add( If(G[h2_index] == 2052, raw_H2_cost[i] == 0.921436916))
        s.add( If(G[h2_index] == 2056, raw_H2_cost[i] == 0.98288354475))
        s.add( If(G[h2_index] == 2057, raw_H2_cost[i] == 1.17079520675))
        s.add( If(G[h2_index] == 2058, raw_H2_cost[i] == 1.1174126927499999))
        s.add( If(G[h2_index] == 2060, raw_H2_cost[i] == 1.13913354475))
        s.add( If(G[h2_index] == 2064, raw_H2_cost[i] == 0.81721364975))
        s.add( If(G[h2_index] == 2065, raw_H2_cost[i] == 1.11853495075))
        s.add( If(G[h2_index] == 2066, raw_H2_cost[i] == 0.95174279775))
        s.add( If(G[h2_index] == 2068, raw_H2_cost[i] == 1.03771598575))
        s.add( If(G[h2_index] == 2080, raw_H2_cost[i] == 0.8827611734999999))
        s.add( If(G[h2_index] == 2081, raw_H2_cost[i] == 1.1507707325))
        s.add( If(G[h2_index] == 2082, raw_H2_cost[i] == 1.0172903215))
        s.add( If(G[h2_index] == 2084, raw_H2_cost[i] == 1.0699517675))
        s.add( If(G[h2_index] == 2112, raw_H2_cost[i] == 0.8351855145))
        s.add( If(G[h2_index] == 2113, raw_H2_cost[i] == 1.1365068155000002))
        s.add( If(G[h2_index] == 2114, raw_H2_cost[i] == 0.9697146624999999))
        s.add( If(G[h2_index] == 2116, raw_H2_cost[i] == 1.0556878505))
        s.add( If(G[h2_index] == 2120, raw_H2_cost[i] == 1.11713447925))
        s.add( If(G[h2_index] == 2121, raw_H2_cost[i] == 1.30504614125))
        s.add( If(G[h2_index] == 2122, raw_H2_cost[i] == 1.2516636272500001))
        s.add( If(G[h2_index] == 2124, raw_H2_cost[i] == 1.27338447925))
        s.add( If(G[h2_index] == 2128, raw_H2_cost[i] == 0.95146458425))
        s.add( If(G[h2_index] == 2129, raw_H2_cost[i] == 1.2527858852500002))
        s.add( If(G[h2_index] == 2130, raw_H2_cost[i] == 1.08599373225))
        s.add( If(G[h2_index] == 2132, raw_H2_cost[i] == 1.17196692025))
        s.add( If(G[h2_index] == 2144, raw_H2_cost[i] == 1.0170121079999999))
        s.add( If(G[h2_index] == 2145, raw_H2_cost[i] == 1.285021667))
        s.add( If(G[h2_index] == 2146, raw_H2_cost[i] == 1.151541256))
        s.add( If(G[h2_index] == 2148, raw_H2_cost[i] == 1.204202702))
        s.add( If(G[h2_index] == 2176, raw_H2_cost[i] == 0.81858163875))
        s.add( If(G[h2_index] == 2177, raw_H2_cost[i] == 1.1199029397500002))
        s.add( If(G[h2_index] == 2178, raw_H2_cost[i] == 0.9531107867499999))
        s.add( If(G[h2_index] == 2180, raw_H2_cost[i] == 1.03908397475))
        s.add( If(G[h2_index] == 2184, raw_H2_cost[i] == 1.1005306035))
        s.add( If(G[h2_index] == 2185, raw_H2_cost[i] == 1.2884422655))
        s.add( If(G[h2_index] == 2186, raw_H2_cost[i] == 1.2350597515000001))
        s.add( If(G[h2_index] == 2188, raw_H2_cost[i] == 1.2567806035))
        s.add( If(G[h2_index] == 2192, raw_H2_cost[i] == 0.9348607085))
        s.add( If(G[h2_index] == 2193, raw_H2_cost[i] == 1.2361820095000002))
        s.add( If(G[h2_index] == 2194, raw_H2_cost[i] == 1.0693898565))
        s.add( If(G[h2_index] == 2196, raw_H2_cost[i] == 1.1553630445))
        s.add( If(G[h2_index] == 2208, raw_H2_cost[i] == 1.0004082322499999))
        s.add( If(G[h2_index] == 2209, raw_H2_cost[i] == 1.26841779125))
        s.add( If(G[h2_index] == 2210, raw_H2_cost[i] == 1.13493738025))
        s.add( If(G[h2_index] == 2212, raw_H2_cost[i] == 1.18759882625))
        s.add( If(G[h2_index] == 2304, raw_H2_cost[i] == 0.8313693625))
        s.add( If(G[h2_index] == 2305, raw_H2_cost[i] == 1.1326906635))
        s.add( If(G[h2_index] == 2306, raw_H2_cost[i] == 0.9658985105))
        s.add( If(G[h2_index] == 2308, raw_H2_cost[i] == 1.0518716984999998))
        s.add( If(G[h2_index] == 2312, raw_H2_cost[i] == 1.11331832725))
        s.add( If(G[h2_index] == 2313, raw_H2_cost[i] == 1.30122998925))
        s.add( If(G[h2_index] == 2314, raw_H2_cost[i] == 1.24784747525))
        s.add( If(G[h2_index] == 2316, raw_H2_cost[i] == 1.26956832725))
        s.add( If(G[h2_index] == 2320, raw_H2_cost[i] == 0.9476484322500001))
        s.add( If(G[h2_index] == 2321, raw_H2_cost[i] == 1.24896973325))
        s.add( If(G[h2_index] == 2322, raw_H2_cost[i] == 1.08217758025))
        s.add( If(G[h2_index] == 2324, raw_H2_cost[i] == 1.16815076825))
        s.add( If(G[h2_index] == 2336, raw_H2_cost[i] == 1.013195956))
        s.add( If(G[h2_index] == 2337, raw_H2_cost[i] == 1.281205515))
        s.add( If(G[h2_index] == 2338, raw_H2_cost[i] == 1.147725104))
        s.add( If(G[h2_index] == 2340, raw_H2_cost[i] == 1.20038655))

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
