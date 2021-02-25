import os

class Making_Folder:

    def __init__(self, directory):
        self.path = os.getcwd()
        self.path_to_folder = self.path + directory
        if os.path.exists(self.path_to_folder) is False:
            os.mkdir(self.path_to_folder)

    def remove(self, filename):
        os.remove(self.path_to_folder + filename)
