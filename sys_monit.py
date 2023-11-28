
import sys
import psutil 
import platform 
import subprocess 
import cpuinfo
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel,QMessageBox,QPushButton,QInputDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import pyqtgraph as pg
from pyqtgraph import PlotWidget
from collections import deque

class SystemMonitor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("System Monitor 3000")
        self.setGeometry(500, 200, 900, 600)
        self.central_widget = QTabWidget(self)
        self.setCentralWidget(self.central_widget)



        self.cpu_widget = QWidget()
        self.gpu_widget = QWidget()
        self.ram_widget = QWidget()
        self.system_widget = QWidget()



        self.central_widget.addTab(self.system_widget, "System")
        self.central_widget.addTab(self.cpu_widget, "CPU")
        self.central_widget.addTab(self.gpu_widget, "GPU")
        self.central_widget.addTab(self.ram_widget, "RAM")
     
        

        self.init_cpu_tab()
        self.init_gpu_tab()
        self.init_ram_tab()
        self.init_system_tab()
        
        

    def init_cpu_tab(self):
        
       
        font = QFont()
        font.setPointSize(10)
        layout = QVBoxLayout(self.cpu_widget)

        self.cpu_label = QLabel()
        layout.addWidget(self.cpu_label)
        

    
        cpu_model_label = QLabel(f"{cpuinfo.get_cpu_info()["brand_raw"]}")
        layout.addWidget(cpu_model_label)
        cpu_model_label.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)


        self.cpu_plot = PlotWidget(title="CPU Usage (%)")
        self.cpu_plot.setMouseEnabled(x=False, y=False) 
        layout.addWidget(self.cpu_plot)
        cpu_model_label.setFont(font)
        
        
       
        self.cpu_curve = self.cpu_plot.plot(pen="b") 
       
        self.cpu_data = deque(maxlen=60) 
        self.cpu_timer = QTimer(self)
        self.cpu_timer.timeout.connect(self.update_cpu_plot)
        self.cpu_timer.start(1000) 



    def update_cpu_plot(self):
        
      
        font = QFont()
        font.setPointSize(10)
        cpu_percent = psutil.cpu_percent(interval=0)
        self.cpu_data.append(cpu_percent)
        self.cpu_curve.setData(self.cpu_data)


        self.cpu_label.setText(f"CPU: {cpu_percent:.2f}%")
        self.cpu_label.setAlignment(Qt.AlignRight)
        self.cpu_label.setFont(font)
        

    def init_gpu_tab(self):
        
        layout = QVBoxLayout(self.gpu_widget)
        self.gpu_temp_label = QLabel()
        self.gpu_temp_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.gpu_temp_label)

       
       
        self.gpu_info_label = QLabel()
        layout.addWidget(self.gpu_info_label)

        self.gpu_temp_plot = pg.PlotWidget(title="GPU Temperature (°C)")
        
        self.gpu_temp_plot.setMouseEnabled(x=False, y=False)  
        layout.addWidget(self.gpu_temp_plot)

        self.gpu_curve=self.gpu_temp_plot.plot(pen='g')
        self.gpu_temp_data = deque(maxlen=60)
        self.gpu_timer = QTimer(self)
        self.gpu_timer.timeout.connect(self.update_gpu_info) 
        self.gpu_timer.start(1000) 



    def update_gpu_info(self):
        
        font = QFont()
        font.setPointSize(10)
    
   
        system = platform.system()
        if system == "Windows":
            result = subprocess.check_output("nvidia-smi --query-gpu=name,memory.total,temperature.gpu --format=csv,noheader", shell=True)
        elif system == "Linux":
            result = subprocess.check_output("nvidia-smi --query-gpu=name,memory.total,temperature.gpu --format=csv,noheader,nounits", shell=True)
        else:
            self.gpu_info_label.setText("Kup normalny komputer")
            return

        gpu_info = result.decode("utf-8").strip().split(', ') 
        name, memory, temperature = gpu_info

        
        gpu_info_text = f" {name} \n {memory} "
        self.gpu_info_label.setText(gpu_info_text)
        self.gpu_info_label.setAlignment(Qt.AlignCenter)
        self.gpu_info_label.setFont(font)
        
        xd=float(temperature) 
        
        self.gpu_temp_label.setText(f"GPU temp: {xd:.2f}°C")
        self.gpu_temp_label.setAlignment(Qt.AlignRight)
        self.gpu_temp_label.setFont(font)
        
       
        temp = float(temperature)
        self.gpu_temp_data.append(temp)
        self.gpu_curve.setData(self.gpu_temp_data)
            

        
    def init_ram_tab(self):
        
        layout = QVBoxLayout(self.ram_widget)

       
        self.ram_percent_label = QLabel()
        layout.addWidget(self.ram_percent_label)
        
        
        self.ram_usage_label=QLabel()
        layout.addWidget(self.ram_usage_label)

        self.ram_total_label = QLabel()
        layout.addWidget(self.ram_total_label)
        
        

        self.ram_plot = pg.PlotWidget(title="RAM Usage (%)")
        self.ram_plot.setMouseEnabled(x=False, y=False)  
        layout.addWidget(self.ram_plot)

        self.ram_curve = self.ram_plot.plot(pen="r")
        self.ram_data = deque(maxlen=60)
        self.ram_timer = QTimer(self)
        self.ram_timer.timeout.connect(self.update_ram_plot)
        self.ram_timer.start(1000)  


    def update_ram_plot(self):
        
        ram_info = psutil.virtual_memory()
        ram_percent = ram_info.percent
        ram_total = ram_info.total
        ram_used=ram_info.used
        self.ram_data.append(ram_percent)
        self.ram_curve.setData(self.ram_data)

        font = QFont()
        font.setPointSize(10)
        
        self.ram_percent_label.setText(f"RAM Usage %: {ram_percent:.2f}%")
        self.ram_percent_label.setAlignment(Qt.AlignRight)
        self.ram_usage_label.setText(f"RAM Usage GB: {ram_used/(1024**3):.2f}GB") #w bajtach więc dzielimy 
        self.ram_usage_label.setAlignment(Qt.AlignRight)
        self.ram_total_label.setText(f"Total RAM: {ram_total / (1024**3):.2f}GB")
        self.ram_total_label.setAlignment(Qt.AlignCenter)
        self.ram_total_label.setFont(font)
        self.ram_percent_label.setFont(font)
        self.ram_usage_label.setFont(font)
        


    def init_system_tab(self):
        
        layout = QVBoxLayout(self.system_widget)
        
        uname = platform.uname()
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)


        system_info = [
            
            f"System: {uname.system}",
            f"Node: {uname.node}", 
            f"Release: {uname.release}",
            f"Version: {uname.version}",
            f"Machine: {uname.machine}",
            f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"
        ]
        
        
        system_info_label = QLabel("\n".join(system_info))
        font = QFont()
        font.setPointSize(15)
        system_info_label.setFont(font)
        system_info_label.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)
        layout.addWidget(system_info_label)
        
        self.current_time_label = QLabel()
        self.current_time_label.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)
        layout.addWidget(self.current_time_label)
        
        self.current_time_label.setFont(font)
        
        
        
        save_button = QPushButton("Save System Info")
        save_button.clicked.connect(self.save_system_info)
        layout.addWidget(save_button)
        
        
        
        self.current_time_timer = QTimer(self)
        self.current_time_timer.timeout.connect(self.update_current_time)
        self.current_time_timer.start(1000) 
    
    
    def update_current_time(self):
     current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     self.current_time_label.setText(f"{current_time}")
     
     
    def save_system_info(self):
        
     dialog = QInputDialog(self)
     dialog.setInputMode(QInputDialog.TextInput)
     dialog.setWindowTitle("System Info Saver 3000")
     dialog.setLabelText("Enter a filename:")
     dialog.setGeometry(800, 500, 400, 100)  
    
     ok = dialog.exec_() 

     if ok:
        filename = dialog.textValue().strip() 
        if not filename:
            QMessageBox.warning(self, "Error", "You must enter filename")
        else: 
            if not filename.endswith(".txt"):
                filename += ".txt"
        
            uname = platform.uname()
            boot_time_timestamp = psutil.boot_time()
            bt = datetime.fromtimestamp(boot_time_timestamp)

            system_info = [
                f"System: {uname.system}",
                f"Node: {uname.node}",
                f"Release: {uname.release}",
                f"Version: {uname.version}",
                f"Machine: {uname.machine}",
                f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}",
                f"RAM: {psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
                f"CPU: {cpuinfo.get_cpu_info()['brand_raw']}\n",
                f"File created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                
            ]

            system_info_text = "\n".join(system_info) 
            with open(filename, "w") as file:
                file.write(system_info_text)

            QMessageBox.information(self, "Info", f"Saved to {filename}")



app = QApplication(sys.argv)
monitor = SystemMonitor()
monitor.show()
sys.exit(app.exec_())
