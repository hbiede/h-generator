# frozen_string_literal: true

# Author: Hundter Biede (hbiede.com)
# Version: 1.0
# License: MIT
require_relative '../gen_h'
require_relative './helper'

# noinspection RubyResolve
class TestFileIO < Test::Unit::TestCase
  def test_read_freq_file
    file = './temp.test_read_freq_file.txt'

    File.open(file, 'w') do |f|
      f.puts 'THE 1000000'
      f.puts "there\t230123"
      f.puts 'Here      47614'
      f.puts 'where 11234'
    end

    result = FileIO.read_freq_file(file, 10)
    expected = {
      'THE' => 1_000_000,
      'THERE' => 230_123,
      'HERE' => 47_614,
      'WHERE' => 11_234
    }
    assert_equal(expected, result)

    result = FileIO.read_freq_file(file, 3)
    expected = {
      'THE' => 1_000_000,
      'THERE' => 230_123,
      'HERE' => 47_614
    }
    assert_equal(expected, result)

    File.delete(file)
  end

  def test_read_g_file
    file = './temp.test_read_g_file.txt'

    File.open(file, 'w') do |f|
      f.puts 'THE '
      f.puts ' THERE'
      f.puts 'HERE'
      f.puts 'here '
      f.puts ' Here'
      f.puts 'hERE'
      f.puts 'a'
      f.puts ' b '
      f.puts 'c'
      f.puts 'd'
      f.puts 'D '
      f.puts ' '
    end

    result = FileIO.read_g_file(file)
    expected = [' ', 'A', 'B', 'C', 'D', 'HERE', 'THE', 'THERE']
    assert_equal(expected, result)
    File.delete(file)

    File.open(file, 'w') do |f|
      f.puts 'THE'
    end
    # Must have a space character
    assert_raise(SystemExit) { FileIO.read_g_file(file) }
  end

  def test_write_h_file
    file = './temp.test_write_h_file.txt'
    FileIO.write_h_file(file, { 'a' => 2, 'b' => 1, 'c' => 3, 'd' => 10, 'e' => 0 })
    assert_equal(true, File.exist?(file))

    assert_equal(%W[d,10\n c,3\n a,2\n b,1\n e,0\n], File.readlines(file))

    File.delete(file)
  end
end
