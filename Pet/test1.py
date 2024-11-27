import sys

# 创建应用程序
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

app = QApplication(sys.argv)

# 创建窗口
window: QWidget = QWidget()
window.setWindowTitle('桌面小宠物')  # 窗口标题
window.resize(100, 100)  # 窗口大小

# 设置窗口为无边框和透明背景
window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
window.setAttribute(Qt.WA_TranslucentBackground, True)

# 加载图片
label = QLabel(window)
pixmap = QPixmap("D:\pythonGame\Photo\Pet1-removebg-preview.png")
resized_pixmap = pixmap.scaled(100, 100, aspectRatioMode=Qt.KeepAspectRatio)
label.setPixmap(resized_pixmap)
label.setScaledContents(True)

# 显示窗口
window.show()

# 程序运行
sys.exit(app.exec_())
