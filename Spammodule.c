#include "python.h"


static PyObject *

spam_Divide(PyObject* self, PyObject* args)
{
	int all = 0;
	int part = 0;

	float ratio = 0.f;

    if(!PyArg_ParseTuple(args, "ii", &all, &part))
        return NULL;
	if (part)
		ratio = ((float)part) / ((float)all);

	return Py_BuildValue("f", ratio);
}

static PyMethodDef SpamMethods[] =
{
    {"Divide", spam_Divide, METH_VARARGS, "Sort Dictionary"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef spammodule =
{
    PyModuleDef_HEAD_INIT,
    "spam",
    "It is test module.",
    -1, SpamMethods
};

PyMODINIT_FUNC
PyInit_spam(void)
{
    return PyModule_Create(&spammodule);
}
