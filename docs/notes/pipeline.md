# The pipeline to format the data

1. Create a new database DONE
2. Create the table `sstubs` (original dataset) from the python script. DONE

3. On TravisTorrent, query the dataset to obtain JSON files of new added projects. DONE 
4. Create TravisTorrent table `selected_travis_torrent` with the python script. DONE
5. Format `selected_travis_torrent` to `selected_travis_torrent_formatted` with the following: 

`UPDATE selected_travis SET gh_commits_in_push = REPLACE(gh_commits_in_push, '#', ',')`

 **add test bool and test log** 
 
 `CREATE TABLE selected_travis_formatted AS WITH RECURSIVE split(tr_build_id, tr_status, git_trigger_commit, gh_project_name, gh_is_pr, gh_commits_in_push, str) AS ( SELECT tr_build_id, tr_status, git_trigger_commit, gh_project_name, gh_is_pr, '', gh_commits_in_push||',' FROM selected_travis UNION ALL SELECT tr_build_id, tr_status, git_trigger_commit, gh_project_name, gh_is_pr, substr(str, 0, instr(str,',')), substr(str, instr(str,',')+1) FROM split WHERE str!='' ) 
 SELECT tr_build_id, tr_status, git_trigger_commit, gh_project_name, gh_is_pr, gh_commits_in_push FROM split WHERE gh_commits_in_push!='';`
 
 6. Create table `selected_sstubs` from the python script. DONE
 7. Create table `commit_guru` with the python script. 
 8. Format table `commit_guru` to `commit_guru_formatted`
 
 `UPDATE selected_travis SET gh_commits_in_push = REPLACE(fixed_by, '#', ',')`

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

9. Create the mapping table `bug_with_fix`

`CREATE TABLE bug_with_fix AS SELECT commit_guru_formatted.commit_hash as bug, selected_sstubs.fixCommitSHA1 as bug_fix, selected_sstubs.bugType FROM selected_sstubs LEFT JOIN commit_guru_formatted WHERE fixCommitSHA1 = fixed_by GROUP BY fixCommitSHA1, bugTYpe`

## How long do bugs stay in the code? 

1. First, need to create a selected_sstubs table that contains commits that are in commit guru so we can access the author date:

`CREATE TABLE selected_sstubs_with_date AS SELECT bugType, fixCommitSHA1, fixCommitParentSHA1, projectName, author_date, is_fix_commit FROM selected_sstubs LEFT JOIN commit_guru_formatted WHERE fixCommitSHA1 = commit_hash`

2. Second, we query to check if a commit from this table is found in the fixed_by column of the commit_guru_formatted table:

`SELECT selected_sstubs_with_date.author_date as fix_date, commit_guru_formatted.author_date as bug_date FROM selected_sstubs_with_date LEFT JOIN commit_guru_formatted WHERE fixCommitSHA1 = fixed_by`

Then use the google sheet for calculations. 

