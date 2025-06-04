# 음악 생성 (K-pop 기반 스타일 분기 적용)

import json
from transformers import MusicgenForConditionalGeneration, MusicgenProcessor
import torchaudio
import torch

# 1. 사전 학습된 MusicGen-Medium 모델 불러오기
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-medium")
processor = MusicgenProcessor.from_pretrained("facebook/musicgen-medium")

# 2. 요약 정보 JSON 로딩
summary_path = "/Documents/pose_music/output/pose_summary.json"
with open(summary_path, "r", encoding="utf-8") as f:
    summary = json.load(f)

# 3. 프롬프트 생성 함수 (K-pop 베이스 + 자동 분기)
def generate_kpop_prompt(summary):
    motion_density = summary.get("motion_density", "")
    style_raw = summary.get("style", "").lower()
    tempo_pattern = summary.get("tempo_pattern", "")
    bpm = summary.get("bpm", 110)

    base = "Modern K-pop dance track"

    if any(keyword in style_raw for keyword in ["powerful", "jumping"]) or motion_density == "high":
        mood = "with strong hip-hop influence, deep bass, aggressive beats, and intense rhythm"
        ref = "Inspired by BTS and Stray Kids"
    elif any(keyword in style_raw for keyword in ["graceful", "fluid", "slow"]) or motion_density == "low":
        mood = "with soft vocals, ambient synths, and emotional melodies"
        ref = "Inspired by Jennie - SOLO and Taeyeon"
    else:
        mood = "with catchy melodies, bright synths, and danceable pop rhythm"
        ref = "Inspired by 2NE1 and TWICE"

    tempo = f"{tempo_pattern} tempo, around {bpm} BPM"

    return f"{base} {mood}. Features {tempo}. {ref}."

# 4. 프롬프트 생성
prompt = generate_kpop_prompt(summary)
print("생성된 프롬프트:", prompt)

# 5. MusicGen 입력 처리
inputs = processor(text=[prompt], return_tensors="pt")

# 6. 음악 생성
print("음악 생성 중...")
with torch.no_grad():
    audio_values = model.generate(**inputs, max_new_tokens=1500)

# 7. 저장 (wav)
output_path = "/Documents/pose_music/output/generated_music.wav"
torchaudio.save(output_path, audio_values[0], 32000, format="wav")
print(f"음악 생성 완료: {output_path}")
