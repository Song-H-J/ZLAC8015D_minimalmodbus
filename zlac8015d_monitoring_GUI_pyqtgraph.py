import pyqtgraph
from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel
from PyQt5.QtCore import pyqtSlot, QTimer, Qt
from zlac8015d import ZLAC8015D
from collections import deque
import atexit


class Main(QWidget):
    def __init__(self):
        super().__init__()
        # 레이아웃 생성
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        vbox1 = QVBoxLayout()
        Gbox0 = QVBoxLayout()
        Gbox1 = QVBoxLayout()
        Gbox2 = QVBoxLayout()
        Gbox3 = QVBoxLayout()
        Gbox4 = QVBoxLayout()
        Gbox5 = QVBoxLayout()
        Gbox6 = QVBoxLayout()
        Gbox7 = QVBoxLayout()
        Gbox8 = QVBoxLayout()
        Gbox9 = QVBoxLayout()

        # 기본 글꼴 설정
        font_tick = QtGui.QFont('Bahnschrift SemiLight', 8)
        font = QtGui.QFont('Bahnschrift SemiLight', 12)
        font.setBold(True)
        self.setFont(font)

        # 그래프 객체 4개 생성 및 X축을 STRING축으로 설정
        self.stringaxisLW = pyqtgraph.AxisItem(orientation='bottom')
        self.stringaxisRW = pyqtgraph.AxisItem(orientation='bottom')
        self.stringaxisRPM = pyqtgraph.AxisItem(orientation='bottom')
        self.stringaxisTQ = pyqtgraph.AxisItem(orientation='bottom')
        self.LeftWatt = pyqtgraph.PlotWidget(axisItems={'bottom': self.stringaxisLW})
        self.RightWatt = pyqtgraph.PlotWidget(axisItems={'bottom': self.stringaxisRW})
        self.RPM = pyqtgraph.PlotWidget(axisItems={'bottom': self.stringaxisRPM})
        self.Torque = pyqtgraph.PlotWidget(axisItems={'bottom': self.stringaxisTQ})

        # 그래프 제목 생성
        self.LeftWatt.setTitle("Left Motor Watt", color="#828282", size="12pt")
        self.RightWatt.setTitle("Right Motor Watt", color="#828282", size="12pt")
        self.RPM.setTitle("Motor RPM", color="#828282", size="12pt")
        self.Torque.setTitle("Motor Torque", color="#828282", size="12pt")

        # 그래프 제목 글꼴 설정
        self.LeftWatt.getPlotItem().titleLabel.item.setFont(font)
        self.RightWatt.getPlotItem().titleLabel.item.setFont(font)
        self.RPM.getPlotItem().titleLabel.item.setFont(font)
        self.Torque.getPlotItem().titleLabel.item.setFont(font)

        # X, Y축 이름 스타일 설정
        labelStyle = {'color': '#828282', 'font-size': '9pt' }

        # X, Y축 이름 생성
        self.LeftWatt.setLabel('left', 'Watt', units='J/s', **labelStyle)
        self.RightWatt.setLabel('left', 'Watt', units='J/s', **labelStyle)
        self.RPM.setLabel('left', 'Velocity', units='RPM', **labelStyle)
        self.Torque.setLabel('left', 'Torque', units='mA', **labelStyle)
        self.LeftWatt.setLabel('bottom', 'Time', **labelStyle)
        self.RightWatt.setLabel('bottom', 'Time', **labelStyle)
        self.RPM.setLabel('bottom', 'Time', **labelStyle)
        self.Torque.setLabel('bottom', 'Time', **labelStyle)

        # x,y 눈금 글꼴 설정
        self.LeftWatt.getAxis('bottom').setStyle(tickFont = font_tick, tickTextOffset=6)
        self.RightWatt.getAxis('bottom').setStyle(tickFont = font_tick, tickTextOffset=6)
        self.RPM.getAxis('bottom').setStyle(tickFont = font_tick, tickTextOffset=6)
        self.Torque.getAxis('bottom').setStyle(tickFont = font_tick, tickTextOffset=6)
        self.LeftWatt.getAxis('left').setStyle(tickFont = font_tick, tickTextOffset=6)
        self.RightWatt.getAxis('left').setStyle(tickFont = font_tick, tickTextOffset=6)
        self.RPM.getAxis('left').setStyle(tickFont = font_tick, tickTextOffset=6)
        self.Torque.getAxis('left').setStyle(tickFont = font_tick, tickTextOffset=6)

        # 그래프 그리드 설정
        self.LeftWatt.showGrid(x=True, y=True)
        self.RightWatt.showGrid(x=True, y=True)
        self.RPM.showGrid(x=True, y=True)
        self.Torque.showGrid(x=True, y=True)

        # 그래프 배경색 지정
        self.LeftWatt.setBackground((240,240,240))
        self.RightWatt.setBackground((240,240,240))
        self.RPM.setBackground((240,240,240))
        self.Torque.setBackground((240,240,240))

        # Data Indicator 그룹 박스 생성
        self.groupbox_DM = QGroupBox('Driver Mode')
        self.groupbox_DT = QGroupBox('Driver Temperature')
        self.groupbox_VT = QGroupBox('Voltage')
        self.groupbox_LT = QGroupBox('Left Torque')
        self.groupbox_LV = QGroupBox('Left RPM')
        self.groupbox_RT = QGroupBox('Right Torque')
        self.groupbox_RV = QGroupBox('Right RPM')
        self.groupbox_LE = QGroupBox('Left Error')
        self.groupbox_RE = QGroupBox('Right Error')
        self.groupbox_Status = QGroupBox('Motor Status')

        # Data Indicator 라벨 생성
        self.label_DM = QLabel('None', self)
        self.label_DT = QLabel('0', self)
        self.label_VT = QLabel('0', self)
        self.label_LT = QLabel('0', self)
        self.label_LV = QLabel('0', self)
        self.label_RT = QLabel('0', self)
        self.label_RV = QLabel('0', self)
        self.label_LE = QLabel('None', self)
        self.label_RE = QLabel('None', self)
        self.label_Status = QLabel('Ready', self)

        # Data Indicator 가운데 정렬
        self.label_DM.setAlignment(Qt.AlignCenter)
        self.label_DT.setAlignment(Qt.AlignCenter)
        self.label_VT.setAlignment(Qt.AlignCenter)
        self.label_LT.setAlignment(Qt.AlignCenter)
        self.label_LV.setAlignment(Qt.AlignCenter)
        self.label_RT.setAlignment(Qt.AlignCenter)
        self.label_RV.setAlignment(Qt.AlignCenter)
        self.label_LE.setAlignment(Qt.AlignCenter)
        self.label_RE.setAlignment(Qt.AlignCenter)
        self.label_Status.setAlignment(Qt.AlignCenter)

        # Data Indicator 배경색 및 테두리 설정
        self.label_DM.setStyleSheet("color:rgb(203, 26, 126);" "background-color:rgb(250,250,250);"
                                    "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                    "border-radius: 5px")
        self.label_DT.setStyleSheet("color:rgb(203, 26, 126);" "background-color:rgb(250,250,250);"
                                    "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                    "border-radius: 5px")
        self.label_VT.setStyleSheet("color:rgb(203, 26, 126);" "background-color:rgb(250,250,250);"
                                    "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                    "border-radius: 5px")
        self.label_LT.setStyleSheet("color:rgb(44, 106, 180);" "background-color:rgb(250,250,250);"
                                    "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                    "border-radius: 5px")
        self.label_LV.setStyleSheet("color:rgb(44, 106, 180);" "background-color:rgb(250,250,250);"
                                    "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                    "border-radius: 5px")
        self.label_RT.setStyleSheet("color:rgb(44, 106, 180);" "background-color:rgb(250,250,250);"
                                    "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                    "border-radius: 5px")
        self.label_RV.setStyleSheet("color:rgb(244, 121, 40);" "background-color:rgb(250,250,250);"
                                   "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                   "border-radius: 5px")
        self.label_LE.setStyleSheet("color:rgb(145, 122, 184);" "background-color:rgb(240,240,240);"
                                     "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                     "border-radius: 5px")
        self.label_RE.setStyleSheet("color:rgb(120, 120, 120);" "background-color:rgb(240,240,240);"
                                     "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                     "border-radius: 5px")
        self.label_Status.setStyleSheet("color:rgb(44, 106, 180)")

        # Data Indicator 글꼴 설정
        labelfont1 = self.label_DM.font()
        labelfont1.setFamily('Bahnschrift SemiLight')
        labelfont1.setPointSize(15)
        labelfont1.setBold(True)
        self.label_DM.setFont(labelfont1)
        self.label_DT.setFont(labelfont1)
        self.label_VT.setFont(labelfont1)
        self.label_LT.setFont(labelfont1)
        self.label_LV.setFont(labelfont1)
        self.label_RT.setFont(labelfont1)
        self.label_RV.setFont(labelfont1)
        self.label_LE.setFont(labelfont1)
        self.label_RE.setFont(labelfont1)
        self.label_Status.setFont(labelfont1)

        # 그룹박스와 Data Indicator 라벨 그룹화
        Gbox0.addWidget(self.label_DM)
        Gbox1.addWidget(self.label_DT)
        Gbox2.addWidget(self.label_VT)
        Gbox3.addWidget(self.label_LT)
        Gbox4.addWidget(self.label_LV)
        Gbox5.addWidget(self.label_RT)
        Gbox6.addWidget(self.label_RV)
        Gbox7.addWidget(self.label_LE)
        Gbox8.addWidget(self.label_RE)
        Gbox9.addWidget(self.label_Status)
        self.groupbox_DM.setLayout(Gbox0)
        self.groupbox_DT.setLayout(Gbox1)
        self.groupbox_VT.setLayout(Gbox2)
        self.groupbox_LT.setLayout(Gbox3)
        self.groupbox_LV.setLayout(Gbox4)
        self.groupbox_RT.setLayout(Gbox5)
        self.groupbox_RV.setLayout(Gbox6)
        self.groupbox_LE.setLayout(Gbox7)
        self.groupbox_RE.setLayout(Gbox8)
        self.groupbox_Status.setLayout(Gbox9)

        # 수평방향으로 창 그룹화 (1행 그래프 2개), (2행 그래프 2개), (3행 라벨 10개)
        hbox1.addWidget(self.LeftWatt)
        hbox1.addWidget(self.RightWatt)
        hbox2.addWidget(self.RPM)
        hbox2.addWidget(self.Torque)
        hbox3.addWidget(self.groupbox_DM)
        hbox3.addWidget(self.groupbox_DT)
        hbox3.addWidget(self.groupbox_VT)
        hbox3.addWidget(self.groupbox_LT)
        hbox3.addWidget(self.groupbox_LV)
        hbox3.addWidget(self.groupbox_RT)
        hbox3.addWidget(self.groupbox_RV)
        hbox3.addWidget(self.groupbox_LE)
        hbox3.addWidget(self.groupbox_RE)
        hbox3.addWidget(self.groupbox_Status)
        
        # 그룹화된 창 수직방향으로 그룹화
        vbox1.addLayout(hbox1)
        vbox1.addLayout(hbox2)
        vbox1.addLayout(hbox3)

        # 윈도우창생성 및 레이아웃 배치
        self.setLayout(vbox1)
        self.setGeometry(100, 100, 2600, 1000)  # 창 위치(x, y), width, height
        self.setWindowTitle("ZLAC8015D MONITORING SYSTEM")

        # X축 범위 생성
        self.LeftWatt.enableAutoRange(axis='x')
        self.RightWatt.enableAutoRange(axis='x')
        self.RPM.enableAutoRange(axis='x')
        self.Torque.enableAutoRange(axis='x')

        # Y축 범위 생성
        self.LeftWatt.setYRange(0, 300)
        self.RightWatt.setYRange(0, 300)
        self.RPM.setYRange(-270, 270)
        self.Torque.setYRange(-15, 15)

        #self.LeftWatt.enableAutoRange(axis='y')
        #self.RightWatt.enableAutoRange(axis='y')
        #self.RPM.enableAutoRange(axis='y')
        #self.Torque.enableAutoRange(axis='y')

        # 그래프 펜 설정
        self.L_Watt = self.LeftWatt.plot(pen=pyqtgraph.mkPen(color=(145, 122, 184), width=3, style=QtCore.Qt.SolidLine ))
        self.R_Watt = self.RightWatt.plot(pen=pyqtgraph.mkPen(color=(203, 26, 126), width=3, style=QtCore.Qt.SolidLine ))
        self.L_RPM = self.RPM.plot(pen=pyqtgraph.mkPen(color=(145, 122, 184), width=4, style=QtCore.Qt.SolidLine ))
        self.R_RPM = self.RPM.plot(pen=pyqtgraph.mkPen(color=(203, 26, 126), width=3, style=QtCore.Qt.SolidLine ))
        self.L_Toq = self.Torque.plot(pen=pyqtgraph.mkPen(color=(145, 122, 184), width=4, style=QtCore.Qt.SolidLine ))
        self.R_Toq = self.Torque.plot(pen=pyqtgraph.mkPen(color=(203, 26, 126), width=3, style=QtCore.Qt.SolidLine ))

        ################################################################
        # 모터 생성자
        self.motors = ZLAC8015D.MotorController(port='COM9', id = 2)

        self.motors.disable_motor()
        self.motors.enable_motor()

        self.motors.set_mode(4)
        self.motors.set_max_rpm(100)
        self.motors.set_max_L_current(5)
        self.motors.set_max_R_current(5)
        self.motors.set_rated_L_current(3)
        self.motors.set_rated_R_current(3)
        self.motors.RATED_TORQUE = 3000
        self.motors.set_rpm_w_toq(200)

        # self.motors.set_mode(3)
        # self.motors.set_max_rpm(250)
        # self.motors.set_max_L_current(15)
        # self.motors.set_max_R_current(15)
        # self.motors.set_rpm(30,-30)
        #################################################################

        queue_size = 200
        self.L_rpm_queue = deque(maxlen=queue_size)
        self.R_rpm_queue = deque(maxlen=queue_size)
        self.L_toq_queue = deque(maxlen=queue_size)
        self.R_toq_queue = deque(maxlen=queue_size)
        self.L_watt_queue = deque(maxlen=queue_size)
        self.R_watt_queue = deque(maxlen=queue_size)


        # 일정 시간 마다 그래프 및 라벨값 갱신
        self.Data_Get_Timer = QTimer()
        self.Data_Get_Timer.setInterval(1) # ms
        self.Data_Get_Timer.timeout.connect(self.update)
        self.Data_Get_Timer.start()
        self.showMaximized()

    @pyqtSlot()
    def update(self):
        # 모터에서 RPM, 토크, 전압 가져오기
        L_rpm, R_rpm = self.motors.get_rpm()
        L_toq, R_toq = self.motors.get_torque()
        Vol = self.motors.get_voltage()
        L_watt = abs(L_toq) * Vol
        R_watt = abs(R_toq) * Vol
        ModeNum = self.motors.get_mode()
        Mode = "Velocity" if ModeNum == 3 else "Torque" if ModeNum == 4 else "Unknown"
        Driver_temp = self.motors.get_driver_temp()
        L_error, R_error = self.motors.get_fault_code()

        self.L_rpm_queue.append(L_rpm)
        self.R_rpm_queue.append(R_rpm)
        self.L_toq_queue.append(L_toq)
        self.R_toq_queue.append(R_toq)
        self.L_watt_queue.append(L_watt)
        self.R_watt_queue.append(R_watt)

        # 그래프 갱신
        self.L_Watt.setData(list(self.L_watt_queue), name="Left Motor Watt")
        self.R_Watt.setData(list(self.R_watt_queue), name="Right Motor Watt")
        self.L_RPM.setData(list(self.L_rpm_queue), name="Left Motor RPM")
        self.R_RPM.setData(list(self.R_rpm_queue), name="Right Motor RPM")
        self.L_Toq.setData(list(self.L_toq_queue), name="Left Motor Torque")
        self.R_Toq.setData(list(self.R_toq_queue), name="Right Motor Torque")

        # 데이터 인디케이터 갱신
        self.label_DM.setText(Mode)
        self.label_DT.setText("%.1f °C" % Driver_temp)
        self.label_VT.setText("%.1f V" % Vol)
        self.label_LT.setText("%.1f A" % L_toq)
        self.label_LV.setText("%.1f RPM" % L_rpm)
        self.label_RT.setText("%.1f A" % R_toq)
        self.label_RV.setText("%.1f RPM" % R_rpm)
        self.label_LE.setText(L_error[0])
        self.label_RE.setText(R_error[0])
    
    def closeEvent(self, QCloseEvent):
        self.motors.disable_motor()
        print("Motor Disabled")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())

