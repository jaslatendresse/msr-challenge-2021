# %%
import pandas as pd 
import os 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# %%
lifespan_df = pd.read_csv('data/lifespan.csv')

# %%
SECONDS_TO_DAYS =  60 * 60 * 24

lifespan_df['duration (days)'] = lifespan_df['duration (unix)'] / SECONDS_TO_DAYS 


# %%
# Distribution using the traditional distplot - It does not work so well...
sns.displot(np.log10(1 + lifespan_df['duration (days)']))


# %%
sns.set_context('paper', font_scale=1.2)

# Because we don't have enough data, it is better to just bin the data and use simple bar plots
to_plot_per_bug = pd.cut(lifespan_df['duration (days)'], bins=[0,1, 7, 183, 365, 1000]).value_counts()

ax = sns.barplot(to_plot_per_bug, y=to_plot_per_bug.index, x=to_plot_per_bug, palette='Blues')

ax.set_xlabel('# of SSBugs')
ax.set_yticklabels(['less than 1 day', '2 - 7 days', '2 week - 6 months', '6 months - 1 year', '> 1 year'])


n_bugs = len(lifespan_df)
# Annotate bars
for p in ax.patches:
    width = p.get_width()
    perc = width / n_bugs * 100.0
    plt.text(15 + p.get_width(), p.get_y() + 0.55*p.get_height(),
             '{:1.2f}%'.format(perc),
             ha='center', va='center')

sns.despine()

plt.tight_layout()
plt.savefig('plots/lifespan_bar.pdf')

# %%
lifespan_commit_df = lifespan_df.drop_duplicates(subset=['bug_hash', 'fix_hash'])

to_plot_per_commit = pd.cut(lifespan_commit_df['duration (days)'], bins=[0,1, 7, 183, 365, 1000]).value_counts()

ax = sns.barplot(to_plot_per_commit, y=to_plot_per_commit.index, x=to_plot_per_commit, palette='Blues')

ax.set_xlabel('# of Commits')
ax.set_yticklabels(['less than 1 day', '2 - 7 days', '2 week - 6 months', '6 months - 1 year', '> 1 year'])


n_bugs = len(lifespan_commit_df)
# Annotate bars
for p in ax.patches:
    width = p.get_width()
    perc = width / n_bugs * 100.0
    plt.text(10 + p.get_width(), p.get_y() + 0.55*p.get_height(),
             '{:1.2f}%'.format(perc),
             ha='center', va='center')

sns.despine()

plt.tight_layout()
plt.savefig('plots/lifespan_bar_commit.pdf')


# %%
