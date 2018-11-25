# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 16:08:38 2018

@author: SarachErudite
"""

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import pandas as pd 

def train_doc2vec(model, tagged_data, max_epochs=100, update_vocab=False, print_detail=False, save_sampling=10):
    print("Building vocab")
    model.build_vocab(tagged_data, update=update_vocab)
    print("Built vocab done")
    for epoch in range(max_epochs):
        if print_detail : 
            print('epoch = {0}'.format(epoch))
        model.train(tagged_data,
                    total_examples=model.corpus_count,
                    epochs=model.epochs)
        # decrease the learning rate
        model.alpha -= 0.0002
        # fix the learning rate, no decay
        model.min_alpha = model.alpha
        if (epoch+1)%save_sampling == 0 :     
            model.save("weight/d2v_"+str(epoch+1)+".model")
    model.save("weight/d2v_final.model")
    print("Model Trained Saved ....")
    print("================  Training Done ! ===================")
    return model 

def tag_document(document_list, print_sampling = 1,verbose=True):
    tagged_doc = [] 
    print("Tagging Document .../ ")
    print("This should take few minutes depend on your data size")
    num_doc = len(doc_list)
    for i, doc in enumerate(document_list):
        #change to lower case and tag document 
        tagged_doc.append(TaggedDocument(words=word_tokenize(doc.lower()), tags=[str(i)]))
        if i%print_sampling == 0 and verbose : 
            print("Tags : ", i ,"/", num_doc,"  Text : " + doc)    
    return tagged_doc

print("Read Cleaned Document !")
news_train_df = pd.read_csv("data/news/news_Cut.csv")
doc_list = news_train_df['headline'].dropna().drop_duplicates().tolist()
max_epochs = 100
vec_size = 20
alpha = 0.025
doc2vec_model = Doc2Vec(vector_size=vec_size,
                alpha=alpha, 
                min_alpha=0.00025,
                min_count=1,
                dm =1)
print("Clear momories before training")

tagged_doc = tag_document(doc_list, print_sampling=50000)

# Clear RAM before training 
news_train_df, doc_list = None, None 
doc2vec_model = train_doc2vec(doc2vec_model, tagged_doc, max_epochs, False, True)
