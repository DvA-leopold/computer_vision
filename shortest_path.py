import cv2
from typing import Tuple, List, Union


class AStar:
    steps = ((0, 1), (1, 0), (1, 1), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1))

    def __init__(self):
        self.image = None  # black white image
        self.open_dict = dict()  # Dict[Tuple[int, int], Tuple[int, Tuple[int, int]]]
        self.closed_dict = dict()
        self.start_point = None  # Tuple[int, int]
        self.finish_point = None  # Tuple[int, int]

    def search_path(self, start: Tuple[int, int], finish: Tuple[int, int], img: List[List[int]]):
        self.start_point = start
        self.finish_point = finish
        self.image = img
        self.open_dict[start] = (0, start)
        while self.open_dict:
            path_price, parent_pixel = self.find_minimal_cost_point()
            if self.wave_path(path_price + 1, parent_pixel):
                self.reconstruct_path()
                break
        self.open_dict.clear()
        self.closed_dict.clear()

    def wave_path(self, path_price: int, parent_pixel_cords: Tuple[int, int]) -> bool:
        y, x = parent_pixel_cords
        for step in AStar.steps:
            step_y, step_x = step
            if self.finish_point == (y + step_y, x + step_x):
                self.closed_dict[self.finish_point] = parent_pixel_cords
                return True
            if y + step_y < self.image.shape[0] and x + step_x < self.image.shape[1]:
                if self.image[y + step_y, x + step_x] == 255 \
                        and (y + step_y, x + step_x) not in self.closed_dict:
                    self.open_dict[(y + step_y, x + step_x)] = \
                        (path_price + self.manhattans_distance(y + step_y, x + step_x), parent_pixel_cords)
        return False

    def find_minimal_cost_point(self) -> Union[int, Tuple[int, int]]:
        child_pixel = min(self.open_dict, key=self.open_dict.get)
        path_price, parent_pixel = self.open_dict.pop(child_pixel)
        self.closed_dict[child_pixel] = parent_pixel
        self.image[child_pixel] = 127
        return path_price, child_pixel

    def manhattans_distance(self, y: int, x: int) -> int:
        f_y, f_x = self.finish_point
        distance = abs(f_x - x) + abs(f_y - y)
        return distance

    def reconstruct_path(self):
        pixel = self.finish_point
        while pixel is not self.start_point:
            self.image[pixel] = 0
            pixel = self.closed_dict.pop(pixel)


def click_callback(event, x, y, flags, param):
    path_search_alg, start_finish_point, img = param
    if event is cv2.EVENT_LBUTTONDOWN:
        start_finish_point.append((y, x))
        if len(start_finish_point) == 2:
            path_search_alg.search_path(start_finish_point[0], start_finish_point[1], img)
            start_finish_point.clear()


if __name__ == '__main__':
    image = cv2.imread('res/image2.bmp', 0)

    path_search = AStar()
    start_finish_points = []
    cv2.namedWindow('img')
    cv2.setMouseCallback('img', click_callback, (path_search, start_finish_points, image))

    while True:
        cv2.imshow('img', image)
        key = cv2.waitKey(100)

        if key == ord('q'):
            break

    cv2.destroyAllWindows()
