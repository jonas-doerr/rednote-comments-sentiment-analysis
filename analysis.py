import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


def load_data():
    folder = Path("Comments data")
    files = sorted(folder.glob("*.xlsx"))
    chinese_media_files = {
    "情书视频评论数据.xlsx",
    "活着视频评论数据.xlsx",
    "狂人日记视频评论数据.xlsx",
    }

    dataframes = []

    for i, file in enumerate(files, start = 1):
        df = pd.read_excel(file)
        df["video_id"] = i

        if file.name in chinese_media_files:
            df["category"] = "Chinese Media"
        else:
            df["category"] = "Chinglish Challenge"

        dataframes.append(df)

    data = pd.concat(dataframes, ignore_index=True)

    return data

def clean_data(data):
     # Replace "赞" with 0
    data["点赞数"] = data["点赞数"].replace("赞", 0)

    # Convert likes to numeric
    data["点赞数"] = pd.to_numeric(
        data["点赞数"],
        errors="coerce"
    )

    # Remove blank comments
    data = data[
        data["评论内容"].notna() &
        (data["评论内容"].astype(str).str.strip() != "")
    ].copy()

    # Calculate comment length
    data["comment_length"] = (
        data["评论内容"].astype(str).str.len()
    )

    return data

def balance_data(data):

    n = data.groupby("video_id").size().min()

    balanced_data = (
        data.groupby("video_id", group_keys=False)
        .sample(n=n, random_state=42)
        .reset_index(drop=True)
    )

    return balanced_data

def save_data(data, balanced_data):

    data.to_csv(
        "combined_comments.csv",
        index=False,
        encoding="utf-8-sig"
    )

    balanced_data.to_csv(
        "balanced_comments.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("Datasets successfully saved.")

def analyze_data(data):
    summary = data.groupby("category").agg(
        total_comments=("评论内容", "count"),
        average_likes=("点赞数", "mean"),
        median_likes=("点赞数", "median"),
        average_length=("comment_length", "mean"),
        median_length=("comment_length", "median")
    )

    video_summary = data.groupby(
        ["video_id", "category"]
    ).agg(
        total_comments=("评论内容", "count"),
        average_likes=("点赞数", "mean"),
        median_likes=("点赞数", "median"),
        average_length=("comment_length", "mean")
    )

    print("\nCategory Summary:")
    print(summary)

    print("\nIndividual Video Summary:")
    print(video_summary)

    print("\nMissing Likes:")
    print(data["点赞数"].isna().sum())

    return summary, video_summary

def validate_data(data, balanced_data):

    print("\nOriginal comment counts:")
    print(data.groupby(["video_id", "category"]).size())

    print("\nBalanced comment counts:")
    print(balanced_data.groupby(["video_id", "category"]).size())

    print("\nMissing like counts:")
    print(data["点赞数"].isna().sum())

    print("\nCategory counts:")
    print(balanced_data["category"].value_counts())

def visualize_data(data):

    data.boxplot(
        column="comment_length",
        by="category"
    )

    plt.title("Comment Length by Video Category")
    plt.suptitle("")
    plt.xlabel("Video Category")
    plt.ylabel("Characters per Comment")

    plt.tight_layout()
    plt.show()

def main():

    data = load_data()

    data = clean_data(data)

    balanced_data = balance_data(data)

    analyze_data(balanced_data)

    validate_data(data, balanced_data)

    visualize_data(balanced_data)

    # save_data(data, balanced_data)

if __name__ == "__main__":
    main()