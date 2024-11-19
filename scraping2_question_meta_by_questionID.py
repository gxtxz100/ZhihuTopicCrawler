# # Get question meta-data for a given question ID

# ### About this script:

# - **Input**: A list of question ID
# - **Output**: A list of question meta-data by question ID: Question Text, Answer Count, Follower Count, View Count, Tags
# Last Run: 2024/11/16 12:51


import os
import time
import pandas as pd
from bs4 import BeautifulSoup as bs
from get_url_text import get_url_text


def get_question_list(filename):
    df = pd.read_csv(filename)
    # 可添加筛选条件
    df = df[df["type"] != "专栏"]
    df = df[df["date"] >= "2024-10-14"]
    q_list = df.values.tolist()
    return q_list

def get_question_data(html_text):

    try:
        bsobj = bs(html_text, "html.parser")

        qContent = bsobj.find_all("meta", attrs={"itemprop": "name"})[0]["content"]
        followerCount = bsobj.find_all("strong", attrs={"class": "NumberBoard-itemValue"})[0]["title"]
        viewCount = bsobj.find_all("strong", attrs={"class": "NumberBoard-itemValue"})[1]["title"]
        answerCount = bsobj.find_all("meta", attrs={"itemprop": "answerCount"})[0]["content"]
        topicTag = bsobj.find_all("meta", attrs={"itemprop": "keywords"})[0]["content"]
        date = bsobj.find_all("meta", attrs={"itemprop": "dateCreated"})[0]["content"]

        return [q_id, qContent, followerCount, viewCount, answerCount, topicTag, date[:10]]

    except:
        print("Unknown Error !")
        return [
            q_id,
            "UnknownError",
            "UnknownError",
            "UnknownError",
            "UnknownError",
            "UnknownError",
            "UnknownError",
        ]

def save_data(q_info_list, filename):
    df = pd.DataFrame(
        q_info_list,
        columns=[
            "q_id",
            "q_content",
            "followerCount",
            "viewCount",
            "answerCount",
            "topicTag",
            "created_date"
        ],
    )
    if os.path.exists(filename):
        df_old = pd.read_csv(filename)
        df = pd.concat([df_old, df], ignore_index=True)
        df = df[df["q_content"] != "UnknownError"]  # 删除已经被删除的问题
        df = df.drop_duplicates(subset=["q_id"], keep="last")
        df["created_date"] = df["created_date"].str.replace("-", "/")
        df["created_date"] = pd.to_datetime(df["created_date"])
        df = df.sort_values(by=["created_date"])
        
    df.to_csv(filename, index=False, header=True, encoding="utf-8")


# 代码一次只能跑250条，之后会变乱码，需要手动去浏览器更新cookie
# 2024/11/16更新：似乎不会再变乱码了，建议保持关注
if __name__ == "__main__":
    #TODO 指定问题列表
    q_list = get_question_list("data/question_list.csv")
    print(f"共{len(q_list)}个问题")
    q_info_list = []

    #TODO 可设置开始和结束位置，用于在出错中断时重新爬取
    for i, item in enumerate(q_list[:]):
        q_id = item[1]

        url = f"https://www.zhihu.com/question/{str(q_id)}"
        text = get_url_text(url)
        q_info = get_question_data(text)
        q_info_list.append(q_info)

        if i % 30 == 0:
            print(q_info[1])
            save_data(q_info_list, "data/question_meta_info.csv")
            q_info_list = []
            time.sleep(1)
            print(f"已保存{i+1}条数据")

    save_data(q_info_list, "data/question_meta_info.csv")

    print("Finish!!")
