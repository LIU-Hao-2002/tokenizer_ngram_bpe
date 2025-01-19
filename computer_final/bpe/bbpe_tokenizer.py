
class bbpe_tokenizer:
    def __init__(self,texts:list[str],num_merges):
        texts=''.join(texts)
        self.tokens = list(map(int, texts.encode("utf-8"))) #ids
        self.train(num_merges)

    def get_stats(self,ids):
        counts = {}
        for pair in zip(ids, ids[1:]): # 迭代连续元素
            counts[pair] = counts.get(pair, 0) + 1
        return counts
    
    def merge(self, ids, pair, idx):
        # 在(ids)列表中, 用新的token idx替换所有的(101,32)字节对
        newids = []
        i = 0
        while i < len(ids):
            if i < len(ids) - 1 and ids[i] == pair[0] and ids[i+1] == pair[1]:
                newids.append(idx)
                i += 2
            else:
                newids.append(ids[i])
                i += 1
        return newids

    def train(self, num_merges):
        ids = self.tokens
        merges = {}
        for i in range(num_merges):
            stats = self.get_stats(ids)
            pair = max(stats, key=stats.get)
            idx = 256 + i
            print(f"merging {pair} into a new token {idx}")
            ids = self.merge(ids, pair, idx)
            merges[pair] = idx
        vocab = {idx: bytes([idx]) for idx in range(256)}
        for (p0, p1), idx in merges.items():
            vocab[idx] = vocab[p0] + vocab[p1]
        self.vocab = vocab  
        self.merges = merges

    def decode(self, ids):
        tokens = b"".join(self.vocab[idx] for idx in ids)
        text = tokens.decode("utf-8", errors="replace")
        # 没有基于动态规划而是简单的将错误字符替换为特殊字符
        return text

    def encode(self, text):
        tokens = list(text.encode("utf-8"))
        while len(tokens) >= 2:
            stats = self.get_stats(tokens)
            # 寻找stats在此次循环中需要合并的对，也就是我们要在merge字典中找到具有最低索引的键或类似键，因为我们想要在后期合并之前完成所有的早期合并
            pair = min(stats, key=lambda p: self.merges.get(p, float("inf")))
            if pair not in self.merges:
                break # 没有在编码范围内
            idx = self.merges[pair]	
            tokens = self.merge(tokens, pair, idx)
        return tokens
    
if __name__=='__main__':
    # text from https://www.reedbeta.com/blog/programmers-intro-to-unicode/
    text = "Ｕｎｉｃｏｄｅ! 🅤🅝🅘🅒🅞🅓🅔‽ 🇺‌🇳‌🇮‌🇨‌🇴‌🇩‌🇪! 😄 The very name strikes fear and awe into the hearts of programmers worldwide. We all know we ought to “support Unicode” in our software (whatever that means—like using wchar_t for all the strings, right?). But Unicode can be abstruse, and diving into the thousand-page Unicode Standard plus its dozens of supplementary annexes, reports, and notes can be more than a little intimidating. I don’t blame programmers for still finding the whole thing mysterious, even 30 years after Unicode’s inception."
    tokenizer = bbpe_tokenizer([text], 100)
    test='我知道，我不是因为偶然才来到这个世界，我是为了践行一个平凡、美丽、无私的梦想而来的；我是为了通过各种苦乐逆顺的体验来历练自己而来的，并由此完善，成长而提升……”金华市环城小学校训，没有一个字和学习有关，却让学生、家长和老师都掉下泪来。校训原文： 世界因我多温暖 我知道，我不是因为偶然才来到这个世界，我是为了践行一个平凡、美丽、无私的梦想而来的;我是为了通过各种苦乐逆顺的体验来历练自己而来的，并由此完善，成长而提升。 我深深地知道，改变这个世界的力量来自太阳，来自人类心灵深处的温度。我，要让世界因我而多温暖。 我知道，我所有的长处都源自父母祖宗的优秀，源自华夏千年文明的积淀。但它不是我炫耀和自私的资本，它是我赖以成长并服务人类的工具，它是我生命的伟大、美好和无私的工具。 我知道，我的缺点与不足不是我的自愿，那是因为我是从有缺点和不足的爸爸妈妈而来，选择这样的爸爸妈妈是我的自愿。对于这些缺陷，我全然接受，并通过今生的感恩、忍受和努力来弥补。 我想对爸爸妈妈说，我愿意从今天开始，不再用完美要求你们，也请你们不再用完美苛求于我，我是你们的一部分，我们是一个整体，让我们一起改变，用爱让家里充满温暖，以影响世界。 从今天起，我将高高地放飞自己的梦想，积极乐观地生活和学习。 命运从来没有规定我此生将是什么?国家没有规定我，父母没有规定我，老师也是一样。一切万物都没有规定我必须是什么样的人，大家把一切主动权交给我，让我自己决定自己的梦想，然后慈悲无私地帮助我，成就我。 因此，我必须让我自己成为一颗最圆润的种子，让周边的世界因我的成长而温暖。 我知道，生命是人世间最美丽的奇迹，读书是人世间最享受的愉悦。 老师对我说，曾经有一个善人，在春天的时候特别给两个乞丐一间破房和一块空地。到了秋天，一个懒惰的乞丐贫病而死，而另一个勤奋的乞丐却富裕安乐。 在宇宙中，每一个灵魂都是乞丐，四处漂泊。父母就是善人，给了属于我的一间破房和广袤无垠的空地，那间破房就是我不完美的身体，而那块空地就是我无边的心灵。我坚信，只要用勤劳播撒智慧与爱的种子，就一定会有硕果累累的明天。 从这一刻起，我要用无限的信心走向未来。 我知道，生命中最珍贵最强大的就是灵魂。环城小学是我人生的第一母校，母校给我的最大眷顾是把我放在春天里，给我规矩，给我阳光，给我一颗春天般温暖柔软的灵魂，去温暖属于我们的世界。 谨此践行我们的校训：世界因我多温暖。 一位刘老师说，她对校训中关于缺点的两段感触颇深：“别说普通家长，就是我们这些当老师的，很多时候也会苛责孩子的不完美，希望他们做得更好，其实我们都挺缺少承认自己和对方都不完美的勇气。”校训文的主要作者是校长俞正强，初稿是他寒假里写好的。俞正强说，写这个文章，主要是想告诉孩子三件事。一、孩子们都是带着使命而来，生活不仅有顺境，也有辛苦挫折，但是这能让我们成长。二、我们的优缺点来自父母，我们都是不完美的人，生活中不应有太多指责、抱怨，只有家庭温暖才能温暖世界。三、孩子最重要的并不是学习多少知识，而是有一个温暖和柔软的灵魂。他说，这篇校训文不仅是为了影响孩子们，也是为了影响家长和老师。 文章来源：行知父母微学堂 教师吧 龙乡教育，向您约稿：如果您有好的文章、好的事例、好的新闻线索，请发至pyxjyxxbs@163.com 微信ID：puyangxianjiaoyu 长按左侧二维码关注'
    encoded = tokenizer.encode(test)
    print(len(encoded)/len(test))
    print(tokenizer.decode(encoded)==test)
    #print(tokenizer.vocab)
    a="Originated as the Imperial University of Peking in 1898, Peking University was China’s first national comprehensive university and the supreme education authority at the time. Since the founding of the People’s Republic of China in 1949, it has developed into a comprehensive university with fundamental education and research in both humanities and science. The reform and opening-up of China in 1978 has ushered in a new era for the University unseen in history. And its merger with Beijing Medical University in 2000 has geared itself up for all-round and vibrant growth in such fields as science, engineering, medicine, agriculture, humanities and social sciences. Supported by the “211 Project” and the “985 Project”, the University has made remarkable achievements, such as optimizing disciplines, cultivating talents, recruiting high-caliber teachers, as well as teaching and scientific research, which paves the way for a world-class university."
    b="博士学位论文应当表明作者具有独立从事科学研究工作的能力，并在科学或专门技术上做出创造性的成果。博士学位论文或摘要，应当在答辩前三个月印送有关单位，并经同行评议。学位授予单位应当聘请两位与论文有关学科的专家评阅论文，其中一位应当是外单位的专家。评阅人应当对论文写详细的学术评语，供论文答辩委员会参考。"
    aa=tokenizer.encode(a)
    bb=tokenizer.encode(b)
    print(len(aa)/len(a))
    print(len(bb)/len(b))
    print(tokenizer.decode(aa)==a)
    print(tokenizer.decode(bb)==b)
    print(aa)
    print(bb)
