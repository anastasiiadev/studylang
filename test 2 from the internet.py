import ftplib


def ftp_upload(ftp_obj, path, ftype='TXT'):
    """
    Функция для загрузки файлов на FTP-сервер
    @param ftp_obj: Объект протокола передачи файлов
    @param path: Путь к файлу для загрузки
    """
    if ftype == 'TXT':
        with open(path) as fobj:
            ftp.storlines('STOR ' + path, fobj)
    else:
        with open(path, 'rb') as fobj:
            ftp.storbinary('STOR ' + path, fobj, 1024)


if __name__ == '__main__':
    ftp = ftplib.FTP('stacey789.beget.tech', 'stacey789_ftp', 'StudyLang456987')
    ftp.login()

    path = 'C:/Users/1/Desktop/for_test.txt'
    ftp_upload(ftp, path)

    #pdf_path = '/path/to/something.pdf'
    #ftp_upload(ftp, pdf_path, ftype='PDF')

    ftp.quit()
