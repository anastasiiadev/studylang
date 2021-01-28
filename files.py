import httplib2
import apiclient
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

    def post(self, filedrive, pathto):
        """
            filedrive -  name of a new file at google drive
            pathto - path to a file
        """

        file_metadata = {'name': filedrive, 'parents': ['1Zpov7-QHU3KoNGZhSLNSXRcgG77Y6K4x']}
        media = apiclient.http.MediaFileUpload(pathto, mimetype='image/png')
        file = self.service.files().create(body=file_metadata,
                                           media_body=media,
                                           fields='id').execute()
        print('File ID: %s' % file.get('id'))


a = File()
a.get("11U88pKL9sloaz1N1gOIDVBNYj7f0E1WN", "new.png")
