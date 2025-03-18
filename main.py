from gui import ImageDownloaderApp
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

# Windows-specific fix for taskbar icon
if sys.platform == "win32":
    import ctypes
    myappid = "rot.front.google-and-yandex-image-downloader"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def main():
    app = QApplication(sys.argv)

    icon_path = os.path.join(os.getcwd(), "assets", "icon.png")

    app.setWindowIcon(QIcon(icon_path))

    window = ImageDownloaderApp()
    window.setWindowIcon(QIcon(icon_path))
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

