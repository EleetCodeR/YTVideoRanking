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

if __name__ == "__main__":
    getVideolist('avengers')

