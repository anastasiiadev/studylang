from ftplib import FTP
import os


try:
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect('stacey789.beget.tech', 21)
    ftp.login('stacey789_ftp', 'StudyLang456987')
    ftp.encoding = 'utf-8'
    ftp.cwd('/img')
    localfile = 'C:/Users/1/Desktop/iconSL.jpg'
    fp = open(localfile, 'rb')
    send = ftp.storbinary('STOR %s' % os.path.basename(localfile), fp, 1024)
except Exception:
    print('Cant send the file')
if 'send' in locals():
    print('yes')
else:
    print('no')

try:
    ftp.cwd('/audio')
    localfile = 'C:/Users/1/Desktop/1.jpg'
    fp = open(localfile, 'rb')
    send = ftp.storbinary('STOR %s' % os.path.basename(localfile), fp, 1024)
except Exception:
    print('Cant send the file')
    print(ftp.pwd())
