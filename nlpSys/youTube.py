from googleapiclient.discovery import build
import os
from dateutil import parser
from dateutil import relativedelta
from datetime import datetime

def getVideolist(query):
    api_service_name = "youtube"
    api_version = "v3"
    api_key = os.environ.get('YOUTUBE_API')# get the API_KEY stored on pc.
    youtube = build(api_service_name,api_version,developerKey=api_key)
    request = youtube.search().list(
            part="snippet",
            maxResults=10,# mention number of result we want to fetch.
            q=query,
            type='video'
        )

    response = request.execute()
    print(response) 

def getVideoMetaData(vid):
    print("  [INFO] : Fetching Video metadata from Youtube...")
    api_service_name = "youtube"
    api_version = "v3"
    api_key = os.environ.get('YOUTUBE_API')# get the API_KEY stored on pc.
    youtube = build(api_service_name,api_version,developerKey=api_key)

    request = youtube.videos().list(
        part="snippet,statistics",
        id = vid         
    )

    response = request.execute()

    # print("  [DEBUG] : Video Info API-")
    # print(f"{response} \n")

    response = response['items']
    response = response[0]

    snippet = response['snippet']
    publishDateTime = parser.isoparse(snippet['publishedAt'])
    today =  datetime.now()
    period = today.year - publishDateTime.year - ((today.month, today.day) < (publishDateTime.month, publishDateTime.day))
    period = period if period else 1

    # print(f"publish date : {publishDateTime} \n")
    # print(f"period : {period} \n")

    stats = response['statistics']
    stats = { 'publishedAt':period,'viewcount':int(stats['viewCount']),'likes':int(stats['likeCount']),'dislikes':int(stats['dislikeCount']),'comments':int(stats['commentCount'])}

    comments = []

    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=vid,
        maxResults = 100 #  Data API can send max 100 comments
    )
    response = request.execute()
    for item in response['items']:
        item = item['snippet']
        item = item['topLevelComment']
        item = item['snippet']
        text = item['textOriginal']
        comments.append(text)


    return (stats,comments)
  




if __name__ == "__main__":
    response  = getVideoMetaData("EytrFc9qIOo")
    print(f" comments : {response[1]}")
    print(f" length : {len(response[1])}")

