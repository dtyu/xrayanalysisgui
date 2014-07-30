#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ElementsDialog import *

# Class for the Periodic Table Dialog
class PeriodicTable(QtGui.QDialog):
    def __init__(self,SelectedElements,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_PeriodicTableDialog()
        self.ui.setupUi(self)

        self.Elements = SelectedElements
        
        # Set properties of buttons for each element
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
        # Load user's previous selection
        if self.Elements[0] == 1:  
            self.ui.Li.click()
        if self.Elements[1] == 1:  
            self.ui.Be.click()
        
    # Handle user's selection
    def modifyElement(self, pressed):
        source = self.sender()
        # If user press the button down, set the value to 1
        if pressed:
            if source.text() == "Li":
                self.Elements[0] = 1
            elif source.text() == "Be":
                self.Elements[1] = 1
            elif source.text() == "B":
                self.Elements[2] = 1
            elif source.text() == "C":
                self.Elements[3] = 1
            elif source.text() == "N":
                self.Elements[4] = 1
            elif source.text() == "O":
                self.Elements[5] = 1
            elif source.text() == "F":
                self.Elements[6] = 1
            elif source.text() == "Ne":
                self.Elements[7] = 1
            elif source.text() == "Na":
                self.Elements[8] = 1
            elif source.text() == "Mg":
                self.Elements[9] = 1
            elif source.text() == "Al":
                self.Elements[10] = 1
            elif source.text() == "Si":
                self.Elements[11] = 1
            elif source.text() == "P":
                self.Elements[12] = 1
            elif source.text() == "S":
                self.Elements[13] = 1
            elif source.text() == "Cl":
                self.Elements[14] = 1
            elif source.text() == "Ar":
                self.Elements[15] = 1
            elif source.text() == "K":
                self.Elements[16] = 1
            elif source.text() == "Ca":
                self.Elements[17] = 1
            elif source.text() == "Sc":
                self.Elements[18] = 1
            elif source.text() == "Ti":
                self.Elements[19] = 1
            elif source.text() == "V":
                self.Elements[20] = 1
            elif source.text() == "Cr":
                self.Elements[21] = 1
            elif source.text() == "Mn":
                self.Elements[22] = 1
            elif source.text() == "Fe":
                self.Elements[23] = 1
            elif source.text() == "Co":
                self.Elements[24] = 1
            elif source.text() == "Ni":
                self.Elements[25] = 1
            elif source.text() == "Cu":
                self.Elements[26] = 1
            elif source.text() == "Zn":
                self.Elements[27] = 1
            elif source.text() == "Ga":
                self.Elements[28] = 1
            elif source.text() == "Ge":
                self.Elements[29] = 1
            elif source.text() == "As":
                self.Elements[30] = 1
            elif source.text() == "Se":
                self.Elements[31] = 1
            elif source.text() == "Br":
                self.Elements[32] = 1
            elif source.text() == "Kr":
                self.Elements[33] = 1
            elif source.text() == "Rb":
                self.Elements[34] = 1
            elif source.text() == "Sr":
                self.Elements[35] = 1
            elif source.text() == "Y":
                self.Elements[36] = 1
            elif source.text() == "Zr":
                self.Elements[37] = 1
            elif source.text() == "Nb":
                self.Elements[38] = 1
            elif source.text() == "Mo":
                self.Elements[39] = 1
            elif source.text() == "Tc":
                self.Elements[40] = 1
            elif source.text() == "Ru":
                self.Elements[41] = 1
            elif source.text() == "Rh":
                self.Elements[42] = 1
            elif source.text() == "Pd":
                self.Elements[43] = 1
            elif source.text() == "Ag":
                self.Elements[44] = 1
            elif source.text() == "Cd":
                self.Elements[45] = 1
            elif source.text() == "In":
                self.Elements[46] = 1
            elif source.text() == "Sn":
                self.Elements[47] = 1
            elif source.text() == "Sb":
                self.Elements[48] = 1
            elif source.text() == "Te":
                self.Elements[49] = 1
            elif source.text() == "I":
                self.Elements[50] = 1
            elif source.text() == "Xe":
                self.Elements[51] = 1
            elif source.text() == "Cs":
                self.Elements[52] = 1
            elif source.text() == "Ba":
                self.Elements[53] = 1
            elif source.text() == "La":
                self.Elements[54] = 1
            elif source.text() == "Ce":
                self.Elements[55] = 1
            elif source.text() == "Pr":
                self.Elements[56] = 1
            elif source.text() == "Nd":
                self.Elements[57] = 1
            elif source.text() == "Pm":
                self.Elements[58] = 1
            elif source.text() == "Sm":
                self.Elements[59] = 1
            elif source.text() == "Eu":
                self.Elements[60] = 1
            elif source.text() == "Gd":
                self.Elements[61] = 1
            elif source.text() == "Tb":
                self.Elements[62] = 1
            elif source.text() == "Dy":
                self.Elements[63] = 1
            elif source.text() == "Ho":
                self.Elements[64] = 1
            elif source.text() == "Er":
                self.Elements[65] = 1
            elif source.text() == "Tm":
                self.Elements[66] = 1
            elif source.text() == "Yb":
                self.Elements[67] = 1
            elif source.text() == "Lu":
                self.Elements[68] = 1
            elif source.text() == "Hf":
                self.Elements[69] = 1
            elif source.text() == "Ta":
                self.Elements[70] = 1
            elif source.text() == "W":
                self.Elements[71] = 1
            elif source.text() == "Re":
                self.Elements[72] = 1
            elif source.text() == "Os":
                self.Elements[73] = 1
            elif source.text() == "Ir":
                self.Elements[74] = 1
            elif source.text() == "Pt":
                self.Elements[75] = 1
            elif source.text() == "Au":
                self.Elements[76] = 1
            elif source.text() == "Hg":
                self.Elements[77] = 1
            elif source.text() == "Tl":
                self.Elements[78] = 1
            elif source.text() == "Pb":
                self.Elements[79] = 1
            elif source.text() == "Bi":
                self.Elements[80] = 1
            elif source.text() == "Po":
                self.Elements[81] = 1
            elif source.text() == "At":
                self.Elements[82] = 1
            elif source.text() == "Rn":
                self.Elements[83] = 1
            elif source.text() == "Fr":
                self.Elements[84] = 1
            elif source.text() == "Ra":
                self.Elements[85] = 1
            elif source.text() == "Ac":
                self.Elements[86] = 1
            elif source.text() == "Th":
                self.Elements[87] = 1
            elif source.text() == "Pa":
                self.Elements[88] = 1
            elif source.text() == "U":
                self.Elements[89] = 1
            elif source.text() == "Np":
                self.Elements[90] = 1
            elif source.text() == "Pu":
                self.Elements[91] = 1
            elif source.text() == "Am":
                self.Elements[92] = 1
        
        # If user press the button up, set the value to 0   
        else:
            if source.text() == "Li":
                self.Elements[0] = 0
            elif source.text() == "Be":
                self.Elements[1] = 0
            elif source.text() == "B":
                self.Elements[2] = 0
            elif source.text() == "C":
                self.Elements[3] = 0
            elif source.text() == "N":
                self.Elements[4] = 0
            elif source.text() == "O":
                self.Elements[5] = 0
            elif source.text() == "F":
                self.Elements[6] = 0
            elif source.text() == "Ne":
                self.Elements[7] = 0
            elif source.text() == "Na":
                self.Elements[8] = 0
            elif source.text() == "Mg":
                self.Elements[9] = 0
            elif source.text() == "Al":
                self.Elements[10] = 0
            elif source.text() == "Si":
                self.Elements[11] = 0
            elif source.text() == "P":
                self.Elements[12] = 0
            elif source.text() == "S":
                self.Elements[13] = 0
            elif source.text() == "Cl":
                self.Elements[14] = 0
            elif source.text() == "Ar":
                self.Elements[15] = 0
            elif source.text() == "K":
                self.Elements[16] = 0
            elif source.text() == "Ca":
                self.Elements[17] = 0
            elif source.text() == "Sc":
                self.Elements[18] = 0
            elif source.text() == "Ti":
                self.Elements[19] = 0
            elif source.text() == "V":
                self.Elements[20] = 0
            elif source.text() == "Cr":
                self.Elements[21] = 0
            elif source.text() == "Mn":
                self.Elements[22] = 0
            elif source.text() == "Fe":
                self.Elements[23] = 0
            elif source.text() == "Co":
                self.Elements[24] = 0
            elif source.text() == "Ni":
                self.Elements[25] = 0
            elif source.text() == "Cu":
                self.Elements[26] = 0
            elif source.text() == "Zn":
                self.Elements[27] = 0
            elif source.text() == "Ga":
                self.Elements[28] = 0
            elif source.text() == "Ge":
                self.Elements[29] = 0
            elif source.text() == "As":
                self.Elements[30] = 0
            elif source.text() == "Se":
                self.Elements[31] = 0
            elif source.text() == "Br":
                self.Elements[32] = 0
            elif source.text() == "Kr":
                self.Elements[33] = 0
            elif source.text() == "Rb":
                self.Elements[34] = 0
            elif source.text() == "Sr":
                self.Elements[35] = 0
            elif source.text() == "Y":
                self.Elements[36] = 0
            elif source.text() == "Zr":
                self.Elements[37] = 0
            elif source.text() == "Nb":
                self.Elements[38] = 0
            elif source.text() == "Mo":
                self.Elements[39] = 0
            elif source.text() == "Tc":
                self.Elements[40] = 0
            elif source.text() == "Ru":
                self.Elements[41] = 0
            elif source.text() == "Rh":
                self.Elements[42] = 0
            elif source.text() == "Pd":
                self.Elements[43] = 0
            elif source.text() == "Ag":
                self.Elements[44] = 0
            elif source.text() == "Cd":
                self.Elements[45] = 0
            elif source.text() == "In":
                self.Elements[46] = 0
            elif source.text() == "Sn":
                self.Elements[47] = 0
            elif source.text() == "Sb":
                self.Elements[48] = 0
            elif source.text() == "Te":
                self.Elements[49] = 0
            elif source.text() == "I":
                self.Elements[50] = 0
            elif source.text() == "Xe":
                self.Elements[51] = 0
            elif source.text() == "Cs":
                self.Elements[52] = 0
            elif source.text() == "Ba":
                self.Elements[53] = 0
            elif source.text() == "La":
                self.Elements[54] = 0
            elif source.text() == "Ce":
                self.Elements[55] = 0
            elif source.text() == "Pr":
                self.Elements[56] = 0
            elif source.text() == "Nd":
                self.Elements[57] = 0
            elif source.text() == "Pm":
                self.Elements[58] = 0
            elif source.text() == "Sm":
                self.Elements[59] = 0
            elif source.text() == "Eu":
                self.Elements[60] = 0
            elif source.text() == "Gd":
                self.Elements[61] = 0
            elif source.text() == "Tb":
                self.Elements[62] = 0
            elif source.text() == "Dy":
                self.Elements[63] = 0
            elif source.text() == "Ho":
                self.Elements[64] = 0
            elif source.text() == "Er":
                self.Elements[65] = 0
            elif source.text() == "Tm":
                self.Elements[66] = 0
            elif source.text() == "Yb":
                self.Elements[67] = 0
            elif source.text() == "Lu":
                self.Elements[68] = 0
            elif source.text() == "Hf":
                self.Elements[69] = 0
            elif source.text() == "Ta":
                self.Elements[70] = 0
            elif source.text() == "W":
                self.Elements[71] = 0
            elif source.text() == "Re":
                self.Elements[72] = 0
            elif source.text() == "Os":
                self.Elements[73] = 0
            elif source.text() == "Ir":
                self.Elements[74] = 0
            elif source.text() == "Pt":
                self.Elements[75] = 0
            elif source.text() == "Au":
                self.Elements[76] = 0
            elif source.text() == "Hg":
                self.Elements[77] = 0
            elif source.text() == "Tl":
                self.Elements[78] = 0
            elif source.text() == "Pb":
                self.Elements[79] = 0
            elif source.text() == "Bi":
                self.Elements[80] = 0
            elif source.text() == "Po":
                self.Elements[81] = 0
            elif source.text() == "At":
                self.Elements[82] = 0
            elif source.text() == "Rn":
                self.Elements[83] = 0
            elif source.text() == "Fr":
                self.Elements[84] = 0
            elif source.text() == "Ra":
                self.Elements[85] = 0
            elif source.text() == "Ac":
                self.Elements[86] = 0
            elif source.text() == "Th":
                self.Elements[87] = 0
            elif source.text() == "Pa":
                self.Elements[88] = 0
            elif source.text() == "U":
                self.Elements[89] = 0
            elif source.text() == "Np":
                self.Elements[90] = 0
            elif source.text() == "Pu":
                self.Elements[91] = 0
            elif source.text() == "Am":
                self.Elements[92] = 0
            
            
    # Returen use's selection result
    @staticmethod
    def getSelectedElements(SelectedElements):
        dialog = PeriodicTable(SelectedElements)
        result = dialog.exec_()
        return (dialog.Elements, result == QDialog.Accepted)
    '''
    # If user click OK
    # Accept the selection
    # Close the Dialog
    '''
    def on_OK_clicked(self, checked=None):
        self.accept()
        self.close()
    '''
    # If user click Cancel
    # Close the Dialog
    '''
    def on_Cancel_clicked(self, checked=None):
        self.close()
