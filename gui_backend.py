from PySide6.QtCore import QRunnable, Slot, Signal, QObject
import os
from read_cm_quantities import ReadCMQuantities

class FindCmWorker(QObject, QRunnable):
    finished = Signal(list)

    @Slot()
    def run(self):
        ipg_home_path = os.environ['IPGHOME']
        rel_cm_versions_path = "carmaker"
        cm_versions_path = os.path.join(ipg_home_path, rel_cm_versions_path)
        cm_versions = os.listdir(cm_versions_path)
        self.finished.emit(cm_versions)

class ReadCmQuantititesWorker(QObject, QRunnable):
    finished = Signal()

    @Slot()
    def run(self):
        read_cm_quantities = ReadCMQuantities()
        self.finished.emit()