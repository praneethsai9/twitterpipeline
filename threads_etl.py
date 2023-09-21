#!/usr/bin/env python
import threads as th
import json
import pandas as pd

def print_json_tree(data, level=0):
    if isinstance(data, dict):
        for key, value in data.items():
            print("  " * level + f"{key}:")
            print_json_tree(value, level + 1)
    elif isinstance(data, list):
        for item in data:
            print_json_tree(item, level + 1)
    else:
        print("  " * level + str(data))

def extract_specific_keys(data, keys_to_extract):
    results = {key: [] for key in keys_to_extract}

    def extract_recursive(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if key in keys_to_extract:
                    results[key].append(value)
                elif isinstance(value, (dict, list)):
                    extract_recursive(value)
        elif isinstance(data, list):
            for item in data:
                extract_recursive(item)

    extract_recursive(data)
    return results

def run_threads_etl():
    threads=th.Threads()
    user_id=314216
    user_threads = threads.public_api.get_user_threads(user_id)
    ut=json.dumps(user_threads, indent=4)
    ut=json.loads(ut)
    user = threads.public_api.get_user(id=user_id)
    keys_to_extract = ["username","caption", "like_count","taken_at"]
    extracted_data = extract_specific_keys(ut, keys_to_extract)
    res=json.dumps(extracted_data, indent=4)
    res=json.loads(res)
    captions_list = [caption["text"] for caption in res["caption"]]
    res["caption"] = captions_list
    counts = {key: len(value) for key, value in res.items()}
    rep_len=len(res["caption"])
    res["username"]=[res["username"][0]]*rep_len
    res["user_id"]=[user_id]*rep_len
    counts = {key: len(value) for key, value in res.items()}
    df=pd.DataFrame(res)
    df.to_csv("sample_data.csv")