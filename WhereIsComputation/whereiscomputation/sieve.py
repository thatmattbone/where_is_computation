

def sieve(max_n):
    """
    Return a list of prime numbers up to `max_n.`

    This is implemented with the sieve of Eratosthenes:
    http://en.wikipedia.org/wiki/Sieve_of_Eratosthenes

    :param max_num:
    :return:
    """
    number_map = {n: 0 for n in range(2, max_n + 1)}

    for n in number_map.keys():
        current_n = n + n
        while current_n < max_n:
            number_map[current_n] += 1
            current_n += n

    return [n for n, count in number_map.items() if count == 0]


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


ONE_HUNDRED_PRIMES = [
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
    101,
    103,
    107,
    109,
    113,
    127,
    131,
    137,
    139,
    149,
    151,
    157,
    163,
    167,
    173,
    179,
    181,
    191,
    193,
    197,
    199,
    211,
    223,
    227,
    229,
    233,
    239,
    241,
    251,
    257,
    263,
    269,
    271,
    277,
    281,
    283,
    293,
    307,
    311,
    313,
    317,
    331,
    337,
    347,
    349,
    353,
    359,
    367,
    373,
    379,
    383,
    389,
    397,
    401,
    409,
    419,
    421,
    431,
    433,
    439,
    443,
    449,
    457,
    461,
    463,
    467,
    479,
    487,
    491,
    499,
    503,
    509,
    521,
    523,
    541,
    ]
ONE_HUNDRED_PRIME_STRINGS = [str(prime) for prime in ONE_HUNDRED_PRIMES]
LAST_PRIME = ONE_HUNDRED_PRIMES[-1]
