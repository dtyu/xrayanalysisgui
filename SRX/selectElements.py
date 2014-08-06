#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ElementsDialog import *

# Class for the Periodic Table Dialog
class PeriodicTable(QtGui.QDialog):
    def __init__(self,previousElementsStatus,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_PeriodicTableDialog()
        self.ui.setupUi(self)
        
        # Set button properties (self.ui.X is the button for element X)
        self.ui.Li.setCheckable(True)
        self.ui.Li.clicked[bool].connect(self.modifyElement)
        self.ui.Li.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Be.setCheckable(True)
        self.ui.Be.clicked[bool].connect(self.modifyElement)
        self.ui.Be.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.B.setCheckable(True)
        self.ui.B.clicked[bool].connect(self.modifyElement)
        self.ui.B.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.C.setCheckable(True)
        self.ui.C.clicked[bool].connect(self.modifyElement)
        self.ui.C.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.N.setCheckable(True)
        self.ui.N.clicked[bool].connect(self.modifyElement)
        self.ui.N.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.O.setCheckable(True)
        self.ui.O.clicked[bool].connect(self.modifyElement)
        self.ui.O.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.F.setCheckable(True)
        self.ui.F.clicked[bool].connect(self.modifyElement)
        self.ui.F.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Ne.setCheckable(True)
        self.ui.Ne.clicked[bool].connect(self.modifyElement)
        self.ui.Ne.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Na.setCheckable(True)
        self.ui.Na.clicked[bool].connect(self.modifyElement)
        self.ui.Na.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Mg.setCheckable(True)
        self.ui.Mg.clicked[bool].connect(self.modifyElement)
        self.ui.Mg.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Al.setCheckable(True)
        self.ui.Al.clicked[bool].connect(self.modifyElement)
        self.ui.Al.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Si.setCheckable(True)
        self.ui.Si.clicked[bool].connect(self.modifyElement)
        self.ui.Si.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.P.setCheckable(True)
        self.ui.P.clicked[bool].connect(self.modifyElement)
        self.ui.P.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.S.setCheckable(True)
        self.ui.S.clicked[bool].connect(self.modifyElement)
        self.ui.S.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Cl.setCheckable(True)
        self.ui.Cl.clicked[bool].connect(self.modifyElement)
        self.ui.Cl.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Ar.setCheckable(True)
        self.ui.Ar.clicked[bool].connect(self.modifyElement)
        self.ui.Ar.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.K.setCheckable(True)
        self.ui.K.clicked[bool].connect(self.modifyElement)
        self.ui.K.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Ca.setCheckable(True)
        self.ui.Ca.clicked[bool].connect(self.modifyElement)
        self.ui.Ca.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Sc.setCheckable(True)
        self.ui.Sc.clicked[bool].connect(self.modifyElement)
        self.ui.Sc.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Ti.setCheckable(True)
        self.ui.Ti.clicked[bool].connect(self.modifyElement)
        self.ui.Ti.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.V.setCheckable(True)
        self.ui.V.clicked[bool].connect(self.modifyElement)
        self.ui.V.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Cr.setCheckable(True)
        self.ui.Cr.clicked[bool].connect(self.modifyElement)
        self.ui.Cr.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Mn.setCheckable(True)
        self.ui.Mn.clicked[bool].connect(self.modifyElement)
        self.ui.Mn.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Fe.setCheckable(True)
        self.ui.Fe.clicked[bool].connect(self.modifyElement)
        self.ui.Fe.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Co.setCheckable(True)
        self.ui.Co.clicked[bool].connect(self.modifyElement)
        self.ui.Co.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Ni.setCheckable(True)
        self.ui.Ni.clicked[bool].connect(self.modifyElement)
        self.ui.Ni.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Cu.setCheckable(True)
        self.ui.Cu.clicked[bool].connect(self.modifyElement)
        self.ui.Cu.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Zn.setCheckable(True)
        self.ui.Zn.clicked[bool].connect(self.modifyElement)
        self.ui.Zn.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Ga.setCheckable(True)
        self.ui.Ga.clicked[bool].connect(self.modifyElement)
        self.ui.Ga.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Ge.setCheckable(True)
        self.ui.Ge.clicked[bool].connect(self.modifyElement)
        self.ui.Ge.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.As.setCheckable(True)
        self.ui.As.clicked[bool].connect(self.modifyElement)
        self.ui.As.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Se.setCheckable(True)
        self.ui.Se.clicked[bool].connect(self.modifyElement)
        self.ui.Se.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Br.setCheckable(True)
        self.ui.Br.clicked[bool].connect(self.modifyElement)
        self.ui.Br.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Kr.setCheckable(True)
        self.ui.Kr.clicked[bool].connect(self.modifyElement)
        self.ui.Kr.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Rb.setCheckable(True)
        self.ui.Rb.clicked[bool].connect(self.modifyElement)
        self.ui.Rb.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Sr.setCheckable(True)
        self.ui.Sr.clicked[bool].connect(self.modifyElement)
        self.ui.Sr.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Y.setCheckable(True)
        self.ui.Y.clicked[bool].connect(self.modifyElement)
        self.ui.Y.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Zr.setCheckable(True)
        self.ui.Zr.clicked[bool].connect(self.modifyElement)
        self.ui.Zr.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Nb.setCheckable(True)
        self.ui.Nb.clicked[bool].connect(self.modifyElement)
        self.ui.Nb.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Mo.setCheckable(True)
        self.ui.Mo.clicked[bool].connect(self.modifyElement)
        self.ui.Mo.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Tc.setCheckable(True)
        self.ui.Tc.clicked[bool].connect(self.modifyElement)
        self.ui.Tc.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Ru.setCheckable(True)
        self.ui.Ru.clicked[bool].connect(self.modifyElement)
        self.ui.Ru.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Rh.setCheckable(True)
        self.ui.Rh.clicked[bool].connect(self.modifyElement)
        self.ui.Rh.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Pd.setCheckable(True)
        self.ui.Pd.clicked[bool].connect(self.modifyElement)
        self.ui.Pd.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Ag.setCheckable(True)
        self.ui.Ag.clicked[bool].connect(self.modifyElement)
        self.ui.Ag.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Cd.setCheckable(True)
        self.ui.Cd.clicked[bool].connect(self.modifyElement)
        self.ui.Cd.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.In.setCheckable(True)
        self.ui.In.clicked[bool].connect(self.modifyElement)
        self.ui.In.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Sn.setCheckable(True)
        self.ui.Sn.clicked[bool].connect(self.modifyElement)
        self.ui.Sn.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Sb.setCheckable(True)
        self.ui.Sb.clicked[bool].connect(self.modifyElement)
        self.ui.Sb.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Te.setCheckable(True)
        self.ui.Te.clicked[bool].connect(self.modifyElement)
        self.ui.Te.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.I.setCheckable(True)
        self.ui.I.clicked[bool].connect(self.modifyElement)
        self.ui.I.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Xe.setCheckable(True)
        self.ui.Xe.clicked[bool].connect(self.modifyElement)
        self.ui.Xe.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Cs.setCheckable(True)
        self.ui.Cs.clicked[bool].connect(self.modifyElement)
        self.ui.Cs.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Ba.setCheckable(True)
        self.ui.Ba.clicked[bool].connect(self.modifyElement)
        self.ui.Ba.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Hf.setCheckable(True)
        self.ui.Hf.clicked[bool].connect(self.modifyElement)
        self.ui.Hf.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Ta.setCheckable(True)
        self.ui.Ta.clicked[bool].connect(self.modifyElement)
        self.ui.Ta.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.W.setCheckable(True)
        self.ui.W.clicked[bool].connect(self.modifyElement)
        self.ui.W.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Re.setCheckable(True)
        self.ui.Re.clicked[bool].connect(self.modifyElement)
        self.ui.Re.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Os.setCheckable(True)
        self.ui.Os.clicked[bool].connect(self.modifyElement)
        self.ui.Os.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Ir.setCheckable(True)
        self.ui.Ir.clicked[bool].connect(self.modifyElement)
        self.ui.Ir.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Pt.setCheckable(True)
        self.ui.Pt.clicked[bool].connect(self.modifyElement)
        self.ui.Pt.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Au.setCheckable(True)
        self.ui.Au.clicked[bool].connect(self.modifyElement)
        self.ui.Au.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Hg.setCheckable(True)
        self.ui.Hg.clicked[bool].connect(self.modifyElement)
        self.ui.Hg.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Tl.setCheckable(True)
        self.ui.Tl.clicked[bool].connect(self.modifyElement)
        self.ui.Tl.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Pb.setCheckable(True)
        self.ui.Pb.clicked[bool].connect(self.modifyElement)
        self.ui.Pb.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Bi.setCheckable(True)
        self.ui.Bi.clicked[bool].connect(self.modifyElement)
        self.ui.Bi.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Po.setCheckable(True)
        self.ui.Po.clicked[bool].connect(self.modifyElement)
        self.ui.Po.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.At.setCheckable(True)
        self.ui.At.clicked[bool].connect(self.modifyElement)
        self.ui.At.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Rn.setCheckable(True)
        self.ui.Rn.clicked[bool].connect(self.modifyElement)
        self.ui.Rn.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Fr.setCheckable(True)
        self.ui.Fr.clicked[bool].connect(self.modifyElement)
        self.ui.Fr.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Ra.setCheckable(True)
        self.ui.Ra.clicked[bool].connect(self.modifyElement)
        self.ui.Ra.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.La.setCheckable(True)
        self.ui.La.clicked[bool].connect(self.modifyElement)
        self.ui.La.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Ce.setCheckable(True)
        self.ui.Ce.clicked[bool].connect(self.modifyElement)
        self.ui.Ce.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Pr.setCheckable(True)
        self.ui.Pr.clicked[bool].connect(self.modifyElement)
        self.ui.Pr.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Nd.setCheckable(True)
        self.ui.Nd.clicked[bool].connect(self.modifyElement)
        self.ui.Nd.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Pm.setCheckable(True)
        self.ui.Pm.clicked[bool].connect(self.modifyElement)
        self.ui.Pm.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Sm.setCheckable(True)
        self.ui.Sm.clicked[bool].connect(self.modifyElement)
        self.ui.Sm.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Eu.setCheckable(True)
        self.ui.Eu.clicked[bool].connect(self.modifyElement)
        self.ui.Eu.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Gd.setCheckable(True)
        self.ui.Gd.clicked[bool].connect(self.modifyElement)
        self.ui.Gd.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Tb.setCheckable(True)
        self.ui.Tb.clicked[bool].connect(self.modifyElement)
        self.ui.Tb.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Dy.setCheckable(True)
        self.ui.Dy.clicked[bool].connect(self.modifyElement)
        self.ui.Dy.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Ho.setCheckable(True)
        self.ui.Ho.clicked[bool].connect(self.modifyElement)
        self.ui.Ho.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Er.setCheckable(True)
        self.ui.Er.clicked[bool].connect(self.modifyElement)
        self.ui.Er.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Tm.setCheckable(True)
        self.ui.Tm.clicked[bool].connect(self.modifyElement)
        self.ui.Tm.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Yb.setCheckable(True)
        self.ui.Yb.clicked[bool].connect(self.modifyElement)
        self.ui.Yb.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Lu.setCheckable(True)
        self.ui.Lu.clicked[bool].connect(self.modifyElement)
        self.ui.Lu.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Ac.setCheckable(True)
        self.ui.Ac.clicked[bool].connect(self.modifyElement)
        self.ui.Ac.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Th.setCheckable(True)
        self.ui.Th.clicked[bool].connect(self.modifyElement)
        self.ui.Th.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Pa.setCheckable(True)
        self.ui.Pa.clicked[bool].connect(self.modifyElement)
        self.ui.Pa.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.U.setCheckable(True)
        self.ui.U.clicked[bool].connect(self.modifyElement)
        self.ui.U.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Np.setCheckable(True)
        self.ui.Np.clicked[bool].connect(self.modifyElement)
        self.ui.Np.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Pu.setCheckable(True)
        self.ui.Pu.clicked[bool].connect(self.modifyElement)
        self.ui.Pu.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        self.ui.Am.setCheckable(True)
        self.ui.Am.clicked[bool].connect(self.modifyElement)
        self.ui.Am.setStyleSheet("QPushButton { background-color: white }"
                      "QPushButton:pressed { background-color: red }" )
        # Load previous status (1 means selected, -1 means disabled)
        self.status = previousElementsStatus
        # status[0] represents Li, status[1] represents Be, etc.
        if self.status[0] == 1:  
            self.ui.Li.click()
        elif self.status[0] == -1:
            self.ui.Li.setEnabled(False)
        if self.status[1] == 1:  
            self.ui.Be.click()
        elif self.status[1] == -1:
            self.ui.Be.setEnabled(False)
        if self.status[2] == 1:  
            self.ui.B.click()
        elif self.status[2] == -1:
            self.ui.B.setEnabled(False)
        if self.status[3] == 1:  
            self.ui.C.click()
        elif self.status[3] == -1:
            self.ui.C.setEnabled(False)
        if self.status[4] == 1:  
            self.ui.N.click()
        elif self.status[4] == -1:
            self.ui.N.setEnabled(False)
        if self.status[5] == 1:  
            self.ui.O.click()
        elif self.status[5] == -1:
            self.ui.O.setEnabled(False)
        if self.status[6] == 1:  
            self.ui.F.click()
        elif self.status[6] == -1:
            self.ui.F.setEnabled(False)
        if self.status[7] == 1:  
            self.ui.Ne.click()
        elif self.status[7] == -1:
            self.ui.Ne.setEnabled(False)
        if self.status[8] == 1:  
            self.ui.Na.click()
        elif self.status[8] == -1:
            self.ui.Na.setEnabled(False)
        if self.status[9] == 1:  
            self.ui.Mg.click()
        elif self.status[9] == -1:
            self.ui.Mg.setEnabled(False)
        if self.status[10] == 1:  
            self.ui.Al.click()
        elif self.status[10] == -1:
            self.ui.Al.setEnabled(False)
        if self.status[11] == 1:  
            self.ui.Si.click()
        elif self.status[11] == -1:
            self.ui.Si.setEnabled(False)
        if self.status[12] == 1:  
            self.ui.P.click()
        elif self.status[12] == -1:
            self.ui.P.setEnabled(False)
        if self.status[13] == 1:  
            self.ui.S.click()
        elif self.status[13] == -1:
            self.ui.S.setEnabled(False)
        if self.status[14] == 1:  
            self.ui.Cl.click()
        elif self.status[14] == -1:
            self.ui.Cl.setEnabled(False)
        if self.status[15] == 1:  
            self.ui.Ar.click()
        elif self.status[15] == -1:
            self.ui.Ar.setEnabled(False)
        if self.status[16] == 1:  
            self.ui.K.click()
        elif self.status[16] == -1:
            self.ui.K.setEnabled(False)
        if self.status[17] == 1:  
            self.ui.Ca.click()
        elif self.status[17] == -1:
            self.ui.Ca.setEnabled(False)
        if self.status[18] == 1:  
            self.ui.Sc.click()
        elif self.status[18] == -1:
            self.ui.Sc.setEnabled(False)
        if self.status[19] == 1:  
            self.ui.Ti.click()
        elif self.status[19] == -1:
            self.ui.Ti.setEnabled(False)
        if self.status[20] == 1:  
            self.ui.V.click()
        elif self.status[20] == -1:
            self.ui.V.setEnabled(False)
        if self.status[21] == 1:  
            self.ui.Cr.click()
        elif self.status[21] == -1:
            self.ui.Cr.setEnabled(False)
        if self.status[22] == 1:  
            self.ui.Mn.click()
        elif self.status[22] == -1:
            self.ui.Mn.setEnabled(False)
        if self.status[23] == 1:  
            self.ui.Fe.click()
        elif self.status[23] == -1:
            self.ui.Fe.setEnabled(False)
        if self.status[24] == 1:  
            self.ui.Co.click()
        elif self.status[24] == -1:
            self.ui.Co.setEnabled(False)
        if self.status[25] == 1:  
            self.ui.Ni.click()
        elif self.status[25] == -1:
            self.ui.Ni.setEnabled(False)
        if self.status[26] == 1:  
            self.ui.Cu.click()
        elif self.status[26] == -1:
            self.ui.Cu.setEnabled(False)
        if self.status[27] == 1:  
            self.ui.Zn.click()
        elif self.status[27] == -1:
            self.ui.Zn.setEnabled(False)
        if self.status[28] == 1:  
            self.ui.Ga.click()
        elif self.status[28] == -1:
            self.ui.Ga.setEnabled(False)
        if self.status[29] == 1:  
            self.ui.Ge.click()
        elif self.status[29] == -1:
            self.ui.Ge.setEnabled(False)
        if self.status[30] == 1:  
            self.ui.As.click()
        elif self.status[30] == -1:
            self.ui.As.setEnabled(False)
        if self.status[31] == 1:  
            self.ui.Se.click()
        elif self.status[31] == -1:
            self.ui.Se.setEnabled(False)
        if self.status[32] == 1:  
            self.ui.Br.click()
        elif self.status[32] == -1:
            self.ui.Br.setEnabled(False)
        if self.status[33] == 1:  
            self.ui.Kr.click()
        elif self.status[33] == -1:
            self.ui.Kr.setEnabled(False)
        if self.status[34] == 1:  
            self.ui.Rb.click()
        elif self.status[34] == -1:
            self.ui.Rb.setEnabled(False)
        if self.status[35] == 1:  
            self.ui.Sr.click()
        elif self.status[35] == -1:
            self.ui.Sr.setEnabled(False)
        if self.status[36] == 1:  
            self.ui.Y.click()
        elif self.status[36] == -1:
            self.ui.Y.setEnabled(False)
        if self.status[37] == 1:  
            self.ui.Zr.click()
        elif self.status[37] == -1:
            self.ui.Zr.setEnabled(False)
        if self.status[38] == 1:  
            self.ui.Nb.click()
        elif self.status[38] == -1:
            self.ui.Nb.setEnabled(False)
        if self.status[39] == 1:  
            self.ui.Mo.click()
        elif self.status[39] == -1:
            self.ui.Mo.setEnabled(False)
        if self.status[40] == 1:  
            self.ui.Tc.click()
        elif self.status[40] == -1:
            self.ui.Tc.setEnabled(False)
        if self.status[41] == 1:  
            self.ui.Ru.click()
        elif self.status[41] == -1:
            self.ui.Ru.setEnabled(False)
        if self.status[42] == 1:  
            self.ui.Rh.click()
        elif self.status[42] == -1:
            self.ui.Rh.setEnabled(False)
        if self.status[43] == 1:  
            self.ui.Pd.click()
        elif self.status[43] == -1:
            self.ui.Pd.setEnabled(False)
        if self.status[44] == 1:  
            self.ui.Ag.click()
        elif self.status[44] == -1:
            self.ui.Ag.setEnabled(False)
        if self.status[45] == 1:  
            self.ui.Cd.click()
        elif self.status[45] == -1:
            self.ui.Cd.setEnabled(False)
        if self.status[46] == 1:  
            self.ui.In.click()
        elif self.status[46] == -1:
            self.ui.In.setEnabled(False)
        if self.status[47] == 1:  
            self.ui.Sn.click()
        elif self.status[47] == -1:
            self.ui.Sn.setEnabled(False)
        if self.status[48] == 1:  
            self.ui.Sb.click()
        elif self.status[48] == -1:
            self.ui.Sb.setEnabled(False)
        if self.status[49] == 1:  
            self.ui.Te.click()
        elif self.status[49] == -1:
            self.ui.Te.setEnabled(False)
        if self.status[50] == 1:  
            self.ui.I.click()
        elif self.status[50] == -1:
            self.ui.I.setEnabled(False)
        if self.status[51] == 1:  
            self.ui.Xe.click()
        elif self.status[51] == -1:
            self.ui.Xe.setEnabled(False)
        if self.status[52] == 1:  
            self.ui.Cs.click()
        elif self.status[52] == -1:
            self.ui.Cs.setEnabled(False)
        if self.status[53] == 1:  
            self.ui.Ba.click()
        elif self.status[53] == -1:
            self.ui.Ba.setEnabled(False)
        if self.status[54] == 1:  
            self.ui.La.click()
        elif self.status[54] == -1:
            self.ui.La.setEnabled(False)
        if self.status[55] == 1:  
            self.ui.Ce.click()
        elif self.status[55] == -1:
            self.ui.Ce.setEnabled(False)
        if self.status[56] == 1:  
            self.ui.Pr.click()
        elif self.status[56] == -1:
            self.ui.Pr.setEnabled(False)
        if self.status[57] == 1:  
            self.ui.Nd.click()
        elif self.status[57] == -1:
            self.ui.Nd.setEnabled(False)
        if self.status[58] == 1:  
            self.ui.Pm.click()
        elif self.status[58] == -1:
            self.ui.Pm.setEnabled(False)
        if self.status[59] == 1:  
            self.ui.Sm.click()
        elif self.status[59] == -1:
            self.ui.Sm.setEnabled(False)
        if self.status[60] == 1:  
            self.ui.Eu.click()
        elif self.status[60] == -1:
            self.ui.Eu.setEnabled(False)
        if self.status[61] == 1:  
            self.ui.Gd.click()
        elif self.status[61] == -1:
            self.ui.Gd.setEnabled(False)
        if self.status[62] == 1:  
            self.ui.Tb.click()
        elif self.status[62] == -1:
            self.ui.Tb.setEnabled(False)
        if self.status[63] == 1:  
            self.ui.Dy.click()
        elif self.status[63] == -1:
            self.ui.Dy.setEnabled(False)
        if self.status[64] == 1:  
            self.ui.Ho.click()
        elif self.status[64] == -1:
            self.ui.Ho.setEnabled(False)
        if self.status[65] == 1:  
            self.ui.Er.click()
        elif self.status[65] == -1:
            self.ui.Er.setEnabled(False)
        if self.status[66] == 1:  
            self.ui.Tm.click()
        elif self.status[66] == -1:
            self.ui.Tm.setEnabled(False)
        if self.status[67] == 1:  
            self.ui.Yb.click()
        elif self.status[67] == -1:
            self.ui.Yb.setEnabled(False)
        if self.status[68] == 1:  
            self.ui.Lu.click()
        elif self.status[68] == -1:
            self.ui.Lu.setEnabled(False)
        if self.status[69] == 1:  
            self.ui.Hf.click()
        elif self.status[69] == -1:
            self.ui.Hf.setEnabled(False)
        if self.status[70] == 1:  
            self.ui.Ta.click()
        elif self.status[70] == -1:
            self.ui.Ta.setEnabled(False)
        if self.status[71] == 1:  
            self.ui.W.click()
        elif self.status[71] == -1:
            self.ui.W.setEnabled(False)
        if self.status[72] == 1:  
            self.ui.Re.click()
        elif self.status[72] == -1:
            self.ui.Re.setEnabled(False)
        if self.status[73] == 1:  
            self.ui.Os.click()
        elif self.status[73] == -1:
            self.ui.Os.setEnabled(False)
        if self.status[74] == 1:  
            self.ui.Ir.click()
        elif self.status[74] == -1:
            self.ui.Ir.setEnabled(False)
        if self.status[75] == 1:  
            self.ui.Pt.click()
        elif self.status[75] == -1:
            self.ui.Pt.setEnabled(False)
        if self.status[76] == 1:  
            self.ui.Au.click()
        elif self.status[76] == -1:
            self.ui.Au.setEnabled(False)
        if self.status[77] == 1:  
            self.ui.Hg.click()
        elif self.status[77] == -1:
            self.ui.Hg.setEnabled(False)
        if self.status[78] == 1:  
            self.ui.Tl.click()
        elif self.status[78] == -1:
            self.ui.Tl.setEnabled(False)
        if self.status[79] == 1:  
            self.ui.Pb.click()
        elif self.status[79] == -1:
            self.ui.Pb.setEnabled(False)
        if self.status[80] == 1:  
            self.ui.Bi.click()
        elif self.status[80] == -1:
            self.ui.Bi.setEnabled(False)
        if self.status[81] == 1:  
            self.ui.Po.click()
        elif self.status[81] == -1:
            self.ui.Po.setEnabled(False)
        if self.status[82] == 1:  
            self.ui.At.click()
        elif self.status[82] == -1:
            self.ui.At.setEnabled(False)
        if self.status[83] == 1:  
            self.ui.Rn.click()
        elif self.status[83] == -1:
            self.ui.Rn.setEnabled(False)
        if self.status[84] == 1:  
            self.ui.Fr.click()
        elif self.status[84] == -1:
            self.ui.Fr.setEnabled(False)
        if self.status[85] == 1:  
            self.ui.Ra.click()
        elif self.status[85] == -1:
            self.ui.Ra.setEnabled(False)
        if self.status[86] == 1:  
            self.ui.Ac.click()
        elif self.status[86] == -1:
            self.ui.Ac.setEnabled(False)
        if self.status[87] == 1:  
            self.ui.Th.click()
        elif self.status[87] == -1:
            self.ui.Th.setEnabled(False)
        if self.status[88] == 1:  
            self.ui.Pa.click()
        elif self.status[88] == -1:
            self.ui.Pa.setEnabled(False)
        if self.status[89] == 1:  
            self.ui.U.click()
        elif self.status[89] == -1:
            self.ui.U.setEnabled(False)
        if self.status[90] == 1:  
            self.ui.Np.click()
        elif self.status[90] == -1:
            self.ui.Np.setEnabled(False)
        if self.status[91] == 1:  
            self.ui.Pu.click()
        elif self.status[91] == -1:
            self.ui.Pu.setEnabled(False)
        if self.status[92] == 1:  
            self.ui.Am.click()
        elif self.status[92] == -1:
            self.ui.Am.setEnabled(False)
    '''
    "button-click" event handler
    '''
    def modifyElement(self, pressed):
        source = self.sender()
        # If user press the button down, set the status value to 1
        if pressed:
            if source.text() == "Li":
                self.status[0] = 1
            elif source.text() == "Be":
                self.status[1] = 1
            elif source.text() == "B":
                self.status[2] = 1
            elif source.text() == "C":
                self.status[3] = 1
            elif source.text() == "N":
                self.status[4] = 1
            elif source.text() == "O":
                self.status[5] = 1
            elif source.text() == "F":
                self.status[6] = 1
            elif source.text() == "Ne":
                self.status[7] = 1
            elif source.text() == "Na":
                self.status[8] = 1
            elif source.text() == "Mg":
                self.status[9] = 1
            elif source.text() == "Al":
                self.status[10] = 1
            elif source.text() == "Si":
                self.status[11] = 1
            elif source.text() == "P":
                self.status[12] = 1
            elif source.text() == "S":
                self.status[13] = 1
            elif source.text() == "Cl":
                self.status[14] = 1
            elif source.text() == "Ar":
                self.status[15] = 1
            elif source.text() == "K":
                self.status[16] = 1
            elif source.text() == "Ca":
                self.status[17] = 1
            elif source.text() == "Sc":
                self.status[18] = 1
            elif source.text() == "Ti":
                self.status[19] = 1
            elif source.text() == "V":
                self.status[20] = 1
            elif source.text() == "Cr":
                self.status[21] = 1
            elif source.text() == "Mn":
                self.status[22] = 1
            elif source.text() == "Fe":
                self.status[23] = 1
            elif source.text() == "Co":
                self.status[24] = 1
            elif source.text() == "Ni":
                self.status[25] = 1
            elif source.text() == "Cu":
                self.status[26] = 1
            elif source.text() == "Zn":
                self.status[27] = 1
            elif source.text() == "Ga":
                self.status[28] = 1
            elif source.text() == "Ge":
                self.status[29] = 1
            elif source.text() == "As":
                self.status[30] = 1
            elif source.text() == "Se":
                self.status[31] = 1
            elif source.text() == "Br":
                self.status[32] = 1
            elif source.text() == "Kr":
                self.status[33] = 1
            elif source.text() == "Rb":
                self.status[34] = 1
            elif source.text() == "Sr":
                self.status[35] = 1
            elif source.text() == "Y":
                self.status[36] = 1
            elif source.text() == "Zr":
                self.status[37] = 1
            elif source.text() == "Nb":
                self.status[38] = 1
            elif source.text() == "Mo":
                self.status[39] = 1
            elif source.text() == "Tc":
                self.status[40] = 1
            elif source.text() == "Ru":
                self.status[41] = 1
            elif source.text() == "Rh":
                self.status[42] = 1
            elif source.text() == "Pd":
                self.status[43] = 1
            elif source.text() == "Ag":
                self.status[44] = 1
            elif source.text() == "Cd":
                self.status[45] = 1
            elif source.text() == "In":
                self.status[46] = 1
            elif source.text() == "Sn":
                self.status[47] = 1
            elif source.text() == "Sb":
                self.status[48] = 1
            elif source.text() == "Te":
                self.status[49] = 1
            elif source.text() == "I":
                self.status[50] = 1
            elif source.text() == "Xe":
                self.status[51] = 1
            elif source.text() == "Cs":
                self.status[52] = 1
            elif source.text() == "Ba":
                self.status[53] = 1
            elif source.text() == "La":
                self.status[54] = 1
            elif source.text() == "Ce":
                self.status[55] = 1
            elif source.text() == "Pr":
                self.status[56] = 1
            elif source.text() == "Nd":
                self.status[57] = 1
            elif source.text() == "Pm":
                self.status[58] = 1
            elif source.text() == "Sm":
                self.status[59] = 1
            elif source.text() == "Eu":
                self.status[60] = 1
            elif source.text() == "Gd":
                self.status[61] = 1
            elif source.text() == "Tb":
                self.status[62] = 1
            elif source.text() == "Dy":
                self.status[63] = 1
            elif source.text() == "Ho":
                self.status[64] = 1
            elif source.text() == "Er":
                self.status[65] = 1
            elif source.text() == "Tm":
                self.status[66] = 1
            elif source.text() == "Yb":
                self.status[67] = 1
            elif source.text() == "Lu":
                self.status[68] = 1
            elif source.text() == "Hf":
                self.status[69] = 1
            elif source.text() == "Ta":
                self.status[70] = 1
            elif source.text() == "W":
                self.status[71] = 1
            elif source.text() == "Re":
                self.status[72] = 1
            elif source.text() == "Os":
                self.status[73] = 1
            elif source.text() == "Ir":
                self.status[74] = 1
            elif source.text() == "Pt":
                self.status[75] = 1
            elif source.text() == "Au":
                self.status[76] = 1
            elif source.text() == "Hg":
                self.status[77] = 1
            elif source.text() == "Tl":
                self.status[78] = 1
            elif source.text() == "Pb":
                self.status[79] = 1
            elif source.text() == "Bi":
                self.status[80] = 1
            elif source.text() == "Po":
                self.status[81] = 1
            elif source.text() == "At":
                self.status[82] = 1
            elif source.text() == "Rn":
                self.status[83] = 1
            elif source.text() == "Fr":
                self.status[84] = 1
            elif source.text() == "Ra":
                self.status[85] = 1
            elif source.text() == "Ac":
                self.status[86] = 1
            elif source.text() == "Th":
                self.status[87] = 1
            elif source.text() == "Pa":
                self.status[88] = 1
            elif source.text() == "U":
                self.status[89] = 1
            elif source.text() == "Np":
                self.status[90] = 1
            elif source.text() == "Pu":
                self.status[91] = 1
            elif source.text() == "Am":
                self.status[92] = 1
        
        # If user press the button up, set the status value to 0   
        else:
            if source.text() == "Li":
                self.status[0] = 0
            elif source.text() == "Be":
                self.status[1] = 0
            elif source.text() == "B":
                self.status[2] = 0
            elif source.text() == "C":
                self.status[3] = 0
            elif source.text() == "N":
                self.status[4] = 0
            elif source.text() == "O":
                self.status[5] = 0
            elif source.text() == "F":
                self.status[6] = 0
            elif source.text() == "Ne":
                self.status[7] = 0
            elif source.text() == "Na":
                self.status[8] = 0
            elif source.text() == "Mg":
                self.status[9] = 0
            elif source.text() == "Al":
                self.status[10] = 0
            elif source.text() == "Si":
                self.status[11] = 0
            elif source.text() == "P":
                self.status[12] = 0
            elif source.text() == "S":
                self.status[13] = 0
            elif source.text() == "Cl":
                self.status[14] = 0
            elif source.text() == "Ar":
                self.status[15] = 0
            elif source.text() == "K":
                self.status[16] = 0
            elif source.text() == "Ca":
                self.status[17] = 0
            elif source.text() == "Sc":
                self.status[18] = 0
            elif source.text() == "Ti":
                self.status[19] = 0
            elif source.text() == "V":
                self.status[20] = 0
            elif source.text() == "Cr":
                self.status[21] = 0
            elif source.text() == "Mn":
                self.status[22] = 0
            elif source.text() == "Fe":
                self.status[23] = 0
            elif source.text() == "Co":
                self.status[24] = 0
            elif source.text() == "Ni":
                self.status[25] = 0
            elif source.text() == "Cu":
                self.status[26] = 0
            elif source.text() == "Zn":
                self.status[27] = 0
            elif source.text() == "Ga":
                self.status[28] = 0
            elif source.text() == "Ge":
                self.status[29] = 0
            elif source.text() == "As":
                self.status[30] = 0
            elif source.text() == "Se":
                self.status[31] = 0
            elif source.text() == "Br":
                self.status[32] = 0
            elif source.text() == "Kr":
                self.status[33] = 0
            elif source.text() == "Rb":
                self.status[34] = 0
            elif source.text() == "Sr":
                self.status[35] = 0
            elif source.text() == "Y":
                self.status[36] = 0
            elif source.text() == "Zr":
                self.status[37] = 0
            elif source.text() == "Nb":
                self.status[38] = 0
            elif source.text() == "Mo":
                self.status[39] = 0
            elif source.text() == "Tc":
                self.status[40] = 0
            elif source.text() == "Ru":
                self.status[41] = 0
            elif source.text() == "Rh":
                self.status[42] = 0
            elif source.text() == "Pd":
                self.status[43] = 0
            elif source.text() == "Ag":
                self.status[44] = 0
            elif source.text() == "Cd":
                self.status[45] = 0
            elif source.text() == "In":
                self.status[46] = 0
            elif source.text() == "Sn":
                self.status[47] = 0
            elif source.text() == "Sb":
                self.status[48] = 0
            elif source.text() == "Te":
                self.status[49] = 0
            elif source.text() == "I":
                self.status[50] = 0
            elif source.text() == "Xe":
                self.status[51] = 0
            elif source.text() == "Cs":
                self.status[52] = 0
            elif source.text() == "Ba":
                self.status[53] = 0
            elif source.text() == "La":
                self.status[54] = 0
            elif source.text() == "Ce":
                self.status[55] = 0
            elif source.text() == "Pr":
                self.status[56] = 0
            elif source.text() == "Nd":
                self.status[57] = 0
            elif source.text() == "Pm":
                self.status[58] = 0
            elif source.text() == "Sm":
                self.status[59] = 0
            elif source.text() == "Eu":
                self.status[60] = 0
            elif source.text() == "Gd":
                self.status[61] = 0
            elif source.text() == "Tb":
                self.status[62] = 0
            elif source.text() == "Dy":
                self.status[63] = 0
            elif source.text() == "Ho":
                self.status[64] = 0
            elif source.text() == "Er":
                self.status[65] = 0
            elif source.text() == "Tm":
                self.status[66] = 0
            elif source.text() == "Yb":
                self.status[67] = 0
            elif source.text() == "Lu":
                self.status[68] = 0
            elif source.text() == "Hf":
                self.status[69] = 0
            elif source.text() == "Ta":
                self.status[70] = 0
            elif source.text() == "W":
                self.status[71] = 0
            elif source.text() == "Re":
                self.status[72] = 0
            elif source.text() == "Os":
                self.status[73] = 0
            elif source.text() == "Ir":
                self.status[74] = 0
            elif source.text() == "Pt":
                self.status[75] = 0
            elif source.text() == "Au":
                self.status[76] = 0
            elif source.text() == "Hg":
                self.status[77] = 0
            elif source.text() == "Tl":
                self.status[78] = 0
            elif source.text() == "Pb":
                self.status[79] = 0
            elif source.text() == "Bi":
                self.status[80] = 0
            elif source.text() == "Po":
                self.status[81] = 0
            elif source.text() == "At":
                self.status[82] = 0
            elif source.text() == "Rn":
                self.status[83] = 0
            elif source.text() == "Fr":
                self.status[84] = 0
            elif source.text() == "Ra":
                self.status[85] = 0
            elif source.text() == "Ac":
                self.status[86] = 0
            elif source.text() == "Th":
                self.status[87] = 0
            elif source.text() == "Pa":
                self.status[88] = 0
            elif source.text() == "U":
                self.status[89] = 0
            elif source.text() == "Np":
                self.status[90] = 0
            elif source.text() == "Pu":
                self.status[91] = 0
            elif source.text() == "Am":
                self.status[92] = 0      
    '''      
    Return user's modification
    '''
    @staticmethod
    def updateElementsStatus(previousElementsStatus):
        dialog = PeriodicTable(previousElementsStatus)
        result = dialog.exec_()
        return (dialog.status, result == QDialog.Accepted)
    '''
    Click OK, Accept the modification & Close the dialog
    '''
    def on_OK_clicked(self, checked=None):
        self.accept()
        self.close()
    '''
    Click Cancel, Discard modification & Close the dialog
    '''
    def on_Cancel_clicked(self, checked=None):
        self.close()
