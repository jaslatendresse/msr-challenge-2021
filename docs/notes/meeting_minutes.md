# 2020-11-17

## Selected research questions: 
1. How many of the bugs were captured by CI?
2. If the bug was caught by CI, was it fixed (immediately, ignored, etc...)?
3. How do bugs caught by CI compare to those not caught by CI? How long to they stay in the code base before they get fixed? 

## Validation
Run queries on the dataset dumped in sqlite and validate the results by searching the commits on GH and make sure they contain what they should. Document this validation. 
## Next 
With the small dataset, narrow down the number of projects we will select for the research. 

Project characteristics: 
- 10-30 sizable projects
- Use of Travis CI
- Young projects for mature CI usage
- Have a baseline of less than 5-6 years of CI use. 
- Have been using CI from the beginning to ensure the commit is covered by CI. 

## TravisTorrent
https://travistorrent.testroots.org/page_access/ 

Get projects from TravisTorrent and look if projects from the dataset are part of them. If so, select them. 

Then, for each selected project, ensure that they have at least one of each of the 16 bug template. 

# 2020-12-18

## Brainstorming

Find the commit that introduced the bug. 
- When the bug was introduced? When was the bug fixed?
- Did CI capture the bug? How long between "when the bug was introduced and when it was fixed"?

Some further ideas:
- Compare CI results before fix and after fix. 
- It could be that CI caught the bug between the introduction and the fix. 
- Was the CI effective? How long did the bug stay in the code? 

## Next Step

1. Find projects in commit guru, if not there add them. 
2. Download CSV files + merge them + create table from them with python in sqlite db.
3. Query tables to find how much of our commit fixing (corrective commits) data is in commit guru.

Possible tools: 
http://pure.tudelft.nl/ws/portalfiles/portal/46282428/main.pdf or commit guru (docker). 

What we are interested in next: 
- % of commits in MSR dataset (untouched) that have triggered CI builds 
- % of commits that commit guru finds them as bug fixes. 

# 2020-12-23

## Brainstorming 

Quantitive analysis

- How many commits triggered the CI (must be a PR)? 
- How many are part of the PR (in the list)? 
- How long the bugs stay in the code before they're fixed? (if long time, then maybe not risky?) 

Qualitative analysis

- Why CI pipeline doesn't not catch these bugs? 
- When bugs fixed, are tests added to the code? 
- Is the bug covered by a test? 

Include commits that are not part of the CI table. 

## Questions

- What % of bugs are caught by the CI? 
- If not caught, why? 

## Next Step 

- Set up document to work on the paper
- Set up the pipeline for the latex template (GitHub actions) 

# 2021-01-05

Validate the 15 commits that are not PR nor appear in the list gh_commits_in_push (just to make sure).

Panda explode - replicate row for each value of the list you have in one column (For the fixed_by column in the commit guru set)

Next step: find out how long do bugs stay in the code (from selected_sstubs - the 830 distinct commits) with the fixed_by column from commit guru. 

# 2021-01-07

## Next step + brainstorming
- Start gathering the data, write it in the paper (answering the questions) to define the scope. 
- More interesting if a bug was caught by the CI. 
  - We have a timeline of the bug fix, we can compare the CI pipeline of the timeline before and after the fix. 
  - Use travis torrent data set, is there a test passing or failing after the fix? 
  - Was it caught? Did devs add tests to catch it after? 

Methodology - do we trust the results? 
Conclusions - are our findings relevant? 

Next:

- Find bugs not caught by the CI. 
- Start sketching the methology, make the tables (put what you find interesting, results answering the questions, etc)
- Related works (from this summer) to be included in the introduction. 
- Schema (maybe) overview of our approach 
- Consider doing some visualization (plots, graphs) 
- Classify findings by bugType

# 2021-01-12

## TODO

- ~~Send 10 additional projects to Diego for commit guru.~~ 
- Validate fail 5 builds and the error builds. 
- ~~Remove pie chart and put table instead for proportion of bugs caught by CI.~~
- ~~Be more specific about "caught by CI".~~
- With the lifespan, shows that CI did not catch it at all. 
- ~~Add number of instances in lifespan table.~~
- ~~Abstract: rephrase "program repair" --> software maintenance or bug fixing.~~
- Add datasets from database to repo (in csv file) 

## Brainstorming

- If there are a bug that CI doesn't catch, are they tested? Are they severe?
- How many of those bugs were prevented from being pushed in production because of the CI? 
- Manually validate if CI is responsible for catching bugs? 
- Not caught by CI: need to be more precise - 74% not part of a build. 
- From those that were in build: how many bugs were actually caught by the CI? how many actually throw an error? 
- Being caught by CI does not mean caught bugs: did tests fail or pass? (column tr_log_bool_tests_failed and tr_log_tests_failed from travis set) 
- Were bugs fixed right after? if yes, then the CI might have captured it.
- If not, then it might be that the CI didn't catch it -- validate that. 
- Errored build: ex, missed dependency, build too long so crash, build stopped by dev so doesn't finish. 
- Failed build: I guess more related to code. 
- 16.1% are part of a build, not necessarily captured. Rephrase that everywhere. 

Next meeting: friday 13h30. 

# 2021-01-15

## Brainstorming 

Can CI help indicate one-line bugs? Probably not when the bugs was introduced

Need to investigate before/after the fix for all commits (closer to the fix). 

Repeat build failed tests, etc after the bug fix comes. 

CI capturing the introduction of the bug may be enough 

- Bugs stay in the code for a long time
- CI does not fail immediately
- CI doesn't help with those bugs 

## Some important numbers 

How many fixes have a build? 366/1284. -- 366 fixes out of 1284 are associated with a CI build. 

6/366 failed or errored in the previous build. 

How many previous builds have failed? Previous build of the build associated with the fix commit. 

Can CI help us catch this at bug intro time? No

Can CI help us catch the bug before the fix? No 

`CREATE TABLE selected_travis_formatted AS WITH RECURSIVE split(tr_build_id, tr_status, git_trigger_commit, gh_project_name, gh_is_pr, tr_log_bool_tests_ran, tr_log_bool_tests_failed, tr_log_tests_failed, tr_prev_build, gh_commits_in_push, str) AS ( SELECT tr_build_id, tr_status, git_trigger_commit, gh_project_name, gh_is_pr, tr_log_bool_tests_ran, tr_log_bool_tests_failed, tr_log_tests_failed, tr_prev_build, '', gh_commits_in_push||',' FROM selected_travis UNION ALL SELECT tr_build_id, tr_status, git_trigger_commit, gh_project_name, gh_is_pr, tr_log_bool_tests_ran, tr_log_bool_tests_failed, tr_log_tests_failed, tr_prev_build, substr(str, 0, instr(str,',')), substr(str, instr(str,',')+1) FROM split WHERE str!='' ) SELECT tr_build_id, tr_status, git_trigger_commit, gh_project_name, gh_is_pr, tr_log_bool_tests_ran, tr_log_bool_tests_failed, tr_log_tests_failed, tr_prev_build, gh_commits_in_push FROM split WHERE gh_commits_in_push!=''`

`CREATE TABLE builds_before_fix AS SELECT builds.tr_build_id, builds.tr_status, builds.tr_log_bool_tests_failed, builds.tr_log_tests_failed FROM builds LEFT JOIN selected_travis_formatted WHERE builds.tr_prev_build = selected_travis_formatted.git_trigger_commit OR builds.tr_prev_build = selected_travis_formatted.gh_commits_in_push GROUP BY builds.tr_build_id`

## Direction of the paper 

Have paper focus on bug introducing commits

Can CI help warn about one-line bugs? (title)

CI is meant to conduct "checks" and helps catch bugs quickly, we want to know if they catch one-line bugs. 

### RQS

- How many bug inducing commits does CI fail on? - 5
- Why are they not caught? - tests coverage, some just don't fail, some just no tests, etc. 

Challenges and possible threats to validity: traceability is difficult (map bug fix - bug induce lose a lot of data, bugs might not be very severe so the build doesn't fail --> they end up living in the code for a long time)

# 2020-01-22

- Mention that this paper is part of the MSR challenge
- Start using name of the dataset
- Rearrange the process diagram (font and content to match the data analysis and filtering section)

## Data Filtering 

- DF 1 is not select all projects --> while it was reported 100 projects, we only found 84. Then start the steps. 
  - So basically, df 2 becomes df 1. and so on...
- Filter unsuitable projects - rephrase that 
  - Filter project for diversity of bugs, limited time and resources, we selected 15 projects. don't mention suitability, don't mention computational power. 

## RQ 1

- Motivation: if bug not captured at introduction, we want to see if it was caught along the way. 
- Cross reference data sets based on commit hash 
- Bug inducing commits that did not trigger a CI - we dont talk enough about that. Practices of some projects may have limited that. % limitation - commit guru - how many bugs we can find
- Talk about commits that trigger the CI. 
- How many bug inducing commits are caught by CI (50) 
- If bug was caught in the first stage, it wouldnt need to be caught later on. 
- Why more failures after fix? Sometimes, bug fixing introduces other bugs, sometimes pipelines are not reliable. 
- A build may contain more commits than just the ones relating to bugs
- Include tests that failed - not related to actual bug 

## RQ2

No test coverage. Failed tests not related to the actual bug.



# 2020-01-25

Introduction: CI not just building, it improves quality - why we focus on CI? put citations 

Describe the approach in the introduction. 

Despite huge benefits of CI, no work was done with single-statment bugs: 

Preliminary analysis: data on the chosen data (commits, contributors, maturity) 

Get the commit message for fix commits. 

After the builds fail, does phase b have more tests than phase a? -- see travis set. (RQ2) 

Be more clear about phase a and b

phase a: bug inducing commit

a + b: single statement bug

Table 1: needs to go. 

RQ2: from the builds that fail, how many captured the bug? 

Phase (c) should be removed? 

Update RQ 2 summary in introduction. 

RQ 2 talk about phase a and phase b. 

Make a pipeline diagram to show when bug was introduced and before it was fixed --> RQ 1 should be about single-statement bugs, not just bug-inducing commits 

After fix (phase c) analyze nb tests introduced. 





