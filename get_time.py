import cv2
import numpy as np
import sys

if __name__ == '__main__':

    args = sys.argv

    # 動画ファイルのパス
    video_path = args[1]

    cap = cv2.VideoCapture(video_path)

    cap_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    telop_height = 50

    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    writer = cv2.VideoWriter('telop_time.mp4',fourcc, fps, (cap_width, cap_height + telop_height))

    count = 0
    try :
        while True:
            if not cap.isOpened():
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            ret, frame = cap.read()

            if frame is None:
                break

            telop = np.zeros((telop_height, cap_width, 3), np.uint8)
            telop[:] = tuple((128,128,128))

            images = [frame, telop]

            frame = np.concatenate(images, axis=0)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, "{:.4f} [sec]".format(round(count/fps, 4)), 
                        (cap_width - 250, cap_height + telop_height - 10), 
                        font, 
                        1, 
                        (0, 0, 255), 
                        2, 
                        cv2.LINE_AA)
            writer.write(frame)
            count += 1

    except cv2.error as e:
        print(e)    

    writer.release()
    cap.release()

