import sys, EndDo
from ftplib import FTP
from PyQt5.QtWidgets import QApplication

'''import requests

url = 'http://stacey789.beget.tech/source'
files = {'file': open('img/S.jpg', 'rb')}
r = requests.post(url, files=files)
r.text
if r.status_code == 200:
    print('fine')
else:
    print('error')
'''
'''
audiofile = 'Atlas.WAV'
path = os.getcwd()
folder = path + '\\audio\\'
if os.path.exists(folder) is False:
    os.mkdir(folder)
if os.path.exists(folder + audiofile) is False:
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect('stacey789.beget.tech', 21)
    ftp.login('stacey789_ftp', 'StudyLang456987')
    ftp.encoding = 'utf-8'
    ftp.cwd('/audio')
    download = ftp.retrbinary("RETR " + audiofile, open(folder + audiofile, 'wb').write)
    ftp.close()
'''
app = QApplication(sys.argv)
a = EndDo.ThisWindow()
sys.exit(app.exec_())

