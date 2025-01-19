import re
from collections import defaultdict,Counter
from pprint import pprint
from load_data import load_data,preprocess

class bpe_chn_tokenizer:
    def __init__(self,texts:list[str],num_merges:int):
        self.tokens=self.get_single_char(texts)
        self.merges,self.vocab=self.train(texts,num_merges)
        for left,right in self.merges:
            self.tokens.add(left+right)
        self.token2id={token:i for i,token in enumerate(self.tokens)}
        self.id2token={i:token for i,token in enumerate(self.tokens)}

    def get_single_char(self,texts):
        single_char=set()
        for text in texts:
            single_char.update(set(text.strip()))
        single_char.add('</w>')
        single_char.add('<unk>')
        return single_char

    def get_vocab(self,texts):
        vocab=Counter()
        for text in texts:
            tokens=list(text.strip())
            tokens.append('</w>')
            vocab[' '.join(tokens)]+=1
        return vocab

    def get_stats(self,vocab):
        pairs=defaultdict(int)
        for word,freq in vocab.items():
            symbols=word.split()
            for i in range(len(symbols)-1):
                pairs[(symbols[i],symbols[i+1])]+=freq
        return pairs

    def merge_vocab(self,pair,vocab,merges:set):
        pattern = re.escape(' '.join(pair))
        regex=re.compile(r'(?<!\S)'+pattern+r'(?!\S)') 
        new_vocab={}
        merged_symbol="".join(pair)
        for word in vocab:
            new_word=regex.sub(merged_symbol,word)
            new_vocab[new_word]=vocab[word]
        vocab = new_vocab
        merges.add(pair)
        return vocab,merges

    def train(self,texts,num_merges):
        vocab=self.get_vocab(texts)
        merges=set()
        for i in range(num_merges):
            pairs=self.get_stats(vocab)
            if not pairs:
                break
            best_pair=max(pairs,key=pairs.get)
            if pairs[best_pair]<1:
                break
            vocab,merges=self.merge_vocab(best_pair,vocab,merges)
            #print(f'Merge {i+1}:{best_pair},Frequency:{pairs[best_pair]}')
        return merges,vocab

    def tokenize(self,text):
        tokens=list(text.strip())
        tokens.append('</w>')
        i=0
        while i<len(tokens)-1:
            pair=(tokens[i],tokens[i+1])
            if pair in self.merges:
                tokens[i:i+2]=["".join(pair)]
                if i>0:
                    i-=1
            else:
                i+=1
        if tokens[-1]=='</w>':
            tokens.pop()
        return tokens

    def encode(self,text):
        tokens=self.tokenize(text)
        ids=[self.token2id.get(token,self.token2id['<unk>']) for token in tokens]
        return ids
    
    def decode(self,ids):
        tokens=[self.id2token.get(i,'<unk>') for i in ids]
        return "".join(tokens)

    
if __name__=='__main__':
    texts=load_data(limit=100)
    num_merges=100
    tokenizer=bpe_chn_tokenizer(texts,num_merges)
    test=texts[0][:100]
    ids=tokenizer.encode(test)
    print('*'*20+'原始文本'+'*'*20)
    print(test)
    print('*'*20+'编码后'+'*'*20)
    print(ids)
    print('*'*20+'解码后'+'*'*20)
    print(tokenizer.decode(ids))
    print('*'*20+'分词后'+'*'*20)
    print(tokenizer.tokenize(test))