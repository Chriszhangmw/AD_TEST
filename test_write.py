

import os
import json


def get_test_by_kedaxunfei(path):
    total_num = 0
    catalog_num = 0
    text_dic = {}
    dirs = os.listdir(path)
    k = open('./test00.json', 'w', encoding='utf-8')
    for dir in dirs:
        patient_catalog = {}
        patient_name = str(dir)
        child_path = os.path.join(path,dir)
        child_files = os.listdir(child_path)
        for file in child_files:
            if file.endswith('wav'):
                total_num += 1
                file_catalogs = str(file).replace('.wav','')
                file_catalogs = file_catalogs
                catalog = file_catalogs
                catalog_num+=1
                text = "jjjj"
                print(text)
                patient_catalog[catalog] = text
        text_dic[patient_name] = patient_catalog
        json.dump(text_dic, k, indent=2,sort_keys=True,ensure_ascii=False)
        text_dic={}
        k.write('\n')
    print("total sample :",total_num,catalog_num)







get_test_by_kedaxunfei('./CER_test/20hours')








