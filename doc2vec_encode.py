import pandas as pd 
import gensim 
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

def open_csv():
    """
    Read news data from all CSV files and append them together. 
    """
    df = pd.DataFrame(columns=['time','headline','assetCodes','sentimentNegative','sentimentNeutral','sentimentPositive'])
    file_count = 10
    for i in range(0,file_count):
        i += 1 
        if i < 10 : 
            file_name = "data/news/news_data_"+str(0)+str(i)+".csv"
        else : 
            file_name = "data/news/news_data_"+str(i)+".csv"
        print("Open : " + file_name)
        load_df = pd.read_csv(file_name)
        load_df = load_df[[['time','headline','assetCodes','sentimentNegative','sentimentNeutral','sentimentPositive']]]
        df = df.append(load_df)
    return df

def sector_ric():
    """
    Read sector symbol 
    """
    df = pd.read_csv("data/tech_sector_ric.csv")
    ric = df["RIC"].tolist()
    return ric 

def clean_headline(text_list):
    """
    Pre-processing the data 
    1. cut stock quotes 
    2. cut special alphabets
    3. change to lower 

    input variable : text_list --> list/series/array of string 
    input type : list/series/array-like 
    return list/series/array-like of cleaning data 
    """
    return text_list 

def encode_to_doc2vec(model, text_list, verbose=False):
    """
    Encode document 

    input variable : text_list --> list/series/array of string 
    input type : list/series/array-like 
    return 2d list/array 
    """
    doc_vector = [] 
    for paragraph in text_list : 
        vec = model.infer_vector(paragraph)
        doc_vector.append(vec)
        if verbose : 
            print("Encode : " + paragraph + " to ", vec)
    return doc_vector 

def select_data(df, ric):   
    """
    Select only used data 
    """
    return df 

if __name__ == "__main__":
    model= Doc2Vec.load("d2v_60.model")  
    news_df = open_csv()
    news_df.headline = clean_headline(news_df.headline)
    