import httplib2
import apiclient
import dbinteraction as db
from oauth2client.service_account import ServiceAccountCredentials


class File:

    def __init__(self):
        CREDENTIALS_FILE = 'creds.json'
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('drive', 'v3', http=httpAuth)

    def get(self, filedrive, pathto):
        """
            filedrive -  fileid at google drive
            pathto - path to a new file
        """

        data = self.service.files().get_media(fileId=filedrive).execute()
        if data:
            with open(pathto, 'wb') as f:
                f.write(data)

    def post(self, filedrive, pathto, directory='general'):
        """
            filedrive -  name of a new file at google drive
            pathto - path to a file
            directory - a name of a parent directory
        """

        dirs_ids = {'answers': '1dMpj6wlLrJUdW3_GtxnJBkOQJoPV-4y7', 'audio': '15UIN3O1iSv0F5s28czXEpCJZlrzYVaVl',
                    'img': '12JO-0jjME-X_IFge6SIa9jegxowVCiwO', 'tests': '1wdfbE4HsS-7BCW3zNTY4U4bcaEHc9QLc',
                    'general': '1Zpov7-QHU3KoNGZhSLNSXRcgG77Y6K4x'}
        if directory == 'img':
            type = 'image/' + pathto.split('.')[-1]
        elif directory == 'audio':
            if pathto.split('.')[-1] == 'mp3':
                type = 'audio/mpeg'
            elif pathto.split('.')[-1] == 'wav':
                type = 'x-wav'
        else:
            type = 'text/plain'
        print(type)
        file_metadata = {'name': filedrive, 'parents': [dirs_ids[directory]]}
        media = apiclient.http.MediaFileUpload(pathto, mimetype=type)
        file = self.service.files().create(body=file_metadata,
                                           media_body=media,
                                           fields='id').execute()
        new_id = file.get('id')
        print('File ID: %s' % new_id)
        return new_id


if __name__ == "__main__":
    a = File()
    a.post("new999.png", "img/prof.png", 'img')
