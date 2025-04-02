from googleapiclient.discovery import build
import isodate

API_KEY = 'AIzaSyDJcYOr6DfoB8cWtqu3kjMExFKi9GbL_kg'  # 여기에 본인의 API 키 입력
REGION_CODE = 'KR'
MAX_RESULTS = 50

# 카테고리 ID → 카테고리 이름 매핑
CATEGORY_MAP = {
    '1': 'Film & Animation',
    '2': 'Autos & Vehicles',
    '10': 'Music',
    '15': 'Pets & Animals',
    '17': 'Sports',
    '20': 'Gaming',
    '22': 'People & Blogs',
    '23': 'Comedy',
    '24': 'Entertainment',
    '25': 'News & Politics',
    '26': 'Howto & Style',
    '28': 'Science & Technology'
}

youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_top_videos_by_category(category_id):
    request = youtube.videos().list(
        part='snippet,statistics,contentDetails',
        chart='mostPopular',
        regionCode=REGION_CODE,
        videoCategoryId=category_id,
        maxResults=MAX_RESULTS
    )
    response = request.execute()

    videos = []
    for item in response['items']:
        duration = isodate.parse_duration(item['contentDetails']['duration']).total_seconds()
        if duration > 3600:
            continue  # 1시간 이상은 제외
        videos.append({
            'title': item['snippet']['title'],
            'videoId': item['id'],
            'channelTitle': item['snippet']['channelTitle'],
            'viewCount': int(item['statistics'].get('viewCount', 0)),
            'duration': duration,
            'isShorts': duration <= 60
        })
    return videos

# 전체 카테고리에 대해 반복
all_results = {}
all_links = []
shorts_links = []

for category_id, category_name in CATEGORY_MAP.items():
    try:
        top_videos = get_top_videos_by_category(category_id)
        all_results[category_name] = top_videos
        for video in top_videos:
            link = f"https://www.youtube.com/watch?v={video['videoId']}"
            if video['isShorts']:
                shorts_links.append(link)
            else:
                all_links.append(link)
        print(f"[{category_name}] Top videos loaded.")
    except Exception as e:
        print(f"[{category_name}] Error: {e}")

# 예시 출력 (카테고리당 상위 3개 영상만)
for category, videos in all_results.items():
    print(f"\n {category}")
    for video in videos[:3]:
        print(f"- {video['title']} ({video['viewCount']} views)")

# 일반 영상 링크 저장
with open("youtube_top_links.txt", "w", encoding="utf-8") as f:
    for link in all_links:
        f.write(link + "\n")

# 쇼츠 영상 링크 저장
with open("youtube_shorts_links.txt", "w", encoding="utf-8") as f:
    for link in shorts_links:
        f.write(link + "\n")

print("\n 영상 링크가 저장되었습니다:")
print("- 일반 영상: youtube_top_links.txt")
print("- 쇼츠 영상: youtube_shorts_links.txt")