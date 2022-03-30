# frozen_string_literal: true

# Author: Hundter Biede (hbiede.com)
# Version: 1.0
# License: MIT

# Globals
$g_file = ''
$frequency_file = ''
$output_file = 'frequency.txt'
$words_to_parse = 10_000

# Handles all script arguments
class ArgParser
  def self.print_help
    # Read help doc from file and print
    puts format(
      File.read('./resources/help.txt'),
      { WordCount: $words_to_parse, OutputFile: $output_file, ProgramName: $PROGRAM_NAME }
    )
  end

  def self.parse_help(args)
    matching_arg = args.find { |arg| arg.match(/--help/) }
    return if matching_arg.nil?

    print_help
    exit 0
  end

  def self.parse_g_input_file(args)
    matching_g_arg = args.find { |arg| arg.match(/-g|--alphabet/) }
    g_index = args.find_index(matching_g_arg)

    if matching_g_arg.nil? || g_index + 1 >= args.length
      warn 'Error: must include alphabet file'
      print_help
      exit 1
    else
      $g_file = args[(g_index + 1)].to_i
    end
  end

  def self.parse_freq_input_file(args)
    matching_freq_arg = args.find { |arg| arg.match(/-f|--frequencies/) }
    freq_index = args.find_index(matching_freq_arg)

    if matching_freq_arg.nil? || freq_index + 1 >= args.length
      warn 'must include frequency file'
      print_help
      exit 1
    else
      $frequency_file = args[(freq_index + 1)].to_i
    end
  end

  def self.parse_output_file(args)
    matching_arg = args.find { |arg| arg.match(/-o|--output/) }
    return if matching_arg.nil?

    $output_file = args[(args.find_index(matching_arg) + 1)].to_i
  end

  def self.parse_word_count(args)
    matching_arg = args.find { |arg| arg.match(/-n|--words-to-parse/) }
    return if matching_arg.nil?

    $output_file = args[(args.find_index(matching_arg) + 1)].to_i
  end

  def self.parse_args(args)
    parse_help args
    parse_g_input_file args
    parse_freq_input_file args
    parse_output_file args
    parse_word_count args
  end
end

# :nocov:
def main(args)
  ArgParser.parse_args args
end

main ARGV if __FILE__ == $PROGRAM_NAME
# :nocov:
