import sys
from PyQt5 import QtWidgets
from utils import ModelWrapper
from ui import ClassifierUI


class AlzheimerApp(QtWidgets.QMainWindow):
    def __init__(self, model_path, classes):
        super().__init__()
        self.wrapper = ModelWrapper(model_path)
        self.ui = ClassifierUI(classes)
        self.setCentralWidget(self.ui)
        self.ui.parent = lambda: self

    def predict_image(self, image_path):
        idx, conf = self.wrapper.predict(image_path)
        cls_name = self.ui.classes[idx]
        self.ui.result_label.setText(
            f"Prediction: <b>{cls_name}</b>\nConfidence: {conf*100:.1f}%"
        )

if __name__ == '__main__':
    # Define class order same as during training
    classes = ['MildDemented', 'ModerateDemented', 'NonDemented', 'VeryMildDemented']
    
    model_path = './models/model.pth'

    app = QtWidgets.QApplication(sys.argv)
    # Load and apply QSS stylesheet
    try:
        with open("styles.qss", "r") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f"Failed to load stylesheet: {e}")
    window = AlzheimerApp(model_path, classes)
    window.show()
    sys.exit(app.exec_())
