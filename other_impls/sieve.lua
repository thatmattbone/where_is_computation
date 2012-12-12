function sieve(max_n)
   number_map = {}
   for n = 2, max_n + 1 do
      number_map[n] = 0
   end

   for n, value in pairs(number_map) do
      current_n = n + n
      while current_n < max_n do
         number_map[current_n] = number_map[current_n] + 1
         current_n = current_n + n
      end
   end

   primes = {}
   for n, value in pairs(number_map) do
      if value == 0 then
         table.insert(primes, n)
      end
   end
   return primes
end

for index, prime in pairs(sieve(100)) do
   print(prime)
end

print(table.concat(sieve(100), ", "))