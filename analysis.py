import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

folder = Path("Comments data")
files = sorted(folder.glob("*.xlsx"))
dataframes = []

chinese_media_files = {
    "情书视频评论数据.xlsx",
    "活着视频评论数据.xlsx",
    "狂人日记视频评论数据.xlsx",
}

for i, file in enumerate(files, start = 1):
    df = pd.read_excel(file)
    df["video_id"] = i

    if file.name in chinese_media_files:
        df["category"] = "Chinese Media"
    else:
        df["category"] = "Chinglish Challenge"

    dataframes.append(df)

#standardize like counts and remove empty comments
data = pd.concat(dataframes, ignore_index = True)
data["点赞数"] = data["点赞数"].replace("赞", 0)
data = data[
    data["评论内容"].notna() &
    (data["评论内容"].astype(str).str.strip() != "")
]

# print(data.head())
# print(data.shape)
# print(data.info())

#Save combined comments as csv file
data.to_csv(
    "combined_comments.csv",
    index=False,
    encoding="utf-8-sig"
)

#Create csv with equal number of comments per video (should be 43)
n = data.groupby("video_id").size().min()
balanced_data = (
    data.groupby("video_id", group_keys = False)
    .sample(n=n, random_state = 42)
    .reset_index(drop = True)
)

# print(balanced_data.groupby(["video_id", "category"]).size())
balanced_data.to_csv(
    "balanced_comments.csv",
    index = False,
    encoding = "utf-8-sig"
)

# Convert likes into numeric values, get comment length
balanced_data["点赞数"] = pd.to_numeric(
    balanced_data["点赞数"],
    errors="coerce"
)
print(data["点赞数"].isna().sum())
balanced_data["comment_length"] = balanced_data["评论内容"].astype(str).str.len()

# Group statistics by category
summary = balanced_data.groupby("category").agg(
    total_comments=("评论内容", "count"),
    average_likes=("点赞数", "mean"),
    median_likes=("点赞数", "median"),
    average_length=("comment_length", "mean"),
    median_length=("comment_length", "median")
)

print(summary)

#create data visualization
balanced_data.boxplot(
    column="comment_length",
    by="category"
)

plt.title("Comment Length by Video Category")
plt.suptitle("")
plt.xlabel("Video Category")
plt.ylabel("Characters per Comment")

plt.show()