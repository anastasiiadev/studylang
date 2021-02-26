import os

class Making_Folder:

    def __init__(self, directory):

        """
        :param directory: папка на жестком диске ПК
        Атрибут self.path_to_folder представляет собой путь до указанной папки
        Если папки не существует, то функция создает ее
        """

        self.path = os.getcwd()
        self.path_to_folder = self.path + directory
        if os.path.exists(self.path_to_folder) is False:
            os.mkdir(self.path_to_folder)

    def remove(self, filename):

        """
        :param filename: имя файла, который необходимо удалить
        Функция удаляет файл из указанной ранее папки.
        """
        os.remove(self.path_to_folder + filename)
