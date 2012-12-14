import redis

sieve_lua = """\
local max_n = tonumber(ARGV[1])
local number_map = {}
for n = 2, max_n + 1 do
   number_map[n] = 0
end

for n, value in pairs(number_map) do
   local current_n = n + n
   while current_n < max_n do
      number_map[current_n] = number_map[current_n] + 1
      current_n = current_n + n
   end
end

local primes = {}
for n, value in pairs(number_map) do
   if value == 0 then
      table.insert(primes, n)
   end
end
return primes
"""

if __name__ == "__main__":
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    sieve = r.register_script(sieve_lua)
    print(sieve(args=[100]))
