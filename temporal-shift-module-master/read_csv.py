# -*- coding:utf8 -*-
import os
import csv
import json


if __name__ == '__main__':
    csv_file = '/nfs/volume-95-7/temporal-shift-module/TSM_labeling_results.csv'

    dict1 = dict()
    gt_json = '/nfs/volume-95-7/illegal_parking/dataset/stop_results_v2.json'

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)

        for i, row in enumerate(reader):
            if i == 0:
                continue
            file_key = row[7]
            results = row[10]

            if results == '':
                results_word = []
            else:
                results_word = results.split(',')
                if '' in results_word:
                    results_word.remove('')
                results_word = list(map(int, results_word))

            print(i, file_key, results_word)
            dict1[file_key] = results_word

    with open(gt_json, 'w') as f1:
        json.dump(dict1, f1, indent=4, separators=(',', ':'))