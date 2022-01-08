#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>

namespace py = pybind11;


class Comparator {
    public:
    virtual double compare() = 0;
};

PYBIND11_MODULE(_comparator,m) {

  m.doc() = "";
  m.attr("__name__") = "groupbyrule.comparator._comparator";

  py::class_<Comparator>(m, "Comparator")
        .def("compare", &Comparator::compare);
  
}