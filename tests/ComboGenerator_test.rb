# frozen_string_literal: true

# Author: Hundter Biede (hbiede.com)
# Version: 1.0
# License: MIT
require_relative '../gen_h'
require_relative './helper'

# noinspection RubyResolve
class TestComboGenerator < Test::Unit::TestCase
  def test_generate_h
    g_set = [' ', 'a', 'b', 'c', 'tion', 're', 'ation', 'are']
    expected_h = {
      ' _:::_ ' => 0,
      ' _:::_a' => 0,
      ' _:::_b' => 0,
      ' _:::_c' => 0,
      ' _:::_tion' => 0,
      ' _:::_re' => 0,
      ' _:::_ation' => 0,
      ' _:::_are' => 0,
      'a_:::_ ' => 0,
      'a_:::_a' => 0,
      'a_:::_b' => 0,
      'a_:::_c' => 0,
      'a_:::_ation' => 0,
      'a_:::_are' => 0,
      'b_:::_ ' => 0,
      'b_:::_a' => 0,
      'b_:::_b' => 0,
      'b_:::_c' => 0,
      'b_:::_tion' => 0,
      'b_:::_re' => 0,
      'b_:::_ation' => 0,
      'b_:::_are' => 0,
      'c_:::_ ' => 0,
      'c_:::_a' => 0,
      'c_:::_b' => 0,
      'c_:::_c' => 0,
      'c_:::_tion' => 0,
      'c_:::_re' => 0,
      'c_:::_ation' => 0,
      'c_:::_are' => 0,
      'tion_:::_ ' => 0,
      'tion_:::_a' => 0,
      'tion_:::_b' => 0,
      'tion_:::_c' => 0,
      'tion_:::_tion' => 0,
      'tion_:::_re' => 0,
      'tion_:::_ation' => 0,
      'tion_:::_are' => 0,
      're_:::_ ' => 0,
      're_:::_a' => 0,
      're_:::_b' => 0,
      're_:::_c' => 0,
      're_:::_tion' => 0,
      're_:::_re' => 0,
      're_:::_ation' => 0,
      're_:::_are' => 0,
      'ation_:::_ ' => 0,
      'ation_:::_a' => 0,
      'ation_:::_b' => 0,
      'ation_:::_c' => 0,
      'ation_:::_tion' => 0,
      'ation_:::_re' => 0,
      'ation_:::_ation' => 0,
      'ation_:::_are' => 0,
      'are_:::_ ' => 0,
      'are_:::_a' => 0,
      'are_:::_b' => 0,
      'are_:::_c' => 0,
      'are_:::_tion' => 0,
      'are_:::_re' => 0,
      'are_:::_ation' => 0,
      'are_:::_are' => 0
    }
    assert_equal(expected_h, ComboGenerator.generate_h(g_set))
  end
end
