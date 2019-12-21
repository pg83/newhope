#pragma once

#include <stddef.h>

namespace dl_n {
  struct symbol_t {
    void* addr;
    const char* name;
  };
  
  struct table_t {
    const symbol_t* ptr;
    size_t count;
    const char* lib_name;
  };

  void register_symbol_table(const table_t& tbl);

  struct init_t {
    inline init_t(const symbol_t* ptr, size_t count, const char* lib_name) {
      register_symbol_table(table_t{ptr, count, lib_name});
    }
  };
}

#define XSTR(s) STR(s)
#define STR(s) #s

#define DL_BEG namespace { ::dl_n::symbol_t symbols[] = {
#define DL_END }; static const ::dl_n::init_t initializer(symbols, sizeof(symbols) / sizeof(symbols[0]), __FILE__); }
#define DL_SYM(x) {(void*)&x, XSTR(x)},
#define DL_EXP(x) extern "C" void x();

#if defined(DL_DEF)
DL_DEF(DL_EXP)
DL_BEG
DL_DEF(DL_SYM)
DL_END
#endif
