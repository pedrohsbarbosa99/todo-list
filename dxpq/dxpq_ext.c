#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <libpq-fe.h>

typedef struct {
    PyObject_HEAD
    PGconn *conn;
} PGConnection;

typedef struct {
    PyObject_HEAD
    PGresult *result;
    PGConnection *PGConnection;
} PGCursor;


static void PGCursor_dealloc(PGCursor *self) {
    if (self->result) {
        PQclear(self->result);
    }
    PyObject_Del(self);
}


static PyObject *PGCursor_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    PGCursor *self;
    self = (PGCursor *) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->result = NULL;
        self->PGConnection = NULL;
    }
    return (PyObject *) self;
}

static int PGCursor_init(PGCursor *self, PyObject *args, PyObject *kwds) {
    const PyObject *connection;
    static char *listkws[] = {"connection", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O", listkws, &connection)) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse arguments");
        return -1;
    }
    self->PGConnection = (PGConnection *)connection;
    return 0;
}


static PyObject *PGCursor_execute(PGCursor *self, PyObject *args, PyObject *kwds) {
    const char *sql;
    static char *listkws[] = {"sql", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "s", listkws, &sql)) {
        PyErr_SetString(PyExc_RuntimeError, "argument 'sql' is required");
        return NULL;
    }
    PGresult *result = PQexec(self->PGConnection->conn, sql);
    if (PQresultStatus(result) != PGRES_COMMAND_OK && PQresultStatus(result) != PGRES_TUPLES_OK) {
        PyErr_SetString(PyExc_RuntimeError, PQresultErrorMessage(result));
        return NULL;
    }
    
    self->result = result;

    Py_RETURN_NONE;
    
}


static PyObject *PGCursor_fetchall(PGCursor *self, PyObject *args) {
    if (!self->result) {
        PyErr_SetString(PyExc_RuntimeError, "Cursor has no result");
        return NULL;
    }

    PGresult *result = self->result;

    int nrows = PQntuples(result);
    int ncols = PQnfields(result);

    PyObject *list_results = PyList_New(nrows);

    for (int i = 0; i < nrows; i++) {
        PyObject *row = PyTuple_New(ncols);

        for (int j = 0; j < ncols; j++) {
            PyObject *value = PyUnicode_FromString(PQgetvalue(result, i, j));
            PyTuple_SET_ITEM(row, j, value);
        }

        PyList_SET_ITEM(list_results, i, row);
    }

    PQclear(result);
    return list_results;
}


static PyObject *PGCursor_fetchone(PGCursor *self, PyObject *args) {
    if (!self->result) {
        PyErr_SetString(PyExc_RuntimeError, "Cursor has no result");
        return NULL;
    }

    PGresult *result = self->result;

    int nrows = PQntuples(result);
    int ncols = PQnfields(result);

    if (nrows == 0) {
        Py_RETURN_NONE;
    }

    PyObject *row = PyTuple_New(ncols);

    for (int j = 0; j < ncols; j++) {
        PyObject *value = PyUnicode_FromString(PQgetvalue(result, 0, j));
        PyTuple_SET_ITEM(row, j, value);
    }

    PQclear(result);
    return row;
}

static PyObject *PGCursor_close(PGCursor *self) {
    if (self->PGConnection && self->result) {
        PQclear(self->result);
        self->result = NULL;
    }
    Py_RETURN_NONE;
}


static PyMethodDef PGCursor_methods[] = {
    {"execute", (PyCFunction)PGCursor_execute, METH_VARARGS | METH_KEYWORDS, "Execute a query"},
    {"fetchall", (PyCFunction)PGCursor_fetchall, METH_NOARGS, "Fetch all rows from a query"},
    {"fetchone", (PyCFunction)PGCursor_fetchone, METH_NOARGS, "Fetch one row from a query"},
    {"close", (PyCFunction)PGCursor_close, METH_NOARGS, "Close the cursor"},
    {NULL}
};

static PyTypeObject PGCursorType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "dxpq_ext.PGCursor",
    .tp_doc = "PostgreSQL Cursor Object",
    .tp_basicsize = sizeof(PGCursor),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PGCursor_new,
    .tp_init = (initproc) PGCursor_init,
    .tp_dealloc = (destructor) PGCursor_dealloc,
    .tp_methods = PGCursor_methods,
};



static void PGConnection_dealloc(PGConnection *self) {
    if (self->conn) {
        PQfinish(self->conn);
        self->conn = NULL;
    }
    PyObject_Del(self);
}


static PyObject *PGConnection_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    PGConnection *self;
    self = (PGConnection *) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->conn = NULL;
    }
    return (PyObject *) self;
}

static int PGConnection_init(PGConnection *self, PyObject *args, PyObject *kwds) {
    const char *conninfo = NULL;
    static char *listkws[] = {"conninfo", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "s", listkws, &conninfo)) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse arguments");
        return -1;
    }

    self->conn = PQconnectdb(conninfo);
    if (PQstatus(self->conn) != CONNECTION_OK) {
        PyErr_SetString(PyExc_RuntimeError, PQerrorMessage(self->conn));
        return -1;
    }

    return 0;
}

static PyObject *PGConnection_close(PGConnection *self) {
    if (self->conn) {
        PQfinish(self->conn);
        self->conn = NULL;
    }
    Py_RETURN_NONE;
}

static PyMethodDef PGConnection_methods[] = {
    {"close", (PyCFunction)PGConnection_close, METH_NOARGS, "Close the connection"},
    {NULL}
};

static PyTypeObject PGConnectionType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "dxpq_ext.PGConnection",
    .tp_doc = "PostgreSQL Connection Object",
    .tp_basicsize = sizeof(PGConnection),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PGConnection_new,
    .tp_init = (initproc) PGConnection_init,
    .tp_dealloc = (destructor) PGConnection_dealloc,
    .tp_methods = PGConnection_methods,
};

static PyMethodDef dxpq_ext_functions[] = {
    {NULL, NULL, 0, NULL}
};


static PyModuleDef dxpq_ext_mod = {
    PyModuleDef_HEAD_INIT,
    "dxpq_ext",
    "Driver to connect to Postgresql",
    -1,
    dxpq_ext_functions
};

PyMODINIT_FUNC PyInit_dxpq_ext(void) {
    PyObject *m;

    if (PyType_Ready(&PGConnectionType) < 0)
        return NULL;
    
    if (PyType_Ready(&PGCursorType) < 0)
        return NULL;

    m = PyModule_Create(&dxpq_ext_mod);
    if (m == NULL)
        return NULL;

    Py_INCREF(&PGConnectionType);
    PyModule_AddObject(m, "PGConnection", (PyObject *)&PGConnectionType);

    Py_INCREF(&PGCursorType);
    PyModule_AddObject(m, "PGCursor", (PyObject *)&PGCursorType);

    return m;
}

