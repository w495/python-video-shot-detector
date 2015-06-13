# -*- coding: utf8 -*-


from simple_detector import SimpleDetector


if (__name__ == '__main__'):
    detector = SimpleDetector()

    video_file_name  = './v.hi.und.mp4'
    t1 = time.time()
    detector.detect(video_file_name)

