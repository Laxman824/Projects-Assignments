all: method3.cpp
	g++ method3.cpp -o method3 -pthread -std=c++11 `pkg-config --cflags --libs opencv`

utility: utility-runtime.cpp
	g++ utility-runtime.cpp -o a.out

clean:
	rm -f method3

