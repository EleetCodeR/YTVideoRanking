from googleapiclient.discovery import build
import os

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
        part="statistics",
        id = vid         
    )

    response = request.execute()
    response = response['items']
    response = response[0]
    stats = response['statistics']
    stats = { 'viewcount':int(stats['viewCount']),'likes':int(stats['likeCount']),'dislikes':int(stats['dislikeCount']),'comments':int(stats['commentCount'])}

    comments = []

    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=vid
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

    getVideoMetaData("SkcddD0LGlM")

