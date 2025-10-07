import os, datetime, whisper

def format_time(seconds: float) -> str:
    """초를 HH:MM:SS,ms 형식의 SRT 타임스탬프로 변환합니다."""
    td = datetime.timedelta(seconds=seconds)
    # timedelta를 문자열로 변환 (HH:MM:SS.ffffff)
    time_str = str(td)

    # 마이크로초(ffffff) 부분을 밀리초(ms)로 맞추고 SRT 형식으로 변환
    try:
        # '.'가 있는 경우 (1초 이상)
        h_m_s, ms = time_str.split('.')
        ms = ms[:3]  # 밀리초는 3자리까지
    except ValueError:
        # '.'가 없는 경우 (정확히 초 단위로 떨어짐)
        h_m_s = time_str
        ms = '000'

    # 가끔 h_m_s가 7:00:00처럼 한 자리 수 시간으로 나올 때 07:00:00로 패딩
    parts = h_m_s.split(':')
    if len(parts[0]) == 1:
        h_m_s = f'0{h_m_s}'

    return f"{h_m_s},{ms}"


def generate_subtitle(video_path: str, output_path: str):
    """Whisper를 사용하여 표준 SRT 자막 파일을 생성합니다."""
    model = whisper.load_model("large")  # medium, large 등으로 변경 가능

    print("음성 인식을 시작합니다... (시간이 걸릴 수 있습니다)")
    result = model.transcribe(
        video_path,
        language="ko",
        temperature=0,
        beam_size=3,
        best_of=3
    )
    print("음성 인식이 완료되었습니다. SRT 파일을 생성합니다.")

    # 디렉토리가 존재하지 않으면 생성
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_path, "w", encoding='utf-8') as f:
        for i, segment in enumerate(result["segments"], start=1):
            # 1. 순번
            f.write(f"{i}\n")

            # 2. 시간 (포맷 변환)
            start_time = format_time(segment['start'])
            end_time = format_time(segment['end'])
            f.write(f"{start_time} --> {end_time}\n")

            # 3. 텍스트 (앞뒤 공백 제거)
            f.write(segment["text"].strip() + "\n\n")

    print(f"자막 파일이 '{output_path}' 경로에 저장되었습니다.")