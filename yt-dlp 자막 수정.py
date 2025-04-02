import os
import re

# 파일 경로들을 가져올 폴더 경로 지정
folder_path = r"C:\Users\user\Desktop\집가는 코드\잡것들\자율연구\날유툽자막"

# 저장할 폴더 지정
output_folder = r"C:\Users\user\Desktop\집가는 코드\잡것들\자율연구\정리유툽자막"
os.makedirs(output_folder, exist_ok=True)

# 폴더 내 모든 파일의 전체 경로를 리스트로 저장
paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) 
              if os.path.isfile(os.path.join(folder_path, f))]

for path in paths:

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 타임스탬프(예: 00:00:00.160)나 빈 줄 제거, 그리고 HTML 태그 제거
        timestamp_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}\.\d{3}")
        cleaned_lines = []

        for line in lines:
            line = line.strip()
            # 타임스탬프 라인이나 빈 줄은 건너뜁니다.
            if timestamp_pattern.match(line) or not line:
                continue
            # HTML-like 태그 제거 (예: <c> ... </c> 등의 태그)
            line = re.sub(r"<[^>]+>", "", line)
            cleaned_lines.append(line)

        # 중복된 라인을 제거 (순서를 유지)
        seen = set()
        unique_lines = []
        for cline in cleaned_lines:
            if cline not in seen:
                unique_lines.append(cline)
                seen.add(cline)

        cleaned_subtitle = "\n".join(unique_lines)
        # 출력 파일의 이름을 원본 파일의 이름 기반으로 생성
        output_filename = os.path.splitext(os.path.basename(path))[0] + ".txt"
        output_path = os.path.join(output_folder, output_filename)

        # 정리된 자막 내용을 txt 파일로 저장
        with open(output_path, "w", encoding="utf-8") as outfile:
            outfile.write(cleaned_subtitle)
    else:
        print("자막 파일을 찾을 수 없습니다:", path)