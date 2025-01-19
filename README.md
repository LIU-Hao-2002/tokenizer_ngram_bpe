# 介绍
本代码仓记录某次关于分词实践的期末大作业，已做数据脱敏处理。代码和报告的参考源已清晰列出。
# 结构
```
.
├── computer_final
│   ├── bpe
│   │   ├── bbpe_tokenizer.py
│   │   ├── bpe_chn_tokenizer.py
│   │   └── bpe_eng_tokenizer.py
│   ├── model
│   │   ├── trans_dict_2.model
│   │   ├── trans_dict.model
│   │   ├── word_dict_2.model
│   │   └── word_dict.model
│   └── ngram
│       ├── build_vocab.py
│       ├── evaluate.py
│       ├── forward_cut.py
│       ├── load_data.py
│       ├── max_prob_cut.py
│       ├── train.py
│       └── visualization.py
├── README.md
└── 分词原理和实践.pdf
```