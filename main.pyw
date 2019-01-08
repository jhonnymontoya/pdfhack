import sys
from PyQt5 import QtWidgets

from hack_pdf import HackPdf

app = QtWidgets.QApplication(sys.argv)

form = HackPdf()

sys.exit(app.exec_())