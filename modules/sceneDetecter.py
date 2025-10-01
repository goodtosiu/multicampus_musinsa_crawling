import os, yt_dlp, subprocess, scenedetect, pickle, json
from pathlib import Path
from datetime import datetime, timedelta
from scenedetect.detectors import ContentDetector

#  동영상 파일에서 장면을 감지하고, 시작과 끝 타임코드 목록을 반환합니다.
#     Args:
#         video_path (str): 동영상 파일 경로.
#         threshold (float): 감지기의 민감도. 값이 높을수록 더 큰 변화가 있는
#                            장면만 감지되어 장면 수가 줄어듭니다.

#     Returns:
#         list: 각 장면의 (시작 타임코드, 끝 타임코드)를 담은 튜플의 리스트.
#               예: [('00:00:00.000', '00:00:15.250')]

def find_scenes(PROJECT_ROOT: str, video_path, threshold=30.0):
    """
    동영상 파일에서 장면을 감지하고, 시작과 끝 타임코드 목록을 반환합니다.
    (기존과 동일)
    """
    video = None
    formatted_scenes = [] # 함수가 성공적으로 종료될 때 반환할 변수
    try:
        # 1. 비디오 열기 (중략)
        video = scenedetect.open_video(video_path)
        
        # print(video_path)
        print(f"현재 사용 중인 비디오 객체 타입: {type(video)}")
        print("---------- 비디오 파일 정보 확인 ----------")
        print(f"해상도: {video.frame_size}, 총 길이: {video.duration}, FPS: {video.frame_rate:.2f}")

        # 2. 비디오 길이 체크
        DURATION = video.duration.get_seconds()
        
        #------로그------#
        first_frame = video.read()
        if first_frame is False:
            raise ValueError("첫 프레임 읽기 실패! 비디오 파일 손상 또는 코덱 문제를 확인하세요.")
        print("✅ 첫 프레임 읽기 성공! 비디오 파일은 정상입니다.")
        video.seek(0)
        #-----------------#

        # 3. 샷 탐지 (중략)
        scene_manager = scenedetect.SceneManager()
        scene_manager.add_detector(ContentDetector(threshold=threshold))
        scene_manager.detect_scenes(video=video)
        
        scene_list = scene_manager.get_scene_list()

        if not scene_list:
            print("감지된 챕터가 없습니다.")

        else:
             #------로그------#
            for i, scene in enumerate(scene_list):
                start, end = scene
                print(f"  장면 {i+1}: 시작 {start.get_timecode()} / 종료 {end.get_timecode()}")
                formatted_scenes.append((start.get_timecode(), end.get_timecode()))
            #-----------------#

            # 디렉토리 경로
            SHOT_LIST_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "shot_list")
            VIDEO_ID = Path(video_path).stem

            # 경로 만들기
            os.makedirs(SHOT_LIST_OUTPUT_DIR, exist_ok=True)
            output_filename = f"{VIDEO_ID}.pkl"
            output_filepath = os.path.join(SHOT_LIST_OUTPUT_DIR, output_filename)

            # --- 파일로 저장하기 ---
            with open(output_filepath, 'wb') as f: # 바이너리 쓰기 모드 'wb'
                pickle.dump(formatted_scenes, f)
            print("파일 저장이 완료되었습니다.")

    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return []

    finally:
        if video is not None:
            try:
                video.release()  # 안전하게 리소스 해제
                print("🔒 비디오 파일 닫기 완료.")
            except Exception:
                print("⚠️ 비디오 파일 닫기 중 문제가 발생했습니다.")

# 함수 호출 및 후처리 로직은 DAG의 다음 Task나, 현재 Task가 반환하는 XCom 값을 활용하여 수행해야 합니다.
# 이 함수는 오직 장면 목록(formatted_scenes)만 반환해야 합니다.
