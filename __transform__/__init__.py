# -*- coding: utf-8 -*-
from source_transform import BaseTransform


class TestTransform(BaseTransform):

    @staticmethod
    def trigger(mmaped_file, **kwargs):
        return mmaped_file.find(b'DEADBEEF') >= 0

    @staticmethod
    def transform(data):
        return data.replace(
            'DEADBEEF',
            'REALBEEF'
        )
