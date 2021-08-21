# from textPreprocessing import textPreprocess
from text_recognition import textRecog
from textPreprocessing import textPreprocess
from similarityScore import calcSimilarityScore
from youTube import getVideoMetaData
from polarityScore import getPolarityScore
import pafy 
import time




def irfSys(vid,query,corpus): 
    print('\n')
    print("  [INFO] : IRF-System Initialized...")
    start_time = time.time()

    # Text Processing
    print("  [INFO] : ============================= Query-Text-preprocessing ===========================")
    query = textPreprocess(query)
    print("  [INFO] : ============================= Corpus-Text-preprocessing ==========================")
    corpus = textPreprocess(corpus)

    # SimilarityScore
    print("  [INFO] : ============================= Similarity score calculation =======================")
    similarity = calcSimilarityScore(query,corpus)

    # PolarityScore
    print("  [INFO] : ============================= Polarity score calculation =========================")
    metaData = getVideoMetaData(vid)
    stats = metaData[0]
    comments = metaData[1]
    polarity = 0
    # pass comments for polarity score
    if(comments):
        polarity = getPolarityScore(comments)
    else:
        print("  [INFO] : ------> Comments Turned Off!")    

    # Index Calculation
    print("  [INFO] : ============================= Index calculation stage ============================")       
    viewCount = stats['viewcount']
    likes = stats['likes']
    dislikes = stats['dislikes']
    totalComments = stats['comments']
    age = stats['age']
    years = age if age else 1

    index = (likes/viewCount)-(dislikes/viewCount)+similarity+polarity


    elapsed_time = time.time() - start_time
    elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
   
    print(f"  [INFO] : Exiting IRF system ! \n  [INFO] : Elapsed Time -{elapsed_time}")
    print("  [INFO] : ============== Video Info ==============") 
    print(f"  [INFO] : Published - {age} years ago ")
    print(f"  [INFO] : views - {viewCount} , likes - {likes} , dislikes- {dislikes} , total comments - {totalComments} ")
    print(f"  [INFO] : likes-views ratio : {likes/viewCount} ,  dislikes-views ratio : {dislikes/viewCount}, views-years ratio : {viewCount/years} ")
    print(f"  [INFO] : Similarity score - {similarity} , Polarity score - {polarity} ")
    print(f"  [INFO] : Index :  {index} ")
    return index


def getIndex(searchQuery,vid,vidCount):
    folderPath = 'C:/Users/Vishal Ramane/Documents/GitHub/MTProject/nlpSys/frames'     
    # Female Reproductive sys vids : SkcddD0LGlM , L-cXrt8RWek      
    # Access Math vids : AsDfluoYB4Q , 7D8-R-4Cdfg&t=237s    
    # url of the video 
    url = F"https://www.youtube.com/watch?v={vid}"  
    # creating pafy object of the video 
    video = pafy.new(url)  
    # getting best stream 
    best = video.getbest() 
    # best.download()          
   
    corpus = textRecog(best.url,folderPath,vidCount)  

    index = irfSys(vid,searchQuery,corpus)

    return index


def start():
    print('\n')
    print("  [INFO] : ****************************** Start ******************************")
    start_time = time.time()

    searchQuery = "animal kingdom vertebrates and invertebrates"

    videoList = ['mRidGna-V4E', 'mQnRYL8zATs', 'S7oXYEUyAug','KjpGfqqvQ3E','R50Xc1EUHwg','L6anmd7DnYw']

    videoCount = 0
    ranking = {}

    for vid in videoList :
        videoCount += 1
        index = getIndex(searchQuery,vid,videoCount)
        ranking[vid] = index

    ranking = dict(sorted(ranking.items(),key=lambda item:item[1],reverse=True))

    elapsed_time = time.time() - start_time
    elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

    
    print('\n')
    print("  [INFO] : ============================= Old Ranking ===========================")
    print(videoList)

    print('\n')
    print("  [INFO] : ============================= New Ranking ===========================")
    print(ranking)

    print('\n')
    print("  [INFO] : ****************************** END ******************************")
    print(f"  [INFO] : Total Elapsed Time - {elapsed_time}")


if __name__ == '__main__':
    start()
    
    # Female Reproductive System slides
    # HH_2yge9uYY
    # SkcddD0LGlM
    # toKp0SGyv5w

    # geography, The solar system, sun, mars, mercury
    # EytrFc9qIOo
    # PxGJ0eDYYkM
    # libKVRa01L8
    # frUMSrnFTNY
    # videoList = ['EytrFc9qIOo', 'PxGJ0eDYYkM', 'libKVRa01L8','frUMSrnFTNY']

    # animal kingdom vertebrates and invertebrates
    # mRidGna-V4E
    # mQnRYL8zATs
    # S7oXYEUyAug
    # KjpGfqqvQ3E
    # R50Xc1EUHwg
    # L6anmd7DnYw
    
    # url = "https://www.youtube.com/watch?v=SkcddD0LGlM"