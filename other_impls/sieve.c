#include <stdio.h>
#include <assert.h>
#include <string.h>

#define MAX_PRIME 100000

void sieve(int max_n, short primes[MAX_PRIME]) {
  short zero = 0;
  memset(primes, zero, MAX_PRIME);

  for(int n=2; n<max_n; n++) {
    int current_n = n + n;
    while(current_n < max_n) {
      primes[current_n] = 1;
      current_n += n;
    }
  }
}

int main(void) {
  int max_n = 100;
  short primes[MAX_PRIME];
  assert(max_n < MAX_PRIME);
  
  sieve(100, primes);
  
  for(int i=2; i<max_n; i++) {
    if(primes[i] == 0) {
      printf("%i, ", i);
    }
  }
  printf("\n");
  
  return 0;
}
