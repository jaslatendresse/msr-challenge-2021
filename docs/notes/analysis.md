## Quantitative Questions

- How many commits triggered the CI (must be a PR/part of a PR)? 
- How many are part of the PR (in the list)? 
- How long do bugs stay in the code before they are fixed?
    - If a long time, maybe it was assumed they were not risky? 

## Qualitative Questions

- Why doesn't the CI pipeline catch certain bugs? 
- When bugs are fixed, are tests added to the code? 
- Is the bug covered by a test? 

Include commits that are not aprt of the CI table. 

## Research Questions

- What percentage of bugs are caught by the CI? 
- If not caught, why? 


## Quantitative Data 

How many commits triggered the CI? This can be split into the following questions: 

1. How many commits are pull requests? 
2. How many commits are part of pull requests? 
3. How many commits just go straight into the main branch without triggering anything? 

For this, I will query the join table of `selected_sstubs` and `selected_travis` because we want CI data from the projects we selected. I will NOT use `selected_merged` because this table only contains commits that triggered a build. 

**For question 1: How many commits are pull requests?**

How many commits are in the join of `selected_sstubs` and `selected_travis` ? (In other words, how many commits in `selected_sstubs` triggered a build?)

`SELECT * FROM selected_sstubs LEFT JOIN selected_travis WHERE fixCommitSha1 = git_trigger_commit GROUP BY fixCommitSha1`

**98 distinct commits have triggered a CI build (out of 830 total distinct commits in `selected_sstubs`)** 

How many commits are PRs? 

```
SELECT * FROM
(SELECT * FROM selected_sstubs LEFT JOIN selected_travis WHERE fixCommitSha1 = git_trigger_commit GROUP BY fixCommitSha1)
WHERE gh_is_pr = 'True'
```

**6 distinct commits that have triggered a CI build are pull requests (6.12%)**

```
SELECT * FROM
(SELECT * FROM selected_sstubs LEFT JOIN selected_travis WHERE fixCommitSha1 = git_trigger_commit GROUP BY fixCommitSha1)
WHERE gh_is_pr = 'False'
```

**92 distincts commits that have triggered a CI build are NOT pull requests (93.88%)**

We want to see if this number (92) corresponds to the number of commits that are part of the "part of the build, but not a PR" list. For this: write a script that will query the `selected_travis` table and obtain the `gh_commits_in_push` to get the list of all commits that are part of a build. Then, for each build, we will check if the commits in `selected_sstubs` that are not PR are part of the aforementioned list. This will give us an idea of the proportion of commits that are caught by the CI. 


