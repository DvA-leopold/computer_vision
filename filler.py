import cv2


def coroutine(f):
    def wrap(*args, **kwargs):
        gen = f(*args, **kwargs)
        gen.send(None)
        return gen
    return wrap


@coroutine
def fill_image_part(y, x):
    points_set = {(y, x)}
    image_shape = image.shape
    try:
        while True:
            y, x = points_set.pop()
            if image[y, x] == 255:
                image[y, x] = 127
                if y < image_shape[0] - 1:
                    points_set.add((y + 1, x))
                if y > 0:
                    points_set.add((y - 1, x))
                if x < image_shape[1] - 1:
                    points_set.add((y, x + 1))
                if x > 0:
                    points_set.add((y, x - 1))
            yield True
    except KeyError:
        yield False


def click_callback(event, x, y, flags, param):
    if event is cv2.EVENT_LBUTTONDOWN:
        routine = fill_image_part(y, x)
        while next(routine):
            pass


image = cv2.imread('res/image2.bmp', 0)
print('image size:', image.shape)

cv2.namedWindow('img')
cv2.setMouseCallback('img', click_callback)

while True:
    cv2.imshow('img', image)
    key = cv2.waitKey(10)

    if key == ord('q'):
        break

cv2.destroyAllWindows()
