# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import platform
import psutil
import time
from PySide6.QtCharts import QChart, QLineSeries

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class NewThread(QThread):
    # 自定义信号声明
    # 使用自定义信号和 UI 主线程通讯，参数是发送信号时附带参数的数据类型，可以是 str，int，list 等
    finishSignal = Signal(str)

    # 带一个参数 t
    def __init__(self, parent=None):
        super(NewThread, self).__init__(parent)

    # run 函数是子线程中的操作，线程启动后开始执行
    if os.path.exists(f"./computer_info.csv"):
        pass
    else:
        with open(r"./computer_info.csv", "w") as f:
            pass
    
    def run(self):
        timer = 0
        while True:
            timer += 1
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_info = cpu_percent
            virtual_memory = psutil.virtual_memory()
            memory_percent = virtual_memory.percent
            with open(r"./computer_info.csv", "a") as f:
                f.write(f"{timer},{cpu_info},{memory_percent}\n")
            time.sleep(1)
            # 发射自定义信号
            # 通过 emit 函数将参数 i 传递给主线程，触发自定义信号
            self.finishSignal.emit("1")

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "自由"
        description = "我一定成为自由的人"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)
        # 新增功能：切换皮肤
        widgets.btn_message.clicked.connect(self.buttonClick)
        # 新增功能：电脑信息数据分析
        widgets.btn_computer.clicked.connect(self.buttonClick)
        widgets.computer_info_start.clicked.connect(self.start_computer_info)
        widgets.computer_info_clear.clicked.connect(self.clear_computer_info)
        # 新增功能：打开本地文件
        widgets.btn_local.clicked.connect(self.open_file)
        # 新增功能：打开网站
        widgets.btn_web.clicked.connect(self.open_web)
        # 新增功能：切换图片
        widgets.btn_pic.clicked.connect(self.change_pic)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        # 开始修改
        # 路径冻结，防止打包成 exe 后路径错乱
        if getattr(sys, 'frozen', False):
            absPath = os.path.dirname(os.path.abspath(sys.executable))
        elif __file__:
            absPath = os.path.dirname(os.path.abspath(__file__))
        useCustomTheme = True
        self.useCustomTheme = useCustomTheme
        self.absPath = absPath
        themeFile = os.path.abspath(os.path.join(absPath, "themes\py_dracula_light.qss"))
        # 结束修改

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))


    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        if btnName == "btn_save":
            # print("Save BTN clicked!")
            QMessageBox.information(self, "提示", "该功能暂未实现", QMessageBox.Yes)
        
        # 切换主题
        if btnName == "btn_message":
            if self.useCustomTheme:
                themeFile = os.path.abspath(os.path.join(self.absPath, "themes\py_dracula_dark.qss"))
                # 跟着原先的代码走
                UIFunctions.theme(self, themeFile, True)
                AppFunctions.setThemeHack(self)
                self.useCustomTheme = False
            else:
                themeFile = os.path.abspath(os.path.join(self.absPath, "themes\py_dracula_light.qss"))
                # 跟着原先的代码走
                UIFunctions.theme(self, themeFile, True)
                AppFunctions.setThemeHack(self)
                self.useCustomTheme = True
        
        # 电脑信息数据分析
        if btnName == "btn_computer":
            widgets.stackedWidget.setCurrentWidget(widgets.computer_info) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

            self.seriesS = QLineSeries()
            self.seriesL = QLineSeries()
            self.seriesS.setName("cpu")
            self.seriesL.setName("memory")

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')


    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        p = event.globalPosition()
        globalPos = p.toPoint()
        self.dragPos = globalPos

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

    def start_computer_info(self):
        """
        开始获取电脑数据
        """
        # 开始分析记录电脑数据，需要持续获取，然后分析
        self.thread1 = NewThread() # 实例化一个线程
        # 将线程 thread 的信号 finishSignal 和 UI 主线程中的槽函数 data_display 进行连接
        self.thread1.finishSignal.connect(self.data_display)
        # 启动线程，执行线程类中的 run 函数
        self.thread1.start()
    
    def data_display(self, str_):
        """
        电脑信息的数据展示
        """
        # 获取已经记录好的数据并展示
        # 设置一个 flag
        with open(r"./computer_info.csv", "r") as f:
            reader = f.readlines()
            reader_last = reader[-1].replace("\n", "").split(",")
            # 横坐标
            col = int(reader_last[0])
            # cpu
            cpu = float(reader_last[1])
            # 内存
            memory = float(reader_last[2])
        
        self.seriesS.append(col, cpu)
        self.seriesL.append(col, memory)
        self.chart = QChart()
        self.chart.setTitle("设备资源图")
        self.chart.addSeries(self.seriesS)
        self.chart.addSeries(self.seriesL)
        self.chart.createDefaultAxes()
        widgets.graphicsView.setChart(self.chart)
    
    def clear_computer_info(self):
        """
        清除设备表格信息
        """
        self.seriesS.clear()
        self.seriesL.clear()
        self.chart.addSeries(self.seriesS)
        self.chart.addSeries(self.seriesL)
    
    def open_file(self):
        import webbrowser
        webbrowser.open("说明书" + ".docx")
    
    def open_web(self):
        import webbrowser
        webbrowser.open("www.baidu.com")
    
    def change_pic(self):
        url_list = [
            "./1.jpg",
            "./2.jpg",
            "./3.jpg",
            "./4.jpg",
            "./5.png"
        ]
        import random
        index = random.randint(0, 4) # 很神奇，能显示 5 张图片
        lb1 = widgets.label # 同页面下的控件
        pix = QPixmap(url_list[index]).scaled(lb1.size(), aspectMode=Qt.KeepAspectRatio)
        lb1.setPixmap(pix)
        lb1.repaint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec())
