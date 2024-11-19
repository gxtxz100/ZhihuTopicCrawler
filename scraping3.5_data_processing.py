# authors to token and drop duplicates
# Last Run: 2024/11/16 15:05

import os
import pandas as pd

#TODO:设置好文件路径
folder_path = "data/answers_of_question"  # 文件夹路径
filename_list = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(".csv")]

dfs = (pd.read_csv(file) for file in filename_list)

merged_df = pd.concat(dfs, axis=0, ignore_index=True)
user_token_df = merged_df.loc[:, ["au_urltoken", "au_name"]].drop_duplicates(subset=["au_urltoken"])

merged_df.to_csv("data/all_answers.csv", index=False, encoding="utf-8")
user_token_df.to_csv("data/user_tokens.csv", index=False, encoding="utf-8", header=False)

print(
    f"所有回答已合并保存到 data/all_answers.csv 文件中, 共有 {len(filename_list)} 个问题，包含 {len(merged_df)} 条回答"
)
print(
    f"用户清单已保存到 data/user_tokens.csv 文件中, 共获取 {len(user_token_df)} 个不重复用户token"
)
