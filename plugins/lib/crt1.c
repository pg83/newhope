#include <features.h>
#include "libc.h"

#define START "_start"

#include "crt_arch.h"

int main();
int _Z4mainiPPc();
int _Z4mainiPPKc();
int _Z4mainiPKPKc();
int _Z4maini();
int _Z4main();
int _Z4mainv();

#pragma weak main
#pragma	weak _Z4mainiPPc
#pragma weak _Z4mainiPPKc
#pragma weak _Z4mainiPKPKc
#pragma weak _Z4mainv
#pragma weak _Z4maini
#pragma weak _Z4main

#define checkf(x) if (x) {return x;}

static void* get_main() {
  checkf(main);
  checkf(_Z4mainiPPc);
  checkf(_Z4mainiPPKc);
  checkf(_Z4mainiPKPKc);
  checkf(_Z4maini);
  checkf(_Z4main);
  checkf(_Z4mainv);

  abort();
}

weak void _init();
weak void _fini();
int __libc_start_main(int (*)(), int, char **,
	void (*)(), void(*)(), void(*)());

void _start_c(long *p)
{
	int argc = p[0];
	char **argv = (void *)(p+1);
	__libc_start_main(get_main(), argc, argv, _init, _fini, 0);
}
