

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


