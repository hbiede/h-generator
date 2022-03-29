# frozen_string_literal: true

# Author: Hundter Biede (hbiede.com)
# Version: 1.0
# License: MIT

# Globals
$g_file = ''
$frequency_file = ''
$output_file = 'frequency.txt'
$words_to_parse = 10_000

def print_help
  error_message = 'Example usage: ruby %<ProgramName>s -g alphabet.txt, -f freqs.txt'
  error_message += "\n\nFlags:"
  error_message += "\n\t-g,--alphabet: Specifies the alphabet of inputs allowed"
  error_message += "\n\t-f,--frequencies: Defined the frequencies of all words to be tested against. Assumed to be in"
  error_message += 'sorted from most to least common'
  error_message += "\n\t-n,--words-to-parse: [Optional] Number of words in the frequency file to parse. Default: %<WordCount>s"
  error_message += "\n\t-o,--output: [Optional] Output file to write to. Default: %<OutputFile>s"
  puts format(error_message, { WordCount: $words_to_parse, OutputFile: $output_file, ProgramName: $PROGRAM_NAME })
end

def parse_help
  matching_arg = ARGV.find { |arg| arg.match(/--help/) }
  return if matching_arg.nil?

  print_help
  exit 0
end

def parse_g_input_file
  matching_g_arg = ARGV.find { |arg| arg.match(/-g|--alphabet/) }
  g_index = ARGV.find_index(matching_g_arg)

  if matching_g_arg.nil? || g_index + 1 >= ARGV.length
    warn 'must include alphabet file'
    print_help
    exit 1
  else
    $g_file = ARGV[(g_index + 1)].to_i
  end
end

def parse_freq_input_file
  matching_freq_arg = ARGV.find { |arg| arg.match(/-f|--frequencies/) }
  freq_index = ARGV.find_index(matching_freq_arg)

  if matching_freq_arg.nil? || freq_index + 1 >= ARGV.length
    warn 'must include frequency file'
    print_help
    exit 1
  else
    $frequency_file = ARGV[(freq_index + 1)].to_i
  end
end

def parse_output_file
  matching_arg = ARGV.find { |arg| arg.match(/-o|--output/) }
  return if matching_arg.nil?

  $output_file = ARGV[(ARGV.find_index(matching_arg) + 1)].to_i
end

def parse_word_count
  matching_arg = ARGV.find { |arg| arg.match(/-n|--words-to-parse/) }
  return if matching_arg.nil?

  $output_file = ARGV[(ARGV.find_index(matching_arg) + 1)].to_i
end

def parse_args
  parse_help
  parse_g_input_file
  parse_freq_input_file
  parse_output_file
  parse_word_count
end
