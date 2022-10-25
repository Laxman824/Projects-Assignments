all: method2.cpp
	g++ method2.cpp -o method2 -pthread -std=c++11 `pkg-config --cflags --libs opencv`

utility: utility-runtime.cpp
	g++ utility-runtime.cpp -o a.out

clean:
	rm -f method2

