import numpy as np
import cv2


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1200)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 750)
    if not cap.isOpened():
        cap.open()

    threshold = 2
    history_buffer = []
    points = None
    while True:
        ret, frame = cap.read()
        if not ret:
            print('frame read error')
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        h, w = frame.shape[:2]
        eigen = cv2.cornerEigenValsAndVecs(gray, 30, 3).reshape(h, w, 3, 2)  # [[e1, e2], v1, v2]
        flow = eigen[:, :, 2]
        frame[:] = (np.uint32(frame)) / 2
        d = 12
        points = np.dstack(np.mgrid[d / 2:w:d, d / 2:h:d]).reshape(-1, 2)

        if len(history_buffer) >= 3:
            for x, y in np.int32(points):
                local_flow = history_buffer[0][1]
                local_flow_second = history_buffer[1][1]

                local_vx, local_vy = np.int32(local_flow[y, x] * d)
                local_s_vx, local_s_vy = np.int32(local_flow_second[y, x] * d)
                vx, vy = np.int32(flow[y, x] * d)
                if abs(vx - local_s_vx) < threshold and abs(vy - local_s_vy) < threshold and abs(local_vy - local_s_vy) < threshold and abs(local_vx - local_s_vx) < threshold:
                    cv2.line(frame, (x - vx, y - vy), (x + vx, y + vy), (0, 0, 0), 1, cv2.LINE_AA)
            cv2.imshow('flow', frame)
            history_buffer.pop(0)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        history_buffer.append((frame, flow))
    cap.release()
    cv2.destroyAllWindows()

