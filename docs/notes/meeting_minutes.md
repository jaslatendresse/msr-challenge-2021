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

