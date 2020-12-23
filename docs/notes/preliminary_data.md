# Corrective Commits

## Database Overview

**sstubs** - Original dataset

**selected_sstubs** - Sstubs commits from projects that were found in TravisTorrent 

**selected_travis** - Travis builds from the selected projects

**selected_merged** - Sstubs commits that have triggered a build in Travis

**commit_guru** - Commits from repositories that are in selected_merged 

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
    <td></td>
  </tr>
  <tr>
    <td>checkstyle.checkstyle</td>
    <td></td>
  </tr>
  <tr>
    <td>druid-io.druid</td>
    <td>http://commit.guru/repo/druid(master)-1</td>
  </tr>
  <tr>
    <td>facebook.presto</td>
    <td></td>
  </tr>
  <tr>
    <td>google.closure-compiler</td>
    <td></td>
  </tr>
  <tr>
    <td>xetorthio.jedis</td>
    <td>http://commit.guru/repo/jedis(master)</td>
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

**690/830 distinct commits are in Commit Guru - 83.1% coverage** 

`SELECT * FROM selected_sstubs LEFT JOIN commit_guru WHERE fixCommitSha1 = commit_hash AND Classification = 'Corrective' GROUP BY fixCommitSha1`

**545/830 distinct commits were flagged as "corrective" by Commit Guru - 65.7% of bug fix commits are considered corrective by Commit Guru**

## Commits found in Commit Guru from `selected_merged` (that also triggered a CI build)

`SELECT * FROM selected_merged LEFT JOIN commit_guru WHERE commit_hash = fixCommitSha1 GROUP BY fixCommitSha1`

**98/98 (100%) commits that triggered a CI build are in Commit Guru** 

`SELECT * FROM selected_merged LEFT JOIN commit_guru WHERE commit_hash = fixCommitSha1 AND Classification = 'Corrective' GROUP BY fixCommitSha1`

**87/98 (88.8%) commits that triggered a CI build are flagged as "corrective" by Commit Guru** 

## CI results before/after fix

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

**78/98 (79.6%) distinct commits that triggered a CI build 'passed' after the fix is introduced**

**20/98 (20.4%) distinct commits that triggered a CI build 'failed' after the fix is introduced** 






