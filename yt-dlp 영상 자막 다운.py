import subprocess
import os

# txt 파일에서 링크들을 읽어서 리스트에 순서대로 저장하는 코드

file_path = r"C:\Users\user\Desktop\집가는 코드\잡것들\자율연구\유툽 링크들1.txt"

# 파일을 읽어서 링크를 리스트로 저장
with open(file_path, "r", encoding="utf-8") as file:
    links = [line.strip() for line in file if line.strip()]


# 1. 출력 디렉토리 지정 (Windows 경로, raw string 사용)
output_dir = r"C:\Users\user\Desktop\집가는 코드\잡것들\자율연구\날유툽자막"

# 2. 출력 디렉토리가 없으면 생성
os.makedirs(output_dir, exist_ok=True)

# 3. 출력 파일 템플릿 지정 (영상 제목을 기반으로 파일 이름 생성)
output_template = os.path.join(output_dir, "%(title)s.ko.vtt")

# 4. yt-dlp를 이용해 자동생성 자막 다운로드 (영상 파일은 다운로드하지 않음)
for link in links:
    subprocess.run([
        "yt-dlp", 
        "--skip-download", 
        "--write-auto-subs", 
        "--sub-lang", "ko", 
        "-o", output_template, 
        link
    ])