# 기본영상에 음악 입히기 

from moviepy.editor import VideoFileClip, AudioFileClip

# 경로 설정
video_path = "input.mp4"
audio_path = "/Documents/pose_music/output/generated_music.wav"
output_path = "final_output.mp4"

# 비디오와 오디오 로드
video = VideoFileClip(video_path)
audio = AudioFileClip(audio_path).set_duration(video.duration)

# 오디오를 비디오에 입히기
final_video = video.set_audio(audio)
final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

print(" 최종 영상 저장 완료:", output_path)
