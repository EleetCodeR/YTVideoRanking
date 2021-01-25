from gensim.parsing import preprocessing as textPre
from gensim.utils import tokenize
import time
from halo import Halo

def textPreprocess(corpus):
    spinner = Halo(text='processing', spinner='dots')
    print("  [INFO] : Text-pre processing started...")
    spinner.start()
    start_time = time.time()
    sanitizedCorpus = []
    
    for text in corpus :
        # Sanitize
        text = textPre.strip_punctuation(text)
        text = textPre.strip_numeric(text)
        text = textPre.strip_multiple_whitespaces(text)
        text = textPre.remove_stopwords(text)
        # Tokenize
        text = list(tokenize(text,lowercase=True,deacc=True))
        _ = [sanitizedCorpus.append(txt) for txt in text]
    
    elapsed_time = time.time() - start_time
    elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    spinner.succeed(f"[INFO] : Text Processing finished ! Elapsed Time :{elapsed_time}")
    
    return set(sanitizedCorpus)




if __name__ == '__main__':
    
    corpus = ['Female Reproductive System','SAP5(a)','Explain how the','function of the reproductive','regulated by hormonal','organs','are','interactions','Functions','Reproduction','Production of eggs','Through ovulation','Discharge of mature egg','Production of female sex hormones','Structures','Ovaries','female','gonad; produces eggs','and sex hormones','Follicles','structure in','gral','aorirnni','ovary that makes the','egg and progesterone','developing','Oocyte','uterus','fallopian','egg','IuuE=','_1_7}161','female sex cell','Egg','vagina','Structures','Uterine tubes','conducts egg towards','uterus; AKA','female organ','Uterus','a=48','where the fetus','develops','4=tr','Vagina','female','copulatory organ and','birth canal','Estrogen','Secreted by ovaries','Main female sex hormone','Estrogen at puberty stimulates','the','growth','of the uterus and the vagina','Egg maturation','Sexual characteristics','Menstruation']

    print(textPreprocess(corpus))