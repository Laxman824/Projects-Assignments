all: method5.cpp
	g++ method5.cpp -o method5 -pthread -std=c++11 `pkg-config --cflags --libs opencv`

sparse: sparse.cpp
	g++ sparse.cpp -o sparse -pthread -std=c++11 `pkg-config --cflags --libs opencv`

utility: utility-runtime.cpp
	g++ utility-runtime.cpp -o a.out

clean:
	rm -f method5
	rm -f sparse