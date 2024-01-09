import cv2
import numpy as np


class Track:
    def __init__(self, region, draw_len=20):#регулирование длины отрисовки трека
        self.points = []
        self.region = np.array([region], dtype=np.int32)
        self.was_updated = False
        self.draw_len = draw_len

    def add_point(self, point):
        if len(self.points) == 0:
            self.points.append(point)
        self.points.append(point)
        self.was_updated = True

    def display_track(self, frame):
        range_start = max(1, len(self.points) - self.draw_len)# если точек меньше draw_len, то рисуем все

        for i in range(range_start, len(self.points)):
            start, end = self.points[i - 1], self.points[i]

            # проверка нахождения в области интереса и отображение корректного цвета
            is_in_interest = cv2.pointPolygonTest(self.region, start, measureDist=False) >= 0
            color = (0, 0, 255) if is_in_interest else (0, 255, 255)

            # Отображение трека линиями на кадре
            cv2.line(frame, start, end, color=color)
