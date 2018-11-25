import csv
from collections import defaultdict

columns = defaultdict(list)

wantToChange = ['\\\\','..','--'] #ลบตัวที่ไม่ต้องการทิ้ง


for i in range(1,11):
    if i < 10 :
        numStr = "0" + str(i)
    else:
        numStr = str(i)
    path = 'news/news_data_'+ numStr + '.csv' # path ของ ข่าวทั้งหมด 10 ตัว
    print("Load data from {0}".format('news_data_'+ numStr + '.csv'))
    with open(path,encoding="utf8", mode = "r") as f:
        reader = csv.DictReader(f) # read rows into a dictionary format
        for row in reader: # read a row as {column1: value1, column2: value2,...}
            for (k,v) in row.items(): # go over each column name and value 
                columns[k].append(v)

# print(columns["headline"])
with open('news_Cut.csv',encoding="utf8", mode = "w") as csv_file:
    fieldnames = ["headline"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    memory = []
    for x in columns["headline"]:
        word = x
        if ('{' in word):
            wordSplit = word.split('{')
            CreateWord = ''
            for y in range(len(wordSplit)-1):
                if CreateWord == '' and len(CreateWord.split('}')) != 1:
                    CreateWord = CreateWord + wordSplit[0] + wordSplit[1].split('}')[1]
                elif len(CreateWord.split('}')) != 1:
                    CreateWord = CreateWord.split('{')[0]+CreateWord.split('}')[1]
                else:
                    CreateWord = CreateWord.split('{')[0]
        
            word = CreateWord
        if '(' in word:
            wordSplit = word.split('(')
            CreateWord = ''
            for y in range(len(wordSplit)-1):
                if CreateWord == '' and len(CreateWord.split(')')) != 1:
                    CreateWord = CreateWord + wordSplit[0] + wordSplit[1].split(')')[1]
                elif len(CreateWord.split(')')) != 1:
                    CreateWord = CreateWord.split('(')[0]+CreateWord.split(')')[1]
                else:
                    CreateWord = CreateWord.split('(')[0]
        
            word = CreateWord
        if '<' in word:
            wordSplit = word.split('<')
            CreateWord = ''
            # try:
            for y in range(len(wordSplit)-1):
                if CreateWord == '' and len(CreateWord.split('>')) != 1:
                    CreateWord = CreateWord + wordSplit[0] + wordSplit[1].split('>')[1]
                elif len(CreateWord.split('>')) != 1:
                    CreateWord = CreateWord.split('<')[0]+CreateWord.split('>')[1]
                else:
                    CreateWord = CreateWord.split('<')[0]
        
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

        word = word.upper()

        if word != "" and word not in memory :
            writer.writerow({"headline": word})
            if len(memory) > 5:
                del memory[0]
            memory.append(word)

print("finish")