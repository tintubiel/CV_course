import numpy as np
from track import Track


class TrackManager:
    def __init__(self):
        self.tracks = []

    def create_tracks_list(self):
        # Удаление треков, которые не были обновлены
        self.tracks = [track for track in self.tracks if track.was_updated]

    def clear_updated_param(self):
        # Подготовка треков к работе на следующем фрейме
        for track in self.tracks:
            track.was_updated = False

    @staticmethod
    def _velocity(last_point, new_point):
        # Вычисление вектора скорости между двумя точками
        return [last_point[0] - new_point[0], last_point[1] - new_point[1]]

    @staticmethod
    def _delta_velocity(last_velocity, new_velocity):
        # Вычисление изменения вектора скорости
        return abs(last_velocity[0] - new_velocity[0])**2 + abs(last_velocity[1] - new_velocity[1])**2

    @staticmethod
    def _not_in_area(last_point, new_point, eps):
        # Проверка, находится ли новая точка в пределах области
        return (last_point[0] - new_point[0])**2 + (last_point[1] - new_point[1])**2 > eps ** 2

    def add_track_point(self, point, area_points):
        point_area = 20
        min_velocity_delta = np.float('inf')
        track_index = -1

        for i, track in enumerate(self.tracks):
            prev_last_point, last_point, new_point = track.points[-2], track.points[-1], point
            if track.was_updated or self._not_in_area(last_point, new_point, point_area):
                continue
            # Вычисление векторов скорости
            delta_velocity = self._delta_velocity(self._velocity(prev_last_point, last_point), self._velocity(new_point, last_point))

            if delta_velocity < min_velocity_delta:
                track_index = i
                min_velocity_delta = delta_velocity

        if track_index < 0: # точка принадлежит новому треку
            new_track = Track(area_points)
            new_track.add_point(point)
            self.tracks.append(new_track)
        else:
            self.tracks[track_index].add_point(point)

    def display_tracks(self, frame):
        for track in self.tracks:
            track.display_track(frame)
