import sys
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
    # cost_hi: int = 17227064385339908 # Reachable upper bound for standard H
    cost_hi: int =   10000000000000000 # Upper bound for G_24
    # cost_hi: int =   3000000000000000 # Upper bound for G_16 and G_12
    cost_lo: int =  1
    cost_res: int = 1
    # -Easy SAT and clearly UNSAT problems are solved quickly.
    # -The solver learns more from solving SAT problems.
    #   Therefore search begins at cost_hi and decreases each time by initial_hi_to_lo_ratio_step_up.
    #   Once the first UNSAT or UNKNOWN is encountered, after_failure_step_up_ratio is used instead.
    #   Set initial_hi_to_lo_ratio_step_up to zero to enter after_failure_step_up_ratio immediately.
    initial_hi_to_lo_ratio_step_up: float = 1/100000000
    #   After first failure increase guess more conservatively.
    after_failure_step_up_ratio: float = 1/100000000
    # The number of miliseconds the solver should spend on any single iteration.
    #   Higher is better and slower.
    timeout: timedelta = timedelta(hours=5)
    # After a solver query is SAT, UNSAT, or UNKNOWN only print update to screen
    #   if at least update_time has passed since last printed update.
    #   Prevents screen from being spammed with lots of SATs when problem is easy.
    #   First solver query always prints.
    update_time: timedelta = timedelta(seconds=0.01)
    # After a solver query is SAT only print update to file if at least sat_time
    #   has passed since last sat printed to file.
    #   Prevents output file from being spammed with lots of SATs when problem is easy.
    sat_time: timedelta = timedelta(seconds=0.01)
    # Program will stop after max_time has been exceeded. This includes time of all runs,
    #   but does not include setup time.
    #   Will even quit mid-solve if max_time has been exceeded, but timeout has not.
    max_time: timedelta = timedelta(hours=5)
    # Contains the strings that will have chords assigned to them.
    G_file: str = "input/G_24.txt"
    # Frequency files to load:
    H_file: str = "input/H_24.txt"
    # Striding is assumed to be faster than normal, this is the discount given to strides.
    #   https://github.com/lancegatlin/typemax/blob/master/basic_layout_design.md#stride
    stride: float = 0.5
    # Stuttering is assumed to be faster than normal, this is the discount given to stutters.
    #   https://github.com/lancegatlin/typemax/blob/master/basic_layout_design.md#stutter
    stutter: float = 0.75

    # Finger to reserve for switching between numbers, symbols, and alphabet.
    reserved_finger: str = "pinky"

    def print_parameters(self, handle):
        print("---------------------------------------------------------------------------------------------", file=handle)
        print(f'Hi: {self.cost_hi}, Lo: {self.cost_lo}, Resolution: {self.cost_res}, Max Time: {self.max_time}', file=handle)
        print(f'Timeout: {self.timeout}, Update Time: {self.update_time}, SAT Update Time: {self.sat_time}', file=handle)
        print(f"Stride discount: {self.stride}, Stutter discount: {self.stutter}", file=handle)
        print(f"Reserved finger: {self.reserved_finger}", file=handle)
        print("---------------------------------------------------------------------------------------------", file=handle)

    def setup():
        p = Parameters()
        assert p.cost_hi > p.cost_lo
        assert p.cost_hi - p.cost_lo > p.cost_res
        p.print_parameters(sys.stdout)
        p.print_parameters(sys.stderr)
        return p

    def initial_step_up(self) -> float:
        return (self.cost_hi - self.cost_lo) * self.initial_hi_to_lo_ratio_step_up

    def after_failure_step_up(self, hi, low) -> float:
        return hi - (hi - low) * self.after_failure_step_up_ratio

