from gensim.parsing import preprocessing as textPre
import time

start_time = time.time()

corpus = ['Female Reproductive System','SAP5(a)','Explain how the','function of the reproductive','regulated by hormonal','organs','are','interactions','Functions','Reproduction','Production of eggs','Through ovulation','Discharge of mature egg','Production of female sex hormones','Structures','Ovaries','female','gonad; produces eggs','and sex hormones','Follicles','structure in','gral','aorirnni','ovary that makes the','egg and progesterone','developing','Oocyte','uterus','fallopian','egg','IuuE=','_1_7}161','female sex cell','Egg','vagina','Structures','Uterine tubes','conducts egg towards','uterus; AKA','female organ','Uterus','a=48','where the fetus','develops','4=tr','Vagina','female','copulatory organ and','birth canal','Estrogen','Secreted by ovaries','Main female sex hormone','Estrogen at puberty stimulates','the','growth','of the uterus and the vagina','Egg maturation','Sexual characteristics','Menstruation']

sanitizedCorpus = []


for text in corpus :
    text = textPre.strip_punctuation(text)
    text = textPre.strip_numeric(text)
    text = textPre.strip_multiple_whitespaces(text)
    # text = textPre.stem_text(text)
    sanitizedCorpus.append(textPre.remove_stopwords(text)) 

print(sanitizedCorpus)

elapsed_time = time.time() - start_time
print(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
