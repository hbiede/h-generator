# frozen_string_literal: true

# Author: Hundter Biede (hbiede.com)
# Version: 1.0
# License: MIT
require_relative '../gen_h'
require_relative './helper'

# noinspection RubyResolve
class TestFrequencyGenerator < Test::Unit::TestCase
  def test_find_greedy_next
    word_to_split = 'therefore'
    g_set = %w[the t he re ere fo f for e o]

    assert_equal('the', FrequencyGenerator.find_greedy_next(word_to_split, 'the', g_set))
    assert_equal('the', FrequencyGenerator.find_greedy_next(word_to_split, 'therefore', g_set))
    assert_equal('he', FrequencyGenerator.find_greedy_next(word_to_split, 'herefore', g_set))
    assert_equal('ere', FrequencyGenerator.find_greedy_next(word_to_split, 'erefore', g_set))
    assert_equal('re', FrequencyGenerator.find_greedy_next(word_to_split, 'refore', g_set))
    assert_equal('e', FrequencyGenerator.find_greedy_next(word_to_split, 'efore', g_set))
    assert_equal('for', FrequencyGenerator.find_greedy_next(word_to_split, 'fore', g_set))
    assert_equal('o', FrequencyGenerator.find_greedy_next(word_to_split, 'ore', g_set))
    assert_equal('re', FrequencyGenerator.find_greedy_next(word_to_split, 're', g_set))
    assert_equal('e', FrequencyGenerator.find_greedy_next(word_to_split, 'e', g_set))
  end

  def test_theta_splitter
    g_set = %w[the t he re ere fo f for e o]
    assert_equal([' ', 'the', 're', 'for', 'e', ' '], FrequencyGenerator.theta_splitter('therefore', g_set))
    assert_equal([' ', 'the', ' '], FrequencyGenerator.theta_splitter('the', g_set))
    assert_equal([' ', 'he', 're', ' '], FrequencyGenerator.theta_splitter('here', g_set))
    # Errors on words that are impossible given the g_set
    assert_raise(SystemExit) { FrequencyGenerator.theta_splitter('wherefore', g_set) }
    assert_raise(SystemExit) { FrequencyGenerator.theta_splitter('alphabet', g_set) }
    assert_raise(SystemExit) { FrequencyGenerator.theta_splitter('test', g_set) }
  end

  def test_add_to_h_set
    g_set = ['the', 't', 'he', 're', 'ere', 'fo', 'f', 'for', 'e', 'o', ' ']
    initial_h_set = {
      'the_:::_re' => 0,
      'he_:::_re' => 0,
      're_:::_for' => 0,
      'for_:::_e' => 0,
      ' _:::_the' => 0,
      ' _:::_he' => 0,
      're_:::_ ' => 0,
      'e_:::_ ' => 0
    }
    new_h = initial_h_set.clone
    FrequencyGenerator.add_to_h_set('there', 10, g_set, new_h)
    assert_equal({
                   **initial_h_set,
                   'the_:::_re' => 10,
                   ' _:::_the' => 10,
                   're_:::_ ' => 10
                 }, new_h)

    new_h = initial_h_set.clone
    FrequencyGenerator.add_to_h_set('here', 25, g_set, new_h)
    assert_equal({
                   **initial_h_set,
                   'he_:::_re' => 25,
                   ' _:::_he' => 25,
                   're_:::_ ' => 25
                 }, new_h)

    new_h = initial_h_set.clone
    FrequencyGenerator.add_to_h_set('therefore', 1000, g_set, new_h)
    assert_equal({
                   **initial_h_set,
                   'the_:::_re' => 1000,
                   ' _:::_the' => 1000,
                   're_:::_for' => 1000,
                   'for_:::_e' => 1000,
                   'e_:::_ ' => 1000
                 }, new_h)

    assert_raise(SystemExit) { FrequencyGenerator.add_to_h_set('error', 1000, ['error'], initial_h_set.clone) }
  end

  def test_generate_frequency_set
    g_set = ['the', 't', 'he', 're', 'ere', 'fo', 'f', 'for', 'e', 'o', ' ']
    initial_h_set = {
      'the_:::_re' => 0,
      'he_:::_re' => 0,
      're_:::_for' => 0,
      'for_:::_e' => 0,
      ' _:::_the' => 0,
      ' _:::_he' => 0,
      're_:::_ ' => 0,
      'e_:::_ ' => 0
    }
    new_h = initial_h_set.clone
    FrequencyGenerator.generate_frequency_set(g_set, new_h, { 'there' => 30, 'here' => 50 })
    assert_equal({ **initial_h_set,
                   ' _:::_the' => 30,
                   ' _:::_he' => 50,
                   'the_:::_re' => 30,
                   'he_:::_re' => 50,
                   're_:::_ ' => 80 }, new_h)
  end
end
