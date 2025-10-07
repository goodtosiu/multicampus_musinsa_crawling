# media_downloader.py
import os
import yt_dlp

# --- 1단계: 영상과 음성을 함께 다운로드하는 함수 ---
def download_video_with_audio(PROJECT_ROOT: str, video_url: str) -> str:
  
    # 인증 정보
    cookies_path = os.path.join(PROJECT_ROOT, "data", "cookies", "www.youtube.com_cookies.txt")
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    
    # 출력 디렉토리 생성
    output_dir = os.path.join(PROJECT_ROOT, "data", "video")
    os.makedirs(output_dir, exist_ok=True)
    
    # 저장될 파일의 전체 경로 템플릿
    video_id = video_url.split("v=")[-1]
    output_template = os.path.join(output_dir, f'{video_id}.%(ext)s')

    ydl_opts = {
        # 1. 파일명 및 경로 설정
        'outtmpl': output_template,

        # 2. 포맷 설정: 480p 이하 비디오 + 가장 좋은 음질의 오디오를 합침
        # bestvideo[height<=480][ext=mp4] : 480p 이하의 mp4 영상 중 최상의 화질
        # bestaudio[ext=m4a] : m4a 오디오 중 최상의 음질
        # /best[height<=480] : 위 조합이 불가능할 경우 480p 이하의 영상/음성 통합본 중 최상의 것
        'format': 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]',
        
        # 3. 다운로드 후 비디오 포맷을 mp4로 통일
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],

        # 4. 인증 정보
        'cookiefile': cookies_path,
        'user_agent': user_agent
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        # 실제 저장된 파일 경로를 가져옴
        downloaded_path = ydl.prepare_filename(info_dict)

    print(f"영상 저장 경로: {downloaded_path}")
    
    # XCom으로 파일 경로 반환
    return downloaded_path

