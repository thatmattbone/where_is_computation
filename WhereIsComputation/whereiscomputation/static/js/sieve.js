/**
 * Return a list of prime numbers up to `max_n.`
 *
 * This is implemented with the sieve of Eratosthenes:
 * http://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
 *
 * @param maxN
 * @return {Array}
 */
function sieve(maxN) {
    var n, numberMap = {}, primes = [];

    for(n=2; n <= maxN; n++) {
        numberMap[n] = 0;
    }

    for(n=2; n <= maxN; n++) {
        var currentN = n + n;
        while(currentN <= maxN) {
            numberMap[currentN] += 1;
            currentN += n;
        }
    }

    for(n in numberMap) {
        if(numberMap[n] === 0) {
            primes.push(parseInt(n));
        }
    }

    primes.sort(function(a, b) { return a -b; });
    return primes;
}
