# Creation Process

1. Take list of top 90 n-grams for each n [1,9] (total of 746 n-grams)
1. Run `gen_h.rb`
1. Reduce resulting H (using utility script listed below to convert H into a G ->
   frequency mapping)
    - Eliminate infrequently used n-grams from G
1. Repeat until full set fits in desired set size (ensuring the full alphabet always
   remains)


## Utility Script for Sorting G

```ruby
def read
  lines = File.readlines ARGV[0]
  g = {}
  lines.each do |line|
    split = line.split ','
    g[split[1]] = g[split[1]].nil? ? split[3].to_i : (g[split[1]] + split[3].to_i)
    g[split[2]] = g[split[2]].nil? ? split[3].to_i : (g[split[2]] + split[3].to_i)
  end
  g.sort_by { |_k, v| v }.reverse
  g.each do |g1|
    puts "#{g1[0]},#{g1[1]}"
  end
end

read
```
