import json

def analyze_pose_data(pose_data):
    total_frames = len(pose_data)
    joint_activity = {}
    prev_landmarks = None

    for frame in pose_data:
        landmarks = frame["landmarks"]
        if prev_landmarks:
            for i, lm in enumerate(landmarks):
                dx = lm["x"] - prev_landmarks[i]["x"]
                dy = lm["y"] - prev_landmarks[i]["y"]
                dz = lm["z"] - prev_landmarks[i]["z"]
                dist = (dx**2 + dy**2 + dz**2)**0.5
                joint_activity[i] = joint_activity.get(i, 0) + dist
        prev_landmarks = landmarks

    sorted_joints = sorted(joint_activity.items(), key=lambda x: x[1], reverse=True)
    dominant_joints = [i for i, _ in sorted_joints[:3]]

    avg_motion = sum(joint_activity.values()) / total_frames
    motion_density = "high" if avg_motion > 0.05 else "moderate" if avg_motion > 0.02 else "low"
    tempo_pattern = "irregular" if avg_motion > 0.05 else "steady"
    style = "powerful" if motion_density == "high" else "graceful" if motion_density == "low" else "dynamic"

    return {
        "dominant_joints": dominant_joints,
        "motion_density": motion_density,
        "tempo_pattern": tempo_pattern,
        "style": style
    }

if __name__ == "__main__":
    json_path = "/Document/pose_music/output/pose_output.json"
    with open(json_path, "r", encoding="utf-8") as f:
        pose_data = json.load(f)

    summary = analyze_pose_data(pose_data)

    out_path = "/Documents/pose_music/output/pose_summary.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"분석 완료: {out_path}")
