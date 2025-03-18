import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog,
    QComboBox, QLineEdit, QMessageBox, QHBoxLayout, QFrame
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QIcon
from google_image_downloader import search_google_images, download_images
from yandex_image_downloader import search_yandex_images
from webdriver_setup import init_webdriver

class DownloadWorker(QThread):
    finished = pyqtSignal(str)  # Signal to update the UI after downloading

    def __init__(self, search_engine, search_query, folder_path):
        super().__init__()
        self.search_engine = search_engine
        self.search_query = search_query
        self.folder_path = folder_path

    def run(self):
        driver = init_webdriver()

        if self.search_engine == "google":
            image_links = search_google_images(driver, self.search_query)
        else:
            image_links = search_yandex_images(driver, self.search_query)

        success_count = 0

        if image_links:
            success_count = download_images(image_links, folder=self.folder_path)

        driver.quit()
        self.finished.emit(str(success_count))

class ImageDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Скачивание картинок")
        self.setGeometry(100, 100, 500, 300)

        self.setWindowIcon(QIcon("assets/icon.png"))

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f5;
                font-family: Tahoma, sans-serif;
                font-size: 12px;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #b0c4de;
            }
            QComboBox, QLineEdit {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Main Container Frame
        container = QFrame()
        container_layout = QVBoxLayout(container)

        # Folder Selection
        self.folder_label = QLabel("📂 Выберите папку для скачивания: ")
        container_layout.addWidget(self.folder_label)

        folder_layout = QHBoxLayout()
        self.folder_button = QPushButton("Выбрать папку")
        self.folder_button.clicked.connect(self.select_folder)
        self.folder_path = os.getcwd()
        self.folder_display = QLabel(f"{self.folder_path}")
        folder_layout.addWidget(self.folder_display)
        folder_layout.addWidget(self.folder_button)
        container_layout.addLayout(folder_layout)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        container_layout.addWidget(line)

        # Search Engine Selection
        self.engine_label = QLabel("🌍 Выберите поисковик:")
        container_layout.addWidget(self.engine_label)

        self.engine_dropdown = QComboBox()
        self.engine_dropdown.addItems(["Google", "Yandex"])
        container_layout.addWidget(self.engine_dropdown)

        # Search Query
        self.search_label = QLabel("🔎 Введите поисковой запрос:")
        container_layout.addWidget(self.search_label)

        self.search_input = QLineEdit()
        container_layout.addWidget(self.search_input)

        # Centered Button Layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Pushes button to center
        self.search_button = QPushButton("Скачать картинки")
        self.search_button.clicked.connect(self.start_search)
        button_layout.addWidget(self.search_button)
        button_layout.addStretch()  # Pushes button to center

        container_layout.addLayout(button_layout)  # Add centered button

        # Status Label
        self.status_label = QLabel("")
        container_layout.addWidget(self.status_label)

        layout.addWidget(container)
        self.setLayout(layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder:
            self.folder_path = folder
            self.folder_display.setText(folder)

    def start_search(self):
        search_query = self.search_input.text().strip()
        search_engine = self.engine_dropdown.currentText().lower()

        if not search_query:
            QMessageBox.warning(self, "Ошибка", "Введите поисковой запрос.")
            return
        
        # Disable all UI elements during download
        self.set_ui_enabled(False)

        # Show loading status
        self.status_label.setText("Скачивание в процессе...")

        # Start worker thread for downloading images
        self.worker = DownloadWorker(search_engine, search_query, self.folder_path)
        self.worker.finished.connect(self.download_complete)
        self.worker.start()

    def set_ui_enabled(self, enabled):
        self.folder_button.setEnabled(enabled)
        self.engine_dropdown.setEnabled(enabled)
        self.search_input.setEnabled(enabled)
        self.search_button.setEnabled(enabled)

    def download_complete(self, num_downloaded):
        self.status_label.setText(f"Скачано {num_downloaded} изображений.")
        QMessageBox.information(self, "Скачивание закончено", f"Скачано {num_downloaded} изображений.")

        # Re-enable UI elements
        self.set_ui_enabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageDownloaderApp()
    window.show()
    sys.exit(app.exec())
