import re, collections
class bpe_eng:
    def __init__(self,filename='pg16457.txt'):
        # vocab = {'l o w </w>': 5, 'l o w e r </w>': 2, 'n e w e s t </w>': 6, 'w i d e s t </w>': 3}
        self.vocab = self.get_vocab(filename)
        self.tokens_frequencies,self.vocab_tokenization = None,None
        self.token2idx = None
        self.idx2token = None

    def get_vocab(self,filename):
        vocab = collections.defaultdict(int)
        with open(filename, 'r', encoding='utf-8') as fhand:
            for line in fhand:
                words = line.strip().split()
                for word in words:
                    vocab[' '.join(list(word)) + ' </w>'] += 1

        return vocab

    def get_stats(self,vocab):
        pairs = collections.defaultdict(int)
        for word, freq in vocab.items():
            symbols = word.split()
            for i in range(len(symbols)-1):
                pairs[symbols[i],symbols[i+1]] += freq
        return pairs

    def merge_vocab(self,pair, v_in):
        v_out = {}
        bigram = re.escape(' '.join(pair))
        p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
        for word in v_in:
            w_out = p.sub(''.join(pair), word)
            v_out[w_out] = v_in[word]
        return v_out

    def get_tokens_from_vocab(self,vocab):
        tokens_frequencies = collections.defaultdict(int)
        vocab_tokenization = {}
        for word, freq in vocab.items():
            word_tokens = word.split()
            for token in word_tokens:
                tokens_frequencies[token] += freq
            vocab_tokenization[''.join(word_tokens)] = word_tokens
        return tokens_frequencies, vocab_tokenization

    def measure_token_length(self,token):
        if token[-4:] == '</w>':
            return len(token[:-4]) + 1
        else:
            return len(token)

    def tokenize_word(self,string, sorted_tokens, unknown_token='</u>'):
        
        if string == '':
            return []
        if sorted_tokens == []:
            return [unknown_token]

        string_tokens = []
        for i in range(len(sorted_tokens)):
            token = sorted_tokens[i]
            token_reg = re.escape(token.replace('.', '[.]'))

            matched_positions = [(m.start(0), m.end(0)) for m in re.finditer(token_reg, string)]
            if len(matched_positions) == 0:
                continue
            substring_end_positions = [matched_position[0] for matched_position in matched_positions]

            substring_start_position = 0
            for substring_end_position in substring_end_positions:
                substring = string[substring_start_position:substring_end_position]
                string_tokens += self.tokenize_word(string=substring, sorted_tokens=sorted_tokens[i+1:], unknown_token=unknown_token)
                string_tokens += [token]
                substring_start_position = substring_end_position + len(token)
            remaining_substring = string[substring_start_position:]
            string_tokens += self.tokenize_word(string=remaining_substring, sorted_tokens=sorted_tokens[i+1:], unknown_token=unknown_token)
            break
        return string_tokens
    
    def train(self,num_merges = 10000):
        for i in range(num_merges):
            pairs = self.get_stats(self.vocab)
            if not pairs:
                break
            best = max(pairs, key=pairs.get)
            self.vocab = self.merge_vocab(best, self.vocab)
            print('Iter: {}'.format(i))
            print('Best pair: {}'.format(best))
            tokens_frequencies, vocab_tokenization = self.get_tokens_from_vocab(self.vocab)
            print('All tokens: {}'.format(tokens_frequencies.keys()))
            print('Number of tokens: {}'.format(len(tokens_frequencies.keys())))
            print('==========')
        self.tokens_frequencies=tokens_frequencies
        self.vocab_tokenization=vocab_tokenization
        self.token2idx = {token: idx for idx, token in enumerate(tokens_frequencies.keys())}
        self.idx2token = {idx: token for idx, token in enumerate(tokens_frequencies.keys())}

    def encode_word(self,word):
        sorted_tokens_tuple = sorted(self.tokens_frequencies.items(), key=lambda item: (self.measure_token_length(item[0]), item[1]), reverse=True)
        sorted_tokens = [token for (token, freq) in sorted_tokens_tuple]
        if word in self.vocab_tokenization:
            encoded=self.vocab_tokenization[word]
        else:
            encoded=self.tokenize_word(string=word, sorted_tokens=sorted_tokens, unknown_token='</u>')
        res=[]
        for token in encoded:
            res.append(self.token2idx[token])
        return res+[self.token2idx['</w>']]
    
    def encode(self,sentence):
        words=sentence.split()
        res=[]
        for word in words:
            res+=self.encode_word(word)
        return res

    def decode(self,ids):
        return ''.join([self.idx2token[id] for id in ids]).replace('</w>',' ')

if __name__=='__main__':
    bpe = bpe_eng()
    bpe.train(num_merges=10)
    sen='I was served lemon, but I made lemonade.'
    print(sen)
    print(bpe.encode(sen))
    print(bpe.decode(bpe.encode(sen)))
