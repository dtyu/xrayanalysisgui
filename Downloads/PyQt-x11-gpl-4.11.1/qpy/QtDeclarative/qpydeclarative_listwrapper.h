// This is the definition of the ListWrapper class.
//
// Copyright (c) 2014 Riverbank Computing Limited <info@riverbankcomputing.com>
// 
// This file is part of PyQt.
// 
// This file may be used under the terms of the GNU General Public
// License versions 2.0 or 3.0 as published by the Free Software
// Foundation and appearing in the files LICENSE.GPL2 and LICENSE.GPL3
// included in the packaging of this file.  Alternatively you may (at
// your option) use any later version of the GNU General Public
// License if such license has been publicly approved by Riverbank
// Computing Limited (or its successors, if any) and the KDE Free Qt
// Foundation. In addition, as a special exception, Riverbank gives you
// certain additional rights. These rights are described in the Riverbank
// GPL Exception version 1.1, which can be found in the file
// GPL_EXCEPTION.txt in this package.
// 
// If you are unsure which license is appropriate for your use, please
// contact the sales department at sales@riverbankcomputing.com.
// 
// This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
// WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.


#ifndef _QPYDECLARATIVELISTWRAPPER_H
#define _QPYDECLARATIVELISTWRAPPER_H


#include <Python.h>

#include <QObject>
#include <QList>


class ListWrapper : public QObject
{
    Q_OBJECT

public:
    static ListWrapper *wrapper(PyObject *py_list, QObject *parent);

    static void append(QObject *qobj, QList<QObject *> *qlist, QObject *el);
    static void clear(QObject *qobj, QList<QObject *> *qlist);

    QList<QObject *> qobject_list;

private:
    ListWrapper(PyObject *py_list, QObject *parent);
    ~ListWrapper();

    static ListWrapper *findWrapper(QObject *qobj, QList<QObject *> *qlist);

    PyObject *_py_list;
};


#endif