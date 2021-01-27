import os
from ftplib import FTP

path = os.getcwd()
folder = path + '\\audio\\'
if os.path.exists(folder) is False:
    os.mkdir(folder)
file = 'Хлеб - Арабская девчёнка.mp3'
if os.path.exists(folder + file) is True:
    print('yes')
else:
    print('no')

try:
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect('stacey789.beget.tech', 21)
    ftp.login('stacey789_ftp', 'StudyLang456987')
    ftp.encoding = 'utf-8'
    download = ftp.retrbinary("RETR " + file, open(folder + file, 'wb').write)
    ftp.close()
except Exception:
    print('Cant download the file')
if 'download' in locals():
    print('downloaded')
else:
    print('not downloaded')

try:
    path = os.getcwd()
    folder = path + '\\audio\\'
    if os.path.exists(folder) is False:
        os.mkdir(folder)
    if os.path.exists(folder + file) is False:
        ftp = FTP()
        ftp.set_debuglevel(2)
        ftp.connect('stacey789.beget.tech', 21)
        ftp.login('stacey789_ftp', 'StudyLang456987')
        ftp.encoding = 'utf-8'
        ftp.cwd('/audio')
        download = ftp.retrbinary("RETR " + file, open(folder + file, 'wb').write)
        ftp.close()
except Exception:
    self.msgnofile = QMessageBox(self)
    self.msgnofile.critical(self, "Ошибка ", "Не удалось загрузить ваш файл.", QMessageBox.Ok)
if 'download' in locals():
    print('downloaded')
else:
    print('not downloaded')
