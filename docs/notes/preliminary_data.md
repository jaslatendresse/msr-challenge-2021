# Corrective Commits

## Database Overview

**sstubs** - Original dataset

**selected_sstubs** - Sstubs commits from projects that were found in TravisTorrent 

**selected_travis** - Travis builds from the selected projects

**selected_merged** - Sstubs commits that have triggered a build in Travis

**commit_guru** - Commits from repositories that are in selected_merged 

## Commit Guru Overview

- **commit_id**: a unique ID that companies the repository id and the commit hash.
- **author_date**: the commit author date in the Unix Time format.
- **buggy**: a boolean indicated if the commit has been identified as bug inducing (fix inducing) using the SZZ algorithm.
- **repository_id**: a unique ID for the repository.
- **commit_hash**: the git commit's SHA-1 hash.
- **author_name**: the name of the commit author.
- **author_email**: the email of the commit author.
- **commit_message**: the first line of the commit message (max 70 characters).
- **is_fix_commit**: a boolean indicates if the commit is a corrective commit.
- **fixed_by**: commit hashes (separated by ;) for commits that fix changes induced by this commit.
- **files_count**: number of files changed by the commit (including none-source code files).
- **files**: paths of changed files (separated by ;).
- **bug_potential**: the probability that the commit is bug inducing (predicted using a random forest model).
- **ns**: is the number of modified subsystems.
- **ns**: is the number of modified directories.
- **nf**: is the number of modified files.
- **entropy**: is the distribution of modified code across each file.
- **la**: is lines of code added in the commit.
- **ld**: is lines of code deleted in the commit.
- **ha**: is hunks of code added in the commit.
- **hd**: is hunks of code deleted in the commit.
- **lt**: is lines of code in the modified files before the commit.
- **ndev**: is the number of developers that changed the modified files in the past.
- **age**: is the average time interval between the last and the current change of modified files.
- **nuc**: is the number of unique last changes that touched the modified files.
- **exp**: is the developer experience, measured by the number of submitted commits.
- **rexp**: is the recent developer experience in the modified files.
- **sexp**: is the developer experience on modified subsystems.

## Selected Projects (Sstubs, TravisTorrent, CommitGuru) 

Projects that correspond to the following: 
- Mature CI usage
- Use of Travis
- Have at least 10 distinct bugType 

<table>
<thead>
  <tr>
    <th>Projects</th>
    <th>Commit Guru Link</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Graylog2.graylog2-server</td>
    <td>http://commit.guru/repo/graylog2-server(master)</td>
  </tr>
  <tr>
    <td>apache.storm</td>
    <td>http://commit.guru/repo/storm(master)-1</td>
  </tr>
  <tr>
    <td>checkstyle.checkstyle</td>
    <td>http://commit.guru/repo/checkstyle(master)</td>
  </tr>
  <tr>
    <td>druid-io.druid</td>
    <td>http://commit.guru/repo/druid(master)-1</td>
  </tr>
  <tr>
    <td>facebook.presto</td>
    <td>http://commit.guru/repo/presto(master)</td>
  </tr>
  <tr>
    <td>google.closure-compiler</td>
    <td>http://commit.guru/repo/closure-compiler(master)</td>
  </tr>
  <tr>
    <td>xetorthio.jedis</td>
    <td>http://commit.guru/repo/jedis(master)</td>
  </tr>
  <tr>
    <td>apache.flink</td>
    <td></td>
  </tr>
</tbody>
</table>

## Commits in `selected_sstubs` that have triggered a CI build

`SELECT * FROM selected_sstubs LEFT JOIN selected_travis WHERE fixCommitSha1 = git_trigger_commit GROUP BY fixCommitSha1`

Yields 98 distinct commits that have triggered a CI build. 

Within the Sstubs dataset, 34 projects are found in the Travis Torrent dataset (selected_sstubs table) with 830 distinct commits. 

**98/830 (11.8%) commits have triggered a CI build** 

--- The numbers in the section below are subject to change because some Commit Guru data is still missing --- 

## Commits found in Commit Guru from `selected_sstubs`

`SELECT * FROM selected_sstubs LEFT JOIN commit_guru WHERE fixCommitSha1 = commit_hash GROUP BY fixCommitSha1`

**703/830 distinct commits are in Commit Guru - 84.7% coverage** 

`SELECT * FROM selected_sstubs LEFT JOIN commit_guru WHERE fixCommitSha1 = commit_hash AND is_fix_commit = 1 GROUP BY fixCommitSha1`

**278/830 distinct commits were flagged as "corrective" by Commit Guru - 33.5% of bug fix commits are considered corrective by Commit Guru**

## Commits found in Commit Guru from `selected_merged` (that also triggered a CI build)

`SELECT * FROM selected_merged LEFT JOIN commit_guru WHERE commit_hash = fixCommitSha1 GROUP BY fixCommitSha1`

**88/98 (89.8%) commits that triggered a CI build are in Commit Guru - slight decrease (as opposed to 100%) because apache-flink project added to set and was missing previously** 

`SELECT * FROM selected_merged LEFT JOIN commit_guru WHERE commit_hash = fixCommitSha1 AND is_fix_commit = 1 GROUP BY fixCommitSha1`

**33/98 (33.7%) commits that triggered a CI build are flagged as "corrective" by Commit Guru** 

## CI results before/after fix

**This cannot be compared with the "after" results because even though this is the previous built commit, the bug might still be IN the code and was just not "caught" yet, we need to know when the bug was actually introduced, but this is just to see what we can do with the tables** 

### Before

To obtain the previous built commit: `git_prev_built_commit` column from Travis Torrent.
Join `selected_merged` and `selected_travis` -- we want the previous built commit from selected_merged to be equal to the trigger commit of the selected_travis: 

`SELECT selected_travis.git_trigger_commit, selected_travis.tr_status FROM selected_travis LEFT JOIN selected_merged WHERE selected_travis.git_trigger_commit = selected_merged.git_prev_built_commit GROUP BY selected_travis.git_trigger_commit`

**Yields a total of 95 distinct commits** 

Compare the build status: 

`SELECT * FROM (SELECT selected_travis.git_trigger_commit, selected_travis.tr_status FROM selected_travis LEFT JOIN selected_merged WHERE selected_travis.git_trigger_commit = selected_merged.git_prev_built_commit GROUP BY selected_travis.git_trigger_commit) WHERE tr_status = 'passed'`

**71/95 (74.7%) distinct commits that triggered a CI build passed before the "bug fix" is introduced**

**24/95 (25.3%) distinct commits that triggered a CI build either "errored" or "failed" before the bug fix is introduced** 

### After 

`SELECT * FROM selected_merged WHERE tr_status = 'passed' GROUP BY fixCommitSha1`

**79/98 (79.6%) distinct commits that triggered a CI build 'passed' after the fix is introduced**

**19/98 (19.4%) distinct commits that triggered a CI build 'failed' after the fix is introduced** 






