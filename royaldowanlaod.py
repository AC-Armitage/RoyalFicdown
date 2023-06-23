import requests
from bs4 import BeautifulSoup
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont
from PyQt6.QtCore import *
from PyQt6 import uic
import subprocess
import os
import threading



class Royaldownloader(QMainWindow):
	
	def __init__(self):
		self.link = ''
		self.chapters = ''
		super(Royaldownloader, self).__init__()
		uic.loadUi("Rui.ui", self)
		self.show()
		self.Dirselect.clicked.connect(self.getDir)
		self.startButt.clicked.connect(self.lookUp)
		self.progressBar.hide()
	
	def getDir(self):
	
		if os.name == 'nt':
			directory_path = "C:\\Users\\"
			subprocess.Popen(f'start "" /D "{directory_path}" explorer.exe')
			self.Dirtext.setText(selected_directory)
			self.startButt.setEnabled(True)
		else:
			directory_path = "/home/"
			result = subprocess.run(['zenity', '--file-selection', '--directory', '--title=Select Directory'], capture_output=True, text=True)
			selected_directory = result.stdout.strip()
			self.Dirtext.setText(selected_directory)
			self.startButt.setEnabled(True)
	
	def showinfo(self, title, author, numChapter, desc):
		downButt = QPushButton("Download", self)
		downButt.move(650, 460)
		downButt.setFixedWidth(80)
		downButt.setFixedHeight(22)
		titleLabel = QLabel(title, self)
		titleLabel.move(200, 150)
		titleLabel.setFixedWidth(541)
		titleLabel.setFixedHeight(75)
		titleLabel.setWordWrap(True)
		authorLabel = QLabel(author, self)
		authorLabel.move(200, 240)
		authorLabel.setFixedWidth(171)
		authorLabel.setFixedHeight(61)
		authorLabel.setWordWrap(True)
		chapterLabel = QLabel(numChapter, self)
		chapterLabel.move(200, 320)
		chapterLabel.setFixedWidth(151)
		chapterLabel.setFixedHeight(20)
		shortdesc = f"{desc[:170]}..."
		descLabel = QLabel(shortdesc, self)
		descLabel.move(190, 370)
		descLabel.setFixedWidth(541)
		descLabel.setFixedHeight(101)
		descLabel.setWordWrap(True)
		downButt.show()
		titleLabel.show()
		authorLabel.show() 
		chapterLabel.show()
		descLabel.show()
		totalProgress = len(self.chapters)
		currentProgress = 0
		self.progressBar.move(10, 460)
		self.progressBar.setFixedWidth(591)
		self.progressBar.setFixedHeight(23)
		self.progressBar.setValue(0)
		self.progressBar.setMinimum(0)
		self.progressBar.setMaximum(totalProgress)
		downTread = threading.Thread(target=self.Download)
		def startDown(self):
			descLabel.close()
			downButt.setEnabled(False)
			downTread.start()
			downTread.join()
			titleLabel.close()
			authorLabel.close()
			chapterLabel.close()
			downButt.setEnabled(True)
		downButt.clicked.connect(startDown)
		


	def lookUp(self):
		self.link = self.linkBox.text()
		novel = requests.get(self.link)
		novelpage = novel.text
		page = BeautifulSoup(novelpage, "lxml")
		self.chapters = page.find_all(class_="chapter-row")
		numChapter = f"{len(self.chapters)} chapters"
		info = page.find_all(class_="font-white")
		title = info[0].getText()
		author = info[1].getText()
		desc = page.find(class_="description").getText()
		self.showinfo(title, author, numChapter, desc)
	def Download(self):
		self.progressBar.show()
		for chapter in self.chapters:
			chapTitle = chapter.a.string
			a_link = chapter.find("a")
			chapLink = a_link["href"]
			chapPage = requests.get(f"https://www.royalroad.com{chapLink}")
			chapHTML = BeautifulSoup(chapPage.text, "lxml")
			chapText = chapHTML.find(class_="chapter-inner chapter-content")
			goalChap = chapText.text
			seleDir = self.Dirtext.toPlainText()
			goalFile = f"{seleDir}/{chapTitle.strip()}"
			with open(f"{goalFile}.txt", "w") as f:
				f.write(goalChap)
				print(f"downloaded {chapTitle.strip()}")
				value = self.progressBar.value() + 1
				self.progressBar.setValue(value)

if __name__ == "__main__":
	app = QApplication([])
	window = Royaldownloader()
	app.exec()


