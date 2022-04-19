# frozen_string_literal: true

# Author: Hundter Biede (hbiede.com)
# Version: 1.0
# License: MIT

# Defaults
$output_file = './output_frequency_table.txt'
$words_to_parse = '10000'
$must_match_alphabet = true

ERROR_CODES = {
  IMPOSSIBLE_COMBO: 3,
  INCOMPLETE_ARGS: 1,
  NO_SPACE: 2
}.freeze

# Handles all script arguments
class ArgParser
  # Checks if the argument pair is valid
  #
  # @param args [Array<String>] The arguments to check
  # @param index [Integer,NilClass] The index of the argument to check
  # @return [Boolean] true iff the argument pair is valid
  def self.valid_arg_pair(args, index)
    !index.nil? && index + 1 < args.length && !args[index + 1].start_with?('-')
  end

  # Checks that a value is a string representation of an integer
  #
  # @param value [String] the value to check
  # @return [Boolean] true iff the value is an integer represented as a string
  def self.valid_integer(value)
    value.gsub(
      /[_,]/, ''
    ).to_i.to_s == value.gsub(/[_,]/, '')
  end

  # Prints the help message text, formatted with default values
  #
  # @return [String] the help message text
  def self.generate_help_text
    # Read help doc from file
    format(
      File.read('./resources/help.txt'),
      { WordCount: $words_to_parse, OutputFile: $output_file, ProgramName: $PROGRAM_NAME }
    )
  end

  # Parse the script arguments to determine if the user asked for input help
  #
  # @param args [Array] The arguments passed to the script
  # @return [void]
  # @raise [SystemExit] If the help flag is used
  def self.parse_help(args)
    matching_arg = args.find { |arg| arg.match(/--help/) }
    return if matching_arg.nil?

    puts generate_help_text
    exit 0
  end

  # Parse for the alphabet input file path
  #
  # @param args [Array] The arguments to parse
  # @return [String] The path to the alphabet file
  # @raise [SystemExit] If the alphabet file path was input incorrectly
  def self.parse_g_input_file(args)
    matching_g_arg = args.find { |arg| arg.match(/-g|--alphabet/) }
    g_index = args.find_index(matching_g_arg)

    if matching_g_arg.nil? || !valid_arg_pair(args, g_index)
      warn 'Error: must include alphabet file'
      warn generate_help_text
      exit ERROR_CODES[:INCOMPLETE_ARGS]
    end
    args[g_index + 1]
  end

  # Parse for the frequency input file path
  #
  # @param args [Array] The arguments to parse
  # @return [String] The path to the frequency file
  # @raise [SystemExit] If the frequency file path is input incorrectly
  def self.parse_freq_input_file(args)
    matching_freq_arg = args.find { |arg| arg.match(/-f|--frequencies/) }
    freq_index = args.find_index(matching_freq_arg)

    if matching_freq_arg.nil? || !valid_arg_pair(args, freq_index)
      warn 'Must include frequency file'
      warn generate_help_text
      exit ERROR_CODES[:INCOMPLETE_ARGS]
    end
    args[freq_index + 1]
  end

  # Parse for the output input file path
  #
  # @param args [Array] The arguments to parse
  # @return [String] The path to the output file
  # @raise [SystemExit] If the output file path is input incorrectly
  def self.parse_output_file(args)
    matching_arg = args.find { |arg| arg.match(/-o|--output/) }
    return $output_file if matching_arg.nil?

    out_file_index = args.find_index(matching_arg) + 1
    if out_file_index >= args.length || args[out_file_index].start_with?('-')
      warn 'Invalid argument usage'
      warn generate_help_text
      exit ERROR_CODES[:INCOMPLETE_ARGS]
    end

    args[out_file_index]
  end

  # Parse for a required matching alphabet
  #
  # @param args [Array] The arguments to parse
  # @return [Boolean] True if must match the given alphabet for all words in frequency table
  # @raise [SystemExit] If the value is input incorrectly
  def self.parse_must_match_alphabet(args)
    matching_arg = args.find { |arg| arg.match(/-m|--match/) }
    return $must_match_alphabet if matching_arg.nil?

    out_file_index = args.find_index(matching_arg) + 1
    if out_file_index >= args.length || args[out_file_index].start_with?('-')
      warn 'Invalid argument usage'
      warn generate_help_text
      exit ERROR_CODES[:INCOMPLETE_ARGS]
    end

    args[out_file_index].downcase == 'true'
  end

  # Ensure word count args are valid
  #
  # @param args [Array] The arguments to parse
  # @param word_count_index [Integer] The index of the word count argument
  # @return [void]
  # @raise [SystemExit] If word count value is invalid
  def self.check_for_word_count_error(args, word_count_index)
    return unless !valid_arg_pair(args, word_count_index - 1) || !valid_integer(args[word_count_index])

    warn 'Invalid argument usage'
    warn generate_help_text
    exit ERROR_CODES[:INCOMPLETE_ARGS]
  end

  # Parse for the number of words to parse from the frequency file
  #
  # @param args [Array] The arguments to parse
  # @return [String] The number represented as a string
  def self.parse_word_count(args)
    matching_arg = args.find { |arg| arg.match(/-n|--words-to-parse/) }
    return $words_to_parse if matching_arg.nil?

    word_count_index = args.find_index(matching_arg) + 1
    check_for_word_count_error(args, word_count_index)

    args[word_count_index].gsub(/[_,]/, '')
  end

  # Parses all arguments and returns a list
  #
  # @param args [Array] list of arguments
  # @return [Array<String, Boolean>] list of arguments
  def self.parse_args(args)
    parse_help args
    g_in = parse_g_input_file args
    freq_in = parse_freq_input_file args
    out = parse_output_file args
    count = parse_word_count args
    must_match = parse_must_match_alphabet args
    [g_in, freq_in, out, count, must_match]
  end
end

# Read in the input files
class FileIO
  # Reads the frequency file into a mapping
  # Note: Contents are assumed to be in decreasing order of frequency
  #
  # @param file_path [String] The path to the frequency file
  # @param words_to_parse [Integer] The number of words to parse from the file
  # @return [Hash{String => Integer}] The mapping of words to frequencies
  def self.read_freq_file(frequency_file, words_to_parse)
    data = File.readlines(frequency_file).slice(0, words_to_parse.to_i)
    result = {}
    data.each do |line|
      trimmed = line.chomp
      if trimmed.length.positive?
        split = trimmed.split(/\s+/)
        result[split[0].upcase] = split[1].to_i
      end
    end
    result
  end

  # Reads in the alphabet file and returns a list of strings
  #
  # @param alphabet_file [String] The path to the alphabet file
  # @return [Array<String>] The list of strings
  # @raise [SystemExit] If the alphabet does not contain the space character
  def self.read_g_file(g_file)
    result = File.readlines(g_file).map { |line| line.chomp == ' ' ? ' ' : line.strip.upcase }.uniq.sort
    unless result.include?(' ')
      warn 'Error: alphabet file must contain the space character'
      exit ERROR_CODES[:NO_SPACE]
    end
    result
  end

  # Write the output file
  #
  # @param output_file [String] The file to write the data to
  # @param data [Hash{String => Integer}] The data to write to the output file
  # @return [void]
  def self.write_h_file(output_file, data)
    f = File.open(output_file, 'w')
    # Sort by negative frequency to get a descending order
    data
      .entries
      .filter { |_, value| value.positive? }
      .sort_by { |_, value| -value }
      .each do |key, value|
      g1, g2 = key.split('_:::_')
      f.puts "#{g1}#{g2},#{g1},#{g2},#{value}"
    end
    f.close
  end
end

# Generates the H set as a mapping of strings onto integers (initialized as 0)
class ComboGenerator
  # Generate the H mapping such that $ g_1 \in G, g_2 \in G, (g_1 + g_2) \notin G, (g_1 + g_2) \in H $
  #
  # @param g_set [Array<String>] The set of strings in G
  # @return [Hash{String => Integer}] The H mapping
  def self.generate_h(g_set)
    h_set = {}
    g_set.each do |g1|
      g_set.each do |g2|
        h_set["#{g1}_:::_#{g2}"] = 0 unless g_set.include?(g1 + g2)
      end
    end
    h_set
  end
end

# Generate the frequency mapping for H based on the occurrences of the frequency set
class FrequencyGenerator
  # Finds the longest possible string in the alphabet that is a prefix substring of the word to split
  #
  # @param word_to_split [String] The full word to split
  # @param curr [String] The current string to check. Expected to be a suffix substring of the word to split
  # @param g_set [Array<String>] The set of strings in the alphabet
  # @param must_succeed [Boolean] Whether or not the current string must be input-able from the current alphabet
  # @return [String] The longest possible string in the alphabet that is a prefix substring of the word to split
  # @raise [SystemExit] If the alphabet does not contain sufficient characters to map the space
  def self.find_greedy_next(word_to_split, curr, g_set, must_succeed)
    substrings = g_set.filter { |g| !Regexp.new("^#{g}").match(curr).nil? }
    if substrings.length.zero?
      if must_succeed
        warn "Error: #{word_to_split} is not possible to type with the alphabet"
        exit ERROR_CODES[:IMPOSSIBLE_COMBO]
      end
      return ''
    end
    # Not possible for this to be nil due to prior checks
    # noinspection RubyMismatchedReturnType
    substrings.max_by(&:length)
  end

  # Performs a greedy selection split on the word to split
  # Note: The resulting array will always be suffixed and prefixed with the space character
  #
  # @param word_to_split [String] The word to split
  # @param g_set [Array<String>] The set of strings in the alphabet
  # @param must_match [Boolean] Whether or not the alphabet must be able to map the word
  # @return [Array<String>] The resulting array of strings
  def self.theta_splitter(word_to_split, g_set, must_match)
    curr = word_to_split
    result = [' ']
    while curr.length.positive?
      next_piece = find_greedy_next(word_to_split, curr, g_set, must_match)
      return [] if next_piece.empty?

      result << next_piece
      curr = curr.gsub(Regexp.new("^#{next_piece}"), '')
    end
    result << ' '
    result
  end

  # Parse a word into the substrings used to enter it, and append the frequencies of adjacent chords to H
  #
  # @param word [String] The word to split
  # @param freq [Integer] The number of times `word` appears in the frequency data set
  # @param g_set [Array<String>] The alphabet set
  # @param h_set [Hash{String => Integer}] The H set mapping
  # @param must_match [Boolean] Whether or not the alphabet must be able to map the word
  # @return [void]
  # @raise [SystemExit] If the alphabet does not contain sufficient characters to map the space
  def self.add_to_h_set(word, freq, g_set, h_set, must_match)
    parts = theta_splitter(word, g_set, must_match)
    return if parts.empty?

    parts[0, parts.length - 1].each_with_index do |part, i|
      concat = "#{part}_:::_#{parts[i + 1]}"
      unless h_set.key? concat
        warn "Error: #{concat} is not a possible combination in the given alphabet"
        exit ERROR_CODES[:IMPOSSIBLE_COMBO]
      end
      h_set[concat] += freq
    end
  end

  # Generate the H mapping based on the frequency data set
  #
  # @param g_set [Array<String>] The alphabet set
  # @param h_set [Hash{String => Integer}] The H mapping
  # @param freq_set [Hash{String => Integer}] The frequency data set
  # @param must_match [Boolean] Whether or not the alphabet must be able to map the word
  # @return [void]
  def self.generate_frequency_set(g_set, h_set, freq_set, must_match)
    freq_set.each_pair do |key, value|
      add_to_h_set(key, value, g_set, h_set, must_match)
    end
  end
end

# :nocov:
# Run the full script
#
# @return [void]
def main(args)
  (g_in, freq_in, out, count, must_match) = ArgParser.parse_args args
  out = out.to_i

  freq_list = FileIO.read_freq_file(freq_in, count)
  g_set = FileIO.read_g_file(g_in)

  h_set = ComboGenerator.generate_h g_set
  FrequencyGenerator.generate_frequency_set(g_set, h_set, freq_list, must_match)

  FileIO.write_h_file(out, h_set)
end

main ARGV if __FILE__ == $PROGRAM_NAME
# :nocov:
