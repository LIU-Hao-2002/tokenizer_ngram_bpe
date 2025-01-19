import json 
def load_data(data_dir=r"news2016zh_train.json", limit=500) -> list[str]:
    data = []
    with open(data_dir, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line)['content'])
            if len(data) >= limit:
                break
    #data = preprocess(data)
    return data

def preprocess(texts: list[str]) -> list[list]:
    if type(texts) == str:
        texts = [texts]
    nums = "0123456789"
    punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
    chinese_puncuation = "！“”#￥%&‘（）*+，-。/：；《=》？@【】、…—·"
    punctuation += chinese_puncuation
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    more = "↓「」ã«æ¥ïçè§µ»¤±º◆"
    nots = set(list(nums + punctuation + letters + more))
    res = []
    for text in texts:
        text = [x for x in list(text.strip()) if x not in nots]
        res.append(''.join(text))
    return res

def compare_train_data(new_path='/root/computer_final/seg_result_train_r1.txt',old_path='/root/computer_final/forward_cut_data_train.txt',if_save=False):
    with open(new_path,'r',encoding='utf-8') as f:
        new_sentences=f.readlines()
        new_sentences=[x.strip().split(' ') for x in new_sentences]
    n=len(new_sentences)
    with open(old_path,'r',encoding='utf-8') as f:
        old_sentences=f.readlines()
        old_sentences=[x.strip().split(' ') for x in old_sentences]
    count=[]
    for new_sentence,old_sentence in zip(new_sentences,old_sentences[:n]):
        if new_sentence!=old_sentence:
            count.append((new_sentence,old_sentence))
    if if_save:
        old_sentences=new_sentences+old_sentences[n:]
        with open(if_save,'w',encoding='utf-8') as f:
            for sentence_list in old_sentences:
                f.write(' '.join(sentence_list)+'\n')
    return len(count)/n,count

if __name__=='__main__':
    ratio,count=compare_train_data(if_save='./round2_data_train.txt')
    print(ratio)
    for x in count:
        if len(x[0])>30 and len(x[0])<60:
            print(' '.join(x[0]))
            print(' '.join(x[1]))
            break

