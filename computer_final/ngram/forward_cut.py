import load_data
class ForWardMaxNgram():
    def __init__(self,wordict_path = 'vocab.txt'):
        self.word_dict = self.load_word_dict(wordict_path)

    def load_word_dict(self, wordict_path):
        res=set()
        for line in open(wordict_path,encoding='utf-8'):
            res.add(line.strip())
        for line in open(r'/root/computer_final/WordSegment-master/WordSegment-master/dict/dict.txt',encoding='utf-8'):
            res.add(line.strip())
        return res

    def max_forward(self, sentence):
        window_size = 6
        cutlist = []
        index = 0
        while index < len(sentence):
            matched = False
            for i in range(window_size, 0, -1):
                cand_word = sentence[index: index + i]
                if cand_word in self.word_dict:
                    cutlist.append(cand_word)
                    matched = True
                    break

            # 如果没有匹配上，则按字符切分
            if not matched:
                i = 1
                cutlist.append(sentence[index])
            index += i
        return cutlist

if __name__=='__main__':
    data=load_data.load_data(data_dir='/root/computer_final_data/news2016zh_valid/news2016zh_valid.json',limit=1200)
    data=load_data.preprocess(data)
    cut = ForWardMaxNgram()
    cut_data=[]
    for sentence in data:
        cut_data.append(cut.max_forward(sentence))
    with open('forward_cut_data_valid.txt','w',encoding='utf-8') as f:
        for sentence in cut_data:
            f.write(' '.join(sentence)+'\n')