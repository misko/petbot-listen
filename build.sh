#gcc -o listen_for_bark -lasound -lfftw3 -lm ./listen_for_bark.c -O3
gcc -o listen_for_bark -lasound -lfftw3 -lm ./listen_for_bark.c ./model.c -O3  -Wall
gcc -o run_model -lasound -lfftw3 -lm run_model.c ./model.c -Wall -O3 -Wall 
gcc -o capture -lasound -lfftw3 -lm ./capture2.c -O3
