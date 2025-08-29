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
    """예제: 모든 비디오 파일을 여러 해상도로 프레임 저장"""
    
    # videos 폴더의 모든 mp4 파일 찾기
    videos_folder = "videos"
    video_files = []
    
    if os.path.exists(videos_folder):
        for file in os.listdir(videos_folder):
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                video_files.append(os.path.join(videos_folder, file))
    
    if not video_files:
        print(f"'{videos_folder}' 폴더에서 비디오 파일을 찾을 수 없습니다.")
        print("videos/ 폴더에 mp4 파일을 넣어주세요.")
        return
    
    print(f"발견된 비디오 파일: {len(video_files)}개")
    for video_file in video_files:
        print(f"  - {video_file}")
    print()
    
    # 각 비디오 파일에 대해 처리
    for video_file in video_files:
        file_name = os.path.basename(video_file).split(".")[0]
        output_folder = f"saved_frames/{file_name}"
        
        print(f"=== {file_name} 처리 시작 ===")
        print(f"비디오 파일: {video_file}")
        print(f"출력 폴더: {output_folder}")
        print("여러 해상도로 프레임 저장을 시작합니다...")
        
        # 프레임 저장 전략으로 실행 (모든 해상도: 30, 50, 75, 100)
        player.play(
            filename=video_file,
            strategy="save-frames", 
            output=output_folder
        )
        
        print(f"=== {file_name} 처리 완료 ===\n")

if __name__ == "__main__":
    save_frames_example()
