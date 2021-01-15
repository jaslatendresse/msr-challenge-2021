# Database Tables

### sstubs

Contains original untouched dataset from MSR. 

## selected_sstubs

Contains fix commits for simple, one-line bugs from projects that were selected: 
 
- graylog2.graylog2-server
- apache.flink
- apache.storm
- checkstyle.checkstyle
- dropwizard.dropwizard
- dropwizard.metrics
- druid-io.druid
- facebook.presto
- google.closure-compiler
- google.guava
- google.guice
- junit-team.junit
- mybatis-mybatis-3
- naver.pinpoint
- xetorthio.jedis

### Fields

- "bugType" : The bug type (16 possible values).
- "commitSHA1" : The hash of the commit fixing the bug.
- "fixCommitParentSHA1" : The hash of the last commit containing the bug.
- "commitFile" : Path of the fixed file.
- "patch" : The diff of the buggy and fixed file containing all the changes applied by the fix commit.
- "projectName" : The concatenated repo owner and repo name separated by a '.'.
- "bugLineNum" : The line in which the bug exists in the buggy version of the file.
- "bugNodeStartChar" : The character index (i.e., the number of characters in the java file that must be read before encountering the first one of the AST node) at which the affected ASTNode starts in the buggy version of the file.
- "bugNodeLength" : The length of the affected ASTNode in the buggy version of the file.
- "fixLineNum" : The line in which the bug was fixed in the fixed version of the file.
- "fixNodeStartChar" : The character index (i.e., the number of characters in the java file that must be read before encountering the first one of the AST node) at which the affected ASTNode starts in the fixed version of the file.
- "fixNodeLength" : The length of the affected ASTNode in the fixed version of the file.
- "sourceBeforeFix" : The affected AST's tree (sometimes subtree e.g. Change Numeric Literal) text before the fix.
- "sourceAfterFix" : The affected AST's tree (sometimes subtree e.g. Change Numeric Literal) text after the fix.

## selected_travis

TravisTorrent build data for the selected projects. 

### Fields

https://travistorrent.testroots.org/page_dataformat/

## commit_guru

Commit Guru data for the selected projects. 

### Fields

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
- **nd**: is the number of modified directories.
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

## selected_travis_formatted

Contains the same data as `selected_travis` but the column `gh_commits_in_push` was exploded for better manipulation of the data. 

## commit_guru_formatted

Contains the same data as `commit_guru` but the column `fixed_by` was exploded for better manipulation of the data. 

## bug_with_fix

A join of `selected_sstubs` and `commit_guru_formatted` to create a mapping between a bug and its fix. 

### Fields

- **bug**: the bug hash
- **bug_fix**: the fix hash
- **bugType**: the bug type column from `selected_sstubs`

## selected_sstubs_with_date

A join of `selected_sstubs` and `commit_guru_formatted` that contains rows where the fix hash column of `selected_sstubs` is equal to the commit hash column of `commit_guru_formatted`. This is necessary as we need to obtain a timestamp for the bug fix. 

### Fields

- **bugType**: the bug type column from `selected_sstubs`
- **fixCommitSHA1**: the hash from the fix commit
- **projectName**: the name of the project to which the commit belongs to
- **author_date**: the unix timestamp for which the commit was pushed 
- **is_fix_commit**: boolean that states if the commit is considered a fix commit or not by commit guru. this is important for validation later and threats to validity (coverage). 

