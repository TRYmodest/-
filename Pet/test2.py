import sys
import os

from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMenu

frame_folder = "D:/pythonGame/Photo/simeiAction/"  # 动画帧路径


class PetApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.frames = self.load_frames(frame_folder, "simei_flush_0")  # 加载帧序列
        self.current_frame_index = 0  # 当前帧索引
        self.flipped = True
        self.play_count = 0
        resized_pixmap = self.frames[self.current_frame_index].scaled(self.size(), aspectRatioMode=Qt.KeepAspectRatio)
        self.label.setPixmap(resized_pixmap)
        # 闲置定时器
        self.idle_timer = QTimer()
        self.current_action = "idle"
        self.frames = self.load_frames(frame_folder, "simei_idle")
        self.idle_timer.timeout.connect(self.walk_update_frame)
        # self.idle_timer.start(585)
        self.idle_timer.start(250)

    def initUI(self):
        self.petSize = 150
        self.setWindowTitle('桌面小宠物')
        self.resize(self.petSize, self.petSize)  # 设置窗口大小，适应图片大小

        # 设置无边框和透明背景
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # 加载图片标签
        self.label = QLabel(self)

        self.label.setScaledContents(True)

        # 定时器：切换动画帧
        self.animation_timer = QTimer()
        self.animation_timer.start(400)  # 每 100 毫秒切换一帧

        # 定时器：移动
        self.timer = QTimer()
        # self.timer.timeout.connect(self.animate)
        self.timer.start(50)




        # 初始位置和移动方向
        self.start_x = 200
        self.start_y = 200
        self.direction = -1
        self.move(self.start_x, self.start_y)
        self.current_action = "flush"

        self.mouse_drag_pos = QPoint()

    def idle(self):
        # 先断开现有的信号连接
        try:
            self.animation_timer.timeout.disconnect()
        except TypeError:
            pass  # 忽略未连接信号的错误
        self.timer.stop()
        self.animation_timer.stop()
        self.idle_timer.stop()
        self.current_action = "idle"
        self.frames = self.load_frames(frame_folder, "simei_idle")
        self.idle_timer.timeout.connect(self.update_frame)
        self.idle_timer.start(100)
        self.idle_timer.start(250)

    def set_action(self, action_name, frame_prefix, interval, connection = None, play_count_limit = None):
        self.stop_timer()
        self.current_action = action_name
        self.frames = self.load_frames(frame_folder, frame_prefix)
        self.current_frame_index = 0
        self.play_count = 0
        self.animation_timer.timeout.connect(self.update_frame)
        self.animation_timer.start(interval)


    def stop_timer(self):
        # 先断开现有的信号连接
        try:
            self.animation_timer.timeout.disconnect()
        except TypeError:
            pass  # 忽略未连接信号的错误
        try:
            self.timer.timeout.disconnect()
        except TypeError:
            pass  # 忽略未连接信号的错误
        self.timer.stop()
        self.animation_timer.stop()

    def bling(self):
        # 先断开现有的信号连接
        try:
            self.animation_timer.timeout.disconnect()
        except TypeError:
            pass  # 忽略未连接信号的错误
        self.timer.stop()
        self.animation_timer.stop()
        self.current_action = "bling"
        self.frames = self.load_frames(frame_folder, "simei_bling")
        self.animation_timer.timeout.connect(self.update_frame)
        self.animation_timer.start(200)

    def walk(self):
        # 先断开现有的信号连接
        try:
            self.timer.timeout.disconnect()
        except TypeError:
            pass  # 忽略未连接信号的错误

        self.timer.stop()
        self.animation_timer.stop()
        self.timer.timeout.connect(self.animate)
        self.timer.start(50)
        self.current_action = "walk"
        self.frames = self.load_frames(frame_folder, "simei_walk-")
        self.animation_timer.timeout.connect(self.walk_update_frame)
        self.animation_timer.start(200)

    def flow(self):
        # 先断开现有的信号连接
        try:
            self.animation_timer.timeout.disconnect()
        except TypeError:
            pass  # 忽略未连接信号的错误
        self.timer.stop()
        self.animation_timer.stop()
        self.current_action = "flow"
        self.frames = self.load_frames(frame_folder, "simei_flow")
        self.animation_timer.timeout.connect(self.update_frame)
        self.animation_timer.start(200)

    def load_frames(self, frame_folder, action):
        """
        加载所有动画帧，并返回帧的列表。
        :param frame_folder: 动画帧所在文件夹路径
        :return: 包含帧的 QPixmap 对象列表
        """
        frame_files = sorted(
            [os.path.join(frame_folder, f) for f in os.listdir(frame_folder) if f.startswith(action)]
        )

        frames = [QPixmap(frame) for frame in frame_files]
        return frames
    def walk_update_frame(self):
        """
        切换到下一帧并更新宠物图像。
        """
        if self.frames:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            current_frame = self.frames[self.current_frame_index]

            # 如果翻转状态为真，保持翻转状态
            if self.flipped:
                transform = QTransform().scale(-1, 1)
                current_frame = current_frame.transformed(transform, mode=Qt.SmoothTransformation)
            # 设置图像大小，统一调整为合适的大小
            resized_pixmap = current_frame.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(resized_pixmap)

    def update_frame(self):
        """
        切换到下一帧并更新宠物图像。
        """
        if self.frames:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            current_frame = self.frames[self.current_frame_index]
            # 检测是否完成一轮播放
            if self.current_frame_index == 0:
                self.play_count += 1
                if self.play_count >= 2:  # 播放达到最大次数时停止
                    self.play_count = 0
                    self.animation_timer.stop()
                    #结束后进入闲置的状态
                    self.idle()
                    return

            # 如果翻转状态为真，保持翻转状态
            if self.flipped:
                transform = QTransform().scale(-1, 1)
                current_frame = current_frame.transformed(transform, mode=Qt.SmoothTransformation)
            # 设置图像大小，统一调整为合适的大小
            resized_pixmap = current_frame.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(resized_pixmap)

    def animate(self):
        """
        让宠物水平移动并在边界时反转方向和图像。
        """
        current_pos = self.pos()
        next_x = current_pos.x() + self.direction * 5  # 每次移动 5 像素

        # 获取屏幕的宽度
        screen_geometry = QApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()

        # 检测是否碰到屏幕边界
        if next_x <= 0:
            self.direction = 1  # 改为向右
            if self.flipped:
                self.flip_image()  # 恢复图像方向
        elif next_x + self.width() >= screen_width:
            self.direction = -1  # 改为向左
            if not self.flipped:
                self.flip_image()  # 翻转图像

        # 更新宠物的位置
        self.move(next_x, current_pos.y())

    def flip_image(self):
        """
        水平翻转图像。
        """
        self.flipped = not self.flipped
        self.update_frame()  # 立即更新图像

    def mousePressEvent(self, event):
        """
        捕获鼠标按下事件，记录当前位置，开始拖动。
        """
        if event.button() == Qt.LeftButton:
            self.timer.stop()
            self.animation_timer.stop()
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self.setCursor(Qt.ClosedHandCursor)  # 改变鼠标形状
            event.accept()

    def mouseReleaseEvent(self, event):
        """
        释放鼠标时恢复定时器，继续动画和移动。
        """
        if event.button() == Qt.LeftButton:
            if self.current_action == "walk":
                self.timer.start()
            self.animation_timer.start()
            self.setCursor(Qt.ArrowCursor)  # 恢复默认鼠标形状
            event.accept()

    def mouseMoveEvent(self, event):
        """
        捕获鼠标移动事件，更新窗口的位置。
        """
        # 这里使用的是buttons（）会返回按钮的状态
        if event.buttons() & Qt.LeftButton:
            # 更新窗口位置
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        actions = {
            "退出": QApplication.quit,
            "冒星星啦": lambda: self.set_action("bling", "simei_bling", 200, connection=self.idle, play_count_limit=2),
            "散散步": lambda: self.walk(),
            "吹吹风": lambda: self.set_action("flow", "simei_flow", 200, connection=self.idle, play_count_limit=2),
            "打瞌睡": lambda: self.set_action("sleepy", "simei_sleepy", 300),
        }
        for label, method in actions.items():
            menu.addAction(label).triggered.connect(method)
        menu.exec_(self.mapToGlobal(event.pos()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = PetApp()
    pet.show()
    sys.exit(app.exec())
