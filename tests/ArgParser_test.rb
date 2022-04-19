# frozen_string_literal: true

# Author: Hundter Biede (hbiede.com)
# Version: 1.0
# License: MIT
require_relative '../gen_h'
require_relative './helper'

# noinspection RubyResolve
class TestArgParser < Test::Unit::TestCase
  def test_generate_help_text
    assert_false(ArgParser.generate_help_text.empty?)
  end

  def test_parse_help
    assert_raise(SystemExit) { ArgParser.parse_help(%w[--help]) }
    assert_raise(SystemExit) { ArgParser.parse_help(%w[-n 1000 --help]) }

    assert_nothing_raised { ArgParser.parse_help(%w[]) }
    assert_nothing_raised { ArgParser.parse_help(%w[-n 1000]) }
    assert_nothing_raised { ArgParser.parse_help(%w[-n 1000 -g text.txt]) }
  end

  def test_parse_g_input_file
    assert_raise(SystemExit) { ArgParser.parse_g_input_file(%w[--help]) }
    assert_raise(SystemExit) { ArgParser.parse_g_input_file(%w[]) }
    assert_raise(SystemExit) { ArgParser.parse_g_input_file(%w[-n 1000 -o text_out.txt]) }
    assert_raise(SystemExit) { ArgParser.parse_g_input_file(%w[-g]) }
    assert_raise(SystemExit) { ArgParser.parse_g_input_file(%w[-g -n 1000]) }
    assert_raise(SystemExit) { ArgParser.parse_g_input_file(%w[-n 1000 -o text_out.txt -g]) }
    assert_raise(SystemExit) { ArgParser.parse_g_input_file(%w[--alphabet]) }
    assert_raise(SystemExit) { ArgParser.parse_g_input_file(%w[-n 1000 -o text_out.txt --alphabet]) }

    assert_nothing_raised { ArgParser.parse_g_input_file(%w[-g text.txt]) }
    assert_equal('text.txt', ArgParser.parse_g_input_file(%w[-g text.txt]))
    assert_nothing_raised { ArgParser.parse_g_input_file(%w[--alphabet ./data/test/input_text.txt]) }
    assert_equal('./data/test/input_text.txt', ArgParser.parse_g_input_file(%w[--alphabet ./data/test/input_text.txt]))
  end

  def test_parse_freq_input_file
    assert_raise(SystemExit) { ArgParser.parse_freq_input_file(%w[--help]) }
    assert_raise(SystemExit) { ArgParser.parse_freq_input_file(%w[]) }
    assert_raise(SystemExit) { ArgParser.parse_freq_input_file(%w[-n 1000 -o text_out.txt]) }
    assert_raise(SystemExit) { ArgParser.parse_freq_input_file(%w[-f]) }
    assert_raise(SystemExit) { ArgParser.parse_freq_input_file(%w[-n 1000 -o text_out.txt -f]) }
    assert_raise(SystemExit) { ArgParser.parse_freq_input_file(%w[--frequencies]) }
    assert_raise(SystemExit) { ArgParser.parse_freq_input_file(%w[--frequencies -n 1000]) }
    assert_raise(SystemExit) { ArgParser.parse_freq_input_file(%w[-n 1000 -o text_out.txt --frequencies]) }

    assert_nothing_raised { ArgParser.parse_freq_input_file(%w[-f text.txt]) }
    assert_equal('text.txt', ArgParser.parse_freq_input_file(%w[-f text.txt]))
    assert_nothing_raised { ArgParser.parse_freq_input_file(%w[--frequencies ./data/test/input_text.txt]) }
    assert_equal('./data/test/input_text.txt',
                 ArgParser.parse_freq_input_file(%w[--frequencies ./data/test/input_text.txt]))
  end

  def test_parse_output_file
    assert_nothing_raised { ArgParser.parse_output_file([]) }
    assert_equal('./output_frequency_table.txt', ArgParser.parse_output_file([]))
    assert_nothing_raised { ArgParser.parse_output_file(%w[-o text.txt]) }
    assert_equal('text.txt', ArgParser.parse_output_file(%w[-o text.txt]))
    assert_nothing_raised { ArgParser.parse_output_file(%w[--words-to-parse ./data/test/output_text.txt]) }
    assert_equal('./data/test/output_text.txt', ArgParser.parse_output_file(%w[--output ./data/test/output_text.txt]))

    assert_raise(SystemExit) { ArgParser.parse_output_file(%w[-o]) }
    assert_raise(SystemExit) { ArgParser.parse_output_file(%w[--output]) }
    assert_raise(SystemExit) { ArgParser.parse_output_file(%w[-o -n 1000]) }
    assert_raise(SystemExit) { ArgParser.parse_output_file(%w[--output -n 1000]) }
  end

  def test_parse_word_count
    assert_nothing_raised { ArgParser.parse_word_count([]) }
    assert_equal('10000', ArgParser.parse_word_count([]))
    assert_nothing_raised { ArgParser.parse_word_count(%w[-o test.txt]) }
    assert_equal('10000', ArgParser.parse_word_count(%w[-o test.txt]))
    assert_equal('10000', ArgParser.parse_word_count([]))
    assert_nothing_raised { ArgParser.parse_word_count(%w[-n 1000]) }
    assert_equal('1000', ArgParser.parse_word_count(%w[-n 1000]))
    assert_nothing_raised { ArgParser.parse_word_count(%w[--words-to-parse 123]) }
    assert_equal('123', ArgParser.parse_word_count(%w[--words-to-parse 123]))
    assert_nothing_raised { ArgParser.parse_word_count(%w[--words-to-parse 100_000]) }
    assert_equal('100000', ArgParser.parse_word_count(%w[--words-to-parse 100_000]))
    assert_nothing_raised { ArgParser.parse_word_count(%w[--words-to-parse 12,000]) }
    assert_equal('12000', ArgParser.parse_word_count(%w[--words-to-parse 12,000]))

    assert_raise(SystemExit) { ArgParser.parse_word_count(%w[-n]) }
    assert_raise(SystemExit) { ArgParser.parse_word_count(%w[--words-to-parse]) }
    assert_raise(SystemExit) { ArgParser.parse_word_count(%w[-n -o test.txt]) }
    assert_raise(SystemExit) { ArgParser.parse_word_count(%w[--words-to-parse -o test.txt]) }
    assert_raise(SystemExit) { ArgParser.parse_word_count(%w[-n not_a_number]) }
    assert_raise(SystemExit) { ArgParser.parse_word_count(%w[--words-to-parse not_a_number]) }
  end

  def test_parse_must_match_alphabet
    assert_nothing_raised { ArgParser.parse_must_match_alphabet(%w[--match true]) }
    assert_equal(true, ArgParser.parse_must_match_alphabet(%w[--match true]))
    assert_nothing_raised { ArgParser.parse_must_match_alphabet(%w[--match TRUE]) }
    assert_equal(true, ArgParser.parse_must_match_alphabet(%w[--match TRUE]))
    assert_nothing_raised { ArgParser.parse_must_match_alphabet(%w[--match True]) }
    assert_equal(true, ArgParser.parse_must_match_alphabet(%w[--match True]))
    assert_nothing_raised { ArgParser.parse_must_match_alphabet(%w[-m true]) }
    assert_equal(true, ArgParser.parse_must_match_alphabet(%w[-m true]))
    assert_nothing_raised { ArgParser.parse_must_match_alphabet(%w[--match false]) }
    assert_equal(false, ArgParser.parse_must_match_alphabet(%w[--match false]))
    assert_nothing_raised { ArgParser.parse_must_match_alphabet(%w[-m false]) }
    assert_equal(false, ArgParser.parse_must_match_alphabet(%w[-m false]))

    assert_raise(SystemExit) { ArgParser.parse_must_match_alphabet(%w[-m]) }
    assert_raise(SystemExit) { ArgParser.parse_must_match_alphabet(%w[--match]) }
    assert_raise(SystemExit) { ArgParser.parse_must_match_alphabet(%w[-m -o test.txt]) }
    assert_raise(SystemExit) { ArgParser.parse_must_match_alphabet(%w[--match -o test.txt]) }
  end

  def test_parse_args
    assert_nothing_raised do
      ArgParser.parse_args(%w[--words-to-parse 12,000 -o ./test.txt -f ./data/freq.txt -g alphabet.txt])
    end
    assert_equal(['alphabet.txt', './data/freq.txt', './test.txt', '12000', true],
                 ArgParser.parse_args(%w[--words-to-parse 12,000 -o ./test.txt -f ./data/freq.txt -g alphabet.txt]))
    assert_equal(['alphabet.txt', './data/freq.txt', './test.txt', '12000', false],
                 ArgParser.parse_args(%w[--words-to-parse 12,000 -o ./test.txt -f ./data/freq.txt -g alphabet.txt
                                         --match false]))
    assert_raise(SystemExit) do
      ArgParser.parse_args(%w[--words-to-parse -o ./test.txt -f ./data/freq.txt -g alphabet.txt --help])
    end
  end
end
