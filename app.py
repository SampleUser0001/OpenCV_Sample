import cv2
import numpy as np
import sys

if __name__ == '__main__':

    args = sys.argv

    # 動画ファイルのパス
    video_path = args[1]

    # OpenCVで動画ファイルを読み込み
    cap = cv2.VideoCapture(video_path)

    # フレーム間の差分の閾値
    threshold = 10_000_000

    # 前のフレームを保存する変数（初期化）
    ret, prev_frame = cap.read()
    prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    # ハイライトとして保存するフレームのカウンタ
    frame_count = 0

    while cap.isOpened():
        # 現在のフレームを読み込み
        ret, frame = cap.read()
        if not ret:
            break
        
        # 現在のフレームをグレースケールに変換
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 現在のフレームと前のフレームとの差分を計算
        diff = cv2.absdiff(prev_frame, gray)
        
        # 差分の合計が閾値を超えた場合、そのフレームを保存
        if np.sum(diff) > threshold:
            print(frame_count)
            cv2.imwrite(f'highlight_{frame_count}.jpg', frame)
            frame_count += 1
        
        # 現在のフレームを次の比較のために保存
        prev_frame = gray

    # 動画キャプチャを解放
    cap.release()
