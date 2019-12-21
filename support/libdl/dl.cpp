#include "dl.h"

#include <dlfcn.h>
#include <vector>
#include <string>
#include <unordered_map>

using namespace dl_n;

namespace {
  struct dl_t {
    static inline dl_t& instance() {
      static dl_t i;

      return i;
    }

    inline void register_me(const table_t& tbl) {
      for (size_t i = 0; i < tbl.count; ++i) {
	auto sym = tbl.ptr[i];

	symbols[sym.name] = sym;
      }
      
      tables.push_back(tbl);
    }
    
    inline void* open(const char*, int) {
      return &symbols;
    }

    inline void* sym(void* hndl, const char* symbol) {
      if (!hndl) {
	return nullptr;
      }
      
      symbols_t& tbl = *(symbols_t*)hndl;

      auto it = tbl.find(symbol);

      if (it == tbl.end()) {
	return nullptr;
      }

      return it->second.addr;
    }

    using symbols_t = std::unordered_map<std::string, symbol_t>;
    
    symbols_t symbols;
    std::vector<table_t> tables;
  };
}

void dl_n::register_symbol_table(const table_t& tbl) {
  dl_t::instance().register_me(tbl);
}

extern "C" {
  int dlclose(void*) {
    return 0;
  }
  
  char* dlerror() {
    static char ret[] = "not found";
    
    return ret;
  }

  void* dlopen(const char* lib_name, int flags) {
    return dl_t::instance().open(lib_name, flags);
  }
  
  void* dlsym(void* hndl, const char* symbol) {
    return dl_t::instance().sym(hndl, symbol); 
  }
}
