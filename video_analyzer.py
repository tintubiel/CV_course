import cv2
from area_of_interest import AreaOfInterest
from track_manager import TrackManager


class VideoAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.cap = cv2.VideoCapture(filename)
        self.bg = cv2.createBackgroundSubtractorKNN(history=1000)
        self.area_of_interest = AreaOfInterest()
        self.track_manager = TrackManager()

    def analyze(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if ret:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
                fg_mask = self.bg.apply(gray_frame)
                frame = cv2.medianBlur(frame, 3)
                if self.area_of_interest.num_points == 0:# Если область  интереса не установлена
                    self.area_of_interest.set_points(frame)

                contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                self.area_of_interest.draw(frame)  # Отображение области интереса

                for i, contour in enumerate(contours):
                    area = cv2.contourArea(contour)
                    if area < 50 or area > 10_000:
                        continue

                    M = cv2.moments(contour)
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    cv2.circle(frame, (cx, cy), radius=3, color=(0, 255, 255), thickness=2)
                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(frame, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 255), thickness=1)

                    self.track_manager.add_track_point((cx, cy), self.area_of_interest.get_points())
                    self.track_manager.display_tracks(frame)

                self.track_manager.create_tracks_list()
                self.track_manager.clear_updated_param()

                cv2.namedWindow("Output video", cv2.WINDOW_NORMAL)
                cv2.imshow('Output video', frame)

            if cv2.waitKey(25) & 0xff == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    filename = r'../lab3_m/videoplayback.mp4'
    analyzer = VideoAnalyzer(filename)
    analyzer.analyze()
