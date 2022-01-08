#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>

namespace py = pybind11;

template <class dtype>
class Comparator {
    public:
    virtual double compare(const dtype s, const dtype t);
};

class StringComparator: public Comparator<std::string> {};

template<class T>
void declare_comparator(py::module &m, std::string name) {
    py::class_<T>(m, name.c_str())
        .def("compare", &T::compare);
}

PYBIND11_MODULE(_comparator, m) {

    m.doc() = "";
    m.attr("__name__") = "groupbyrule.comparator._comparator";

    declare_comparator<Comparator<py::object>>(m, "Comparator");
    declare_comparator<StringComparator>(m, "StringComparator");
}
