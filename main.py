# -*- coding: utf8 -*-


from shot_detector.main_detector import SimpleDetector

DEFAULT_FILE_NAME = '/home/video/file.mp4'

if __name__ == '__main__':
    detector = SimpleDetector()
    detector.detect(DEFAULT_FILE_NAME)
