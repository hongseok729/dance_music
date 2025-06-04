import torchaudio
from moviepy.editor import VideoFileClip
import torch

# 영상 파일 경로
video_path = "input"

# 영상 길이 자동 추출
clip = VideoFileClip(video_path)
video_duration_sec = clip.duration  # 초 단위 float 값
clip.close()

print(f"영상 길이: {video_duration_sec:.2f}초")

# 생성된 음악 불러오기
music_path = "/Documents/pose_music/output/generated_music.wav"
waveform, sample_rate = torchaudio.load(music_path)

# 음악 길이 계산
audio_duration_sec = waveform.shape[1] / sample_rate

# 필요한 반복 횟수 계산
repeat_count = int(video_duration_sec / audio_duration_sec) + 1

# 오디오 반복 및 자르기
looped_waveform = waveform.repeat(1, repeat_count)
final_sample_count = int(video_duration_sec * sample_rate)
looped_waveform = looped_waveform[:, :final_sample_count]

# 저장
output_looped_path = "/Documents/pose_music/output/looped_music.wav"
torchaudio.save(output_looped_path, looped_waveform, sample_rate)
print(f"영상 길이에 맞춘 음악 저장 완료: {output_looped_path}")
