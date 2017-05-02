# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import av
from av.video.frame import VideoFrame
from av.video.stream import VideoStream

# В этом списке будем хранить кадры в виде numpy-векторов.
array_list = []

# Откроем контейнер на чтение
input_container = av.open('input.mp4')

# Применим «инверсное мультиплексирование» =)
# Получим пакеты из потока.
input_packets = input_container.demux()

# Получии все кадры видео и положим их в `array_list`.
for packet in input_packets:
    if isinstance(packet.stream, VideoStream):
        # Получим все кадры пакета
        frames = packet.decode()
        for raw_frame in frames:
            # Переформатируем кадры, к нужному размеру и виду.
            # Это лучше делать средствами pyav (libav)
            #   потому что быстрее.
            frame = raw_frame.reformat(32, 32, 'rgb24')
            # Превратить каждый кадр в numpy-вектор (dtype=int).
            array = frame.to_nd_array()
            # Положим в список numpy-векторов.
            array_list += [array]

# Откроем контейнер на запись.
output_container = av.open('out.mp4', mode='w', format='mp4')

# Добавим к контейнеру поток c кодеком h264.
output_stream = output_container.add_stream('h264', rate=25)

# В этом списке будем хранить пакеты выходного потока.
output_packets = []

# Пройдем по списку векторов и упакуем их в пакеты выходного протока.
for array in array_list:
    # Построим видео-кадр по вектору.
    frame = VideoFrame.from_ndarray(array, format='rgb24')
    # Запакуем полученный кадр.
    packet = output_stream.encode(frame)
    # Положим в список пакетов.
    output_packets += [packet]

# Применим «прямое мультиплексирование» =)
# Для каждого пакета вызовем мультиплексор.
for packet in output_packets:
    if packet:
        output_container.mux(packet)

output_container.close()
