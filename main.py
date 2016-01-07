# -*- coding: utf8 -*-


from shot_detector.main_detector import SimpleDetector

DEFAULT_FILE_NAME = '/run/media/w495/A2CAE41FCAE3ED8B/home/w495/Videos/Djadja_Stepa Milicioner_96.lw.und.mp4'

if (__name__ == '__main__'):
    detector = SimpleDetector()

    detector.detect(DEFAULT_FILE_NAME)
