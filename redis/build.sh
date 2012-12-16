#!/bin/bash

##creating patchfile (for development)
#git clone https://github.com/antirez/redis.git
#git checkout 2.6.7
##if making new changes, stage everything
#git diff HEAD -p >sieve.patch

#get redis 2.6.7
wget http://redis.googlecode.com/files/redis-2.6.7.tar.gz
tar xzf redis-2.6.7.tar.gz
cd redis-2.6.7

#patch it
patch -p1 < ../sieve.patch

#build it
make
