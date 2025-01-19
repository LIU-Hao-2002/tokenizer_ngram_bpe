# coding: utf-8
# File: train_ngram.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-3-27
# 本代码借鉴github仓如上
import jieba
import time
import os
import pickle	
def load_dp(gold_cut_path,pred_cut_path='./valid_seg_result1.txt',limit=2400):
    with open(pred_cut_path,'r',encoding='utf-8') as f:
        pred_cut_list = f.readlines()
    pred_cut_list = [x.strip() for x in pred_cut_list] # space seperated string
    pred_cut_list = [x.split(' ') for x in pred_cut_list][:limit] # list of words
    if os.path.exists(gold_cut_path):
        with open(gold_cut_path,'rb') as f:
            gold_cut_list = pickle.load(f)
    else:
        gold_cut_list = []
        for sentence in pred_cut_list:
            sentence=''.join(sentence)
            gold_cut=list(jieba.cut(sentence))
            gold_cut_list.append(gold_cut) #
        with open(gold_cut_path,'wb') as f:
            pickle.dump(gold_cut_list,f)
    return pred_cut_list, gold_cut_list
	
def score(gold_cut_path,pred_cut_path='./valid_seg_result1.txt'):
    start_time = time.time()
    count = 1
    count_right = 0
    count_split = 0
    count_gold = 0
    process_count = 0
    pred_cut_list, gold_cut_list=load_dp(gold_cut_path, pred_cut_path)
    for inlist,goldlist in zip(pred_cut_list,gold_cut_list):
        process_count += 1
        if process_count % 1000 == 0:
            print(process_count)
        count += 1
        count_split += len(inlist)
        count_gold += len(goldlist)
        tmp_in = inlist
        tmp_gold = goldlist

        for key in tmp_in:
            if key in tmp_gold:
                count_right += 1
                tmp_gold.remove(key)

        P = count_right / count_split
        R = count_right / count_gold
        F = 2 * P * R / (P + R)

    end_time = time.time()
    cost = (end_time - start_time)
    print(P, R, F, cost,process_count)
    return P, R, F, cost


if __name__ == "__main__":
	gold_cut_path = './jieba_cut_valid.pkl'
	P, R, F, cost = score(gold_cut_path,pred_cut_path="/root/computer_final/seg_result_valid_r1.txt")



		

