# A program writed in Python code with a simple visual graphical interface, to help download images and videos from web pages.

# This program is free software: you can redistribute it and/or modify

# Programmed by Eric V. Gramunt.


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class DownloaderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.save_path = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Simple GUI Web Downloader by Eric V.')
        self.setGeometry(100, 100, 500, 200)

        layout = QVBoxLayout()

        self.url_label = QLabel('Enter an URL:')
        self.url_input = QLineEdit()

        self.select_folder_button = QPushButton('Select Folder')
        self.select_folder_button.clicked.connect(self.select_folder)

        self.download_button = QPushButton('Download')
        self.download_button.clicked.connect(self.download_images_videos)

        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.select_folder_button)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def select_folder(self):
        self.save_path = QFileDialog.getExistingDirectory(self, "Select Download Folder")

    def download_images_videos(self):
        url = self.url_input.text().strip()
        if not url:
            return

        if not self.save_path:
            QMessageBox.warning(self, "No Folder Selected", "Please select a folder before downloading.")
            return

        # Check if the URL is a direct link to an image or video
        parsed_url = urlparse(url)
        file_ext = parsed_url.path.split('.')[-1].lower()

        if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'mp4', 'webm', 'ogg']:
            self.download_file(url, self.save_path, url)
        else:
            self.download_from_webpage(url)

    def download_from_webpage(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        for img in soup.find_all('img'):
            img_url = urljoin(url, img.get('src'))
            self.download_file(img_url, self.save_path, url)

        for video in soup.find_all('video'):
            video_url = urljoin(url, video.get('src'))
            self.download_file(video_url, self.save_path, url)

    def download_file(self, file_url, save_path, referer_url):
        if not file_url:
            return

        file_name = file_url.split('/')[-1]

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Referer': referer_url
        }

        response = requests.get(file_url, headers=headers)
        with open(save_path + '/' + file_name, 'wb') as f:
            f.write(response.content)


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    downloader_app = DownloaderApp()
    downloader_app.show()

    sys.exit(app.exec_())



