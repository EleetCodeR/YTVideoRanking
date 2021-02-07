# from textPreprocessing import textPreprocess
from textPreprocessing import textPreprocess
from similarityScore import calcSimilarityScore
from polarityScore import getPolarityScore
from youTube import getVideoMetaData
import time




def irfSys(vid,query,corpus): 
    print("  [INFO] : IRF-System Initialized...")
    start_time = time.time()

    # Text Processing
    print("  [INFO] : Query Text-preprocessing...")
    query = textPreprocess(query)
    corpus = textPreprocess(corpus)

    # SimilarityScore
    print("  [INFO] : Similarity score calculation...")
    similarity = calcSimilarityScore(query,corpus)

    # PolarityScore
    print("  [INFO] : Polarity score calculation...")
    metaData = getVideoMetaData(vid)
    stats = metaData[0]
    # pass comments for polarity score
    polarity = getPolarityScore(metaData[1])

    print()
    # Index Calculation
    print("  [INFO] : Index calculation stage...")
    # view count , likes , dislikes

    elapsed_time = time.time() - start_time
    elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    print(f"  [INFO] : Exiting IRF system ! \n Elapsed Time :{elapsed_time}")


if __name__ == '__main__':
    
    vid = 'SkcddD0LGlM'
    corpus = ['Female Reproductive System','SAP5(a)','Explain how the','function of the reproductive','regulated by hormonal','organs','are','interactions','Functions','Reproduction','Production of eggs','Through ovulation','Discharge of mature egg','Production of female sex hormones','Structures','Ovaries','female','gonad; produces eggs','and sex hormones','Follicles','structure in','gral','aorirnni','ovary that makes the','egg and progesterone','developing','Oocyte','uterus','fallopian','egg','IuuE=','_1_7}161','female sex cell','Egg','vagina','Structures','Uterine tubes','conducts egg towards','uterus; AKA','female organ','Uterus','a=48','where the fetus','develops','4=tr','Vagina','female','copulatory organ and','birth canal','Estrogen','Secreted by ovaries','Main female sex hormone','Estrogen at puberty stimulates','the','growth','of the uterus and the vagina','Egg maturation','Sexual characteristics','Menstruation']
    query = "Female Reproductive System."
     
    irfSys(vid,query,corpus)