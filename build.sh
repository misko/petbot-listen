#gcc -o listen_for_bark -lasound -lfftw3 -lm ./listen_for_bark.c -O3
gcc -o listen_for_bark -lasound -lfftw3 -lm ./listen_for_bark.c ./model.c -O3  -Wall
gcc -o capture -lasound -lfftw3 -lm ./capture2.c -O3
