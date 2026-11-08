import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import jieba
from collections import Counter
import re


def load_data():
    folder = Path("Comments_data")
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

def summarize_by_video(data):

    summary = data.groupby(
        ["video_id", "category"]
    ).agg(
        comment_count=("评论内容", "count"),
        median_likes=("点赞数", "median"),
        mean_likes=("点赞数", "mean"),
        median_length=("comment_length", "median"),
        mean_length=("comment_length", "mean")
    ).round(2)

    print("\nSummary by Video:")
    print(summary)

    return summary

def plot_comment_counts(data):

    counts = data.groupby(
        ["video_id", "category"]
    ).size().reset_index(name="comment_count")

    counts.plot(
        x="video_id",
        y="comment_count",
        kind="bar",
        legend=False
    )

    plt.title("Collected Comments by Video")
    plt.xlabel("Video ID")
    plt.ylabel("Number of Comments")
    plt.tight_layout()
    plt.show()

def visualize_likes_and_length(data):

    like_order = ["0", "1–5", "6–20", ">20"]

    # Assign each comment to a like-count group
    data = data.copy()
    data["like_group"] = pd.cut(
        data["点赞数"],
        bins=[-0.1, 0, 5, 20, float("inf")],
        labels=like_order
    )

    # Calculate median comment length for each group
    summary = (
        data.groupby(
            ["like_group", "category"],
            observed=False
        )["comment_length"]
        .median()
        .unstack()
    )

    summary = summary.reindex(like_order)

    # Create grouped bar chart
    ax = summary.plot(
        kind="bar",
        figsize=(10, 6),
        width=0.8
    )

    ax.set_title("Median Comment Length by Like Count and Category")
    ax.set_xlabel("Number of Likes")
    ax.set_ylabel("Median Comment Length (Characters)")
    ax.legend(title="Video Category")
    ax.tick_params(axis="x", rotation=0)

    plt.tight_layout()
    plt.show()

def visualize_video_averages(data):

    video_summary = data.groupby(
        ["video_id", "category"]
    ).agg(
        average_likes=("点赞数", "mean"),
        average_length=("comment_length", "mean")
    ).reset_index()

    # Create labels for the six videos
    video_summary["video_label"] = (
        "Video " + video_summary["video_id"].astype(str)
        + "\n" + video_summary["category"]
    )

    # Two panels because the measurements use different units
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Average likes
    axes[0].bar(
        video_summary["video_label"],
        video_summary["average_likes"]
    )
    axes[0].set_title("Average Likes per Video")
    axes[0].set_ylabel("Average Number of Likes")
    axes[0].tick_params(axis="x", rotation=45)

    # Average comment length
    axes[1].bar(
        video_summary["video_label"],
        video_summary["average_length"]
    )
    axes[1].set_title("Average Comment Length per Video")
    axes[1].set_ylabel("Average Characters per Comment")
    axes[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.show()

def normalize_token(word):
    # Combine repeated Chinese laughter
    if re.fullmatch(r"哈{2,}", word):
        return "哈哈"

    return word

def tokenize_comments(data):

    data = data.copy()

    stopwords = {
        "的", "了", "是", "我", "你", "他", "她",
        "我们", "他们", "这个", "那个", "一个",
        "也", "都", "就", "在", "有", "和",
        "很", "还", "不", "啊", "吗", "吧"
    }

    data["tokens"] = data["评论内容"].astype(str).apply(
        lambda comment: [
            normalize_token(word.strip())
            for word in jieba.lcut(comment)
            if word.strip()
            and normalize_token(word.strip()) not in stopwords
            and len(normalize_token(word.strip())) > 1
        ]
    )

    return data

def analyze_word_frequencies(data):

    for category in data["category"].unique():

        category_data = data[data["category"] == category]

        all_words = [
            word
            for tokens in category_data["tokens"]
            for word in tokens
        ]

        word_counts = Counter(all_words)

        print(f"\nTop 20 words: {category}")
        for word, count in word_counts.most_common(20):
            print(f"{word}: {count}")

def analyze_video_word_frequencies(data):

    for video_id in sorted(data["video_id"].unique()):

        video_data = data[data["video_id"] == video_id]

        category = video_data["category"].iloc[0]

        all_words = [
            word
            for tokens in video_data["tokens"]
            for word in tokens
        ]

        word_counts = Counter(all_words)

        print(f"\nVideo {video_id} — {category}")

        for word, count in word_counts.most_common(15):
            print(f"{word}: {count}")


def main():

    data = load_data()

    data = clean_data(data)

    balanced_data = balance_data(data)

    analyze_data(balanced_data)

    # validate_data(data, balanced_data)

    summarize_by_video(data)

    # save_data(data, balanced_data)

    # data visualizations (uncomment to see plots, but all are listed in outputs)
    # visualize_data(balanced_data)
    # plot_comment_counts(data)
    # visualize_likes_and_length(balanced_data)
    # visualize_video_averages(balanced_data)

    # basic tokenization and analysis
    balanced_data = tokenize_comments(balanced_data)
    analyze_word_frequencies(balanced_data)
    analyze_video_word_frequencies(balanced_data)

if __name__ == "__main__":
    main()