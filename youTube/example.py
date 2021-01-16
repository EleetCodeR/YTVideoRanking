# importing vlc module 
import vlc 
  
# importing pafy module 
import pafy 
  
# url of the video 
url = "https://www.youtube.com/watch?v=SkcddD0LGlM"
  
# creating pafy object of the video 
video = pafy.new(url) 
  
# getting best stream 
best = video.getbest() 
  
print(video,type(best))
print(best,type(best))