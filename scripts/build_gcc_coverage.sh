#/bin/sh

# this script is to build gcc with coverage option
cd /home/coverage

git clone git://gcc.gnu.org/git/gcc.git gcc-13
cd gcc-13
git checkout releases/gcc-13.1.0
./contrib/download_prerequisites

mkdir ../gcc-coverage-build
cd ../gcc-coverage-build
./../gcc-13/configure --enable-languages=c,c++ --prefix=/home/coverage/GCC-13-COVERAGE --enable-coverage

make -j 12
make install
