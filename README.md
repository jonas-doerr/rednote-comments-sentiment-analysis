# Strangers in the Comment Section
**An introductory analysis of Chinese-language comments on an American creator's RedNote (小红书) videos**

*Pilot study · Jonas Doerr (乔烁) · Hubei University · 2026*

📄 **Read the paper:** [English (PDF)](paper/Strangers_in_the_Comment_Section_EN.pdf) · [中文 (PDF)](paper/Strangers_in_the_Comment_Section_ZH.pdf)

---

## Summary

How do Chinese netizens react when a foreigner makes Chinese-language content, and does the *type* of content change the kind of conversation that follows?

I compared comments on two kinds of videos from one creator's RedNote account:

| Category | Videos | Length |
|---|---|---|
| **"Chinglish Challenge"** (Chinglish and internet-meme content) | 3 | 10–20 sec |
| **"Chinese Media"** (discussion of Chinese books and films) | 3 | 1–3 min |

**Sample:** 43 randomly sampled comments per video, 258 in total (drawn from [TODO: total number scraped] scraped comments).

**Methods:** descriptive statistics (likes, comment length), hand-coded thematic analysis with a codebook (including a re-coding check), and sentiment analysis with [SnowNLP](https://github.com/isnowfy/snownlp).

### Main findings

- **Length:** comments on the "Chinese Media" videos were much longer (all three averaged over 35 characters) than on the "Chinglish Challenge" videos (none above 15).
- **Themes:** "Chinglish" comments were dominated by humor and quick reactions; "Media" comments centered on culture/society and national identity.
- **Sentiment:** SnowNLP scored "Media" comments as more positive, but humor, memes and sarcasm make this the least reliable part of the analysis (see Limitations).
- **Likes:** only a loose relationship with video type.

<p align="center">
  <img src="Outputs\Thematic Differences Between Video Categories.png" width="70%" alt="Thematic differences between video categories">
</p>

## Limitations (short version)

One creator, six videos, 258 coded comments, and the researcher is also the creator. Video length, topic and language use are confounded with video type, and SnowNLP is not designed for memes and sarcasm. This is a **feasibility pilot**, not a generalizable result. See the paper for details and for directions for follow-up work (other creators, BiliBili/Douyin, larger samples).

## Repository contents

```
├── paper/        Full paper (EN and ZH, PDF)
├── Outputs/      Figures 1–4 (PNG) as well as supplemental data
├── codebook/     Thematic coding codebook: definitions and explanation
├── data/         Aggregated results and anonymized coded sample (no raw comment text)
├── analysis.py   Python scripts for sampling, descriptives, sentiment, coding summaries, figures
├── requirements.txt
├── CITATION.cff
└── LICENSE
```

## Reproducing the analysis

```bash
git clone https://github.com/jonas-doerr/rednote-comments-sentiment-analysis.git
cd rednote-foreigner-comments-pilot
pip install -r requirements.txt
python analysis.py
```

## Data and privacy

Usernames, locations and any other identifying fields were removed. **Raw comment text is not redistributed** in this repository, out of respect for commenters' privacy and platform terms. Researchers who want the underlying text for replication or extension are welcome to contact me.

## Cite this work

See [`CITATION.cff`](CITATION.cff), or:

> Doerr, J. (2026). *Strangers in the Comment Section: An Introductory Analysis of Comments on an American's RedNote Videos.* GitHub repository.

## License

Code: MIT · Paper, figures and codebook: CC BY 4.0

## Contact

Jonas Doerr (乔烁) · [jonasdoerr2@gmail.com]

---

## 中文简介

本研究是一项探索性的小规模研究,关注中国网友如何回应外国人用中文创作的内容。研究者以一位美国创作者在小红书上的六条视频为样本(三条"中式英语挑战"类、三条"中国书籍与电影"类),对共 258 条随机抽样评论进行了描述性统计、人工主题编码和 SnowNLP 情感分析。

初步发现:短视频的评论以幽默和即时反应为主,篇幅较短;谈论中国书籍和电影的较长视频则引发更长、更偏向文化与社会、国家认同话题的讨论。由于样本仅来自一位创作者的六条视频,且研究者本人即为创作者,本研究只能作为可行性试点,结论不宜推广。

完整中文论文见 [`paper/Strangers_in_the_Comment_Section_ZH.pdf`](paper/Strangers_in_the_Comment_Section_ZH.pdf)。