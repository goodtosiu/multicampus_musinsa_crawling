from __future__ import annotations
import pendulum
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from videoDownloader import download_video_480p
from sceneDetecter import find_scenes

# 프로젝트 루트 상수
PROJECT_ROOT = "/opt/airflow"

# DAG 기본 설정
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
}

with DAG(
    dag_id="video_scene_detection_pipeline",
    default_args=default_args,
    description="A DAG to download a video and then detect scenes from it.",
    # schedule=None 으로 설정하면 수동으로만 실행됩니다.
    # 매일 자정에 실행하려면 'schedule="@daily"' 등으로 변경하세요.
    schedule=None,
    start_date=pendulum.datetime(2025, 9, 26, tz="Asia/Seoul"),
    # catchup=False 로 설정하면 DAG가 배포되기 전 누락된 스케줄을 실행하지 않습니다.
    catchup=False,
    tags=["video", "pipeline"],
) as dag:
    
    # 첫 번째 Task: downloader_video.py 실행
    # modules 폴더에 있는 파이썬 스크립트를 실행합니다.
    download_task = PythonOperator(
        task_id="download_task",
        python_callable=download_video_480p,
        op_kwargs={
            "PROJECT_ROOT": PROJECT_ROOT,
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", # URL 하드코딩            
        },
    )

    # 두 번째 Task: detecter_scene.py 실행
    detect_task = PythonOperator(
        task_id="detect_task",
        python_callable=find_scenes,
        op_kwargs={
            "PROJECT_ROOT": PROJECT_ROOT,
            "video_path": "{{ task_instance.xcom_pull(task_ids='download_task') }}",
            "threshold": 50,
        },
    )

    # Task 실행 순서 설정
    # download_task가 성공적으로 끝나면 detect_task를 실행합니다.
    download_task >> detect_task