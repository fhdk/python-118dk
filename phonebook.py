#!/usr/bin/python3
# -*- coding: utf8 -*-

# Copyright 2021 Frede Hundewadt
#
# Permission is hereby granted, free of charge,
# to any person obtaining a copy of this software and
# associated documentation files (the "Software"),
# to deal in the Software without restriction,
# including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished
# to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from PySide6 import QtCore, QtWidgets
import sys
import parse_url


class Lookup(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.buttonLookup = QtWidgets.QPushButton("Lav opslag 118.dk")
        self.labelAddressHint = QtWidgets.QLabel("Husnummer kan bruges som afgrænsning på større områder.\nEksempel: Ryhaven, 8210 eller Bispehavevej 121, 8210")
        self.textAddress = QtWidgets.QLineEdit("vejnavn [nr], postnummer")
        self.textResult = QtWidgets.QTextEdit("")
        self.textResult.setReadOnly(True)
        self.textResult.setFontFamily("monospace")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.labelAddressHint)
        self.layout.addWidget(self.textAddress)
        self.layout.addWidget(self.buttonLookup)
        self.layout.addWidget(self.textResult)

        self.buttonLookup.clicked.connect(self.lookup)

    @QtCore.Slot()
    def lookup(self):
        """ run lookup """
        self.textResult.clear()
        if self.textAddress.text() == "vejnavn [nr], postnummer":
            self.textResult.setPlainText("kan ikke findes")
            return
        # run lookup

        self.textResult.setPlainText("Vent venligst ...")
        results = parse_url.parse_url(self.textAddress.text())
        txt = ""
        for result in results:
            txt = f"{txt}Adresse : {result['address']}\n"
            txt = f"{txt}   Navn : {result['name']}\n"
            for number in result["phones"]:
                txt = f"{txt}    Tlf : {number}\n"
            txt = f"{txt}---------------------\n"
        self.textResult.setPlainText(txt)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Lookup()
    widget.resize(600, 600)
    widget.show()
    sys.exit(app.exec())
