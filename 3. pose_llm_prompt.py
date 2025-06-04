# key-point.json -> 관절의 포인트로 음악 분위기 + LLM prompt - 생성

import json
import numpy as np

# 1. JSON 불러오기
with open("/Documents/pose_music/output/pose_output.json", "r") as f:
    pose_data = json.load(f)

# 2. 사용할 관절 인덱스 정의
key_joints = {
    "left_foot": 31,
    "right_hand": 16
}

# 3. 관절별 프레임 간 거리 변화 계산
joint_motion = {name: [] for name in key_joints}

for i in range(1, len(pose_data)):
    prev = pose_data[i - 1]["landmarks"]
    curr = pose_data[i]["landmarks"]
    for name, idx in key_joints.items():
        dx = abs(curr[idx]["x"] - prev[idx]["x"])
        dy = abs(curr[idx]["y"] - prev[idx]["y"])
        motion = np.sqrt(dx**2 + dy**2)
        joint_motion[name].append(motion)

# 4. 움직임 이벤트 추정
motion_events = {}
threshold = 0.015
for name, deltas in joint_motion.items():
    motion_events[name] = [1 if d > threshold else 0 for d in deltas]

# 5. BPM 추정
fps = 30
window_size = fps
bpm_counts = []

for i in range(0, len(pose_data) - window_size, window_size):
    beat_sum = sum(motion_events["left_foot"][i:i+window_size]) + sum(motion_events["right_hand"][i:i+window_size])
    bpm_counts.append(beat_sum)

avg_bps = np.mean(bpm_counts)
bpm_estimate = int(avg_bps * 60)

# 6. 움직임 밀도
total_frames = len(pose_data)
total_events = sum([sum(v) for v in motion_events.values()])
motion_density = "high" if total_events > total_frames else "moderate" if total_events > total_frames * 0.5 else "low"

# 7. 패턴 분석 (규칙성 판단)
pattern_std = np.std(bpm_counts)
tempo_pattern = "regular" if pattern_std < 2 else "variable"

# 8. 가장 활발한 관절
total_movement = {name: sum(vals) for name, vals in joint_motion.items()}
dominant_joints = sorted(total_movement, key=total_movement.get, reverse=True)[:2]

# 9. 스타일 추정 함수
def estimate_style(bpm, motion_density, tempo_pattern):
    if bpm > 140 or motion_density == "high":
        return "powerful, jumping"
    elif tempo_pattern == "variable" and motion_density == "moderate":
        return "dynamic, energetic"
    else:
        return "fluid, slow"

# 10. 스타일 결정
style = estimate_style(bpm_estimate, motion_density, tempo_pattern)

# 11. 결과 요약 정보 생성
summary = {
    "bpm": bpm_estimate,
    "dominant_joints": dominant_joints,
    "motion_density": motion_density,
    "tempo_pattern": tempo_pattern,
    "style": style
}

# 12. LLM 프롬프트 생성
joint_kor = {
    "left_foot": "왼발",
    "right_hand": "오른손"
}

prompt = f"""다음은 사람이 춤을 추는 동작의 요약 정보입니다:
- BPM: {summary['bpm']}
- 주로 사용된 관절: {', '.join(joint_kor.get(j, j) for j in summary['dominant_joints'])}
- 동작 밀도: {motion_density}
- 특징: 동작 패턴이 {tempo_pattern}하며, 전체적으로 {style}

이런 춤 동작에 어울리는 음악 스타일은 무엇인가요?
장르, 템포, 분위기, 트렌드에 맞춰 제안해주세요.
"""

# 13. 저장
with open("/Documents/pose_music/output/pose_summary.json", "w") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

with open("/Documents/pose_music/output/llm_prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)

print("요약 JSON, LLM 프롬프트 저장 완료")
