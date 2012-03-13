/* written by Siu Cheung Yu  wykscyu <at> aol <dot> com */
/* "parser" module */

/* on pdclab use next line: */
#include "/usr/local/Cellar/python/2.7.1/include/python2.7/Python.h"
/* on bumblebee use this line instead: */
/* 
#include "/usr/local/Python-2.3.2/include/python2.3/Python.h"
*/

/* External declarations */
extern int parser(char* url, char* doc, char* buf, int blen);

/*Wrapper for the parser() function*/
PyObject *parser_parser(PyObject *self, PyObject *args){
	char* url, *doc, *buf;
	int blen, returnValue;
	
	if(!PyArg_ParseTuple(args, "sssi", &url, &doc, &buf, &blen))
	{
		return NULL;
	}
	/*call the C function*/
	returnValue=parser(url, doc, buf, blen);
	return Py_BuildValue("is",returnValue, buf);
}

static PyMethodDef parsermethods[]={
	{"parser", parser_parser, METH_VARARGS},
	{NULL, NULL}
};

/* Module initialization function*/
initparser(void){
	Py_InitModule("parser", parsermethods);
}
