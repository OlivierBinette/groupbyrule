#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>

#include "_jaro.cpp"

namespace py = pybind11;
using namespace std;

class JaroWinkler: public StringComparator {
public:

  bool similarity;

  JaroWinkler(bool similarity=false){
    this->similarity = similarity;
  }

  double jarowinkler(const string &s, const string &t, double p=0.1) {
      int ell = 0;
      for (int i = 0; i < 4; i++) {
          if (s[i] == t[i]){
              ell += 1;
          } else {
              break;
          }
      }

      double sim = Jaro::jaro(s, t);

      return sim + ell * p * (1-sim);
  }

  double compare(const string &s, const string &t) {
      if (this->similarity == true) {
          return jarowinkler(s, t);
      } else { 
          return 1.0 - jarowinkler(s, t);
      } 
  }
  
};


PYBIND11_MODULE(_jarowinkler,m) {

  m.doc() = "";
  m.attr("__name__") = "groupbyrule.comparator._jarowinkler";

  py::class_<JaroWinkler, StringComparator>(m, "JaroWinkler")
        .def(py::init<bool>(), py::arg("similarity")=false)
        .def("compare", &JaroWinkler::compare);

}
