all: method4.cpp
	g++ method4.cpp -o method4 -pthread -std=c++11 `pkg-config --cflags --libs opencv`

utility: utility-runtime.cpp
	g++ utility-runtime.cpp -o a.out

clean:
	rm -f method4

