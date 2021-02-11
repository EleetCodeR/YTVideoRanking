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
    # pass comments for polarity score
    polarity = getPolarityScore(metaData[1])

    # Index Calculation
    print("  [INFO] : ============================= Index calculation stage ============================")       
    viewCount = stats['viewcount']
    likes = stats['likes']
    dislikes = stats['dislikes']

    index = (likes/viewCount)-(dislikes/viewCount)+similarity+polarity


    elapsed_time = time.time() - start_time
    elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    print(f"  [INFO] : Exiting IRF system ! \n  [INFO] : Elapsed Time -{elapsed_time}")
    print(f"  [INFO] : Index :  {index} ")
    return index


def getIndex(searchQuery,vid,vidCount):
    folderPath = 'C:/Users/vrama/Documents/GitHub/MTProject/nlpSys/frames'     
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
    # corpus = ['Female Reproductive System','SAP5(a)','Explain how the','function of the reproductive','regulated by hormonal','organs','are','interactions','Functions','Reproduction','Production of eggs','Through ovulation','Discharge of mature egg','Production of female sex hormones','Structures','Ovaries','female','gonad; produces eggs','and sex hormones','Follicles','structure in','gral','aorirnni','ovary that makes the','egg and progesterone','developing','Oocyte','uterus','fallopian','egg','IuuE=','_1_7}161','female sex cell','Egg','vagina','Structures','Uterine tubes','conducts egg towards','uterus; AKA','female organ','Uterus','a=48','where the fetus','develops','4=tr','Vagina','female','copulatory organ and','birth canal','Estrogen','Secreted by ovaries','Main female sex hormone','Estrogen at puberty stimulates','the','growth','of the uterus and the vagina','Egg maturation','Sexual characteristics','Menstruation']
   
    index = irfSys(vid,searchQuery,corpus)

    return index


def start():
    print("  [INFO] : ****************************** Start ******************************")
    start_time = time.time()

    searchQuery = "Female Reproductive System slides"
    videoList = ['HH_2yge9uYY', 'SkcddD0LGlM', 'toKp0SGyv5w']
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
    print(f"  [INFO] : Total Elapsed Time -{elapsed_time}")


if __name__ == '__main__':
    start()
    