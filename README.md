#  Pose-to-Music: 춤에서 음악을 만드는 AI 프로젝트

춤 영상을 입력하면, AI가 **관절(Pose)을 분석**하고 **움직임에 어울리는 음악**을 직접 생성합니다.  
K-pop 스타일을 기반으로, 관절 움직임과 템포를 분석하여 **춤에 맞는 음악 스타일을 자동 생성**하는 프로젝트입니다.

---

##  프로젝트 개요

춤 영상 → 관절(Pose) 추출 → 움직임 분석 → 스타일 예측 → 음악 생성 → 영상 + 음악 합성


> 음악은 Meta의 [MusicGen](https://huggingface.co/facebook/musicgen-medium) 모델을 사용해 텍스트 기반으로 생성됩니다.

---

## 동기 및 특징

- **동기**: 기존에는 댄서들이 정해진 음악에 맞춰 춤을 췄다면, 이 프로젝트는 그 반대로, 춤에 맞는 음악을 AI가 생성함으로써 댄서 고유의 움직임과 개성을 살릴 수 있도록 돕는 데에 목적이 있습니다.
- **이 프로젝트**는:  
  → 춤 동작을 자동 해석하고  
  → AI가 음악을 생성하는 파이프라인 제공

---

##  실행 순서

```bash
# 1단계: 포즈 추출
python pose.py

# 2단계: 움직임 분석
python analyze_pose.py

# 3단계: 요약 정보 정리
python pose_llm_prompt.py

# 4단계: 음악 생성 (K-pop 기반 스타일 자동 분기)
python generate_music.py

# 5단계: 음악 반복/루프 처리 (영상 길이에 맞춤)
python music_loop.py

# 6단계: 영상 + 음악 합성
python music_video.py

---
##  필수 패키지 설치 
pip install mediapipe opencv-python pandas moviepy torchaudio transformers
pip install moviepy

---
## 핵심 기술요소

-MediaPipe: 관절 추출 (33개 keypoint)
-움직임 분석: 이동량, BPM, 패턴 등으로 특징 분석
-스타일 분류: 아래 조건으로 자동 분기

def estimate_style(bpm, motion_density, tempo_pattern):
    if bpm > 140 or motion_density == "high":
        return "powerful, jumping"
    elif tempo_pattern == "variable" and motion_density == "moderate":
        return "dynamic, energetic"
    else:
        return "fluid, slow"

프롬프트 자동화: style 기반으로 K-pop 느낌의 프롬프트 생성
MusicGen: 요약된 텍스트로 음악 생성 (Medium 이상 권장) (small 성능 bad)

---

문제 및 개선
-문제 발생
격렬한 춤인데 "fluid, slow"로 분류되는 사례
-개선
BPM과 패턴을 함께 고려하는 estimate_style() 함수 도입
motion_density만 보던 기존 방식 보완

---

파일명	설명
pose_output.json	프레임별 관절 위치 좌표
pose_summary.json	BPM, 스타일 등 요약 정보
llm_prompt.txt	LLM 입력용 텍스트 프롬프트
generated_music.wav	생성된 음악
pose_output_video.mp4	관절 시각화된 출력 영상
final_output.mp4	음악과 영상이 합쳐진 결과물

---

확장 아이디어
음악 장르 확장 (EDM, Jazz 등)
댄서별 맞춤형 스타일 학습

---

제작자
GitHub: hongseok729
Repository: dance_music

출처
https://www.instagram.com/ssxnng_xo?igsh=eHpvbm1mcmwzaTk5  (친구 동생 영상 지원)
  
