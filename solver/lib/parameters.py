from dataclasses import dataclass, field
from datetime import datetime, timedelta

# ***************************************
# Guide the Search
# ***************************************
# This problem is too big for the solver to find a solution to by itself in a
#   reasonable amount of time. So we play with these variables to find a good solution.
@dataclass
class Parameters:
    # We want a model with a low cost. The solver will search this range for the lowest cost
    #   it can find. It will quit once the difference between the lowest satisfiable (sat)
    #   solution and the highest unsatisfiable/timeout (unsat/unknown) is less than the
    #   resolution.
    # cost_hi: int = 20000000
    # cost_lo: int = 0
    cost_hi: int = 31092424832503900
    cost_lo: int = 5624260931670580
    cost_res: int = 1
    # -Easy SAT and clearly UNSAT problems are solved quickly.
    # -The solver learns more from solving SAT problems.
    #   Therefore search begins at cost_hi and decreases each time by initial_hi_to_lo_ratio_step_up.
    #   Once the first UNSAT or UNKNOWN is encountered, after_failure_step_up_ratio is used instead.
    #   Set initial_hi_to_lo_ratio_step_up to zero to enter after_failure_step_up_ratio immediately.
    initial_hi_to_lo_ratio_step_up: float = 1/1000
    #   After first failure increase guess more conservatively.
    after_failure_step_up_ratio: float = 1/10
    # The number of miliseconds the solver should spend on any single iteration.
    #   Higher is better and slower.
    timeout: timedelta = timedelta(hours=2)
    # After a solver query is SAT, UNSAT, or UNKNOWN only print update to screen
    #   if at least update_time has passed since last printed update.
    #   First solver query always prints.
    update_time: timedelta = timedelta(minutes=5)
    # After a solver query is SAT only print update to file if at least sat_time
    #   has passed since last sat printed to file.
    sat_time: timedelta = timedelta(minutes=10)
    # Contains the strings that will have chords assigned to them.
    G_file: str = "G.txt"
    # Frequency files to load:
    H_file: str = "H.txt"
    # Striding is assumed to be faster than normal, this is the discount given to strides.
    #   https://github.com/lancegatlin/typemax/blob/master/basic_layout_design.md#stride
    stride: float = 0.5
    # Stuttering is assumed to be faster than normal, this is the discount given to stutters.
    #   https://github.com/lancegatlin/typemax/blob/master/basic_layout_design.md#stutter
    stutter: float = 0.75

    # Finger to reserve for switching between numbers, symbols, and alphabet.
    reserved_finger: str = "pinky"

    def setup():
        print("---------------------------------------------------------------------------------------------")
        p = Parameters()
        assert p.cost_hi > p.cost_lo
        assert p.cost_hi - p.cost_lo > p.cost_res
        print(f'Hi: {p.cost_hi}, Lo: {p.cost_lo}, Resolution: {p.cost_res}')
        print(f'Timeout: {p.timeout}, Update Time: {p.update_time}, SAT Update Time: {p.sat_time}')
        print(f"Stride discount: {p.stride}, Stutter discount: {p.stutter}")
        print(f"Reserved finger: {p.reserved_finger}")
        # min_print_time replaced with update_time and sat_time. No need to print those out.
        # print(f"If not last SAT solution print to STDOUT and file only if timer exceeds: {p.min_print_time}")
        print("---------------------------------------------------------------------------------------------")
        return p

    def initial_step_up(self) -> float:
        return (self.cost_hi - self.cost_lo) * self.initial_hi_to_lo_ratio_step_up

    def after_failure_step_up(self, hi, low) -> float:
        return hi - (hi - low) * self.after_failure_step_up_ratio

