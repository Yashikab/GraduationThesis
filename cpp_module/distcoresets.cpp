//#include "boost/numpy.hpp"
#include <iostream>
#include <boost/python.hpp>
#include <stdexcept>
#include <algorithm>
#define EPSILON 0.01
#define D 10

namespace py = boost::python;

int N = 10000;
int N1, N2;

double data[2][10000][D];

void datalen(int num1, int num2){
	N1 = num1;
    N2 = num2;
	
}
void inputdata(py::list& set_A, py::list& set_B)
{
	
	// input data
	for(int i = 0; i < N1; i++){
		for(int j = 0; j < D; j++){
			data[0][i][j] = py::extract<double>(set_A[i][j]);
			// data[node][1][i][j] = py::extract<double>(set_B[i][j]);
		}
	}
    for(int i = 0; i < N2; i++){
		for(int j = 0; j < D; j++){
			// data[node][0][i][j] = py::extract<double>(set_A[i][j]);
			data[1][i][j] = py::extract<double>(set_B[i][j]);
		}
	}
}

py::list dotlist(py::list& x1,py::list& x2, int AB){
    switch(AB){
        case 0:
            N = N1;
            break;
        case 1:
            N = N2;
            break;
    }
	double cppx1[D],x2_x1[D];
	for(int i=0; i < D; i++){
		cppx1[i] = py::extract<double>(x1[i]);
		x2_x1[i] = py::extract<double>(x2[i]) - py::extract<double>(x1[i]);
	}
	double x_l2 = 0.0;
	for(int i=0; i < D; i++){
		x_l2 += x2_x1[i]*x2_x1[i];
	}
	x_l2 = std::sqrt(x_l2);

	py::list return_list;
	for(int i=0; i < N; i++){
		double dot = 0;
		for(int j=0; j < D;j++){
			dot+=x2_x1[j]*(data[AB][i][j]-cppx1[j]);
			
		}
		return_list.append(dot/(double)x_l2);
	}
	return return_list;
}
py::list l2list(py::list& x11, int AB){
    switch(AB){
        case 0:
            N = N1;
            break;
        case 1:
            N = N2;
            break;
    }
	py::list return_list;
	for(int i=0; i<N; i++){
		double x_l2 = 0.0;
		for(int j=0; j<D; j++){
			x_l2 += (py::extract<double>(x11[j]) - data[AB][i][j])*(py::extract<double>(x11[j]) - data[AB][i][j]);
		}
		x_l2 = std::sqrt(x_l2);
		return_list.append(x_l2);
	}
	return return_list;
}


BOOST_PYTHON_MODULE(distbasic)
{
	Py_Initialize();
	py::def("datalen", &datalen);
    py::def("inputdata", &inputdata);
	py::def("dotlist", &dotlist);
	py::def("l2list", &l2list);
}