#!/usr/bin/env python3
"""
비디오 프레임을 ASCII로 변환하여 저장하는 예제 스크립트
"""

import sys
import os

# 현재 스크립트의 디렉토리를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from video_to_ascii import player

def save_frames_example():
    """예제: 비디오 파일을 프레임별로 저장"""
    
    # 샘플 비디오 파일 경로
    video_file = "videos/soda.mp4"


    file_name = video_file.split("/")[-1].split(".")[0]
    output_folder = f"saved_frames/{file_name}"
    
    if not os.path.exists(video_file):
        print(f"비디오 파일을 찾을 수 없습니다: {video_file}")
        print("videos/ 폴더에 mp4 파일을 넣어주세요.")
        return
    
    print(f"비디오 파일: {video_file}")
    print(f"출력 폴더: {output_folder}")
    print("프레임 저장을 시작합니다...")
    
    # 프레임 저장 전략으로 실행
    player.play(
        filename=video_file,
        strategy="save-frames", 
        output=output_folder
    )

if __name__ == "__main__":
    save_frames_example()
