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
