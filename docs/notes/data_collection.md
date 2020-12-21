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

**196/830 distinct commits are in Commit Guru** 

`SELECT * FROM selected_sstubs LEFT JOIN commit_guru WHERE fixCommitSha1 = commit_hash AND Classification = 'Corrective' GROUP BY fixCommitSha1`

**166/830 distinct commits were flagged as "corrective" by Commit Guru**

## Commits found in Commit Guru from `selected_merged` (that also triggered a CI build)

`SELECT * FROM selected_merged LEFT JOIN commit_guru WHERE commit_hash = fixCommitSha1 GROUP BY fixCommitSha1`

**45/98 (45.9%) commits that triggered a CI build are in Commit Guru** 

`SELECT * FROM selected_merged LEFT JOIN commit_guru WHERE commit_hash = fixCommitSha1 AND Classification = 'Corrective' GROUP BY fixCommitSha1`

**41/98 (41.8%) commits that triggered a CI build are flagged as "corrective" by Commit Guru** 




