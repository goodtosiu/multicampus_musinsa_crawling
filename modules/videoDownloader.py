import os, yt_dlp

# downloader_video.py
def download_video_480p(PROJECT_ROOT: str, video_url: str) -> str:
    # 인증 정보
    cookies_path = f"{PROJECT_ROOT}/data/cookies/www.youtube.com_cookies.txt"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    
    # 출력 디렉토리가 없으면 생성
    output_dir = os.path.join(PROJECT_ROOT, "data", "video")
    os.makedirs(output_dir, exist_ok=True)
    
    # 저장될 파일의 전체 경로 템플릿 (확장자는 .mp4)
    video_id = video_url.split("v=")[1]
    output_template = os.path.join(output_dir, f'{video_id}.mp4')

    ydl_opts = {
        # 1. 파일명 및 경로 설정: 함수 인자를 사용하여 동적으로 경로 지정
        'outtmpl': output_template,

        # 2. 포맷 설정:
        'format': 'best[height<=480][ext=mp4]/best[height<=480]',

        # 함수 인자로 받은 쿠키와 User-Agent 사용
        'cookiefile': cookies_path,
        'user_agent': user_agent
    }


    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    print(f"저장된 경로: {output_template}")
    
    # Xcom에 반환
    return output_template

