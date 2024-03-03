from googleapiclient.discovery import build
import os
from dateutil import parser
from dateutil import relativedelta
from datetime import datetime

def getVideolist(query):
    api_service_name = "youtube"
    api_version = "v3"
    api_key = os.environ.get('YOUTUBE_API')
    youtube = build(api_service_name,api_version,developerKey=api_key)
    request = youtube.search().list(
            part="snippet",
            maxResults=10,# mention number of result we want to fetch.
            q=query,
            type='video'
        )

    response = request.execute()
    print(response) 

def getComments(vid):
    api_service_name = "youtube"
    api_version = "v3"
    api_key = os.environ.get('YOUTUBE_API')# get the API_KEY stored on pc.
    youtube = build(api_service_name,api_version,developerKey=api_key)
    
    comments = []
    try:
        request = youtube.commentThreads().list(
        part="snippet",
        videoId=vid,
        maxResults = 100) #  Data API can send max 100 comments    
        response = request.execute()
    except :
        comments = None
        return comments
        
    for item in response['items']:
        item = item['snippet']
        item = item['topLevelComment']
        item = item['snippet']
        text = item['textOriginal']
        comments.append(text)
    return comments

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


    # print(f"publish date : {publishDateTime} \n")
    # print(f"period : {period} \n")

    stats = response['statistics']

    if 'commentCount' in stats:
        stats = { 'age':period,'viewcount':int(stats['viewCount']),'likes':int(stats['likeCount']),'dislikes':int(stats['dislikeCount']),'comments':int(stats['commentCount'])}
    else:
        stats = { 'age':period,'viewcount':int(stats['viewCount']),'likes':int(stats['likeCount']),'dislikes':int(stats['dislikeCount']),'comments': 0}


    comments = []

    try:
        request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=vid,
        maxResults = 100) #  Data API can send max 100 comments    
        response = request.execute()
    except :
        comments = None
        return (stats,comments)
        
    for item in response['items']:
        item = item['snippet']
        item = item['topLevelComment']
        item = item['snippet']
        text = item['textOriginal']
        comments.append(text)


    return (stats,comments)
  




if __name__ == "__main__":

    vid ="L6anmd7DnYw"
    # Female Reproductive System slides
    # HH_2yge9uYY
    # SkcddD0LGlM
    # toKp0SGyv5w
    
    # geography solar system
    # EytrFc9qIOo  Stats : {'age': 3, 'viewcount': 2112795, 'likes': 41378, 'dislikes': 2067, 'comments': 1372}  
    # PxGJ0eDYYkM  Stats : {'age': 1, 'viewcount': 42045, 'likes': 1852, 'dislikes': 75, 'comments': 57}
    # libKVRa01L8 Stats : {'age': 3, 'viewcount': 16549830, 'likes': 106886, 'dislikes': 6292, 'comments': 5044}
    # frUMSrnFTNY  Stats : {'age': 1, 'viewcount': 82484, 'likes': 2159, 'dislikes': 101, 'comments': 190}

    # animal kingdom vertebrates and invertebrates
    # mRidGna-V4E
    # mQnRYL8zATs
    # S7oXYEUyAug
    # KjpGfqqvQ3E
    # R50Xc1EUHwg
    # L6anmd7DnYw

    # response  = getVideoMetaData("frUMSrnFTNY")
    
    response  = getComments(vid)
 
    print(f" ========================== VID - {vid} ========================== \n")

    for comment in response:
        print(comment,'\n')

    print(f" ========================== END ==========================")
