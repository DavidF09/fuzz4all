#/bin/sh

# this script is to build gcc with coverage option
cd /home/coverage

git clone https://github.com/cvc5/cvc5 cvc5
cd cvc5
git checkout cvc5-1.0.5
./configure.sh debug --coverage --prefix=/home/coverage/CVC5-1.0.5-COVERAGE --auto-download

cd build
make -j 12
make install
