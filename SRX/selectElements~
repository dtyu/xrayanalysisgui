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
        # Intialize variables
        self.SelectTi = 0
        self.SelectV = 0
        self.SelectCr = 0
        self.SelectMn = 0
        self.SelectFe = 0
        self.SelectCo = 0
        self.SelectNi = 0
        self.SelectCu = 0
        self.SelectZn = 0
        self.SelectGa = 0
        self.SelectGe = 0
        self.SelectAs = 0
        self.SelectSe = 0
        self.SelectBr = 0
        self.SelectKr = 0
        self.SelectRb = 0
        self.SelectSr = 0
        self.SelectY = 0
        self.SelectZr = 0
        self.SelectNb = 0
        self.SelectMo = 0
        self.SelectTc = 0
        self.SelectRu = 0
        self.SelectRh = 0
        self.SelectPd = 0
        self.SelectAg = 0
        self.SelectCd = 0
        self.SelectIn = 0
        self.SelectSn = 0
        self.SelectSb = 0
        self.SelectTe = 0
        self.SelectI = 0
        self.SelectXe = 0
        self.SelectCs = 0
        self.SelectBa = 0
        self.SelectHf = 0
        self.SelectTa = 0
        self.SelectW = 0
        self.SelectRe = 0
        self.SelectOs = 0
        self.SelectIr = 0
        self.SelectPt = 0
        self.SelectAu = 0
        self.SelectHg = 0
        self.SelectTl = 0
        self.SelectPb = 0
        self.SelectBi = 0
        self.SelectPo = 0
        self.SelectAt = 0
        self.SelectRn = 0
        self.SelectFr = 0
        self.SelectRa = 0
        self.SelectLa = 0
        self.SelectCe = 0
        self.SelectPr = 0
        self.SelectNd = 0
        self.SelectPm = 0
        self.SelectSm = 0
        self.SelectEu = 0
        self.SelectGd = 0
        self.SelectTb = 0
        self.SelectDy = 0
        self.SelectHo = 0
        self.SelectEr = 0
        self.SelectTm = 0
        self.SelectYb = 0
        self.SelectLu = 0
        self.SelectAc = 0
        self.SelectTh = 0
        self.SelectPa = 0
        self.SelectU = 0
        self.SelectNp = 0
        self.SelectPu = 0
        self.SelectAm = 0
        # Set properties of buttons for each element
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
        if SelectedElements[0] == 1:  
            self.ui.Ti.click()
        if SelectedElements[1] == 1:
            self.ui.V.click()
        if SelectedElements[2] == 1:
            self.ui.Cr.click()
        if SelectedElements[3] == 1:
            self.ui.Mn.click()
        if SelectedElements[4] == 1:
            self.ui.Fe.click()
        if SelectedElements[5] == 1:  
            self.ui.Co.click()
        if SelectedElements[6] == 1:
            self.ui.Ni.click()
        if SelectedElements[7] == 1:
            self.ui.Cu.click()
        if SelectedElements[8] == 1:
            self.ui.Zn.click()
        if SelectedElements[9] == 1:
            self.ui.Ga.click()
        if SelectedElements[10] == 1:  
            self.ui.Ge.click()
        if SelectedElements[11] == 1:
            self.ui.As.click()
        if SelectedElements[12] == 1:
            self.ui.Se.click()
        if SelectedElements[13] == 1:
            self.ui.Br.click()
        if SelectedElements[14] == 1:
            self.ui.Kr.click()
        if SelectedElements[15] == 1:  
            self.ui.Rb.click()
        if SelectedElements[16] == 1:
            self.ui.Sr.click()
        if SelectedElements[17] == 1:
            self.ui.Y.click()
        if SelectedElements[18] == 1:
            self.ui.Zr.click()
        if SelectedElements[19] == 1:
            self.ui.Nb.click()
        if SelectedElements[20] == 1:
            self.ui.Mo.click()
        if SelectedElements[21] == 1:
            self.ui.Tc.click()
        if SelectedElements[22] == 1:  
            self.ui.Ru.click()
        if SelectedElements[23] == 1:
            self.ui.Rh.click()
        if SelectedElements[24] == 1:
            self.ui.Pd.click()
        if SelectedElements[25] == 1:
            self.ui.Ag.click()
        if SelectedElements[26] == 1:
            self.ui.Cd.click()
        if SelectedElements[27] == 1:  
            self.ui.In.click()
        if SelectedElements[28] == 1:
            self.ui.Sn.click()
        if SelectedElements[29] == 1:
            self.ui.Sb.click()
        if SelectedElements[30] == 1:
            self.ui.Te.click()
        if SelectedElements[31] == 1:
            self.ui.I.click()
        if SelectedElements[32] == 1:  
            self.ui.Xe.click()
        if SelectedElements[33] == 1:
            self.ui.Cs.click()
        if SelectedElements[34] == 1:
            self.ui.Ba.click()
        if SelectedElements[35] == 1:
            self.ui.Hf.click()
        if SelectedElements[36] == 1:
            self.ui.Ta.click()
        if SelectedElements[37] == 1:  
            self.ui.W.click()
        if SelectedElements[38] == 1:
            self.ui.Re.click()
        if SelectedElements[39] == 1:
            self.ui.Os.click()
        if SelectedElements[40] == 1:
            self.ui.Ir.click()
        if SelectedElements[41] == 1:
            self.ui.Pt.click()
        if SelectedElements[42] == 1:
            self.ui.Au.click()
        if SelectedElements[43] == 1:
            self.ui.Hg.click()
        if SelectedElements[44] == 1:  
            self.ui.Tl.click()
        if SelectedElements[45] == 1:
            self.ui.Pb.click()
        if SelectedElements[46] == 1:
            self.ui.Bi.click()
        if SelectedElements[47] == 1:
            self.ui.Po.click()
        if SelectedElements[48] == 1:
            self.ui.At.click()
        if SelectedElements[49] == 1:  
            self.ui.Rn.click()
        if SelectedElements[50] == 1:
            self.ui.Fr.click()
        if SelectedElements[51] == 1:
            self.ui.Ra.click()
        if SelectedElements[52] == 1:
            self.ui.La.click()
        if SelectedElements[53] == 1:
            self.ui.Ce.click()
        if SelectedElements[54] == 1:  
            self.ui.Pr.click()
        if SelectedElements[55] == 1:
            self.ui.Nd.click()
        if SelectedElements[56] == 1:
            self.ui.Pm.click()
        if SelectedElements[57] == 1:
            self.ui.Sm.click()
        if SelectedElements[58] == 1:
            self.ui.Eu.click()
        if SelectedElements[59] == 1:  
            self.ui.Gd.click()
        if SelectedElements[60] == 1:
            self.ui.Tb.click()
        if SelectedElements[61] == 1:
            self.ui.Dy.click()
        if SelectedElements[62] == 1:
            self.ui.Ho.click()
        if SelectedElements[63] == 1:
            self.ui.Er.click()
        if SelectedElements[64] == 1:
            self.ui.Tm.click()
        if SelectedElements[65] == 1:
            self.ui.Yb.click()
        if SelectedElements[66] == 1:  
            self.ui.Lu.click()
        if SelectedElements[67] == 1:
            self.ui.Ac.click()
        if SelectedElements[68] == 1:
            self.ui.Th.click()
        if SelectedElements[69] == 1:
            self.ui.Pa.click()
        if SelectedElements[70] == 1:
            self.ui.U.click()
        if SelectedElements[71] == 1:  
            self.ui.Np.click()
        if SelectedElements[72] == 1:
            self.ui.Pu.click()
        if SelectedElements[73] == 1:
            self.ui.Am.click()
    # Handle user's selection
    def modifyElement(self, pressed):
        source = self.sender()
        if pressed:
            if source.text() == "Ti":
                self.SelectTi = 1
            elif source.text() == "V":
                self.SelectV = 1
            elif source.text() == "Cr":
                self.SelectCr = 1
            elif source.text() == "Mn":
                self.SelectMn = 1
            elif source.text() == "Fe":
                self.SelectFe = 1
            elif source.text() == "Co":
                self.SelectCo = 1
            elif source.text() == "Ni":
                self.SelectNi = 1
            elif source.text() == "Cu":
                self.SelectCu = 1
            elif source.text() == "Zn":
                self.SelectZn = 1
            elif source.text() == "Ga":
                self.SelectGa = 1
            elif source.text() == "Ge":
                self.SelectGe = 1
            elif source.text() == "As":
                self.SelectAs = 1
            elif source.text() == "Se":
                self.SelectSe = 1
            elif source.text() == "Br":
                self.SelectBr = 1
            elif source.text() == "Kr":
                self.SelectKr = 1
            elif source.text() == "Rb":
                self.SelectRb = 1
            elif source.text() == "Sr":
                self.SelectSr = 1
            elif source.text() == "Y":
                self.SelectY = 1
            elif source.text() == "Zr":
                self.SelectZr = 1
            elif source.text() == "Nb":
                self.SelectNb = 1
            elif source.text() == "Mo":
                self.SelectMo = 1
            elif source.text() == "Tc":
                self.SelectTc = 1
            elif source.text() == "Ru":
                self.SelectRu = 1
            elif source.text() == "Rh":
                self.SelectRh = 1
            elif source.text() == "Pd":
                self.SelectPd = 1
            elif source.text() == "Ag":
                self.SelectAg = 1
            elif source.text() == "Cd":
                self.SelectCd = 1
            elif source.text() == "In":
                self.SelectIn = 1
            elif source.text() == "Sn":
                self.SelectSn = 1
            elif source.text() == "Sb":
                self.SelectSb = 1
            elif source.text() == "Te":
                self.SelectTe = 1
            elif source.text() == "I":
                self.SelectI = 1
            elif source.text() == "Xe":
                self.SelectXe = 1
            elif source.text() == "Cs":
                self.SelectCs = 1
            elif source.text() == "Ba":
                self.SelectBa = 1
            elif source.text() == "Hf":
                self.SelectHf = 1
            elif source.text() == "Ta":
                self.SelectTa = 1
            elif source.text() == "W":
                self.SelectW = 1
            elif source.text() == "Re":
                self.SelectRe = 1
            elif source.text() == "Os":
                self.SelectOs = 1
            elif source.text() == "Ir":
                self.SelectIr = 1
            elif source.text() == "Pt":
                self.SelectPt = 1
            elif source.text() == "Au":
                self.SelectAu = 1
            elif source.text() == "Hg":
                self.SelectHg = 1
            elif source.text() == "Tl":
                self.SelectTl = 1
            elif source.text() == "Pb":
                self.SelectPb = 1
            elif source.text() == "Bi":
                self.SelectBi = 1
            elif source.text() == "Po":
                self.SelectPo = 1
            elif source.text() == "At":
                self.SelectAt = 1
            elif source.text() == "Rn":
                self.SelectRn = 1
            elif source.text() == "Fr":
                self.SelectFr = 1
            elif source.text() == "Ra":
                self.SelectRa = 1
            elif source.text() == "La":
                self.SelectLa = 1
            elif source.text() == "Ce":
                self.SelectCe = 1
            elif source.text() == "Pr":
                self.SelectPr = 1
            elif source.text() == "Nd":
                self.SelectNd = 1
            elif source.text() == "Pm":
                self.SelectPm = 1
            elif source.text() == "Sm":
                self.SelectSm = 1
            elif source.text() == "Eu":
                self.SelectEu = 1
            elif source.text() == "Gd":
                self.SelectGd = 1
            elif source.text() == "Tb":
                self.SelectTb = 1
            elif source.text() == "Dy":
                self.SelectDy = 1
            elif source.text() == "Ho":
                self.SelectHo = 1
            elif source.text() == "Er":
                self.SelectEr = 1
            elif source.text() == "Tm":
                self.SelectTm = 1
            elif source.text() == "Yb":
                self.SelectYb = 1
            elif source.text() == "Lu":
                self.SelectLu = 1
            elif source.text() == "Ac":
                self.SelectAc = 1
            elif source.text() == "Th":
                self.SelectTh = 1
            elif source.text() == "Pa":
                self.SelectPa = 1
            elif source.text() == "U":
                self.SelectU = 1
            elif source.text() == "Np":
                self.SelectNp = 1
            elif source.text() == "Pu":
                self.SelectPu = 1
            elif source.text() == "Am":
                self.SelectAm = 1
        else:
            if source.text() == "Ti":
                self.SelectTi = 0
            elif source.text() == "V":
                self.SelectV = 0
            elif source.text() == "Cr":
                self.SelectCr = 0
            elif source.text() == "Mn":
                self.SelectMn = 0
            elif source.text() == "Fe":
                self.SelectFe = 0
            elif source.text() == "Co":
                self.SelectCo = 0
            elif source.text() == "Ni":
                self.SelectNi = 0
            elif source.text() == "Cu":
                self.SelectCu = 0
            elif source.text() == "Zn":
                self.SelectZn = 0
            elif source.text() == "Ga":
                self.SelectGa = 0
            elif source.text() == "Ge":
                self.SelectGe = 0
            elif source.text() == "As":
                self.SelectAs = 0
            elif source.text() == "Se":
                self.SelectSe = 0
            elif source.text() == "Br":
                self.SelectBr = 0
            elif source.text() == "Kr":
                self.SelectKr = 0
            elif source.text() == "Rb":
                self.SelectRb = 0
            elif source.text() == "Sr":
                self.SelectSr = 0
            elif source.text() == "Y":
                self.SelectY = 0
            elif source.text() == "Zr":
                self.SelectZr = 0
            elif source.text() == "Nb":
                self.SelectNb = 0
            elif source.text() == "Mo":
                self.SelectMo = 0
            elif source.text() == "Tc":
                self.SelectTc = 0
            elif source.text() == "Ru":
                self.SelectRu = 0
            elif source.text() == "Rh":
                self.SelectRh = 0
            elif source.text() == "Pd":
                self.SelectPd = 0
            elif source.text() == "Ag":
                self.SelectAg = 0
            elif source.text() == "Cd":
                self.SelectCd = 0
            elif source.text() == "In":
                self.SelectIn = 0
            elif source.text() == "Sn":
                self.SelectSn = 0
            elif source.text() == "Sb":
                self.SelectSb = 0
            elif source.text() == "Te":
                self.SelectTe = 0
            elif source.text() == "I":
                self.SelectI = 0
            elif source.text() == "Xe":
                self.SelectXe = 0
            elif source.text() == "Cs":
                self.SelectCs = 0
            elif source.text() == "Ba":
                self.SelectBa = 0
            elif source.text() == "Hf":
                self.SelectHf = 0
            elif source.text() == "Ta":
                self.SelectTa = 0
            elif source.text() == "W":
                self.SelectW = 0
            elif source.text() == "Re":
                self.SelectRe = 0
            elif source.text() == "Os":
                self.SelectOs = 0
            elif source.text() == "Ir":
                self.SelectIr = 0
            elif source.text() == "Pt":
                self.SelectPt = 0
            elif source.text() == "Au":
                self.SelectAu = 0
            elif source.text() == "Hg":
                self.SelectHg = 0
            elif source.text() == "Tl":
                self.SelectTl = 0
            elif source.text() == "Pb":
                self.SelectPb = 0
            elif source.text() == "Bi":
                self.SelectBi = 0
            elif source.text() == "Po":
                self.SelectPo = 0
            elif source.text() == "At":
                self.SelectAt = 0
            elif source.text() == "Rn":
                self.SelectRn = 0
            elif source.text() == "Fr":
                self.SelectFr = 0
            elif source.text() == "Ra":
                self.SelectRa = 0
            elif source.text() == "La":
                self.SelectLa = 0
            elif source.text() == "Ce":
                self.SelectCe = 0
            elif source.text() == "Pr":
                self.SelectPr = 0
            elif source.text() == "Nd":
                self.SelectNd = 0
            elif source.text() == "Pm":
                self.SelectPm = 0
            elif source.text() == "Sm":
                self.SelectSm = 0
            elif source.text() == "Eu":
                self.SelectEu = 0
            elif source.text() == "Gd":
                self.SelectGd = 0
            elif source.text() == "Tb":
                self.SelectTb = 0
            elif source.text() == "Dy":
                self.SelectDy = 0
            elif source.text() == "Ho":
                self.SelectHo = 0
            elif source.text() == "Er":
                self.SelectEr = 0
            elif source.text() == "Tm":
                self.SelectTm = 0
            elif source.text() == "Yb":
                self.SelectYb = 0
            elif source.text() == "Lu":
                self.SelectLu = 0
            elif source.text() == "Ac":
                self.SelectAc = 0
            elif source.text() == "Th":
                self.SelectTh = 0
            elif source.text() == "Pa":
                self.SelectPa = 0
            elif source.text() == "U":
                self.SelectU = 0
            elif source.text() == "Np":
                self.SelectNp = 0
            elif source.text() == "Pu":
                self.SelectPu = 0
            elif source.text() == "Am":
                self.SelectAm = 0
    # Returen use's selection result
    @staticmethod
    def getSelectedElements(SelectedElements):
        dialog = PeriodicTable(SelectedElements)
        result = dialog.exec_()
        dialog.SelectElements = [dialog.SelectTi,dialog.SelectV,dialog.SelectCr,
                                 dialog.SelectMn,dialog.SelectFe,dialog.SelectCo,
                                 dialog.SelectNi,dialog.SelectCu,dialog.SelectZn,
                                 dialog.SelectGa,dialog.SelectGe,dialog.SelectAs,
                                 dialog.SelectSe,dialog.SelectBr,dialog.SelectKr,
                                 dialog.SelectRb,dialog.SelectSr,dialog.SelectY,
                                 dialog.SelectZr,dialog.SelectNb,dialog.SelectMo,
                                 dialog.SelectTc,dialog.SelectRu,dialog.SelectRh,
                                 dialog.SelectPd,dialog.SelectAg,dialog.SelectCd,
                                 dialog.SelectIn,dialog.SelectSn,dialog.SelectSb,
                                 dialog.SelectTe,dialog.SelectI,dialog.SelectXe,
                                 dialog.SelectCs,dialog.SelectBa,dialog.SelectHf,
                                 dialog.SelectTa,dialog.SelectW,dialog.SelectRe,
                                 dialog.SelectOs,dialog.SelectIr,dialog.SelectPt,
                                 dialog.SelectAu,dialog.SelectHg,dialog.SelectTl,
                                 dialog.SelectPb,dialog.SelectBi,dialog.SelectPo,
                                 dialog.SelectAt,dialog.SelectRn,dialog.SelectFr,
                                 dialog.SelectRa,dialog.SelectLa,dialog.SelectCe,
                                 dialog.SelectPr,dialog.SelectNd,dialog.SelectPm,
                                 dialog.SelectSm,dialog.SelectEu,dialog.SelectGd,
                                 dialog.SelectTb,dialog.SelectDy,dialog.SelectHo,
                                 dialog.SelectEr,dialog.SelectTm,dialog.SelectYb,
                                 dialog.SelectLu,dialog.SelectAc,dialog.SelectTh,
                                 dialog.SelectPa,dialog.SelectU,dialog.SelectNp,
                                 dialog.SelectPu,dialog.SelectAm,
                                 ]
        return (dialog.SelectElements, result == QDialog.Accepted)
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
