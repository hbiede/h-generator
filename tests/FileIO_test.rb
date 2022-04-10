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
      f.puts ''
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
    File.delete(file)
  end

  def test_write_h_file
    file = './temp.test_write_h_file.txt'
    FileIO.write_h_file(file, { 'a_:::_b' => 2, 'b_:::_c' => 1, 'c_:::_ation' => 3, 'd_:::_og' => 10, 'e_:::_gg' => 0 })
    assert_equal(true, File.exist?(file))

    assert_equal(%W[dog,d,og,10\n cation,c,ation,3\n ab,a,b,2\n bc,b,c,1\n], File.readlines(file))

    File.delete(file)
  end
end
