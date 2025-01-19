import json
class Tokenizer:
    def __init__(self,texts,ratio=0.1):
        self.frequency={}
        self.texts=self.preprocess(texts)
        self.ratio=ratio
        self.cache=[]
        self.vocab=set()
        self.unigram={}
        for text in self.texts:
            for token in text:
                self.unigram[token]=self.unigram.get(token,0)+1
        print('unigram:',len(self.unigram))
        

    def train(self, round):
        track=0
        while track<round:               
            track+=1
            self.bigrams={}
            self.frequency={}
            for text in self.texts: 
                self.process_one(text)
            self.bigrams=dict(sorted(self.bigrams.items(),key=lambda x:x[1],reverse=True))
            for bigram,count in list(self.bigrams.items())[:int(len(self.bigrams)*self.ratio/track)]:
                if count<min(self.frequency[bigram[0]],self.frequency[bigram[1]]): continue
                self.frequency[bigram[0]+bigram[1]]=self.frequency.get(bigram[0]+bigram[1],0)+count
                self.frequency[bigram[0]]-=count
                self.frequency[bigram[1]]-=count
            self.frequency=dict(sorted(self.frequency.items(),key=lambda x:x[1],reverse=True))
            self.vocab=set(list(self.frequency.keys()))
        self.vocab=self.vocab.union(self.unigram)

    def process_one(self,text):
        # 先根据现有的self.vocab更新text进行合并，后统计bigrams
        i=0
        while i<len(text)-1:
            pair=text[i]+text[i+1]
            if pair in self.vocab: 
                text[i:i+2]=[pair]
                if i>0:
                    i-=1
            else:
                i+=1 
        for i,token in enumerate(text):
            self.frequency[token]=self.frequency.get(token,0)+1
        for i in range(len(text)-1):
            if text[i]==text[i+1]:continue
            self.bigrams[(text[i],text[i+1])]=self.bigrams.get((text[i],text[i+1]),0)+1

        
    def preprocess(self, texts):
        nums="0123456789"
        punctuation="!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
        chinese_puncuation="！“”#￥%&‘（）*+，-。/：；《=》？@【】、…—·"
        punctuation+=chinese_puncuation
        letters="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        more="↓「」ã«æ¥ïçè§µ»¤±º"
        nots=set(list(nums+punctuation+letters+more))
        res=[]
        for text in texts:
            text=[x for x in list(text.strip()) if x not in nots]
            res.append(text)
        return res
    
if __name__=='__main__':
    data_dir=r"/root/computer_final_data/SINA_News/news2016zh_train.json"
    data=[]
    with open(data_dir,'r',encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line)['content'])
            if len(data)>=20000:
                break
    tokenizer=Tokenizer(data,ratio=0.3)
    tokenizer.train(3)
    print(max([len(x) for x in tokenizer.vocab]))
    print(len(tokenizer.vocab))
    n=len(tokenizer.vocab)
    with open('vocab.txt','w',encoding='utf-8') as f:
        for token in tokenizer.vocab:
            f.write(token+'\n')

    # comparison
    others=set()
    with open(r'/root/computer_final/WordSegment-master/WordSegment-master/dict/dict.txt','r',encoding='utf-8') as f:
        for line in f:
            others.add(line.strip())
    tokenizer.vocab=tokenizer.vocab-others
    print("new word length:",len(tokenizer.vocab))
    twos=[x for x in tokenizer.vocab if len(x)==2]
    threes=[x for x in tokenizer.vocab if len(x)==3]
    fours=[x for x in tokenizer.vocab if len(x)==4]

    print(f"二元词语占比{len(twos)/n}：{twos[:20]}")
    print(f"三元词语占比{len(threes)/n}：{threes[:20]}")
    print(f"四元词语占比{len(fours)/n}：{fours[:20]}")


    
