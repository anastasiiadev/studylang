import logging
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


class File:

    def __init__(self):

        """
        Создается подключение к google-диску через API.
        """

        CREDENTIALS_FILE = 'creds.json'
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('drive', 'v3', http=httpAuth)

    def get(self, filedrive, pathto):

        """
        :param filedrive: fileid на google-диске
        :param pathto: имя нового файла и путь до него на ПК
        Скачивает файл с google-диска.
        """

        data = self.service.files().get_media(fileId=filedrive).execute()
        if data:
            with open(pathto, 'wb') as f:
                f.write(data)

    def post(self, filedrive, pathto, directory='general'):

        """
            :param filedrive: имя нового файла на google-диске
            :param pathto: имя файла и путь до него на ПК
            :param directory: имя родительской папки на google-диске
            :return: идентификатор нового файла на google-диске
            Загружает файл на google-диск.
        """

        dirs_ids = {'answers': '1dMpj6wlLrJUdW3_GtxnJBkOQJoPV-4y7', 'audio': '15UIN3O1iSv0F5s28czXEpCJZlrzYVaVl',
                    'image': '12JO-0jjME-X_IFge6SIa9jegxowVCiwO', 'tests': '1wdfbE4HsS-7BCW3zNTY4U4bcaEHc9QLc',
                    'general': '1Zpov7-QHU3KoNGZhSLNSXRcgG77Y6K4x'}
        if directory == 'image':
            type = 'image/' + pathto.split('.')[-1]
        elif directory == 'audio':
            if pathto.split('.')[-1] == 'mp3':
                type = 'audio/mpeg'
            elif pathto.split('.')[-1] == 'wav':
                type = 'x-wav'
        else:
            type = 'text/plain'
        logging.info('filetype:', type)
        file_metadata = {'name': filedrive, 'parents': [dirs_ids[directory]]}
        media = apiclient.http.MediaFileUpload(pathto, mimetype=type)
        file = self.service.files().create(body=file_metadata,
                                           media_body=media,
                                           fields='id').execute()
        new_id = file.get('id')
        logging.info(f'File ID: {new_id}')
        return new_id


if __name__ == "__main__":
    logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)
    a = File()
    a.post("new999.png", "img/prof.png", 'image')
