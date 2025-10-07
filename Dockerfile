# 사용할 Airflow 기본 이미지 지정 (최신 버전으로 업데이트될 수 있습니다)
FROM apache/airflow:3.1.0

# requirements.txt 파일을 컨테이너의 /tmp/ 경로로 복사
COPY requirements.txt /tmp/requirements.txt

USER root


RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 ffmpeg


# pip을 사용하여 종속성 설치 (컨테이너 내 사용자: 'airflow')
# Airflow 이미지의 기본 사용자(airflow) 권한으로 설치해야 권한 문제가 발생하지 않습니다.
USER airflow
RUN pip install --no-cache-dir -r /tmp/requirements.txt