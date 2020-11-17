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
