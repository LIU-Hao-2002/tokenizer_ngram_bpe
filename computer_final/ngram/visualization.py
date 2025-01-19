import matplotlib.pyplot as plt
import numpy as np
import os
import json
from collections import Counter
import matplotlib.font_manager as fm
import re
import pickle 
prep="""临 乎 与 为 共 冲 到 兜 于
即 从 以 似 假 去 让 诸 及
往 迆 连 迎 道 遵 对 导 寻
将 当 叫 吃 合 同 向 和 问
如 尽 打 执 把 投 拦 按 捉
洎 给 维 缘 在 因 惟 就 比
照 较 方 爿 暨 拿 替 望 朝
爰 直 由 率 被 用 繇 齐 至
管 自 起 趁 践 跟 当 趁着 从 往 沿着
按照 通过 比 拿 本着 以 凭
为 为了 由于 因为
对 对于 跟 同 关于 除了
被 让 由"""
prep=prep.split()
excla="""吧、罢、呗、啵、的、价、家、啦、来、唻、了、嘞、哩、咧、咯、啰、喽、吗、嘛、嚜、么（麽）、哪、呢、呐、否、呵、哈、不、兮、般、则、连、罗、给、噻、哉、呸、罢了、不成、得了、而已、的话、来着、了得、也罢、已而、着呢、着哩、着呐、来的、也好、便了、起见、就是、似地、是的、一般、一样、再说、不过"""
excla=excla.split("、")
tense="""立刻、正在、在、马上、常常、经常、渐渐、刚、刚刚、曾经、已经、永远、忽然、突然、顿时、从来、仍然、暂且、仍旧、依然、才、终于、一直、一向、始终、早已、向来、从来、往往、每每、就等。"""
tense=tense.split("、")
num="""一、二、三、四、五、六、七、八、九、十、百、千、万、亿、两、几、多、少、半、余、来、共、合、共、各、每、全、双"""
num=num.split("、")
punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
chinese_puncuation = "！“”#￥%&‘（）*+，-。/：；《=》？@【】、…—·"
punctuation += chinese_puncuation


def load_data(data_dir="/root/computer_final/SINA_News/news2016zh_train.json", limit=500) -> list[str]:
    data = []
    with open(data_dir, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line)['content'])
            if len(data) >= limit:
                break
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

def descriptive_statistics(data: list[str]):
    # 字符频率分布
    all_chars = ''.join(data)
    char_counts = Counter(all_chars)
    
    # 二元组分布
    def get_ngarm(data: list[str], n=2) -> Counter:
        ngrams = []
        for text in data:
            ngrams.extend([text[i:i+n] for i in range(len(text)-n+1)])
        return Counter(ngrams)
    bigrams = get_ngarm(data)
    bigram_counts = Counter(bigrams)
    # 三元组分布
    three_grams = get_ngarm(data, 3)
    three_gram_counts = Counter(three_grams)
    # 四元组分布
    four_grams = get_ngarm(data, 4)
    four_gram_counts = Counter(four_grams)

    return [char_counts, bigram_counts, three_gram_counts, four_gram_counts]

def plot_statistics(counter_list: list[Counter], output_dir="/root/computer_final/visualization"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 设置中文字体
    font_path = '/root/computer_final/SimHei.ttf'   
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font file not found: {font_path}")
    my_font = fm.FontProperties(fname=font_path)
    
    def plot_one(obj: Counter, xlabel, ylabel="频率", title="频率分布", top=50):
        plt.figure(figsize=(10, 6))
        top_chars = dict(obj.most_common(top))
        plt.bar(top_chars.keys(), top_chars.values())
        plt.xlabel(xlabel, fontproperties=my_font)
        plt.ylabel(ylabel, fontproperties=my_font)
        plt.title(title, fontproperties=my_font)
        plt.xticks(fontproperties=my_font)
        plt.yticks(fontproperties=my_font)
        plt.savefig(os.path.join(output_dir, f'{xlabel}_fig.png'), bbox_inches='tight')
        plt.show()

    for obj, xlabel,top in zip(counter_list, ["字符", "二元组", "三元组", "四元组"],[50,25,15,10]):
        plot_one(obj, xlabel,top=top)

def visual_main():
    data = load_data(limit=10000)
    data = preprocess(data)
    counter_list = descriptive_statistics(data)
    plot_statistics(counter_list)
    
def pattern_recognition(data):
    # 对于每个文本，统计其中的介词、感叹词、时态词、数字、标点符号对应的pattern
    results = {
        "前面最多的词": {},
        "后面最多的词": {},
        "中间最多的词": {},
        "两端最多的词": {}
    }
    for temp_list in [excla,prep,tense,num,punctuation]:#,
        for temp in temp_list:
            # 统计temp前面出现最多的词
            pattern_before = re.compile(r'(\w)' + re.escape(temp))
            before_words = []
            for text in data:
                before_words.extend(pattern_before.findall(text))
            results["前面最多的词"][temp] = Counter(before_words).most_common(1)
            
            # 统计temp后面出现最多的词
            pattern_after = re.compile(re.escape(temp) + r'(\w)')
            after_words = []
            for text in data:
                after_words.extend(pattern_after.findall(text))
            results["后面最多的词"][temp] = Counter(after_words).most_common(1)
            
            # 统计两个temp中间出现最多的词
            pattern_between = re.compile(re.escape(temp) + r'(\w)' + re.escape(temp))
            between_words = []
            for text in data:
                between_words.extend(pattern_between.findall(text))
            results["中间最多的词"][temp] = Counter(between_words).most_common(1)
            
            # 统计temp两端最多的字符
            pattern_outer = re.compile(r'(\w)' + re.escape(temp) + r'\1')
            outer_words = []
            for text in data:
                outer_words.extend(pattern_outer.findall(text))
            results["两端最多的词"][temp] = Counter(outer_words).most_common(1)
    for key, value in results.items():
        keys_to_delete = [k for k, v in value.items() if len(v) == 0]
        for k in keys_to_delete:
            del value[k]
    with open('/root/computer_final/visualization/pattern.pkl','wb') as f:
        pickle.dump(results,f)
    return results

def pattern_main():
    data = load_data(limit=1000)
    results = pattern_recognition(data)
    print(results)
if __name__=='__main__':
    pattern_main()



