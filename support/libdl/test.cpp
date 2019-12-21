#include <dlfcn.h>

int main() {
  auto hndl = dlopen("dl", 0);
  auto sym = (void (*)(void*))dlsym(hndl, "dlclose");

  sym(hndl);
}
