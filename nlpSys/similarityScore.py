from gensim.models.word2vec import Word2Vec
import gensim.downloader as api
import time
from halo import Halo
from pprint import pprint

def calcSimilarityScore(query,corpus):
    spinner = Halo(text='processing', spinner='dots')
    start_time = time.time()
    # download the model and return as object ready for use
    # model = api.load("glove-wiki-gigaword-100")
    # model = api.load("glove-twitter-25")
    spinner.start("[INFO] : Loading GloVe-Model ...")
    model = api.load("glove-twitter-100")
    spinner.succeed()
    
    print(" [INFO] : Generating Cosine Similarity Matrix ...")
    rows = len(query)
    cols = len(corpus)
    print(f"  [INFO] : {rows} x {cols} matrix")
    cosineSimMatrix = [[0]*(cols+1)]*(rows) 
    
    for i,q in enumerate(query) :

        totalScore = 0
        col = 0
        for j,c in enumerate(corpus) :
            try:
                sim =  model.similarity(q,c)
                if(sim > 0):
                    col +=1
                    totalScore += sim   
                    cosineSimMatrix[i][j] = sim
                else:
                    totalScore += 0   
                    cosineSimMatrix[i][j] = 0

            except KeyError as e:
                cosineSimMatrix[i][j] = 0
                # print(f"  [ERROR] : {e}")
                continue
            except IndexError as e :
                print(f"  [ERROR] : {e}")
        
        # print(f"ROW-SCORE :{totalScore}")
        cosineSimMatrix[i][cols] = totalScore/col
            

    #print(cosineSimMatrix)

    score = 0
    for x in range(0,rows):
        # print(f"ROW {x} : {cosineSimMatrix[x][cols]}")
        score += cosineSimMatrix[x][cols]

    score = score/rows
    elapsed_time = time.time() - start_time
    elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    print(f"  [INFO] : Elapsed Time :{elapsed_time}")
    print(f"  [INFO] : Similarity-Score : {score} ")

    

if __name__ == '__main__':
    
    corpus = ['Female Reproductive System','SAP5(a)','Explain how the','function of the reproductive','regulated by hormonal','organs','are','interactions','Functions','Reproduction','Production of eggs','Through ovulation','Discharge of mature egg','Production of female sex hormones','Structures','Ovaries','female','gonad; produces eggs','and sex hormones','Follicles','structure in','gral','aorirnni','ovary that makes the','egg and progesterone','developing','Oocyte','uterus','fallopian','egg','IuuE=','_1_7}161','female sex cell','Egg','vagina','Structures','Uterine tubes','conducts egg towards','uterus; AKA','female organ','Uterus','a=48','where the fetus','develops','4=tr','Vagina','female','copulatory organ and','birth canal','Estrogen','Secreted by ovaries','Main female sex hormone','Estrogen at puberty stimulates','the','growth','of the uterus and the vagina','Egg maturation','Sexual characteristics','Menstruation']

    query = "sperm male eggs ovary female"


