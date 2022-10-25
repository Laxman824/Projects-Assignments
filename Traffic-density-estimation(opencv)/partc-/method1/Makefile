all: method1.cpp
	g++ method1.cpp -o method1 -pthread -std=c++11 `pkg-config --cflags --libs opencv`

utility: utility-runtime.cpp
	g++ utility-runtime.cpp -o a.out

clean:
	rm -f method1

