# 원본 영상으로 key-point 추출 

import os
import json
import cv2
import mediapipe as mp
import pandas as pd

# 저장 경로 설정
output_dir = "output"

os.makedirs(output_dir, exist_ok=True)

video_path = "input.mp4"

cap = cv2.VideoCapture(video_path)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# 비디오 저장 설정
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
fps = cap.get(cv2.CAP_PROP_FPS)

video_out_path = os.path.join(output_dir, "pose_output_video.mp4")
out = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

pose_data = []
frame_count = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(frame_rgb)

    if result.pose_landmarks:
        landmarks = result.pose_landmarks.landmark
        landmark_list = []
        for lm in landmarks:
            landmark_list.append({
                "x": lm.x,
                "y": lm.y,
                "z": lm.z,
                "visibility": lm.visibility
            })
        pose_data.append({
            "frame": frame_count,
            "landmarks": landmark_list
        })

        # 관절 시각화
        mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    out.write(frame)
    frame_count += 1

cap.release()
out.release()

# JSON 저장
json_out_path = os.path.join(output_dir, "pose_output.json")
with open(json_out_path, "w") as f:
    json.dump(pose_data, f, indent=2)

print(f" 관절 JSON 저장 완료: {json_out_path}")
print(f" 출력 영상 저장 완료: {video_out_path}")  # 관절 추출 test 확인용 
