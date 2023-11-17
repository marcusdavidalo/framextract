import cv2
import os
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, QLineEdit
import qdarkstyle
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtCore import Qt, QUrl
from PyQt5.Qt import QDragEnterEvent, QDropEvent

# Global variables to store video path and output folder
video_path = ""
output_folder = "./outputs"

class VideoPathEntry(QLineEdit):
    def __init__(self, label, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.label = label

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        global video_path
        url = event.mimeData().urls()[0]
        video_path = url.toLocalFile()
        self.setText(video_path)

        # Extract the first frame of the video
        video = cv2.VideoCapture(video_path)
        success, frame = video.read()
        video.release()

        if success:
            # Convert the frame to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the frame to a QImage
            height, width, channel = frame.shape
            bytesPerLine = 3 * width
            qimage = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)

            # Convert the QImage to a QPixmap
            pixmap = QPixmap.fromImage(qimage)

            # Resize the QPixmap
            thumbnail_size = 100  # The desired height of the thumbnail
            pixmap = pixmap.scaledToHeight(thumbnail_size, Qt.SmoothTransformation)

            # Display the QPixmap in the label
            self.label.setPixmap(pixmap)


def extract_frames(video_path, output_folder, button, label):
    video = cv2.VideoCapture(video_path)
    frame_count = 1

    # Create a new folder for each video
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_folder = os.path.join(output_folder, video_name)
    os.makedirs(output_folder, exist_ok=True)

    while True:
        success, frame = video.read()
        if not success:
            break

        output_path = f"{output_folder}/frame_{frame_count}.jpg"
        cv2.imwrite(output_path, frame)
        frame_count += 1

    video.release()
    print(f"Frames extracted: {frame_count}")
    label.setText(f"Frames extracted: {frame_count}")
    button.setEnabled(True)

def select_video(entry):
    global video_path
    video_path = QFileDialog.getOpenFileName()[0]
    entry.setText(video_path)

def select_output_folder(entry):
    global output_folder
    output_folder = QFileDialog.getExistingDirectory()
    entry.setText(output_folder)

def main():
    app = QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    # Global Font
    font = QFont("Bradley Hand ITC", 14)
    app.setFont(font)

    window = QWidget()
    window.resize(512, 512)
    layout = QVBoxLayout()

    thumbnail_label = QLabel()
    layout.addWidget(thumbnail_label)

    video_entry = VideoPathEntry(thumbnail_label)
    video_entry.setPlaceholderText("Select video path")
    layout.addWidget(QLabel("Video Path:"))
    layout.addWidget(video_entry)

    video_button = QPushButton("Select Video")
    video_button.clicked.connect(lambda: select_video(video_entry))
    layout.addWidget(video_button)

    folder_entry = QLineEdit()
    folder_entry.setPlaceholderText("Select output folder, default is in ./Outputs")
    layout.addWidget(QLabel("Output Folder:"))
    layout.addWidget(folder_entry)

    folder_button = QPushButton("Select Output Folder")
    folder_button.clicked.connect(lambda: select_output_folder(folder_entry))
    layout.addWidget(folder_button)

    extract_label = QLabel("")
    layout.addWidget(extract_label)

    extract_button = QPushButton("Extract Frames")
    extract_button.clicked.connect(lambda: threading.Thread(target=extract_frames, args=(video_path, output_folder, extract_button, extract_label)).start())
    layout.addWidget(extract_button)

    window.setLayout(layout)
    window.show()

    app.exec_()

if __name__ == "__main__":
    main()
