# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ElementsDialog.ui'
#
# Created: Tue Jul 29 16:41:46 2014
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PeriodicTableDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(763, 503)
        self.Ti = QtGui.QPushButton(Dialog)
        self.Ti.setGeometry(QtCore.QRect(140, 150, 41, 41))
        self.Ti.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Ti.setObjectName(_fromUtf8("Ti"))
        self.Fe = QtGui.QPushButton(Dialog)
        self.Fe.setGeometry(QtCore.QRect(300, 150, 41, 41))
        self.Fe.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Fe.setObjectName(_fromUtf8("Fe"))
        self.Cancel = QtGui.QPushButton(Dialog)
        self.Cancel.setGeometry(QtCore.QRect(380, 450, 75, 23))
        self.Cancel.setObjectName(_fromUtf8("Cancel"))
        self.OK = QtGui.QPushButton(Dialog)
        self.OK.setGeometry(QtCore.QRect(280, 450, 75, 23))
        self.OK.setObjectName(_fromUtf8("OK"))
        self.H = QtGui.QLabel(Dialog)
        self.H.setEnabled(True)
        self.H.setGeometry(QtCore.QRect(20, 30, 41, 41))
        self.H.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.H.setAutoFillBackground(False)
        self.H.setFrameShape(QtGui.QFrame.StyledPanel)
        self.H.setAlignment(QtCore.Qt.AlignCenter)
        self.H.setObjectName(_fromUtf8("H"))
        self.V = QtGui.QPushButton(Dialog)
        self.V.setGeometry(QtCore.QRect(180, 150, 41, 41))
        self.V.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.V.setObjectName(_fromUtf8("V"))
        self.Cr = QtGui.QPushButton(Dialog)
        self.Cr.setGeometry(QtCore.QRect(220, 150, 41, 41))
        self.Cr.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Cr.setObjectName(_fromUtf8("Cr"))
        self.Mn = QtGui.QPushButton(Dialog)
        self.Mn.setGeometry(QtCore.QRect(260, 150, 41, 41))
        self.Mn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Mn.setObjectName(_fromUtf8("Mn"))
        self.Ga = QtGui.QPushButton(Dialog)
        self.Ga.setGeometry(QtCore.QRect(500, 150, 41, 41))
        self.Ga.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Ga.setObjectName(_fromUtf8("Ga"))
        self.Co = QtGui.QPushButton(Dialog)
        self.Co.setGeometry(QtCore.QRect(340, 150, 41, 41))
        self.Co.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Co.setObjectName(_fromUtf8("Co"))
        self.Ni = QtGui.QPushButton(Dialog)
        self.Ni.setGeometry(QtCore.QRect(380, 150, 41, 41))
        self.Ni.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Ni.setObjectName(_fromUtf8("Ni"))
        self.Cu = QtGui.QPushButton(Dialog)
        self.Cu.setGeometry(QtCore.QRect(420, 150, 41, 41))
        self.Cu.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Cu.setObjectName(_fromUtf8("Cu"))
        self.Zn = QtGui.QPushButton(Dialog)
        self.Zn.setGeometry(QtCore.QRect(460, 150, 41, 41))
        self.Zn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Zn.setObjectName(_fromUtf8("Zn"))
        self.Ge = QtGui.QPushButton(Dialog)
        self.Ge.setGeometry(QtCore.QRect(540, 150, 41, 41))
        self.Ge.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Ge.setObjectName(_fromUtf8("Ge"))
        self.As = QtGui.QPushButton(Dialog)
        self.As.setGeometry(QtCore.QRect(580, 150, 41, 41))
        self.As.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.As.setObjectName(_fromUtf8("As"))
        self.Se = QtGui.QPushButton(Dialog)
        self.Se.setGeometry(QtCore.QRect(620, 150, 41, 41))
        self.Se.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Se.setObjectName(_fromUtf8("Se"))
        self.Br = QtGui.QPushButton(Dialog)
        self.Br.setGeometry(QtCore.QRect(660, 150, 41, 41))
        self.Br.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Br.setObjectName(_fromUtf8("Br"))
        self.Kr = QtGui.QPushButton(Dialog)
        self.Kr.setGeometry(QtCore.QRect(700, 150, 41, 41))
        self.Kr.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Kr.setObjectName(_fromUtf8("Kr"))
        self.He = QtGui.QLabel(Dialog)
        self.He.setEnabled(True)
        self.He.setGeometry(QtCore.QRect(700, 30, 41, 41))
        self.He.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.He.setAutoFillBackground(False)
        self.He.setFrameShape(QtGui.QFrame.StyledPanel)
        self.He.setAlignment(QtCore.Qt.AlignCenter)
        self.He.setObjectName(_fromUtf8("He"))
        self.Y = QtGui.QPushButton(Dialog)
        self.Y.setGeometry(QtCore.QRect(100, 190, 41, 41))
        self.Y.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Y.setObjectName(_fromUtf8("Y"))
        self.Cd = QtGui.QPushButton(Dialog)
        self.Cd.setGeometry(QtCore.QRect(460, 190, 41, 41))
        self.Cd.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Cd.setObjectName(_fromUtf8("Cd"))
        self.Ag = QtGui.QPushButton(Dialog)
        self.Ag.setGeometry(QtCore.QRect(420, 190, 41, 41))
        self.Ag.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Ag.setObjectName(_fromUtf8("Ag"))
        self.Pd = QtGui.QPushButton(Dialog)
        self.Pd.setGeometry(QtCore.QRect(380, 190, 41, 41))
        self.Pd.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Pd.setObjectName(_fromUtf8("Pd"))
        self.Zr = QtGui.QPushButton(Dialog)
        self.Zr.setGeometry(QtCore.QRect(140, 190, 41, 41))
        self.Zr.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Zr.setObjectName(_fromUtf8("Zr"))
        self.Xe = QtGui.QPushButton(Dialog)
        self.Xe.setGeometry(QtCore.QRect(700, 190, 41, 41))
        self.Xe.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Xe.setObjectName(_fromUtf8("Xe"))
        self.Rh = QtGui.QPushButton(Dialog)
        self.Rh.setGeometry(QtCore.QRect(340, 190, 41, 41))
        self.Rh.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Rh.setObjectName(_fromUtf8("Rh"))
        self.In = QtGui.QPushButton(Dialog)
        self.In.setGeometry(QtCore.QRect(500, 190, 41, 41))
        self.In.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.In.setObjectName(_fromUtf8("In"))
        self.Tc = QtGui.QPushButton(Dialog)
        self.Tc.setGeometry(QtCore.QRect(260, 190, 41, 41))
        self.Tc.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Tc.setObjectName(_fromUtf8("Tc"))
        self.Mo = QtGui.QPushButton(Dialog)
        self.Mo.setGeometry(QtCore.QRect(220, 190, 41, 41))
        self.Mo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Mo.setObjectName(_fromUtf8("Mo"))
        self.Nb = QtGui.QPushButton(Dialog)
        self.Nb.setGeometry(QtCore.QRect(180, 190, 41, 41))
        self.Nb.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Nb.setObjectName(_fromUtf8("Nb"))
        self.Sr = QtGui.QPushButton(Dialog)
        self.Sr.setGeometry(QtCore.QRect(60, 190, 41, 41))
        self.Sr.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Sr.setObjectName(_fromUtf8("Sr"))
        self.I = QtGui.QPushButton(Dialog)
        self.I.setGeometry(QtCore.QRect(660, 190, 41, 41))
        self.I.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.I.setObjectName(_fromUtf8("I"))
        self.Rb = QtGui.QPushButton(Dialog)
        self.Rb.setGeometry(QtCore.QRect(20, 190, 41, 41))
        self.Rb.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Rb.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Rb.setStyleSheet(_fromUtf8(""))
        self.Rb.setObjectName(_fromUtf8("Rb"))
        self.Te = QtGui.QPushButton(Dialog)
        self.Te.setGeometry(QtCore.QRect(620, 190, 41, 41))
        self.Te.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Te.setObjectName(_fromUtf8("Te"))
        self.Ru = QtGui.QPushButton(Dialog)
        self.Ru.setGeometry(QtCore.QRect(300, 190, 41, 41))
        self.Ru.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Ru.setObjectName(_fromUtf8("Ru"))
        self.Sb = QtGui.QPushButton(Dialog)
        self.Sb.setGeometry(QtCore.QRect(580, 190, 41, 41))
        self.Sb.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Sb.setObjectName(_fromUtf8("Sb"))
        self.Sn = QtGui.QPushButton(Dialog)
        self.Sn.setGeometry(QtCore.QRect(540, 190, 41, 41))
        self.Sn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Sn.setObjectName(_fromUtf8("Sn"))
        self.Re = QtGui.QPushButton(Dialog)
        self.Re.setGeometry(QtCore.QRect(260, 230, 41, 41))
        self.Re.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Re.setObjectName(_fromUtf8("Re"))
        self.Hf = QtGui.QPushButton(Dialog)
        self.Hf.setGeometry(QtCore.QRect(140, 230, 41, 41))
        self.Hf.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Hf.setObjectName(_fromUtf8("Hf"))
        self.Pt = QtGui.QPushButton(Dialog)
        self.Pt.setGeometry(QtCore.QRect(380, 230, 41, 41))
        self.Pt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Pt.setObjectName(_fromUtf8("Pt"))
        self.Tl = QtGui.QPushButton(Dialog)
        self.Tl.setGeometry(QtCore.QRect(500, 230, 41, 41))
        self.Tl.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Tl.setObjectName(_fromUtf8("Tl"))
        self.Au = QtGui.QPushButton(Dialog)
        self.Au.setGeometry(QtCore.QRect(420, 230, 41, 41))
        self.Au.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Au.setObjectName(_fromUtf8("Au"))
        self.Ir = QtGui.QPushButton(Dialog)
        self.Ir.setGeometry(QtCore.QRect(340, 230, 41, 41))
        self.Ir.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Ir.setObjectName(_fromUtf8("Ir"))
        self.Pb = QtGui.QPushButton(Dialog)
        self.Pb.setGeometry(QtCore.QRect(540, 230, 41, 41))
        self.Pb.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Pb.setObjectName(_fromUtf8("Pb"))
        self.Rn = QtGui.QPushButton(Dialog)
        self.Rn.setGeometry(QtCore.QRect(700, 230, 41, 41))
        self.Rn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Rn.setObjectName(_fromUtf8("Rn"))
        self.Bi = QtGui.QPushButton(Dialog)
        self.Bi.setGeometry(QtCore.QRect(580, 230, 41, 41))
        self.Bi.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Bi.setObjectName(_fromUtf8("Bi"))
        self.Os = QtGui.QPushButton(Dialog)
        self.Os.setGeometry(QtCore.QRect(300, 230, 41, 41))
        self.Os.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Os.setObjectName(_fromUtf8("Os"))
        self.W = QtGui.QPushButton(Dialog)
        self.W.setGeometry(QtCore.QRect(220, 230, 41, 41))
        self.W.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.W.setObjectName(_fromUtf8("W"))
        self.Po = QtGui.QPushButton(Dialog)
        self.Po.setGeometry(QtCore.QRect(620, 230, 41, 41))
        self.Po.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Po.setObjectName(_fromUtf8("Po"))
        self.Hg = QtGui.QPushButton(Dialog)
        self.Hg.setGeometry(QtCore.QRect(460, 230, 41, 41))
        self.Hg.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Hg.setObjectName(_fromUtf8("Hg"))
        self.Cs = QtGui.QPushButton(Dialog)
        self.Cs.setGeometry(QtCore.QRect(20, 230, 41, 41))
        self.Cs.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Cs.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Cs.setStyleSheet(_fromUtf8(""))
        self.Cs.setObjectName(_fromUtf8("Cs"))
        self.At = QtGui.QPushButton(Dialog)
        self.At.setGeometry(QtCore.QRect(660, 230, 41, 41))
        self.At.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.At.setObjectName(_fromUtf8("At"))
        self.Ba = QtGui.QPushButton(Dialog)
        self.Ba.setGeometry(QtCore.QRect(60, 230, 41, 41))
        self.Ba.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Ba.setObjectName(_fromUtf8("Ba"))
        self.Ta = QtGui.QPushButton(Dialog)
        self.Ta.setGeometry(QtCore.QRect(180, 230, 41, 41))
        self.Ta.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Ta.setObjectName(_fromUtf8("Ta"))
        self.Ra = QtGui.QPushButton(Dialog)
        self.Ra.setGeometry(QtCore.QRect(60, 270, 41, 41))
        self.Ra.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Ra.setObjectName(_fromUtf8("Ra"))
        self.Fr = QtGui.QPushButton(Dialog)
        self.Fr.setGeometry(QtCore.QRect(20, 270, 41, 41))
        self.Fr.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Fr.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Fr.setStyleSheet(_fromUtf8(""))
        self.Fr.setObjectName(_fromUtf8("Fr"))
        self.Gd = QtGui.QPushButton(Dialog)
        self.Gd.setGeometry(QtCore.QRect(380, 330, 41, 41))
        self.Gd.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Gd.setObjectName(_fromUtf8("Gd"))
        self.Nd = QtGui.QPushButton(Dialog)
        self.Nd.setGeometry(QtCore.QRect(220, 330, 41, 41))
        self.Nd.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Nd.setObjectName(_fromUtf8("Nd"))
        self.Ce = QtGui.QPushButton(Dialog)
        self.Ce.setGeometry(QtCore.QRect(140, 330, 41, 41))
        self.Ce.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Ce.setObjectName(_fromUtf8("Ce"))
        self.Tm = QtGui.QPushButton(Dialog)
        self.Tm.setGeometry(QtCore.QRect(580, 330, 41, 41))
        self.Tm.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Tm.setObjectName(_fromUtf8("Tm"))
        self.Er = QtGui.QPushButton(Dialog)
        self.Er.setGeometry(QtCore.QRect(540, 330, 41, 41))
        self.Er.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Er.setObjectName(_fromUtf8("Er"))
        self.Tb = QtGui.QPushButton(Dialog)
        self.Tb.setGeometry(QtCore.QRect(420, 330, 41, 41))
        self.Tb.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Tb.setObjectName(_fromUtf8("Tb"))
        self.Yb = QtGui.QPushButton(Dialog)
        self.Yb.setGeometry(QtCore.QRect(620, 330, 41, 41))
        self.Yb.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Yb.setObjectName(_fromUtf8("Yb"))
        self.Ho = QtGui.QPushButton(Dialog)
        self.Ho.setGeometry(QtCore.QRect(500, 330, 41, 41))
        self.Ho.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Ho.setObjectName(_fromUtf8("Ho"))
        self.Sm = QtGui.QPushButton(Dialog)
        self.Sm.setGeometry(QtCore.QRect(300, 330, 41, 41))
        self.Sm.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Sm.setObjectName(_fromUtf8("Sm"))
        self.Pr = QtGui.QPushButton(Dialog)
        self.Pr.setGeometry(QtCore.QRect(180, 330, 41, 41))
        self.Pr.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Pr.setObjectName(_fromUtf8("Pr"))
        self.Pm = QtGui.QPushButton(Dialog)
        self.Pm.setGeometry(QtCore.QRect(260, 330, 41, 41))
        self.Pm.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Pm.setObjectName(_fromUtf8("Pm"))
        self.Lu = QtGui.QPushButton(Dialog)
        self.Lu.setGeometry(QtCore.QRect(660, 330, 41, 41))
        self.Lu.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Lu.setObjectName(_fromUtf8("Lu"))
        self.Eu = QtGui.QPushButton(Dialog)
        self.Eu.setGeometry(QtCore.QRect(340, 330, 41, 41))
        self.Eu.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Eu.setObjectName(_fromUtf8("Eu"))
        self.Dy = QtGui.QPushButton(Dialog)
        self.Dy.setGeometry(QtCore.QRect(460, 330, 41, 41))
        self.Dy.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Dy.setObjectName(_fromUtf8("Dy"))
        self.La = QtGui.QPushButton(Dialog)
        self.La.setGeometry(QtCore.QRect(100, 330, 41, 41))
        self.La.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.La.setObjectName(_fromUtf8("La"))
        self.Pa = QtGui.QPushButton(Dialog)
        self.Pa.setGeometry(QtCore.QRect(180, 370, 41, 41))
        self.Pa.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Pa.setObjectName(_fromUtf8("Pa"))
        self.Ac = QtGui.QPushButton(Dialog)
        self.Ac.setGeometry(QtCore.QRect(100, 370, 41, 41))
        self.Ac.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Ac.setObjectName(_fromUtf8("Ac"))
        self.Th = QtGui.QPushButton(Dialog)
        self.Th.setGeometry(QtCore.QRect(140, 370, 41, 41))
        self.Th.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Th.setObjectName(_fromUtf8("Th"))
        self.U = QtGui.QPushButton(Dialog)
        self.U.setGeometry(QtCore.QRect(220, 370, 41, 41))
        self.U.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.U.setObjectName(_fromUtf8("U"))
        self.Np = QtGui.QPushButton(Dialog)
        self.Np.setGeometry(QtCore.QRect(260, 370, 41, 41))
        self.Np.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Np.setObjectName(_fromUtf8("Np"))
        self.Pu = QtGui.QPushButton(Dialog)
        self.Pu.setGeometry(QtCore.QRect(300, 370, 41, 41))
        self.Pu.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Pu.setObjectName(_fromUtf8("Pu"))
        self.Am = QtGui.QPushButton(Dialog)
        self.Am.setGeometry(QtCore.QRect(340, 370, 41, 41))
        self.Am.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Am.setObjectName(_fromUtf8("Am"))
        self.Sg = QtGui.QLabel(Dialog)
        self.Sg.setEnabled(True)
        self.Sg.setGeometry(QtCore.QRect(220, 270, 41, 41))
        self.Sg.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Sg.setAutoFillBackground(False)
        self.Sg.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Sg.setAlignment(QtCore.Qt.AlignCenter)
        self.Sg.setObjectName(_fromUtf8("Sg"))
        self.Bh = QtGui.QLabel(Dialog)
        self.Bh.setEnabled(True)
        self.Bh.setGeometry(QtCore.QRect(260, 270, 41, 41))
        self.Bh.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Bh.setAutoFillBackground(False)
        self.Bh.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Bh.setAlignment(QtCore.Qt.AlignCenter)
        self.Bh.setObjectName(_fromUtf8("Bh"))
        self.Mt = QtGui.QLabel(Dialog)
        self.Mt.setEnabled(True)
        self.Mt.setGeometry(QtCore.QRect(340, 270, 41, 41))
        self.Mt.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Mt.setAutoFillBackground(False)
        self.Mt.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Mt.setAlignment(QtCore.Qt.AlignCenter)
        self.Mt.setObjectName(_fromUtf8("Mt"))
        self.Rf = QtGui.QLabel(Dialog)
        self.Rf.setEnabled(True)
        self.Rf.setGeometry(QtCore.QRect(140, 270, 41, 41))
        self.Rf.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Rf.setAutoFillBackground(False)
        self.Rf.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Rf.setAlignment(QtCore.Qt.AlignCenter)
        self.Rf.setObjectName(_fromUtf8("Rf"))
        self.Db = QtGui.QLabel(Dialog)
        self.Db.setEnabled(True)
        self.Db.setGeometry(QtCore.QRect(180, 270, 41, 41))
        self.Db.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Db.setAutoFillBackground(False)
        self.Db.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Db.setAlignment(QtCore.Qt.AlignCenter)
        self.Db.setObjectName(_fromUtf8("Db"))
        self.Hs = QtGui.QLabel(Dialog)
        self.Hs.setEnabled(True)
        self.Hs.setGeometry(QtCore.QRect(300, 270, 41, 41))
        self.Hs.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Hs.setAutoFillBackground(False)
        self.Hs.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Hs.setAlignment(QtCore.Qt.AlignCenter)
        self.Hs.setObjectName(_fromUtf8("Hs"))
        self.Uut = QtGui.QLabel(Dialog)
        self.Uut.setEnabled(True)
        self.Uut.setGeometry(QtCore.QRect(500, 270, 41, 41))
        self.Uut.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Uut.setAutoFillBackground(False)
        self.Uut.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Uut.setAlignment(QtCore.Qt.AlignCenter)
        self.Uut.setObjectName(_fromUtf8("Uut"))
        self.Rg = QtGui.QLabel(Dialog)
        self.Rg.setEnabled(True)
        self.Rg.setGeometry(QtCore.QRect(420, 270, 41, 41))
        self.Rg.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Rg.setAutoFillBackground(False)
        self.Rg.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Rg.setAlignment(QtCore.Qt.AlignCenter)
        self.Rg.setObjectName(_fromUtf8("Rg"))
        self.Uuq = QtGui.QLabel(Dialog)
        self.Uuq.setEnabled(True)
        self.Uuq.setGeometry(QtCore.QRect(540, 270, 41, 41))
        self.Uuq.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Uuq.setAutoFillBackground(False)
        self.Uuq.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Uuq.setAlignment(QtCore.Qt.AlignCenter)
        self.Uuq.setObjectName(_fromUtf8("Uuq"))
        self.Cn = QtGui.QLabel(Dialog)
        self.Cn.setEnabled(True)
        self.Cn.setGeometry(QtCore.QRect(460, 270, 41, 41))
        self.Cn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Cn.setAutoFillBackground(False)
        self.Cn.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Cn.setAlignment(QtCore.Qt.AlignCenter)
        self.Cn.setObjectName(_fromUtf8("Cn"))
        self.Ds = QtGui.QLabel(Dialog)
        self.Ds.setEnabled(True)
        self.Ds.setGeometry(QtCore.QRect(380, 270, 41, 41))
        self.Ds.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Ds.setAutoFillBackground(False)
        self.Ds.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Ds.setAlignment(QtCore.Qt.AlignCenter)
        self.Ds.setObjectName(_fromUtf8("Ds"))
        self.Uup = QtGui.QLabel(Dialog)
        self.Uup.setEnabled(True)
        self.Uup.setGeometry(QtCore.QRect(580, 270, 41, 41))
        self.Uup.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Uup.setAutoFillBackground(False)
        self.Uup.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Uup.setAlignment(QtCore.Qt.AlignCenter)
        self.Uup.setObjectName(_fromUtf8("Uup"))
        self.Uuh = QtGui.QLabel(Dialog)
        self.Uuh.setEnabled(True)
        self.Uuh.setGeometry(QtCore.QRect(620, 270, 41, 41))
        self.Uuh.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Uuh.setAutoFillBackground(False)
        self.Uuh.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Uuh.setAlignment(QtCore.Qt.AlignCenter)
        self.Uuh.setObjectName(_fromUtf8("Uuh"))
        self.Uus = QtGui.QLabel(Dialog)
        self.Uus.setEnabled(True)
        self.Uus.setGeometry(QtCore.QRect(660, 270, 41, 41))
        self.Uus.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Uus.setAutoFillBackground(False)
        self.Uus.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Uus.setAlignment(QtCore.Qt.AlignCenter)
        self.Uus.setObjectName(_fromUtf8("Uus"))
        self.Uuo = QtGui.QLabel(Dialog)
        self.Uuo.setEnabled(True)
        self.Uuo.setGeometry(QtCore.QRect(700, 270, 41, 41))
        self.Uuo.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Uuo.setAutoFillBackground(False)
        self.Uuo.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Uuo.setAlignment(QtCore.Qt.AlignCenter)
        self.Uuo.setObjectName(_fromUtf8("Uuo"))
        self.Cf = QtGui.QLabel(Dialog)
        self.Cf.setEnabled(True)
        self.Cf.setGeometry(QtCore.QRect(460, 370, 41, 41))
        self.Cf.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Cf.setAutoFillBackground(False)
        self.Cf.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Cf.setAlignment(QtCore.Qt.AlignCenter)
        self.Cf.setObjectName(_fromUtf8("Cf"))
        self.Lr = QtGui.QLabel(Dialog)
        self.Lr.setEnabled(True)
        self.Lr.setGeometry(QtCore.QRect(660, 370, 41, 41))
        self.Lr.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Lr.setAutoFillBackground(False)
        self.Lr.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Lr.setAlignment(QtCore.Qt.AlignCenter)
        self.Lr.setObjectName(_fromUtf8("Lr"))
        self.Bk = QtGui.QLabel(Dialog)
        self.Bk.setEnabled(True)
        self.Bk.setGeometry(QtCore.QRect(420, 370, 41, 41))
        self.Bk.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Bk.setAutoFillBackground(False)
        self.Bk.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Bk.setAlignment(QtCore.Qt.AlignCenter)
        self.Bk.setObjectName(_fromUtf8("Bk"))
        self.Cm = QtGui.QLabel(Dialog)
        self.Cm.setEnabled(True)
        self.Cm.setGeometry(QtCore.QRect(380, 370, 41, 41))
        self.Cm.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Cm.setAutoFillBackground(False)
        self.Cm.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Cm.setAlignment(QtCore.Qt.AlignCenter)
        self.Cm.setObjectName(_fromUtf8("Cm"))
        self.Es = QtGui.QLabel(Dialog)
        self.Es.setEnabled(True)
        self.Es.setGeometry(QtCore.QRect(500, 370, 41, 41))
        self.Es.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Es.setAutoFillBackground(False)
        self.Es.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Es.setAlignment(QtCore.Qt.AlignCenter)
        self.Es.setObjectName(_fromUtf8("Es"))
        self.No = QtGui.QLabel(Dialog)
        self.No.setEnabled(True)
        self.No.setGeometry(QtCore.QRect(620, 370, 41, 41))
        self.No.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.No.setAutoFillBackground(False)
        self.No.setFrameShape(QtGui.QFrame.StyledPanel)
        self.No.setAlignment(QtCore.Qt.AlignCenter)
        self.No.setObjectName(_fromUtf8("No"))
        self.Fm = QtGui.QLabel(Dialog)
        self.Fm.setEnabled(True)
        self.Fm.setGeometry(QtCore.QRect(540, 370, 41, 41))
        self.Fm.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Fm.setAutoFillBackground(False)
        self.Fm.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Fm.setAlignment(QtCore.Qt.AlignCenter)
        self.Fm.setObjectName(_fromUtf8("Fm"))
        self.Md = QtGui.QLabel(Dialog)
        self.Md.setEnabled(True)
        self.Md.setGeometry(QtCore.QRect(580, 370, 41, 41))
        self.Md.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Md.setAutoFillBackground(False)
        self.Md.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Md.setAlignment(QtCore.Qt.AlignCenter)
        self.Md.setObjectName(_fromUtf8("Md"))
        self.Lanth = QtGui.QLabel(Dialog)
        self.Lanth.setEnabled(True)
        self.Lanth.setGeometry(QtCore.QRect(100, 230, 41, 41))
        self.Lanth.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Lanth.setAutoFillBackground(False)
        self.Lanth.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Lanth.setAlignment(QtCore.Qt.AlignCenter)
        self.Lanth.setObjectName(_fromUtf8("Lanth"))
        self.Act = QtGui.QLabel(Dialog)
        self.Act.setEnabled(True)
        self.Act.setGeometry(QtCore.QRect(100, 270, 41, 41))
        self.Act.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Act.setAutoFillBackground(False)
        self.Act.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Act.setAlignment(QtCore.Qt.AlignCenter)
        self.Act.setObjectName(_fromUtf8("Act"))
        self.Li = QtGui.QPushButton(Dialog)
        self.Li.setGeometry(QtCore.QRect(20, 70, 41, 41))
        self.Li.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Li.setObjectName(_fromUtf8("Li"))
        self.Be = QtGui.QPushButton(Dialog)
        self.Be.setGeometry(QtCore.QRect(60, 70, 41, 41))
        self.Be.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Be.setObjectName(_fromUtf8("Be"))
        self.Ne = QtGui.QPushButton(Dialog)
        self.Ne.setGeometry(QtCore.QRect(700, 70, 41, 41))
        self.Ne.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Ne.setObjectName(_fromUtf8("Ne"))
        self.B = QtGui.QPushButton(Dialog)
        self.B.setGeometry(QtCore.QRect(500, 70, 41, 41))
        self.B.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.B.setObjectName(_fromUtf8("B"))
        self.O = QtGui.QPushButton(Dialog)
        self.O.setGeometry(QtCore.QRect(620, 70, 41, 41))
        self.O.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.O.setObjectName(_fromUtf8("O"))
        self.C = QtGui.QPushButton(Dialog)
        self.C.setGeometry(QtCore.QRect(540, 70, 41, 41))
        self.C.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.C.setObjectName(_fromUtf8("C"))
        self.F = QtGui.QPushButton(Dialog)
        self.F.setGeometry(QtCore.QRect(660, 70, 41, 41))
        self.F.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.F.setObjectName(_fromUtf8("F"))
        self.N = QtGui.QPushButton(Dialog)
        self.N.setGeometry(QtCore.QRect(580, 70, 41, 41))
        self.N.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.N.setObjectName(_fromUtf8("N"))
        self.Ar = QtGui.QPushButton(Dialog)
        self.Ar.setGeometry(QtCore.QRect(700, 110, 41, 41))
        self.Ar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Ar.setObjectName(_fromUtf8("Ar"))
        self.Al = QtGui.QPushButton(Dialog)
        self.Al.setGeometry(QtCore.QRect(500, 110, 41, 41))
        self.Al.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Al.setObjectName(_fromUtf8("Al"))
        self.P = QtGui.QPushButton(Dialog)
        self.P.setGeometry(QtCore.QRect(580, 110, 41, 41))
        self.P.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.P.setObjectName(_fromUtf8("P"))
        self.Na = QtGui.QPushButton(Dialog)
        self.Na.setGeometry(QtCore.QRect(20, 110, 41, 41))
        self.Na.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Na.setObjectName(_fromUtf8("Na"))
        self.S = QtGui.QPushButton(Dialog)
        self.S.setGeometry(QtCore.QRect(620, 110, 41, 41))
        self.S.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.S.setObjectName(_fromUtf8("S"))
        self.Cl = QtGui.QPushButton(Dialog)
        self.Cl.setGeometry(QtCore.QRect(660, 110, 41, 41))
        self.Cl.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Cl.setObjectName(_fromUtf8("Cl"))
        self.Mg = QtGui.QPushButton(Dialog)
        self.Mg.setGeometry(QtCore.QRect(60, 110, 41, 41))
        self.Mg.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Mg.setObjectName(_fromUtf8("Mg"))
        self.Si = QtGui.QPushButton(Dialog)
        self.Si.setGeometry(QtCore.QRect(540, 110, 41, 41))
        self.Si.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Si.setObjectName(_fromUtf8("Si"))
        self.Sc = QtGui.QPushButton(Dialog)
        self.Sc.setGeometry(QtCore.QRect(100, 150, 41, 41))
        self.Sc.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Sc.setObjectName(_fromUtf8("Sc"))
        self.K = QtGui.QPushButton(Dialog)
        self.K.setGeometry(QtCore.QRect(20, 150, 41, 41))
        self.K.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.K.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.K.setStyleSheet(_fromUtf8(""))
        self.K.setObjectName(_fromUtf8("K"))
        self.Ca = QtGui.QPushButton(Dialog)
        self.Ca.setGeometry(QtCore.QRect(60, 150, 41, 41))
        self.Ca.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Ca.setObjectName(_fromUtf8("Ca"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.Ti.setText(_translate("Dialog", "Ti", None))
        self.Fe.setText(_translate("Dialog", "Fe", None))
        self.Cancel.setText(_translate("Dialog", "Cancel", None))
        self.OK.setText(_translate("Dialog", "OK", None))
        self.H.setText(_translate("Dialog", "H", None))
        self.V.setText(_translate("Dialog", "V", None))
        self.Cr.setText(_translate("Dialog", "Cr", None))
        self.Mn.setText(_translate("Dialog", "Mn", None))
        self.Ga.setText(_translate("Dialog", "Ga", None))
        self.Co.setText(_translate("Dialog", "Co", None))
        self.Ni.setText(_translate("Dialog", "Ni", None))
        self.Cu.setText(_translate("Dialog", "Cu", None))
        self.Zn.setText(_translate("Dialog", "Zn", None))
        self.Ge.setText(_translate("Dialog", "Ge", None))
        self.As.setText(_translate("Dialog", "As", None))
        self.Se.setText(_translate("Dialog", "Se", None))
        self.Br.setText(_translate("Dialog", "Br", None))
        self.Kr.setText(_translate("Dialog", "Kr", None))
        self.He.setText(_translate("Dialog", "He", None))
        self.Y.setText(_translate("Dialog", "Y", None))
        self.Cd.setText(_translate("Dialog", "Cd", None))
        self.Ag.setText(_translate("Dialog", "Ag", None))
        self.Pd.setText(_translate("Dialog", "Pd", None))
        self.Zr.setText(_translate("Dialog", "Zr", None))
        self.Xe.setText(_translate("Dialog", "Xe", None))
        self.Rh.setText(_translate("Dialog", "Rh", None))
        self.In.setText(_translate("Dialog", "In", None))
        self.Tc.setText(_translate("Dialog", "Tc", None))
        self.Mo.setText(_translate("Dialog", "Mo", None))
        self.Nb.setText(_translate("Dialog", "Nb", None))
        self.Sr.setText(_translate("Dialog", "Sr", None))
        self.I.setText(_translate("Dialog", "I", None))
        self.Rb.setText(_translate("Dialog", "Rb", None))
        self.Te.setText(_translate("Dialog", "Te", None))
        self.Ru.setText(_translate("Dialog", "Ru", None))
        self.Sb.setText(_translate("Dialog", "Sb", None))
        self.Sn.setText(_translate("Dialog", "Sn", None))
        self.Re.setText(_translate("Dialog", "Re", None))
        self.Hf.setText(_translate("Dialog", "Hf", None))
        self.Pt.setText(_translate("Dialog", "Pt", None))
        self.Tl.setText(_translate("Dialog", "Tl", None))
        self.Au.setText(_translate("Dialog", "Au", None))
        self.Ir.setText(_translate("Dialog", "Ir", None))
        self.Pb.setText(_translate("Dialog", "Pb", None))
        self.Rn.setText(_translate("Dialog", "Rn", None))
        self.Bi.setText(_translate("Dialog", "Bi", None))
        self.Os.setText(_translate("Dialog", "Os", None))
        self.W.setText(_translate("Dialog", "W", None))
        self.Po.setText(_translate("Dialog", "Po", None))
        self.Hg.setText(_translate("Dialog", "Hg", None))
        self.Cs.setText(_translate("Dialog", "Cs", None))
        self.At.setText(_translate("Dialog", "At", None))
        self.Ba.setText(_translate("Dialog", "Ba", None))
        self.Ta.setText(_translate("Dialog", "Ta", None))
        self.Ra.setText(_translate("Dialog", "Ra", None))
        self.Fr.setText(_translate("Dialog", "Fr", None))
        self.Gd.setText(_translate("Dialog", "Gd", None))
        self.Nd.setText(_translate("Dialog", "Nd", None))
        self.Ce.setText(_translate("Dialog", "Ce", None))
        self.Tm.setText(_translate("Dialog", "Tm", None))
        self.Er.setText(_translate("Dialog", "Er", None))
        self.Tb.setText(_translate("Dialog", "Tb", None))
        self.Yb.setText(_translate("Dialog", "Yb", None))
        self.Ho.setText(_translate("Dialog", "Ho", None))
        self.Sm.setText(_translate("Dialog", "Sm", None))
        self.Pr.setText(_translate("Dialog", "Pr", None))
        self.Pm.setText(_translate("Dialog", "Pm", None))
        self.Lu.setText(_translate("Dialog", "Lu", None))
        self.Eu.setText(_translate("Dialog", "Eu", None))
        self.Dy.setText(_translate("Dialog", "Dy", None))
        self.La.setText(_translate("Dialog", "La", None))
        self.Pa.setText(_translate("Dialog", "Pa", None))
        self.Ac.setText(_translate("Dialog", "Ac", None))
        self.Th.setText(_translate("Dialog", "Th", None))
        self.U.setText(_translate("Dialog", "U", None))
        self.Np.setText(_translate("Dialog", "Np", None))
        self.Pu.setText(_translate("Dialog", "Pu", None))
        self.Am.setText(_translate("Dialog", "Am", None))
        self.Sg.setText(_translate("Dialog", "Sg", None))
        self.Bh.setText(_translate("Dialog", "Bh", None))
        self.Mt.setText(_translate("Dialog", "Mt", None))
        self.Rf.setText(_translate("Dialog", "Rf", None))
        self.Db.setText(_translate("Dialog", "Db", None))
        self.Hs.setText(_translate("Dialog", "Hs", None))
        self.Uut.setText(_translate("Dialog", "Uut", None))
        self.Rg.setText(_translate("Dialog", "Rg", None))
        self.Uuq.setText(_translate("Dialog", "Uuq", None))
        self.Cn.setText(_translate("Dialog", "Cn", None))
        self.Ds.setText(_translate("Dialog", "Ds", None))
        self.Uup.setText(_translate("Dialog", "Uup", None))
        self.Uuh.setText(_translate("Dialog", "Uuh", None))
        self.Uus.setText(_translate("Dialog", "Uus", None))
        self.Uuo.setText(_translate("Dialog", "Uuo", None))
        self.Cf.setText(_translate("Dialog", "Cf", None))
        self.Lr.setText(_translate("Dialog", "Lr", None))
        self.Bk.setText(_translate("Dialog", "Bk", None))
        self.Cm.setText(_translate("Dialog", "Cm", None))
        self.Es.setText(_translate("Dialog", "Es", None))
        self.No.setText(_translate("Dialog", "No", None))
        self.Fm.setText(_translate("Dialog", "Fm", None))
        self.Md.setText(_translate("Dialog", "Md", None))
        self.Lanth.setText(_translate("Dialog", "Lanth.", None))
        self.Act.setText(_translate("Dialog", "Act.", None))
        self.Li.setText(_translate("Dialog", "Li", None))
        self.Be.setText(_translate("Dialog", "Be", None))
        self.Ne.setText(_translate("Dialog", "Ne", None))
        self.B.setText(_translate("Dialog", "B", None))
        self.O.setText(_translate("Dialog", "O", None))
        self.C.setText(_translate("Dialog", "C", None))
        self.F.setText(_translate("Dialog", "F", None))
        self.N.setText(_translate("Dialog", "N", None))
        self.Ar.setText(_translate("Dialog", "Ar", None))
        self.Al.setText(_translate("Dialog", "Al", None))
        self.P.setText(_translate("Dialog", "P", None))
        self.Na.setText(_translate("Dialog", "Na", None))
        self.S.setText(_translate("Dialog", "S", None))
        self.Cl.setText(_translate("Dialog", "Cl", None))
        self.Mg.setText(_translate("Dialog", "Mg", None))
        self.Si.setText(_translate("Dialog", "Si", None))
        self.Sc.setText(_translate("Dialog", "Sc", None))
        self.K.setText(_translate("Dialog", "K", None))
        self.Ca.setText(_translate("Dialog", "Ca", None))

