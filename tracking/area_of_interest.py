import cv2
import numpy as np


class AreaOfInterest:
    def __init__(self):
        self.points = []
        self.num_points = 0

    def set_points(self, frame):
        def mouse_callback(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONUP:
                self.points.append((x, y))
                cv2.circle(frame, (x, y), radius=3, color=(0, 0, 255), thickness=-1)
                self.num_points += 1

                if self.num_points == 4:
                    cv2.setMouseCallback('Set Area of Interest', lambda *args: None)

        cv2.namedWindow('Set Area of Interest')
        cv2.setMouseCallback('Set Area of Interest', mouse_callback)
        cv2.putText(frame, 'Click to set the 4 points of ROI', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 255), 2)
        cv2.imshow('Set Area of Interest', frame)

        while True:
            if cv2.waitKey(1) & 0xFF == ord('q') or self.num_points == 4:
                break

        cv2.destroyAllWindows()

    def draw(self, frame):
        if self.num_points == 4:
            roi_points = np.array(self.points, dtype=np.int32)
            cv2.polylines(frame, [roi_points], isClosed=True, color=(0, 0, 255), thickness=2)
            cv2.putText(frame, 'Area of Interest', (roi_points[0][0], roi_points[0][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    def get_points(self):
        return self.points
