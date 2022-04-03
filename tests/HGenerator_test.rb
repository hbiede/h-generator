# frozen_string_literal: true

# Author: Hundter Biede (hbiede.com)
# Version: 1.0
# License: MIT
require_relative '../gen_h'
require_relative './helper'

# noinspection RubyResolve
class TestHGenerator < Test::Unit::TestCase
  def test_generate_h
    g_set = [' ', 'a', 'b', 'c', 'tion', 're', 'ation', 'are']
    expected_h = {
      '  ' => 0,
      ' a' => 0,
      ' b' => 0,
      ' c' => 0,
      ' tion' => 0,
      ' re' => 0,
      ' ation' => 0,
      ' are' => 0,
      'a ' => 0,
      'aa' => 0,
      'ab' => 0,
      'ac' => 0,
      'aation' => 0,
      'aare' => 0,
      'b ' => 0,
      'ba' => 0,
      'bb' => 0,
      'bc' => 0,
      'btion' => 0,
      'bre' => 0,
      'bation' => 0,
      'bare' => 0,
      'c ' => 0,
      'ca' => 0,
      'cb' => 0,
      'cc' => 0,
      'ction' => 0,
      'cre' => 0,
      'cation' => 0,
      'care' => 0,
      'tion ' => 0,
      'tiona' => 0,
      'tionb' => 0,
      'tionc' => 0,
      'tiontion' => 0,
      'tionre' => 0,
      'tionation' => 0,
      'tionare' => 0,
      're ' => 0,
      'rea' => 0,
      'reb' => 0,
      'rec' => 0,
      'retion' => 0,
      'rere' => 0,
      'reation' => 0,
      'reare' => 0,
      'ation ' => 0,
      'ationa' => 0,
      'ationb' => 0,
      'ationc' => 0,
      'ationtion' => 0,
      'ationre' => 0,
      'ationation' => 0,
      'ationare' => 0,
      'are ' => 0,
      'area' => 0,
      'areb' => 0,
      'arec' => 0,
      'aretion' => 0,
      'arere' => 0,
      'areation' => 0,
      'areare' => 0
    }
    assert_equal(expected_h, HGenerator.generate_h(g_set))
  end
end
