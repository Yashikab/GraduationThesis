#!/bin/sh

CC=g++
OPT="-I/usr/include/python3.6m -DPIC -shared -fPIC"

$CC $OPT -o distbasic.so distcoresets.cpp -lboost_python-py36 -lpython3.6m
$CC $OPT -o basic.so coresets.cpp -lboost_python-py36 -lpython3.6m
