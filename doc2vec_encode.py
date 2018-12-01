import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

def open_csv():
    """
    Read news data from all CSV files and append them together.
    """
    df = pd.DataFrame(columns=['time', 'headline', 'assetCodes',
                               'sentimentNegative', 'sentimentNeutral',
                               'sentimentPositive'])
    file_count = 10
    for i in range(file_count):
        file_name = "data/news/news_data_" + "{:02}".format(i+1) + ".csv"
        print("Open : " + file_name)
        load_df = pd.read_csv(file_name)
        load_df = load_df[['time', 'headline', 'assetCodes',
                            'sentimentNegative', 'sentimentNeutral',
                            'sentimentPositive']]
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
    wantToChange = ['\\\\','..','--'] #ลบตัวที่ไม่ต้องการทิ้ง
    memory = []
    text_list_change = []
    for x in text_list:
        word = x
        if ('{' in word):
            wordSplit = word.split('{')
            CreateWord = ''
            for y in range(len(wordSplit)):
                if CreateWord == '' and '}' in word:
                    CreateWord = wordSplit[y]
                elif '}' in wordSplit[y]:
                    CreateWord = CreateWord + wordSplit[y].split('}')[1]
        
            word = CreateWord
        if '(' in word:
            wordSplit = word.split('(')
            CreateWord = ''
            for y in range(len(wordSplit)):
                if CreateWord == '' and ')' in word:
                    CreateWord = wordSplit[y]
                elif ')' in wordSplit[y]:
                    CreateWord = CreateWord + wordSplit[y].split(')')[1]
        
            word = CreateWord
        if '<' in word:
            wordSplit = word.split('<')
            CreateWord = ''

            for y in range(len(wordSplit)):
                if CreateWord == '' and '>' in word:
                    CreateWord = wordSplit[y]
                elif '>' in wordSplit[y]:
                    CreateWord = CreateWord + wordSplit[y].split('>')[1]
        
            word = CreateWord

        if '- Part' in word:
            word = word.split('- Part')[0]
        
        for a in range(len(wantToChange)):
            if wantToChange[a] in word:
                word = word.replace(wantToChange[a],'')        

        while '  ' in word:
            word = word.replace('  ',' ')
        
        if ' ' in word:
            if word[0] == ' ':
                word = word[1:]

        word = word.lower()

        if word != "" and word not in memory :
            text_list_change.append(word)
            if len(memory) > 5:
                del memory[0]
            memory.append(word)

    return text_list_change

def encode_to_doc2vec(model, text_list, verbose=False):
    """
    Encode document

    input variable : text_list --> list/series/array of string
    input type : list/series/array-like
    return 2d list/array
    """
    doc_vector = []
    for paragraph in text_list :
        paragraph = paragraph.to_lower() 
        vec = model.infer_vector(paragraph)
        doc_vector.append(vec)
        if verbose :
            print("="*20)
            print("Encode : " + paragraph + "\n To :", vec)
            print("="*20)
    return doc_vector

def select_data(df, ric):
    """
    Select only used data
    """
    df = df[df["assetCodes"].str.contains(ric)]
    df = df.dropna()
#    print(df)
    return df


if __name__ == "__main__":
#    model= Doc2Vec.load("d2v_60.model")
    news_df = open_csv()
    news_df.headline = clean_headline(news_df.headline)
    goog_df = select_data(news_df, "GOOG")
#    goog_df.to_csv("data/news/goog_news.csv")
    
