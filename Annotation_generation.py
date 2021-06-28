#!/usr/bin/env python
# coding: utf-8

# In[9]:


def save(invertedIndex,name) :
  import json 
  with open('{0}.json'.format(name), 'w') as ij:
    json.dump(invertedIndex,ij)

  ij.close();
  


# # CITATION 

# In[10]:


import xml.etree.ElementTree as ET


def tokenization_caseFoldingg(FILE) :
    # We're at the root node (<page>)
    root_node = ET.parse('{0}.xml'.format(FILE)).getroot()

    # We need to go one level below to get <items>
    # and then one more level from that to go to <item>
    dictt = {}
    tokens = {}
    counter = 0
    i = 0
    #-------------------------------------------------------------------------
    #                     A B S T R A C T 
    #-------------------------------------------------------------------------
    for tag in root_node.findall('ABSTRACT/S'):
        # Get the value from the attribute 'name'
        counter += 1 
        value = tag.attrib['sid']
        #print(value)
        # Get the text of that tag
        string = tag.text
        
        dictt = invertedIndexx(string.lower(),i+1)
        #myfile.close()
        for x,y in dictt.items() :
           if tokens.get(x) == None:
                tokens.update({x:[]})
           tokens[x].extend(y)
        i += 1
    #---------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------
    #                     S E C T I O N S
    #-------------------------------------------------------------------------
    for tag in root_node.findall('SECTION/S'):
        # Get the value from the attribute 'name'
        counter += 1 
        value = tag.attrib['sid']
        #print(value)
        # Get the text of that tag
        string = tag.text
        
        dictt = invertedIndexx(string.lower(),i+1)
        #myfile.close()
        for x,y in dictt.items() :
           if tokens.get(x) == None:
                tokens.update({x:[]})
           tokens[x].extend(y)
        i += 1
    #---------------------------------------------------------------------------
        
    
        

    
    return tokens , counter 


# 

# In[ ]:





# In[11]:




def StopWordsRemoval(token):
    myfile = open('Stopword-List.txt',encoding='utf-8')
    string = myfile.read()
    dictt = {}
    for x,y in token.items() :
      for yy in y :
        if yy not in string.split() :
            if dictt.get(x) == None :
                dictt.update({x:[]})
            dictt[x].append(yy)
    myfile.close()
    return dictt

def invertedIndexx(string,j): 
    s=''
    tokens = {}
    for i in range(len(string)) :
        if string[i] != ' ' and string[i].isalnum():
            s=s+string[i]
        elif s!= '' :
                
            if tokens.get(j) == None :
                    tokens.update({j:[]})
            tokens[j].append(s.lower())
            s=''
    
    return tokens



  

  

import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
def lemmatization(token):
 
  
  wordnet_lemmatizer = WordNetLemmatizer()

  # newword = wordnet_lemmatizer.lemmatize("better")
  # print(newword)
  temp = {}
  for docid,words in token.items() :
    for word in words :
      newword = wordnet_lemmatizer.lemmatize(''.join(map(str, word)))
      if temp.get(docid) == None :
                  temp.update({docid:[]})
      
      temp[docid].append(newword)

  

  return temp

def unique(list1,unique_list):
 
     
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # print list
    
    return unique_list



# ## MAIN INDEX 

# In[12]:


def sortIndex(tokens , n) :
  #print(n)
  for i in range(n) :
    
    try :
        tokens[i+1].sort()
    except :
        pass 

  return tokens

import re #regular Expression 

def MainIndex(File) :
  #breaking string into word and applying caseFolding 
  tokens , counter   = tokenization_caseFoldingg(File)
  # print(len(tokens))
  # print(tokens)
  # #removingStopWords
  # #tokens = StopWordsRemoval(tokens)
  # print(len(tokens))
  invertedIndex = tokens
#   print("StopWordsRemoval->")
  invertedIndex = StopWordsRemoval(invertedIndex)
 # print("Okey")
#   print("lemmatization->")
  invertedIndex = lemmatization(invertedIndex)
  #print("Okey")
  #invertedIndex = stemming(invertedIndex)
  invertedIndex = sortIndex(invertedIndex ,  counter)
  #print(invertedIndex)
  return invertedIndex , counter 
  

#Inverted_index , counter  = MainIndex()


# ## VSM CALCULATION

# In[13]:





def calTermFrequency(tokens,uniquelist , n) :
  

  vectorSpaceModel =  {}
  
  #InvertedIndex
  for i in range(n) :
 
    for Uword in uniquelist :
      counter = 0 
      try :
            
          counter = tokens[i+1].count(Uword)
      except :
        pass
      #print("here==",Uword,counter,i)
      if vectorSpaceModel.get(i+1) == None :
        vectorSpaceModel.update({(i+1):[]})
      vectorSpaceModel[i+1].append(counter)
  
      
  

  return vectorSpaceModel

def calTermFrequency_query(queryy,uniquelist , n) :

  query_tf =  {}
  
  #InvertedIndex
  
 
  for Uword in uniquelist :
    counter = 0 
    counter = queryy.count(Uword)
    # if counter >= 1 :
    #   print("yes i am here ")
    #print("here==",Uword,counter,i)
    if query_tf.get('query') == None :
      query_tf.update({('query'):[]})
    query_tf['query'].append(counter)
  
      
  

  return query_tf

"""#### Document Frequency"""

def DocumentFrequency(tokens,uniquelist ,cnt) :
  df = []
  for j in range(len(uniquelist)) :
     counter = 0 
     for i in range(cnt):
       if tokens[i+1][j] != 0 :
          counter = counter + 1
      
     df.append(counter)

  try :
      df = cal_idf(df,cnt)
  except :
      pass 
  return df

"""#### TF IDF"""

import math 
def cal_idf(df,n) :
  for i in range(len(df)) :
    idf = math.log(df[i],10) / n 
    #idf =  math.log(n/df[i],10)
    df[i] = idf
  return df

def calculateTFIDF(vsm , uniquelt , df , counter) :

  for i in range(len(uniquelt)) :
    
    for j in range(counter) :
      vsm[j+1][i] = vsm[j+1][i] * df[i]

  return vsm


# In[14]:



def MainVSM(tokens,uniquelist,counter) :
  
  
  #calculate the Unique list for VSM
  for i in range(counter) :
    try :
        uniquelist = unique(tokens[i+1],uniquelist)
    except :
        pass 
  uniquelist.sort()
#   print(uniquelist)
  save(uniquelist,"UniqueList")
  VSM  = calTermFrequency(tokens,uniquelist , counter)
  save(VSM,"TF")
  df = DocumentFrequency(VSM , uniquelist , counter)
  VSM = calculateTFIDF(VSM,uniquelist,df,counter)
#   print(VSM)
  save(VSM,"VSM")
  #print(len(uniquelist))

  return VSM
#cal


# 
# # Query 

# In[ ]:





# ## pre processing 

# In[15]:


def PreprocessingQuery(queryy) :
  queryy = CaseFolding_query(queryy)
  queryy = stopWordsRemoval_query(queryy)
  queryy = lemmatization_query(queryy)
  #queryy = stemming_query(queryy)
  return queryy


# In[16]:


def CaseFolding_query(query) :
  listt= []
  for words in query :
    listt.append(words.lower())
  return listt


# ## lemmatization 

# In[17]:


import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

def lemmatization_query(query) :
  wordnet_lemmatizer = WordNetLemmatizer()

  temp = []

  for word in query :
    newword = wordnet_lemmatizer.lemmatize(''.join(map(str, word)))
    temp.append(newword)

  return temp 


# ## STop WorD QUERY 

# In[18]:


def stopWordsRemoval_query(queryy) :
    myfile = open('Stopword-List.txt',encoding='utf-8')
    string = myfile.read()
    
    #temp variable to store new words
    temp = []
    for word in queryy :
      if word not in string.split() :
        temp.append(word)
    return temp 


# ## Stemming_query 

# In[19]:


import nltk 
def stemming_query(queryy) :
  from nltk.stem import PorterStemmer
  porter = PorterStemmer()

  temp = []
  for word in queryy :
    newword = porter.stem(''.join(map(str, word)))
    temp.append(newword) 
  return temp 


# ## main 

# In[20]:


#input Queries
def Inputt(querystring) :
    
    query= Convert(querystring)
    return query


# In[21]:


#string to list converter
def Convert(string):
    li = list(string.split(" "))
    return li


# In[22]:


#Taking input and storing in list


def MAINQUERY(dataQuery) :
    query = []
    query = Inputt(dataQuery)

    ##PreProcessing the Query 
    query = PreprocessingQuery(query)
    #print(query)
    global_query_TF = calTermFrequency_query(query,uniquelist,counter)
    #print(len(global_query_TF['query']))
    save(global_query_TF ,"query")
    #print(type(global_query_TF))
    return global_query_TF

    


# In[ ]:





# 
# # SIM CALCULATION 

# ## Magnitude 

# In[23]:


def magnitude(values) :
  mag = 0
  for i in range(len(values)) :
    mag = mag + math.pow(values[i], 2)
  
  mag = math.sqrt(mag)
  return mag


# ## DOTPRODCUT

# In[24]:


def DotProduct(doc,queryy) :
  dotprod = 0
  for i in range (len(doc)) :
    dotprod = dotprod + doc[i]*queryy[i]

  return dotprod


# In[25]:


#print(uniquelist)
save(uniquelist,"uni")


# ## SIM

# In[26]:



def MainSIMVSM(global_query_TF) :
   # now i have 2 global varible 
   # i) global_query_TF
   # ii) global_VSM
   COS_SIM = {}
   #storing the magnitude of query as it will use in all doc
   mag_query = magnitude(global_query_TF['query'])
   #calculating for each document 
   for i in range(counter) :
     numerator = DotProduct(global_VSM[str(i+1)],global_query_TF['query'])
     mag_doc =  magnitude(global_VSM[str(i+1)])
     denominator = mag_doc * mag_query 
     try :
       ans = numerator / denominator
     except :
       ans = 0
     COS_SIM.update({'SIMDOC{0}'.format(i+1):ans})


   query_res = {}
   #SIM
   for i in range(len(COS_SIM)) :

     val = COS_SIM['SIMDOC{0}'.format(i+1)]
    # if val > 0.25:
#         query_res.append(i+1)
   
     query_res.update({i+1 : val})

   #print(query_res)
   return query_res


# ## CitationFinderRef(FileName)

# In[34]:


def CitationFinderRef(FileName ,list_out):
    
    root_node = ET.parse('{0}.xml'.format(FileName)).getroot()
    
    # We need to go one level below to get <items>
    # and then one more level from that to go to <item>
    dictt = {}
    tokens = {}
    ret_value = ""
    counter = 0
    i = 0
    #param = 90 
    
    for param in list_out :
        #-------------------------------------------------------------------------
        #                     A B S T R A C T 
        #-------------------------------------------------------------------------
        for tag in root_node.findall('ABSTRACT/S'):
            # Get the value from the attribute 'name'
            counter += 1 
            value = tag.attrib['sid']
           #print(type(value))
            if value == str(param) :
                print("true")
                ret_value = tag.text
                break 



         #---------------------------------------------------------------------------

        #-------------------------------------------------------------------------
        #                     S E C T I O N S
        #-------------------------------------------------------------------------
        for tag in root_node.findall('SECTION/S'):
            ## Get the value from the attribute 'name'
            counter += 1 
            value = tag.attrib['sid']
            #print(value)
            if value == str(param) :
                print("true")
                ret_value = tag.text
                break 

        #---------------------------------------------------------------------------

    return ret_value
    


# ## QUERY FROM CSV TABLE 

# In[41]:


import os
def FileGeneration(list_directories) :
    listt = []
    directory = r'C:\Users\LEO\Untitled Folder\DataSet'
    # for filename in os.listdir(directory):
    #     listt.append(filename)
    list_directories = [f for f in os.listdir(directory)]    
    return list_directories


# In[43]:


import pandas as pd
from collections import OrderedDict
#IST_FOLDER = ['A00-2018','A00-2030','A97-1014','D09-1092','D10-1044','E03-1005','J01-2004','P04-1036','P05-1013','P08-1028','P08-1043','P08-1102','P11-1060','P11-1061','P87-1015','W06-2932','W06-3114','W99-0613','W99-0623']
LIST_FOLDER = []
LIST_FOLDER = FileGeneration(LIST_FOLDER)

for Folder in LIST_FOLDER :
    
    
    #============================================================================================================
    #    new folder 
    df = pd.read_csv('DataSet/{0}/annotation/{0}.csv'.format(Folder))

    ############################################################################################
    # Iterate loop to all rows by traversing all 3 col 
    LIST_OUTPUT = []
    List_out_citation = []
    list_out_fact = []
    for i in df[['Reference Article','Citing Article','Citation Text']].itertuples():
        #0 -> Index
        #1 -> rA
        #2 -> cA
        #3 Citation Text 

        #making Indexes using Reference Document
        FileName = i[1]
        FileName = "DataSet/{0}/Reference_XML/{1}".format(Folder,FileName)
        print(FileName)
        Inverted_index , counter  = MainIndex(FileName)

        #MAKing INVERTED INDEX AND VSM CALCULATION 

        uniquelist = []
        global_VSM = MainVSM(Inverted_index,uniquelist,counter)


        #-----------------------------------------------------------------------
        #          S A V E 
        #-----------------------------------------------------------------------

        import json
        with open("VSM.json", 'r') as ii:
            global_VSM = json.load(ii)


        with open("UniqueList.json", 'r') as ij:
            uniquelist = json.load(ij)

        #-----------------------------------------------------------------------
        #-----------------------------------------------------------------------

        #Making Query 
        global_query_TF = MAINQUERY(i[3])  # TEXT 
        print('TEXT =',i[3])

        Result = MainSIMVSM(global_query_TF)

        #SORTING dictionARY----------

        ANS = {k: v for k, v in sorted(Result.items(), key=lambda item: item[1])}

        #REVERSE 
        res = OrderedDict(reversed(list(ANS.items())))
        Output = []
        counter = 0
        for i in res :
            if counter > 0 :
                break
            counter = counter + 1
            Output.append(i)

        #Storing the values in list
        LIST_OUTPUT.append(Output)

        #calling citaitonFinder function and storing value in list in order to make dataframe in future
        List_out_citation.append( CitationFinderRef(FileName , Output) )

        #3rd Output 
        list_out_fact.append("Method_Citation")




        #---------------------------
        #print(df)
        #print(Result)
        print("\n \n")
        ANS = {}
        Result = {}
        global_query_TF= {}
    
    #=====================================================================================



    # making the new data frame 
    dictt = {
        'Reference Article' :df['Reference Article'] ,
        'Citation Marker' : df["Citation Marker"] ,
        'Citance Number' : df["Citance Number"] ,
        'Citing Article' : df["Citing Article"] ,
        'Citation Marker Offset' : df["Citation Marker Offset"] ,
        'Citation Offset' : df["Citation Offset"] ,
        'Citation Text' : df["Citation Text"] ,
        'Reference Offset' : LIST_OUTPUT ,
        'Reference Textt' : List_out_citation ,
        'Discourse Facet' : list_out_fact 
    }
    NewDF  = pd.DataFrame(dictt)

    NewDF.to_csv('DataSet/{0}/annotation/AnnotationNew.csv'.format(Folder))


# In[ ]:





# # -------------------------------------------------------------------------------------------------

# In[239]:


# #DEFAULT

# Inverted_index , counter  = MainIndex(FileName)


# uniquelist = []
# global_VSM = MainVSM(Inverted_index,uniquelist,counter)

# #saving 
# #------------------------------------------------------
# import json
# with open("VSM.json", 'r') as ii:
#     global_VSM = json.load(ii)


# with open("UniqueList.json", 'r') as ij:
#     uniquelist = json.load(ij)
# #------------------------------------------------------


# In[240]:



# import pandas as pd


# In[217]:


# df = pd.read_csv('A00-2018.csv')


# In[218]:




# # print("---------------------------")
# # i[0] = 2
# # a = i[0]
# # print( df.loc[a,'Reference Article'] )
# # df.loc[2,'Reference Article'] = 10
# # print( df.loc[a,'Reference Article'] )
# # print( df.loc[3,'Reference Article'] )
# dictt = {
#     'Reference Article' :df['Reference Article'] ,
#     'Citation Marker' : df["Citation Marker"]
# }
# print(dictt["Citation Marker"])
# ii  = pd.DataFrame(dictt)
# print(ii)
# # df["itance Number"][2] = 500
# # print( df["itance Number"][2])


# ## PRE PROCESSING 

# In[7]:


# print(list_directories)


# In[ ]:





# In[ ]:




