# -*- coding: utf-8 -*-

from os import path
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtCore import Qt
import PyPDF2
from threading import Thread, activeCount
import random

FORM_CLASS, _ = uic.loadUiType(path.join(path.dirname(__file__), 'hack_pdf_ui.ui'))

class HackPdf(QMainWindow, FORM_CLASS):

    archivo_pdf = None
    desde = None
    hasta = None
    correr = False
    thread = None
    
    def __init__(self, parent = None):
        flags = Qt.Window | Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint
        super(HackPdf, self).__init__(parent = parent, flags = flags)
        self.setupUi(self)
        self.show()

    def btnSeleccionarArchivo_clicked(self):
        archivo = QFileDialog.getOpenFileName(self, u"Seleccione un archivo", path.expanduser("~"), "Archivos PDF (*.pdf)")
        if len(archivo[0]):
            self.archivo_pdf = archivo[0]
            nombreArchivo = path.basename(archivo[0])
            self.lblArchivo.setText(nombreArchivo)
            self.wConfig.setEnabled(True)
            self.wStatus.setEnabled(True)
            self.wBotones.setEnabled(True)
            self.btnParar.setEnabled(False)

    def sbDesde_valueChanged(self, numeroDesde):
        self.sbHasta.setMinimum(numeroDesde + 1)

    def btnIniciar_clicked(self):
        self.btnIniciar.setEnabled(False)
        self.btnParar.setEnabled(True)
        self.btnSeleccionarArchivo.setEnabled(False)
        self.wConfig.setEnabled(False)

        self.desde = self.sbDesde.value()
        self.hasta = self.sbHasta.value()

        self.thread = Thread(target = self.procesar)
        self.thread.setDaemon(True)
        self.correr = True
        self.thread.start()
    
    def btnParar_clicked(self):
        self.btnIniciar.setEnabled(True)
        self.btnParar.setEnabled(False)
        self.btnSeleccionarArchivo.setEnabled(True)
        self.wConfig.setEnabled(True)

        self.correr = False
        if self.thread != None:
            while self.thread.is_alive():
                continue
            self.thread = None

    def procesar(self):
        pdfReader = PyPDF2.PdfFileReader(open(self.archivo_pdf, 'rb'))
        while self.correr:
            if self.desde <= self.hasta:
                if random.randrange(50) == 1:
                    self.lblStatus.setText(u"Probando: {0}".format(self.desde))

                passwordParaProbar = str(self.desde)
                if pdfReader.decrypt(passwordParaProbar) == 1:
                    self.lblStatus.setText(u"¡¡Contraseña encontrada {0}!!".format(passwordParaProbar))
                    self.btnParar_clicked()
                    break
            else:
                self.lblStatus.setText(u"Fin, no se encontró contraseña")
                self.btnParar_clicked()
                break
            self.desde += 1
        return