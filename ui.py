
from PyQt5 import QtWidgets, QtGui, QtCore

class ClassifierUI(QtWidgets.QWidget):
    def __init__(self, classes):
        super().__init__()
        self.classes = classes
        self.setAcceptDrops(True)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Alzheimer's MRI Classifier")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setMinimumSize(800, 600)


        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignTop)

        # Header
        header = QtWidgets.QLabel("Alzheimer's MRI Classifier")
        header.setObjectName("header")
        header.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(header)
        subtitle = QtWidgets.QLabel("Upload or drag an MRI scan to predict Alzheimer's stage")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(subtitle)

        # Section Divider
        line1 = QtWidgets.QFrame()
        line1.setFrameShape(QtWidgets.QFrame.HLine)
        line1.setFrameShadow(QtWidgets.QFrame.Sunken)
        main_layout.addWidget(line1)

        # Image display
        self.image_label = QtWidgets.QLabel("Drop an MRI image here or click 'Load Image'")
        self.image_label.setObjectName("image_label")
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label.setFixedSize(400, 400)
        main_layout.addWidget(self.image_label, alignment=QtCore.Qt.AlignCenter)

        # Buttons
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.load_btn = QtWidgets.QPushButton("Load Image")
        self.predict_btn = QtWidgets.QPushButton("Predict")
        self.predict_btn.setEnabled(False)
        btn_layout.addWidget(self.load_btn)
        btn_layout.addWidget(self.predict_btn)
        main_layout.addLayout(btn_layout)

        # Section Divider
        line2 = QtWidgets.QFrame()
        line2.setFrameShape(QtWidgets.QFrame.HLine)
        line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        main_layout.addWidget(line2)

        # Result label
        self.result_label = QtWidgets.QLabel("")
        self.result_label.setObjectName("result_label")
        self.result_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.result_label)

        # Signals
        self.load_btn.clicked.connect(self.load_image)
        self.predict_btn.clicked.connect(self.on_predict)

    def load_image(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp)")
        if path:
            pixmap = QtGui.QPixmap(path).scaled(400, 400, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
            self.image_path = path
            self.result_label.setText("")
            self.predict_btn.setEnabled(True)
        else:
            self.predict_btn.setEnabled(False)

    def on_predict(self):
        if hasattr(self, 'image_path'):
            self.parent().predict_image(self.image_path)
        else:
            QtWidgets.QMessageBox.warning(self, "No Image", "Please load an image first.")

    # Drag and drop support
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.image_label.setStyleSheet(self.image_label.styleSheet() + "border-color: #2d5be3; background: #f0f6ff;")
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.image_label.setStyleSheet(self.image_label.styleSheet().replace("border-color: #2d5be3; background: #f0f6ff;", ""))

    def dropEvent(self, event):
        self.image_label.setStyleSheet(self.image_label.styleSheet().replace("border-color: #2d5be3; background: #f0f6ff;", ""))
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            if file_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                pixmap = QtGui.QPixmap(file_path).scaled(400, 400, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.image_label.setPixmap(pixmap)
                self.image_path = file_path
                self.result_label.setText("")
                self.predict_btn.setEnabled(True)
            else:
                QtWidgets.QMessageBox.warning(self, "Invalid file", "Please drop a valid image file.")
                self.predict_btn.setEnabled(False)


