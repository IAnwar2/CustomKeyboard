import time
import serial
import serial.tools.list_ports
import signal
import msvcrt
import psutil
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class KeyboardApplication:
    def __init__(self, chromedriver_path, pid, vid, bd_rate, verbose=True):
        self.chromedriver_path = chromedriver_path
        self.pid = pid
        self.vid = vid
        self.bd_rate = bd_rate
        self.verbose = verbose
        self.ser = None
        self.is_connected = False
        self.exit = False
        self.chrome_options = None
        self.service = None
        self.driver = None
        self.Open = False

    def find_com_port(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.pid == self.pid and port.vid == self.vid:
                if self.verbose:
                    print(f"Arduino board found on port {port.device}")
                return port.device
        return None

    def connect_board(self):
        com_port = self.find_com_port()
        if com_port:
            self.ser = serial.Serial(com_port, self.bd_rate)
            if self.verbose:
                print(f"Serial port {com_port} opened successfully")
            self.is_connected = True

    def check_connection(self):
        if self.ser and not self.ser.is_open:
            if self.verbose:
                print(f"Serial port {self.ser.port} closed.")
            self.is_connected = False

    # def exit_handler(self, signum, frame):
    def exit_handler(self):
        print("Keyboard application closing...")
        time.sleep(1)
        self.exit = True

    def read_inputs(self):
        if self.ser and self.ser.in_waiting > 0:
            data = self.ser.readline().decode('utf-8').strip()
            if self.verbose:
                print(f"Received from Arduino: {data}")
            return data
        return None
    
    def process_inputs(self, data):
        if not data:
            return

        urls = {
            "Youtube": 'https://www.youtube.com/',
            "Prime": 'https://www.primevideo.com/',
            "Gmail": 'https://mail.google.com/',
            "Zoro": 'https://zorox.to/home',
            "Buffstreams": 'https://sportshub.stream/',
            "Discord": 'https://discord.com/'
        }
        url = urls.get(data)

        if url:
            if not self.Open:
                self.init_webdriver()
                self.driver.get(url)
                self.Open = True
                return

            try:
                self.driver.switch_to.window(self.driver.window_handles[0])
                self.driver.execute_script(f"window.open('{url}', '_blank')")
            except:
                self.init_webdriver()
                self.driver.get(url)      

    def init_webdriver(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.chrome_options.add_argument('--disable-extensions')
        self.chrome_options.add_argument('--disable-popup-blocking')
        # self.chrome_options.add_argument('--user-data-dir=C:/Users/mianw/AppData/Local/Google/Chrome/User Data') no driver available (need exact version for chrome)
        self.chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        self.service = Service(executable_path=self.chromedriver_path)
        self.service.start()
        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)

    def run(self):
        # signal.signal(signal.SIGINT, self.exit_handler)
        # signal.signal(signal.SIGTERM, self.exit_handler)
        while not self.exit:
            if not self.is_connected:
                self.connect_board()
                # print(f"self.is_connected {self.is_connected}")
            else:
                self.check_connection()
                
                self.process_inputs(self.read_inputs())

            if msvcrt.kbhit():
                if msvcrt.getch().decode().lower() == 'q':
                    self.exit_handler()

            time.sleep(0.1)

if __name__ == "__main__":
    app = KeyboardApplication(
        chromedriver_path='C:/Users/mianw/OneDrive/Desktop/Side Projects/Keyboard/chromedriver-win64/chromedriver-win64/chromedriver.exe',
        pid=32852,
        vid=9025,
        bd_rate=9600,
        verbose=True
    )
    app.run()
