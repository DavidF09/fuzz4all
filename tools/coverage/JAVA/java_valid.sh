#!/bin/bash

JAVA_17=$HOME/.sdkman/candidates/java/17.0.2-open/bin/javac

loc=$1
TEST_SUITE_RES=$2

JAVAC_TEST=$(find $loc -type f -name "*.java")

mkdir -p $TEST_SUITE_RES
cd $TEST_SUITE_RES
TEST_SUITE_RES=$(pwd)
cd ..

run_javac () {
    work_dir=$(pwd)
    iter=$1
    dir=$(dirname $2)
    program=$(basename $2)
    cd $dir
    echo $dir
    echo $program
    timeout 5 $JAVA_17 $program
    status=$?
    # append status to array
    echo $status >> $TEST_SUITE_RES/javac_valid_$iter.txt
    cd $work_dir
}

counter=0
for program in $JAVAC_TEST; do
    counter=$((counter+1))
    run_javac $counter $program
done
cd $TEST_SUITE_RES
