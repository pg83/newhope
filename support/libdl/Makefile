CXX = clang++
AR = llvm-ar
RANLIB = llvm-ranlib
NM = llvm-nm
CXXFLAGS = -O2
LDFLAGS =
LIBS =
MY_FLAGS = -std=c++14 -fno-rtti -fno-exceptions

dl.o: dl.cpp dl.h Makefile
	$(CXX) $(CXXFLAGS) $(MY_FLAGS) -c dl.cpp -o dl.o

libdl.o: libdl.cpp dl.h
	$(CXX) -I. $(CXXFLAGS) $(MY_FLAGS) -c libdl.cpp -o libdl.o

libdl.cpp: dl.o
	(echo '#define DL_DEF(X)\ ' && ($(NM) dl.o | grep ' T ' | awk '{print $$3}'| while read line; do echo "  X($$line)\\"; done) && echo && echo && echo '#include <dl.h>') > libdl.cpp.t && mv libdl.cpp.t libdl.cpp

libdl.a: libdl.o dl.o
	(rm -rf libdl.a || true) && $(AR) q libdl.a libdl.o dl.o && $(RANLIB) libdl.a

install: libdl.a test
	./test && (mkdir -p $(DESTDIR)/lib || true) && (mkdir -p $(DESTDIR)/include || true) && cp libdl.a $(DESTDIR)/lib && cp dl.h $(DESTDIR)/include

test: test.cpp libdl.a
	$(CXX) -I. $(CXXFLAGS) $(MY_FLAGS) -L. $(LDFLAGS) $(LIBS) -Wl,--whole-archive -ldl test.cpp

clean:
	rm *.o *.a libdl.cpp

all: libdl.a test
