# coding=utf8
from pyutil.program.db_pool import BaseDAL


class BaseImageDAL(BaseDAL):
    def __init__(self, db_pool):
        super(BaseImageDAL, self).__init__(db_pool.get('image'))


class ImageDAL(BaseImageDAL):
    def insert_image(self, image):
        return self.insert(
            'image',
            info=image,
            on_duplicate_update=True,
            dup_unupdate_keys=['id', 'image_path', 'cdnetworks_status'],
        )
