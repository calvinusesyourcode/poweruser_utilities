from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, Qt
import sys
import time

class TimerApp:
    def __init__(self):
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)
        print("runnning")

        # Create the icon
        self.icon = QIcon("C:\\Users\\calvi\\3D Objects\\test\\anon52x52.jpg")  # Replace with the path to your icon

        # Create the tray
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)

        # Create the menu
        self.menu = QMenu()
        self.exit_action = QAction("Exit")
        self.exit_action.triggered.connect(self.app.quit)
        self.menu.addAction(self.exit_action)

        # Add the menu to the tray
        self.tray.setContextMenu(self.menu)

        # Initialize timer
        self.start_time = time.time()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Update every second

    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        mins, secs = divmod(int(elapsed_time), 60)
        hours, mins = divmod(mins, 60)
        if hours >= 1:
            timer_str = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)
        else:
            timer_str = '{:02d}:{:02d}'.format(mins, secs)
        self.tray.setToolTip(f"Time Elapsed: {timer_str}")

    def run(self):
        self.app.exec_()

if __name__ == "__main__":
    app = TimerApp()
    app.run()

