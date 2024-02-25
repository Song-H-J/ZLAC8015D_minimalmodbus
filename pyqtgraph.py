import os
import pyqtgraph
from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel
from PyQt5.QtCore import pyqtSlot, QTimer, Qt
from pandas import DataFrame
import pandas
import serial
import time
import binascii


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
        self.stringaxisP = pyqtgraph.AxisItem(orientation='bottom')
        self.stringaxisE = pyqtgraph.AxisItem(orientation='bottom')
        self.stringaxisV = pyqtgraph.AxisItem(orientation='bottom')
        self.stringaxisT = pyqtgraph.AxisItem(orientation='bottom')
        self.Power = pyqtgraph.PlotWidget(axisItems={'bottom': self.stringaxisP})
        self.Energy = pyqtgraph.PlotWidget(axisItems={'bottom': self.stringaxisE})
        self.Voltage = pyqtgraph.PlotWidget(axisItems={'bottom': self.stringaxisV})
        self.Temperature = pyqtgraph.PlotWidget(axisItems={'bottom': self.stringaxisT})

        # 그래프 제목 생성
        self.Power.setTitle("Generating Power", color="#828282", size="12pt")
        self.Energy.setTitle("Generating Energy Today", color="#828282", size="12pt")
        self.Voltage.setTitle("Generating Voltage / Efficency", color="#828282", size="12pt")
        self.Temperature.setTitle("Inverter Temperature", color="#828282", size="12pt")

        # 그래프 제목 글꼴 설정
        self.Power.getPlotItem().titleLabel.item.setFont(font)
        self.Energy.getPlotItem().titleLabel.item.setFont(font)
        self.Voltage.getPlotItem().titleLabel.item.setFont(font)
        self.Temperature.getPlotItem().titleLabel.item.setFont(font)

        # X, Y축 이름 스타일 설정
        labelStyle = {'color': '#828282', 'font-size': '9pt' }

        # X, Y축 이름 생성
        self.Power.setLabel('left', 'Power', units='W', **labelStyle)
        self.Energy.setLabel('left', 'Energy', units='Wh', **labelStyle)
        self.Voltage.setLabel('left', 'Voltage', units='V', **labelStyle)
        self.Temperature.setLabel('left', 'Temperature', units='℃', **labelStyle)
        self.Power.setLabel('bottom', 'Time', **labelStyle)
        self.Energy.setLabel('bottom', 'Time', **labelStyle)
        self.Voltage.setLabel('bottom', 'Time', **labelStyle)
        self.Temperature.setLabel('bottom', 'Time', **labelStyle)

        # x,y 눈금 글꼴 설정
        self.Power.getAxis('bottom').setStyle(tickFont = font_tick, tickTextOffset=6)
        self.Energy.getAxis('bottom').setStyle(tickFont = font_tick, tickTextOffset=6)
        self.Voltage.getAxis('bottom').setStyle(tickFont = font_tick, tickTextOffset=6)
        self.Temperature.getAxis('bottom').setStyle(tickFont = font_tick, tickTextOffset=6)
        self.Power.getAxis('left').setStyle(tickFont = font_tick, tickTextOffset=6)
        self.Energy.getAxis('left').setStyle(tickFont = font_tick, tickTextOffset=6)
        self.Voltage.getAxis('left').setStyle(tickFont = font_tick, tickTextOffset=6)
        self.Temperature.getAxis('left').setStyle(tickFont = font_tick, tickTextOffset=6)

        # 그래프 그리드 설정
        self.Power.showGrid(x=True, y=True)
        self.Energy.showGrid(x=True, y=True)
        self.Voltage.showGrid(x=True, y=True)
        self.Temperature.showGrid(x=True, y=True)

        # 그래프 배경색 지정
        self.Power.setBackground((240,240,240))
        self.Energy.setBackground((240,240,240))
        self.Voltage.setBackground((240,240,240))
        self.Temperature.setBackground((240,240,240))

        # Data Indicator 그룹 박스 생성
        self.groupbox_SV = QGroupBox('Solar Voltage')
        self.groupbox_SC = QGroupBox('Solar Current')
        self.groupbox_SP = QGroupBox('Solar Power')
        self.groupbox_LV = QGroupBox('Line Voltage')
        self.groupbox_LC = QGroupBox('Line Current')
        self.groupbox_LP = QGroupBox('Line Power')
        self.groupbox_T = QGroupBox('Temperature')
        self.groupbox_TTL = QGroupBox('Energy Today')
        self.groupbox_LIFE = QGroupBox('LifeTime Energy')
        self.groupbox_Status = QGroupBox('Inverter Status')

        # Data Indicator 라벨 생성
        self.label_SV = QLabel('0', self)
        self.label_SC = QLabel('0', self)
        self.label_SP = QLabel('0', self)
        self.label_LV = QLabel('0', self)
        self.label_LC = QLabel('0', self)
        self.label_LP = QLabel('0', self)
        self.label_T = QLabel('0', self)
        self.label_TTL = QLabel('0', self)
        self.label_LIFE = QLabel('0', self)
        self.label_Status = QLabel('Ready', self)

        # Data Indicator 가운데 정렬
        self.label_SV.setAlignment(Qt.AlignCenter)
        self.label_SC.setAlignment(Qt.AlignCenter)
        self.label_SP.setAlignment(Qt.AlignCenter)
        self.label_LV.setAlignment(Qt.AlignCenter)
        self.label_LC.setAlignment(Qt.AlignCenter)
        self.label_LP.setAlignment(Qt.AlignCenter)
        self.label_T.setAlignment(Qt.AlignCenter)
        self.label_TTL.setAlignment(Qt.AlignCenter)
        self.label_LIFE.setAlignment(Qt.AlignCenter)
        self.label_Status.setAlignment(Qt.AlignCenter)

        # Data Indicator 배경색 및 테두리 설정
        self.label_SV.setStyleSheet("color:rgb(203, 26, 126);" "background-color:rgb(250,250,250);"
                                    "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                    "border-radius: 5px")
        self.label_SC.setStyleSheet("color:rgb(203, 26, 126);" "background-color:rgb(250,250,250);"
                                    "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                    "border-radius: 5px")
        self.label_SP.setStyleSheet("color:rgb(203, 26, 126);" "background-color:rgb(250,250,250);"
                                    "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                    "border-radius: 5px")
        self.label_LV.setStyleSheet("color:rgb(44, 106, 180);" "background-color:rgb(250,250,250);"
                                    "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                    "border-radius: 5px")
        self.label_LC.setStyleSheet("color:rgb(44, 106, 180);" "background-color:rgb(250,250,250);"
                                    "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                    "border-radius: 5px")
        self.label_LP.setStyleSheet("color:rgb(44, 106, 180);" "background-color:rgb(250,250,250);"
                                    "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                    "border-radius: 5px")
        self.label_T.setStyleSheet("color:rgb(244, 121, 40);" "background-color:rgb(250,250,250);"
                                   "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                   "border-radius: 5px")
        self.label_TTL.setStyleSheet("color:rgb(145, 122, 184);" "background-color:rgb(240,240,240);"
                                     "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                     "border-radius: 5px")
        self.label_LIFE.setStyleSheet("color:rgb(120, 120, 120);" "background-color:rgb(240,240,240);"
                                     "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                     "border-radius: 5px")
        self.label_Status.setStyleSheet("color:rgb(44, 106, 180)")

        # Data Indicator 글꼴 설정
        labelfont1 = self.label_SV.font()
        labelfont1.setFamily('Bahnschrift SemiLight')
        labelfont1.setPointSize(15)
        labelfont1.setBold(True)
        self.label_SV.setFont(labelfont1)
        self.label_SC.setFont(labelfont1)
        self.label_SP.setFont(labelfont1)
        self.label_LV.setFont(labelfont1)
        self.label_LC.setFont(labelfont1)
        self.label_LP.setFont(labelfont1)
        self.label_T.setFont(labelfont1)
        self.label_TTL.setFont(labelfont1)
        self.label_LIFE.setFont(labelfont1)
        self.label_Status.setFont(labelfont1)

        # 그룹박스와 Data Indicator 라벨 그룹화
        Gbox0.addWidget(self.label_SV)
        Gbox1.addWidget(self.label_SC)
        Gbox2.addWidget(self.label_SP)
        Gbox3.addWidget(self.label_LV)
        Gbox4.addWidget(self.label_LC)
        Gbox5.addWidget(self.label_LP)
        Gbox6.addWidget(self.label_T)
        Gbox7.addWidget(self.label_TTL)
        Gbox8.addWidget(self.label_LIFE)
        Gbox9.addWidget(self.label_Status)
        self.groupbox_SV.setLayout(Gbox0)
        self.groupbox_SC.setLayout(Gbox1)
        self.groupbox_SP.setLayout(Gbox2)
        self.groupbox_LV.setLayout(Gbox3)
        self.groupbox_LC.setLayout(Gbox4)
        self.groupbox_LP.setLayout(Gbox5)
        self.groupbox_T.setLayout(Gbox6)
        self.groupbox_TTL.setLayout(Gbox7)
        self.groupbox_LIFE.setLayout(Gbox8)
        self.groupbox_Status.setLayout(Gbox9)

        # 수평방향으로 창 그룹화 (1행 그래프 2개), (2행 그래프 2개), (3행 라벨 10개)
        hbox1.addWidget(self.Power)
        hbox1.addWidget(self.Energy)
        hbox2.addWidget(self.Voltage)
        hbox2.addWidget(self.Temperature)
        hbox3.addWidget(self.groupbox_SV)
        hbox3.addWidget(self.groupbox_SC)
        hbox3.addWidget(self.groupbox_SP)
        hbox3.addWidget(self.groupbox_LV)
        hbox3.addWidget(self.groupbox_LC)
        hbox3.addWidget(self.groupbox_LP)
        hbox3.addWidget(self.groupbox_T)
        hbox3.addWidget(self.groupbox_TTL)
        hbox3.addWidget(self.groupbox_LIFE)
        hbox3.addWidget(self.groupbox_Status)
        
        # 그룹화된 창 수직방향으로 그룹화
        vbox1.addLayout(hbox1)
        vbox1.addLayout(hbox2)
        vbox1.addLayout(hbox3)

        # 윈도우창생성 및 레이아웃 배치
        self.setLayout(vbox1)
        self.setGeometry(100, 100, 2600, 1000)  # 창 위치(x, y), width, height
        self.setWindowTitle("DONGYANG E&P INVERTER MONITORING PROGRAM  v0.61 by RAISON  -  %s  -"% Main.DF_Date)

        # X축 범위 생성
        self.Power.enableAutoRange(axis='x')
        self.Energy.enableAutoRange(axis='x')
        self.Voltage.enableAutoRange(axis='x')
        self.Temperature.enableAutoRange(axis='x')

        # Y축 범위 생성
        #self.Power.setYRange(0, 3)
        #self.Energy.setYRange(0, 20)
        #self.Voltage.setYRange(50, 250)
        #self.Temperature.setYRange(-20, 70)
        self.Power.enableAutoRange(axis='y')
        self.Energy.enableAutoRange(axis='y')
        self.Voltage.enableAutoRange(axis='y')
        self.Temperature.enableAutoRange(axis='y')

        # 그래프 펜 설정
        self.SolP_curve = self.Power.plot(pen=pyqtgraph.mkPen(color=(203, 26, 126), width=3, style=QtCore.Qt.SolidLine ))
        self.LineP_curve = self.Power.plot(pen=pyqtgraph.mkPen(color=(44,106, 180), width=3, style=QtCore.Qt.DotLine ))
        self.Energy_curve = self.Energy.plot(pen=pyqtgraph.mkPen(color=(145, 122, 184), width=4, style=QtCore.Qt.SolidLine ))
        self.SolV_curve = self.Voltage.plot(pen=pyqtgraph.mkPen(color=(203, 26, 126), width=3, style=QtCore.Qt.SolidLine ))
        self.LineV_curve = self.Voltage.plot(pen=pyqtgraph.mkPen(color=(44, 106, 180), width=3, style=QtCore.Qt.SolidLine ))
        self.Efficency_curve = self.Voltage.plot(pen=pyqtgraph.mkPen(color=(120, 120, 120), width=3, style=QtCore.Qt.SolidLine ))
        self.Temperature_curve = self.Temperature.plot(pen=pyqtgraph.mkPen(color=(244, 121, 40), width=4, style=QtCore.Qt.SolidLine ))

        # 일정 시간 마다 그래프 및 라벨값 갱신
        self.Data_Get_Timer = QTimer()
        self.Data_Get_Timer.setInterval(Main.Cycle_Time*1000)
        self.Data_Get_Timer.timeout.connect(self.update)
        self.Data_Get_Timer.start()
        self.show()
