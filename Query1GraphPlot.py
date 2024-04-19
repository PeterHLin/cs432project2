import pandas as pd
import matplotlib.pyplot as plt


likes_df = pd.read_csv("all_users_likes.csv")
retweets_df = pd.read_csv("all_users_retweets.csv")
description_lengths_df = pd.read_csv("all_users_description_lengths.csv")


merged_df = pd.merge(description_lengths_df, likes_df, left_index=True, right_index=True)
merged_df = pd.merge(merged_df, retweets_df, left_index=True, right_index=True)


plt.figure(figsize=(8, 6))
plt.scatter(merged_df["description_length"], merged_df["likes"])
plt.title("Likes vs. Description Length")
plt.xlabel("Description Length")
plt.ylabel("Likes")
plt.grid(True)
plt.show()


plt.figure(figsize=(8, 6))
plt.scatter(merged_df["description_length"], merged_df["retweets"])
plt.title("Retweets vs. Description Length")
plt.xlabel("Description Length")
plt.ylabel("Retweets")
plt.grid(True)
plt.show()

