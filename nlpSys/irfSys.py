from textPreprocessing import textPreprocess
from similarityScore import calcSimilarityScore
import time
# from intentRelevanceSys.polarityScore import 



def irfSys(query,corpus):
 
    print("  [INFO] : IRF-System Initialized...")
    start_time = time.time()
    # Text Processing
    query = textPreprocess(query)
    corpus = textPreprocess(corpus)

    # SimilarityScore
    calcSimilarityScore(query,corpus)
    # PolarityScore

    # Index Calculation



    elapsed_time = time.time() - start_time
    elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    print(f"  [INFO] : Exiting IRF system ! Elapsed Time :{elapsed_time}")


if __name__ == '__main__':
    
     corpus = ['Female Reproductive System','SAP5(a)','Explain how the','function of the reproductive','regulated by hormonal','organs','are','interactions','Functions','Reproduction','Production of eggs','Through ovulation','Discharge of mature egg','Production of female sex hormones','Structures','Ovaries','female','gonad; produces eggs','and sex hormones','Follicles','structure in','gral','aorirnni','ovary that makes the','egg and progesterone','developing','Oocyte','uterus','fallopian','egg','IuuE=','_1_7}161','female sex cell','Egg','vagina','Structures','Uterine tubes','conducts egg towards','uterus; AKA','female organ','Uterus','a=48','where the fetus','develops','4=tr','Vagina','female','copulatory organ and','birth canal','Estrogen','Secreted by ovaries','Main female sex hormone','Estrogen at puberty stimulates','the','growth','of the uterus and the vagina','Egg maturation','Sexual characteristics','Menstruation']
     
     query = "Female Reproductive System."
     
     irfSys(query,corpus)