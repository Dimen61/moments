import os
import utils

class Photo:
    ACCEPT_IMAGE_FORMAT = [".jpg", ".png", ".jpeg"]

    @classmethod
    def check_photos(cls, folder_path):
        if not os.path.exists(folder_path):
            return (False, '没有指定文件夹，请指定!')

        file_paths = utils.get_all_files(folder_path)
        if len(file_paths) == 0:
            return (False, '请提供至少一张图片!')

        err_msgs = []
        for file_path in file_paths:
            is_ok, msg = Photo.check_photo_name(file_path)
            if not is_ok:
                err_msgs.append(msg)

        return (is_ok, '\n'.join(err_msgs))

    @classmethod
    def check_photo_name(cls, photo_name):
        file_prefix, format = utils.get_file_prefix_and_suffix(photo_name)
        print(f"file_prefix: {file_prefix}; format: {format}")

        if format.lower() not in Photo.ACCEPT_IMAGE_FORMAT:
            return (False, "照片文件的格式不对!")

        lst = file_prefix.split('-')
        if len(lst) != 2:
            return (False, "照片文件的命名不对哦！")

        return (True, None)

    @classmethod
    def get_photos(cls, folder_path):
        files = utils.get_all_files(folder_path)
        photos = [Photo(file) for file in files]
        return photos

    def __init__(self, photo_path):
        """photo file name format: 
        "{category}-{photo_name}.{format}"

        category can be number to represent 
        photo_name can be any string.
        format can be jpg, png or jpeg.
        """
        file_prefix, format = utils.get_file_prefix_and_suffix(photo_path)
        print(f"file_prefix: {file_prefix}; format: {format}")

        if format.lower() not in Photo.ACCEPT_IMAGE_FORMAT:
            raise TypeError("Not valid photo format!")

        lst = file_prefix.split('-')
        if len(lst) != 2:
            raise TypeError("Not valid photo name!")

        category, photo_name = lst
        print(f"category: {category}; photo_name: {photo_name}")

        self.category = category
        self.month = int(category)
        self.photo_name = photo_name
        self.image_path = photo_path


class Stats:
    def __init__(self):
        self.total_guess_num = 0
        self.guess_right_num = 0
        self.guess_wrong_num = 0

    def guess_right(self):
        self.total_guess_num += 1
        self.guess_right_num += 1

    def guess_wrong(self):
        self.total_guess_num += 1
        self.guess_wrong_num += 1


def main():
    print("Hello, world!")

main()
