## Quantitative Questions

- How many commits triggered the CI (must be a PR/part of a PR)? 
- How many are part of the PR (in the list)? 
- How long do bugs stay in the code before they are fixed?
    - If a long time, maybe it was assumed they were not risky? 

## Qualitative Questions

- Why doesn't the CI pipeline catch certain bugs? 
- When bugs are fixed, are tests added to the code? 
- Is the bug covered by a test? 

Include commits that are not part of the CI table. 

## Research Questions

- What percentage of bugs are caught by the CI? 
- If not caught, why? 


## Quantitative Data 

### How many commits triggered the CI? 

This can be split into the following questions: 

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
SELECT * FROM selected_sstubs LEFT JOIN selected_travis WHERE gh_is_pr = 'True' AND fixCommitSHA1 = git_trigger_commit GROUP BY fixCommitSha1
```

**12 distinct commits that have triggered a CI build are pull requests (12.2%)**

```
SELECT * FROM selected_sstubs LEFT JOIN selected_travis WHERE gh_is_pr = 'False' AND fixCommitSHA1 = git_trigger_commit GROUP BY fixCommitSha1
```

**94 distincts commits that have triggered a CI build are NOT pull requests (95.9%)**

We want to see if this number (94) corresponds to the number of commits that are part of the "part of the build, but not a PR" list. For this: write a script that will query the `selected_travis` table and obtain the `gh_commits_in_push` to get the list of all commits that are part of a build. Then, for each build, we will check if the commits in `selected_sstubs` that are not PR are part of the aforementioned list. This will give us an idea of the proportion of commits that are caught by the CI. 

After running the script to extract the `gh_commits_in_push`, I used the same query as above to get the commits that are not a PR but that have triggered a build and compared the lists. 

**83 distinct NON-PR commits that have triggered a CI build are part of the list of commits in the push that have triggered the build (88.3%)** 

(??) This leaves us with 11 commits that are not PR nor appear in the list of commits in the push that triggered a build but that triggered a build.  

**How many commits do not trigger the CI?**

i.e. commits that just go straight to master: commits that are not PRs and commits that are not in the gh_commits_in_push list.

To answer this question, I need commits from the `selected_sstubs` set since it contains commits from projects that are also in the Travis Torrent set, but it doesn't mean all commits are in the builds. 

## How long do bugs stay in the code? 

In Commit Guru, there is a column called **'fixed_by': commit hashes (separated by ;) for commits that fix changes induced by this commit.**

If a commit from `selected_sstubs` is found in the list of  `fixed_by` commits, then we can trace back to the commit that introduced the bug and get the time stamp. 

In short, we want the row for which a `selected_sstubs` fix commit is found in the 'fixed_by' column. 

**Problem**: The column fixed_by is a string of commits separated by a semicolon. I need to extra the full row with multiple columns to get all the data I need. My script only works for extracting one column and returns the value of the column as a list of strings. 

Pandas (with Python) explode function could not be used in this case because the fixed_by column values were not lists, but strings separated with a semicolon. 

**Solution**:

**Replace ';' with ',' in the fixed_by column from commit_guru table**: 

`UPDATE commit_guru
SET fixed_by = REPLACE(fixed_by, ';', ',')`

**Split the fixed_by column into multiple rows (for each comma separated string) and create new table from the output**: 

`CREATE TABLE commit_guru_formatted AS
WITH RECURSIVE split(commit_id, commit_hash, buggy, repository_id, author_date, is_fix_commit, fixed_by, str) AS (
SELECT commit_id, commit_hash, buggy, repository_id, author_date, is_fix_commit, '', fixed_by||',' FROM commit_guru
UNION ALL SELECT
commit_id, commit_hash, buggy, repository_id, author_date, is_fix_commit,
substr(str, 0, instr(str,',')),
substr(str, instr(str,',')+1)
FROM split WHERE str!=''
)
SELECT commit_id, commit_hash, buggy, repository_id, author_date, is_fix_commit, fixed_by
FROM split
WHERE fixed_by!='';`

Now, to know how long the bugs stayed in the code before they were fixed, I need verify if the selected_sstubs commits are in the commit_guru_formatted table to obtain the timestamp. If yes, then I will check if a selected_sstubs commit is in the fixed_by column. From this, I will get the author_date of the commit that is fixed and compare it with the author date of the fix commit. 

First, need to create a selected_sstubs table that contains commits that are in commit guru so we can access the author date: 

`CREATE TABLE selected_sstubs_with_date AS
SELECT bugType, fixCommitSHA1, fixCommitParentSHA1, projectName, author_date, is_fix_commit FROM selected_sstubs 
LEFT JOIN commit_guru_formatted WHERE fixCommitSHA1 = commit_hash`

This results in 362 rows. 

Second, we query to check if a commit from this table is found in the fixed_by column of the commit_guru_formatted table:

`SELECT selected_sstubs_with_date.author_date as fix_date, commit_guru_formatted.author_date as bug_date FROM selected_sstubs_with_date LEFT JOIN commit_guru_formatted WHERE fixCommitSHA1 = fixed_by `

We obtain 370 rows. 

Now we can compare the unix time stamps and make an average. 

Calculations and data can be found here: 
https://docs.google.com/spreadsheets/d/1mDu3_304ECtOc7F6QlLUJYC-jE4Z-PnEeejnM7c3v6w/edit?usp=sharing

Still need to determine if we should remove duplicate rows, if so, modify GROUP BY in query? 

## Bugs not caught by the CI:

Before anything, I formatted the travis torrent table by exploding the gh_commits_in_push column as I did above for the commit guru table. 

`UPDATE selected_travis
SET fixed_by = REPLACE(fixed_by, '#', ',')`

 `CREATE TABLE selected_travis_formatted AS WITH RECURSIVE split(tr_build_id, tr_status, git_trigger_commit, gh_project_name, gh_is_pr, gh_commits_in_push, str) AS ( SELECT tr_build_id, tr_status, git_trigger_commit, gh_project_name, gh_is_pr, '', gh_commits_in_push||',' FROM selected_travis UNION ALL SELECT tr_build_id, tr_status, git_trigger_commit, gh_project_name, gh_is_pr, substr(str, 0, instr(str,',')), substr(str, instr(str,',')+1) FROM split WHERE str!='' ) SELECT tr_build_id, tr_status, git_trigger_commit, gh_project_name, gh_is_pr, gh_commits_in_push FROM split WHERE gh_commits_in_push!='';`

First, we need to trace back to the commit when the bug was introduced. For This, we join the commit_guru table and the selected_sstubs table and select the commit_hash of commit guru for which a selected_sstubs fix commit appears in the fixed_by column. Since we want a unique pair of fix-bugtype, we group by this pair: 

`CREATE TABLE bug_with_fix AS SELECT commit_guru_formatted.commit_hash as bug, selected_sstubs.fixCommitSHA1 as bug_fix, selected_sstubs.bugType FROM selected_sstubs LEFT JOIN commit_guru_formatted WHERE fixCommitSHA1 = fixed_by GROUP BY fixCommitSHA1, bugTYpe`

**This results in 273 distinct (bug_hash, bugType) pairs.**

Then, we want to take those bugs and search for them in the travis torrent set: 

`SELECT bug, bug_fix, bugType FROM bug_with_fix LEFT JOIN selected_travis_formatted WHERE bug = gh_commits_in_push GROUP BY bug, bugType`

**17/273 (bug_hash, bugType) are part of a build without being the trigger of the build**

`SELECT * FROM bug_with_fix LEFT JOIN selected_travis WHERE bug = git_trigger_commit GROUP BY bug, bugType`

**8/273 pairs triggered a build**

`SELECT * FROM bug_with_fix LEFT JOIN selected_travis_formatted WHERE bug = git_trigger_commit OR bug = gh_commits_in_push GROUP BY bug, bugType`

**44/273 are caught by the CI (either trigger a build or are part of a build**

bugType in the 44 bugs that were caught by the CI: 

- 1 CHANGE_CALLER_IN_FUNCTION_CALL
- 17 CHANGE_IDENTIFIER
- 6 CHANGE_MODIFIER
- 2 CHANGE_NUMERAL
- 1 CHANGE OPERAND
- 1 CHANGE_UNARY_OPERATOR
- 1 DELETE_THROWS_EXCEPTION
- 5 DIFFERENT_METHOD_SAME_ARGS
- 1 MORE_SPECIFIC_IF
- 1 LESS_SPECIFIC_IF
- 1 OVERLOAD_METHOD_DELETED_ARGS
- 6 OVERLOAD_METHOD_MORE_ARGS
- 1 SWAP_BOOLEAN_LITERAL

Now, how long did those bugs stay in the code for? 

