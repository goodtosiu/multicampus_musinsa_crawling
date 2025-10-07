import os
import yt_dlp
def extract_audio_from_video(PROJECT_ROOT: str, video_path: str) -> str:
    """
    로컬에 저장된 비디오 파일에서 음성(.mp3)을 추출합니다.
    이 함수는 네트워크를 사용하지 않고 로컬에서 빠르게 실행됩니다.

    :param PROJECT_ROOT: 프로젝트 루트 디렉토리 경로
    :param video_path: 음성을 추출할 원본 비디오 파일의 경로 (XCom으로 전달받음)
    :return: 저장된 오디오 파일의 전체 경로
    """
    # 음성 저장 디렉토리 생성
    audio_output_dir = os.path.join(PROJECT_ROOT, "data", "audio")
    os.makedirs(audio_output_dir, exist_ok=True)

    # 저장될 오디오 파일 경로 설정 (확장자만 변경)
    base_filename = os.path.basename(video_path)
    filename_without_ext = os.path.splitext(base_filename)[0]
    audio_output_template = os.path.join(audio_output_dir, f'{filename_without_ext}.%(ext)s')

    ydl_opts = {
        # 로컬 파일에 작업을 적용하므로 다운로드는 하지 않음
        'verbose': True,
        #'skip_download': True,
        'outtmpl': audio_output_template,
        'enable_file_urls': True,
        #'force_postprocessors': True,
        # 후처리(Post-processing) 옵션을 사용하여 음성 추출
        'postprocessors': [{
            'key': 'FFmpegExtractAudio', # 음성 추출 기능
            'preferredcodec': 'mp3',      # mp3 포맷으로 지정
            'preferredquality': '192',    # 음질 (192kbps)
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # 다운로드가 아닌, 로컬 파일에 후처리 작업을 적용하기 위해 경로를 전달
        processing_path = f"file://{video_path}"
        ydl.download([processing_path])
        
        # 실제 생성된 파일 경로 생성
        # 위 outtmpl에서 %(ext)s 부분이 'mp3'로 변환됨
        final_audio_path = os.path.join(audio_output_dir, f'{filename_without_ext}.mp3')


    print(f"음성 추출 경로: {final_audio_path}")

    # XCom으로 파일 경로 반환
    return final_audio_path