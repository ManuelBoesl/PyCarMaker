from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QComboBox, QPushButton, QLabel
)
from PySide6.QtCore import QThreadPool, QMetaObject, Qt
import sys
import os
import qdarktheme

from gui_backend import FindCmWorker, ReadCmQuantititesWorker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        qdarktheme.setup_theme()
        self.setWindowTitle("Dropdown Menu Example")
        self.worker = None
        # Set the window size
        self.resize(400, 200)  # width: 400, height: 200

        # Create a central widget and set it as the main window's central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a vertical layout
        self.layout = QVBoxLayout(self.central_widget)

        # Create a dropdown menu (QComboBox)
        self.combo_box = QComboBox()
        self.layout.addWidget(self.combo_box)

        # Create an OK button (QPushButton)
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.on_ok_clicked)
        self.layout.addWidget(self.ok_button)
        self.chosen_cm_version = None
        # Create a thread pool
        self.thread_pool = QThreadPool()

        # Start the worker
        self.start_cm_finder_worker()

    def start_cm_finder_worker(self):
        # Create a FindCmWorker instance
        self.worker = FindCmWorker()

        # Connect the worker's finished signal to the update_combo_box slot
        self.worker.finished.connect(self.update_combo_box)

        # Start the worker
        self.thread_pool.start(self.worker)

    def update_combo_box(self, cm_versions):
        self.combo_box.addItems(cm_versions)
        self.chosen_cm_version = cm_versions[0]
        self.combo_box.currentIndexChanged.connect(lambda index: self.on_combo_box_changed(index, cm_versions))

    def on_combo_box_changed(self, index, cm_versions):
        self.chosen_cm_version = cm_versions[index]


    def on_ok_clicked(self):
        complete_car_maker_exe_path = os.path.join(os.environ['IPGHOME'], "carmaker", self.chosen_cm_version, "bin", "CM.exe")
        # Execute the CarMaker executable with the opetion -cmdport 16660
        os.system(f"{complete_car_maker_exe_path} -cmdport 16660")


        # Clear the current layout
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Create a label with the text "Are you Ready?"
        self.ready_label = QLabel("Start the simulation once. After that, press the Ready button.")
        self.layout.addWidget(self.ready_label)

        # Create a new button with the text "Ready"
        self.ready_button = QPushButton("Ready")
        self.layout.addWidget(self.ready_button)
        self.ready_button.clicked.connect(self.on_ready_clicked)

    def on_ready_clicked(self):
        self.worker = ReadCmQuantititesWorker()
        self.worker.finished.connect(self.on_read_cm_quantities_finished)
        self.thread_pool.start(self.worker)


if __name__ == "__main__":
    # Set the environment variable for demonstration purposes
    os.environ['IPGHOME'] = '/path/to/ipg_home'

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
