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
    for i in range(len(n.G) - 1):
        s.add( [ G[i] != G[j] for j in range(i + 1, len(n.G)) ] )

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
        s.add( Or(raw_G_cost[i] == 0.538116592, raw_G_cost[i] == 0.674157303, raw_G_cost[i] == 0.97722577675, raw_G_cost[i] == 0.465116279, raw_G_cost[i] == 0.7889248097499999, raw_G_cost[i] == 0.594059406, raw_G_cost[i] == 0.8771034055, raw_G_cost[i] == 0.537003738, raw_G_cost[i] == 0.8068966744999999, raw_G_cost[i] == 0.97694756325, raw_G_cost[i] == 1.11147671125, raw_G_cost[i] == 0.78753374225, raw_G_cost[i] == 0.9231757442499999, raw_G_cost[i] == 0.876825192, raw_G_cost[i] == 1.01135434, raw_G_cost[i] == 0.470588235, raw_G_cost[i] == 0.7902927987499999, raw_G_cost[i] == 0.9603436875, raw_G_cost[i] == 1.0948728355, raw_G_cost[i] == 0.7045143635, raw_G_cost[i] == 0.9065718684999999, raw_G_cost[i] == 0.86022131625, raw_G_cost[i] == 0.9947504642499999, raw_G_cost[i] == 0.52173913, raw_G_cost[i] == 0.8030805225, raw_G_cost[i] == 0.97313141125, raw_G_cost[i] == 1.10766055925, raw_G_cost[i] == 0.7684529822500001, raw_G_cost[i] == 0.91935959225, raw_G_cost[i] == 0.8730090399999999, raw_G_cost[i] == 1.0075381879999998, raw_G_cost[i] == 0.526762113, raw_G_cost[i] == 0.8043362682499999, raw_G_cost[i] == 0.974387157, raw_G_cost[i] == 1.108916305, raw_G_cost[i] == 0.774731711, raw_G_cost[i] == 0.920615338, raw_G_cost[i] == 0.8742647857499999, raw_G_cost[i] == 1.0087939337499998, raw_G_cost[i] == 0.80294520075, raw_G_cost[i] == 0.93858720275, raw_G_cost[i] == 1.1086380915, raw_G_cost[i] == 1.2431672395, raw_G_cost[i] == 0.9192242705, raw_G_cost[i] == 1.0548662725, raw_G_cost[i] == 1.00851572025, raw_G_cost[i] == 1.1430448682499998, raw_G_cost[i] == 0.7760997, raw_G_cost[i] == 0.921983327, raw_G_cost[i] == 1.09203421575, raw_G_cost[i] == 1.22656336375, raw_G_cost[i] == 0.89237876975, raw_G_cost[i] == 1.03826239675, raw_G_cost[i] == 0.9919118444999999, raw_G_cost[i] == 1.1264409924999998, raw_G_cost[i] == 0.78888742375, raw_G_cost[i] == 0.93477105075, raw_G_cost[i] == 1.1048219394999998, raw_G_cost[i] == 1.2393510874999998, raw_G_cost[i] == 0.9051664935, raw_G_cost[i] == 1.0510501205, raw_G_cost[i] == 1.00469956825, raw_G_cost[i] == 1.1392287162499999, raw_G_cost[i] == 0.452830189, raw_G_cost[i] == 0.7858532872499999, raw_G_cost[i] == 0.955904176, raw_G_cost[i] == 1.090433324, raw_G_cost[i] == 0.694602896, raw_G_cost[i] == 0.9021323569999999, raw_G_cost[i] == 0.8557818047499999, raw_G_cost[i] == 0.9903109527499999, raw_G_cost[i] == 0.78446221975, raw_G_cost[i] == 0.92010422175, raw_G_cost[i] == 1.0901551105, raw_G_cost[i] == 1.2246842585, raw_G_cost[i] == 0.9007412895, raw_G_cost[i] == 1.0363832915, raw_G_cost[i] == 0.9900327392499999, raw_G_cost[i] == 1.12456188725, raw_G_cost[i] == 0.701442841, raw_G_cost[i] == 0.903500346, raw_G_cost[i] == 1.07355123475, raw_G_cost[i] == 1.20808038275, raw_G_cost[i] == 0.81772191075, raw_G_cost[i] == 1.01977941575, raw_G_cost[i] == 0.9734288634999999, raw_G_cost[i] == 1.1079580115, raw_G_cost[i] == 0.76538145975, raw_G_cost[i] == 0.91628806975, raw_G_cost[i] == 1.0863389584999998, raw_G_cost[i] == 1.2208681064999998, raw_G_cost[i] == 0.8816605295000001, raw_G_cost[i] == 1.0325671395, raw_G_cost[i] == 0.9862165872499999, raw_G_cost[i] == 1.1207457352499999, raw_G_cost[i] == 0.560747664, raw_G_cost[i] == 0.8354637279999999, raw_G_cost[i] == 0.98288354475, raw_G_cost[i] == 1.1174126927499999, raw_G_cost[i] == 0.81721364975, raw_G_cost[i] == 0.95174279775, raw_G_cost[i] == 0.8827611734999999, raw_G_cost[i] == 1.0172903215, raw_G_cost[i] == 0.8351855145, raw_G_cost[i] == 0.9697146624999999, raw_G_cost[i] == 1.11713447925, raw_G_cost[i] == 1.2516636272500001, raw_G_cost[i] == 0.95146458425, raw_G_cost[i] == 1.08599373225, raw_G_cost[i] == 1.0170121079999999, raw_G_cost[i] == 1.151541256, raw_G_cost[i] == 0.81858163875, raw_G_cost[i] == 0.9531107867499999, raw_G_cost[i] == 1.1005306035, raw_G_cost[i] == 1.2350597515000001, raw_G_cost[i] == 0.9348607085, raw_G_cost[i] == 1.0693898565, raw_G_cost[i] == 1.0004082322499999, raw_G_cost[i] == 1.13493738025, raw_G_cost[i] == 0.8313693625, raw_G_cost[i] == 0.9658985105, raw_G_cost[i] == 1.11331832725, raw_G_cost[i] == 1.24784747525, raw_G_cost[i] == 0.9476484322500001, raw_G_cost[i] == 1.08217758025, raw_G_cost[i] == 1.013195956, raw_G_cost[i] == 1.147725104))
        s.add( Or( Not( G[i] == 2),    raw_G_cost[i] == 0.538116592))
        s.add( Or( Not( G[i] == 8),    raw_G_cost[i] == 0.674157303))
        s.add( Or( Not( G[i] == 10),   raw_G_cost[i] == 0.97722577675))
        s.add( Or( Not( G[i] == 16),   raw_G_cost[i] == 0.465116279))
        s.add( Or( Not( G[i] == 18),   raw_G_cost[i] == 0.7889248097499999))
        s.add( Or( Not( G[i] == 32),   raw_G_cost[i] == 0.594059406))
        s.add( Or( Not( G[i] == 34),   raw_G_cost[i] == 0.8771034055))
        s.add( Or( Not( G[i] == 64),   raw_G_cost[i] == 0.537003738))
        s.add( Or( Not( G[i] == 66),   raw_G_cost[i] == 0.8068966744999999))
        s.add( Or( Not( G[i] == 72),   raw_G_cost[i] == 0.97694756325))
        s.add( Or( Not( G[i] == 74),   raw_G_cost[i] == 1.11147671125))
        s.add( Or( Not( G[i] == 80),   raw_G_cost[i] == 0.78753374225))
        s.add( Or( Not( G[i] == 82),   raw_G_cost[i] == 0.9231757442499999))
        s.add( Or( Not( G[i] == 96),   raw_G_cost[i] == 0.876825192))
        s.add( Or( Not( G[i] == 98),   raw_G_cost[i] == 1.01135434))
        s.add( Or( Not( G[i] == 128),  raw_G_cost[i] == 0.470588235))
        s.add( Or( Not( G[i] == 130),  raw_G_cost[i] == 0.7902927987499999))
        s.add( Or( Not( G[i] == 136),  raw_G_cost[i] == 0.9603436875))
        s.add( Or( Not( G[i] == 138),  raw_G_cost[i] == 1.0948728355))
        s.add( Or( Not( G[i] == 144),  raw_G_cost[i] == 0.7045143635))
        s.add( Or( Not( G[i] == 146),  raw_G_cost[i] == 0.9065718684999999))
        s.add( Or( Not( G[i] == 160),  raw_G_cost[i] == 0.86022131625))
        s.add( Or( Not( G[i] == 162),  raw_G_cost[i] == 0.9947504642499999))
        s.add( Or( Not( G[i] == 256),  raw_G_cost[i] == 0.52173913))
        s.add( Or( Not( G[i] == 258),  raw_G_cost[i] == 0.8030805225))
        s.add( Or( Not( G[i] == 264),  raw_G_cost[i] == 0.97313141125))
        s.add( Or( Not( G[i] == 266),  raw_G_cost[i] == 1.10766055925))
        s.add( Or( Not( G[i] == 272),  raw_G_cost[i] == 0.7684529822500001))
        s.add( Or( Not( G[i] == 274),  raw_G_cost[i] == 0.91935959225))
        s.add( Or( Not( G[i] == 288),  raw_G_cost[i] == 0.8730090399999999))
        s.add( Or( Not( G[i] == 290),  raw_G_cost[i] == 1.0075381879999998))
        s.add( Or( Not( G[i] == 512),  raw_G_cost[i] == 0.526762113))
        s.add( Or( Not( G[i] == 514),  raw_G_cost[i] == 0.8043362682499999))
        s.add( Or( Not( G[i] == 520),  raw_G_cost[i] == 0.974387157))
        s.add( Or( Not( G[i] == 522),  raw_G_cost[i] == 1.108916305))
        s.add( Or( Not( G[i] == 528),  raw_G_cost[i] == 0.774731711))
        s.add( Or( Not( G[i] == 530),  raw_G_cost[i] == 0.920615338))
        s.add( Or( Not( G[i] == 544),  raw_G_cost[i] == 0.8742647857499999))
        s.add( Or( Not( G[i] == 546),  raw_G_cost[i] == 1.0087939337499998))
        s.add( Or( Not( G[i] == 576),  raw_G_cost[i] == 0.80294520075))
        s.add( Or( Not( G[i] == 578),  raw_G_cost[i] == 0.93858720275))
        s.add( Or( Not( G[i] == 584),  raw_G_cost[i] == 1.1086380915))
        s.add( Or( Not( G[i] == 586),  raw_G_cost[i] == 1.2431672395))
        s.add( Or( Not( G[i] == 592),  raw_G_cost[i] == 0.9192242705))
        s.add( Or( Not( G[i] == 594),  raw_G_cost[i] == 1.0548662725))
        s.add( Or( Not( G[i] == 608),  raw_G_cost[i] == 1.00851572025))
        s.add( Or( Not( G[i] == 610),  raw_G_cost[i] == 1.1430448682499998))
        s.add( Or( Not( G[i] == 640),  raw_G_cost[i] == 0.7760997))
        s.add( Or( Not( G[i] == 642),  raw_G_cost[i] == 0.921983327))
        s.add( Or( Not( G[i] == 648),  raw_G_cost[i] == 1.09203421575))
        s.add( Or( Not( G[i] == 650),  raw_G_cost[i] == 1.22656336375))
        s.add( Or( Not( G[i] == 656),  raw_G_cost[i] == 0.89237876975))
        s.add( Or( Not( G[i] == 658),  raw_G_cost[i] == 1.03826239675))
        s.add( Or( Not( G[i] == 672),  raw_G_cost[i] == 0.9919118444999999))
        s.add( Or( Not( G[i] == 674),  raw_G_cost[i] == 1.1264409924999998))
        s.add( Or( Not( G[i] == 768),  raw_G_cost[i] == 0.78888742375))
        s.add( Or( Not( G[i] == 770),  raw_G_cost[i] == 0.93477105075))
        s.add( Or( Not( G[i] == 776),  raw_G_cost[i] == 1.1048219394999998))
        s.add( Or( Not( G[i] == 778),  raw_G_cost[i] == 1.2393510874999998))
        s.add( Or( Not( G[i] == 784),  raw_G_cost[i] == 0.9051664935))
        s.add( Or( Not( G[i] == 786),  raw_G_cost[i] == 1.0510501205))
        s.add( Or( Not( G[i] == 800),  raw_G_cost[i] == 1.00469956825))
        s.add( Or( Not( G[i] == 802),  raw_G_cost[i] == 1.1392287162499999))
        s.add( Or( Not( G[i] == 1024), raw_G_cost[i] == 0.452830189))
        s.add( Or( Not( G[i] == 1026), raw_G_cost[i] == 0.7858532872499999))
        s.add( Or( Not( G[i] == 1032), raw_G_cost[i] == 0.955904176))
        s.add( Or( Not( G[i] == 1034), raw_G_cost[i] == 1.090433324))
        s.add( Or( Not( G[i] == 1040), raw_G_cost[i] == 0.694602896))
        s.add( Or( Not( G[i] == 1042), raw_G_cost[i] == 0.9021323569999999))
        s.add( Or( Not( G[i] == 1056), raw_G_cost[i] == 0.8557818047499999))
        s.add( Or( Not( G[i] == 1058), raw_G_cost[i] == 0.9903109527499999))
        s.add( Or( Not( G[i] == 1088), raw_G_cost[i] == 0.78446221975))
        s.add( Or( Not( G[i] == 1090), raw_G_cost[i] == 0.92010422175))
        s.add( Or( Not( G[i] == 1096), raw_G_cost[i] == 1.0901551105))
        s.add( Or( Not( G[i] == 1098), raw_G_cost[i] == 1.2246842585))
        s.add( Or( Not( G[i] == 1104), raw_G_cost[i] == 0.9007412895))
        s.add( Or( Not( G[i] == 1106), raw_G_cost[i] == 1.0363832915))
        s.add( Or( Not( G[i] == 1120), raw_G_cost[i] == 0.9900327392499999))
        s.add( Or( Not( G[i] == 1122), raw_G_cost[i] == 1.12456188725))
        s.add( Or( Not( G[i] == 1152), raw_G_cost[i] == 0.701442841))
        s.add( Or( Not( G[i] == 1154), raw_G_cost[i] == 0.903500346))
        s.add( Or( Not( G[i] == 1160), raw_G_cost[i] == 1.07355123475))
        s.add( Or( Not( G[i] == 1162), raw_G_cost[i] == 1.20808038275))
        s.add( Or( Not( G[i] == 1168), raw_G_cost[i] == 0.81772191075))
        s.add( Or( Not( G[i] == 1170), raw_G_cost[i] == 1.01977941575))
        s.add( Or( Not( G[i] == 1184), raw_G_cost[i] == 0.9734288634999999))
        s.add( Or( Not( G[i] == 1186), raw_G_cost[i] == 1.1079580115))
        s.add( Or( Not( G[i] == 1280), raw_G_cost[i] == 0.76538145975))
        s.add( Or( Not( G[i] == 1282), raw_G_cost[i] == 0.91628806975))
        s.add( Or( Not( G[i] == 1288), raw_G_cost[i] == 1.0863389584999998))
        s.add( Or( Not( G[i] == 1290), raw_G_cost[i] == 1.2208681064999998))
        s.add( Or( Not( G[i] == 1296), raw_G_cost[i] == 0.8816605295000001))
        s.add( Or( Not( G[i] == 1298), raw_G_cost[i] == 1.0325671395))
        s.add( Or( Not( G[i] == 1312), raw_G_cost[i] == 0.9862165872499999))
        s.add( Or( Not( G[i] == 1314), raw_G_cost[i] == 1.1207457352499999))
        s.add( Or( Not( G[i] == 2048), raw_G_cost[i] == 0.560747664))
        s.add( Or( Not( G[i] == 2050), raw_G_cost[i] == 0.8354637279999999))
        s.add( Or( Not( G[i] == 2056), raw_G_cost[i] == 0.98288354475))
        s.add( Or( Not( G[i] == 2058), raw_G_cost[i] == 1.1174126927499999))
        s.add( Or( Not( G[i] == 2064), raw_G_cost[i] == 0.81721364975))
        s.add( Or( Not( G[i] == 2066), raw_G_cost[i] == 0.95174279775))
        s.add( Or( Not( G[i] == 2080), raw_G_cost[i] == 0.8827611734999999))
        s.add( Or( Not( G[i] == 2082), raw_G_cost[i] == 1.0172903215))
        s.add( Or( Not( G[i] == 2112), raw_G_cost[i] == 0.8351855145))
        s.add( Or( Not( G[i] == 2114), raw_G_cost[i] == 0.9697146624999999))
        s.add( Or( Not( G[i] == 2120), raw_G_cost[i] == 1.11713447925))
        s.add( Or( Not( G[i] == 2122), raw_G_cost[i] == 1.2516636272500001))
        s.add( Or( Not( G[i] == 2128), raw_G_cost[i] == 0.95146458425))
        s.add( Or( Not( G[i] == 2130), raw_G_cost[i] == 1.08599373225))
        s.add( Or( Not( G[i] == 2144), raw_G_cost[i] == 1.0170121079999999))
        s.add( Or( Not( G[i] == 2146), raw_G_cost[i] == 1.151541256))
        s.add( Or( Not( G[i] == 2176), raw_G_cost[i] == 0.81858163875))
        s.add( Or( Not( G[i] == 2178), raw_G_cost[i] == 0.9531107867499999))
        s.add( Or( Not( G[i] == 2184), raw_G_cost[i] == 1.1005306035))
        s.add( Or( Not( G[i] == 2186), raw_G_cost[i] == 1.2350597515000001))
        s.add( Or( Not( G[i] == 2192), raw_G_cost[i] == 0.9348607085))
        s.add( Or( Not( G[i] == 2194), raw_G_cost[i] == 1.0693898565))
        s.add( Or( Not( G[i] == 2208), raw_G_cost[i] == 1.0004082322499999))
        s.add( Or( Not( G[i] == 2210), raw_G_cost[i] == 1.13493738025))
        s.add( Or( Not( G[i] == 2304), raw_G_cost[i] == 0.8313693625))
        s.add( Or( Not( G[i] == 2306), raw_G_cost[i] == 0.9658985105))
        s.add( Or( Not( G[i] == 2312), raw_G_cost[i] == 1.11331832725))
        s.add( Or( Not( G[i] == 2314), raw_G_cost[i] == 1.24784747525))
        s.add( Or( Not( G[i] == 2320), raw_G_cost[i] == 0.9476484322500001))
        s.add( Or( Not( G[i] == 2322), raw_G_cost[i] == 1.08217758025))
        s.add( Or( Not( G[i] == 2336), raw_G_cost[i] == 1.013195956))
        s.add( Or( Not( G[i] == 2338), raw_G_cost[i] == 1.147725104))

def stride_stutter_count(G_count, G, G_D, s, n, p):
    for i in range(len(n.G)):
        matching_h2 = []
        for j in range(len(n.H)):
            if n.G[i] == n.H2[j]:
                matching_h2.append(j)
        s.add(
            G_count[i] == Sum([ 
                If(G_D[h1_index] & G_D[h2_index] == 0, p.stride, # Stride discount
                If(G_D[h1_index] & G[h2_index] == G[h1_index] & G_D[h2_index], p.stutter, # Stutter discount
                1.0)) * # No stride or stutter discount
                raw_H2_cost[i] * n.HF[i] for j in matching_h2])
        )

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

def add_up_cumulative_cost(cumulative_cost, discounted_H_cost, s, n):
    print(f"G Size: {len(n.G)}, H Size: {len(n.H)}")
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

    # The raw cost of pressing each g.
    raw_G_cost = [ Real('rc%s' % i) for i in range(len(n.G)) ]
    chord_cost(raw_G_cost, G, s, n)

    # The count of each H, possibly reduced by stride or stutter.
    G_count = [ Int('g_cnt%s' % i) for i in range(len(n.G)) ]
    stride_stutter_count(G_count, G, G_D, s, n, p)

    # The cost of each H according to stride, stutter, and conflict, multiplied by frequency.
    discounted_H_cost = [ Real('dc%s' % i) for i in range(len(n.H)) ]
    stride_stutter_discount(raw_H2_cost, discounted_H_cost, G, G_D, s, n, p)
    
    cumulative_cost = [ Real('cc%s' % i) for i in range(len(n.H)) ]
    add_up_cumulative_cost(cumulative_cost, discounted_H_cost, s, n)

    return Buttons(G=G, G_D=G_D, discounted_H_cost=discounted_H_cost, cumulative_cost=cumulative_cost)
