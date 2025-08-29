"""
이 모듈은 각 비디오 프레임을 색상 정보를 포함한 ASCII로 변환하여 개별 파일로 저장하는 클래스를 포함합니다.
"""

import os
import cv2

from video_to_ascii.render_strategy.ascii_strategy import DEFAULT_TERMINAL_SIZE
from . import ascii_color_strategy as color_strategy


class AsciiFrameSaverStrategy(color_strategy.AsciiColorStrategy):
    """각 프레임을 색상 정보를 포함한 ASCII로 변환하여 개별 파일로 저장"""

    def __init__(self, output_folder="frames_output"):
        """
        초기화

        Args:
            output_folder: 프레임들을 저장할 폴더명
        """
        super().__init__()
        self.output_folder = output_folder

    def render(self, cap, output=None, output_format=None, with_audio=False):
        """
        각 비디오 프레임을 ASCII로 변환하여 개별 파일로 저장

        Args:
            cap: OpenCV 비디오 캡처 객체
            output: 출력 폴더 경로 (지정되지 않으면 기본값 사용)
            output_format: 출력 형식 (무시됨)
            with_audio: 오디오 포함 여부 (무시됨)
        """

        # 출력 폴더 설정
        output_folder = output if output else self.output_folder
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"출력 폴더 생성: {output_folder}")

        # 비디오 정보 가져오기
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        print(f"총 {total_frames}개의 프레임을 처리합니다...")

        frame_count = 0

        # 각 프레임 처리
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            new_height = 50
            # new_height = int(frame.shape[0] * (new_width / frame.shape[1]))
            # print(frame.shape)

            new_width = new_height * frame.shape[1] / frame.shape[0] * 2
            # new_height = 45

            # 프레임 크기 조정 (터미널 크기에 맞춤)
            resized_frame = self.resize_frame(
                frame, (new_width, new_height)
            )  # 적당한 크기로 고정
       

            # ASCII로 변환 (색상 정보 포함)
            ascii_content = self.convert_frame_pixels_to_ascii(
                resized_frame, (new_width, new_height), new_line_chars=True
            )

            # 파일명 생성 (프레임 번호를 0으로 패딩)
            frame_filename = f"frame_{frame_count:06d}.txt"
            frame_path = os.path.join(output_folder, frame_filename)

            # 파일에 저장
            with open(frame_path, "w", encoding="utf-8") as f:
                f.write(ascii_content)

            frame_count += 1

            # 진행상황 출력
            if frame_count % 10 == 0 or frame_count == total_frames:
                progress = (frame_count / total_frames) * 100
                print(f"진행상황: {frame_count}/{total_frames} ({progress:.1f}%)")

        print(
            f"\n완료! {frame_count}개의 프레임이 '{output_folder}' 폴더에 저장되었습니다."
        )
