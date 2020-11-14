## Overview
The file database.py is used to create a local sqlite database called "sstubs" with a table called "commits". In this table, I dump the small dataset "sstubs" found in the folder "docs". The JSON file is dumped in such a way that it can be queried as a normal table and not a whole JSON file. 

## Goal of this dataset
Provide a dataset large enough to study the recall of repair techniques for simple bugs (one-line bugs for example) → percentage of real-world bugs that can be repaired by one of the templates. 

## Motivation for this dataset
Program repair is important but difficult. We need an effective way to evaluate and study program repair techniques for simple bugs because simple bugs (such as one-line bugs) are amongst the most common, yet difficult bugs to see because they are latent (they do not appear until an event triggers them). Program repair is one of the core tasks in software maintenance. It requires to analyze failed executions, locate the cause of the fault, come up with a bug fix, validate that the fault has been corrected (with unit test for example) all this without introducing a new bug. This process is costly because it requires effort and time this is why most development teams will adopt automatic repair. A major concern in the industry is that such automation is required to have high precision without risking achieving high enough recall (have a false positive rate as low as possible for example). To achieve this (maintain high precision with adequate recall) is to focus on repairing simple bugs that fall into a set of templates. 

## Approach
Provide two datasets:
- Small dataset containing 25,539 single-statement bug-fix changes mined from 100 popular open-source java maven projects. 
- Large dataset containing 153,652 single-statement bug-fix changes mined from 1,000 popular open-source java projects. 
The bug fix changes are annotated by whether they match any of the 16 bug templates. The templates aim at extracting bugs that compile both before and after repair → very difficult to detect manually, but very easy and simple to fix. 

To obtain high quality datasets, java projects with high popularity were selected.

## JSON Fields
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

## Meta on the commits
- Bugs in test code are not included in this dataset.
- Commits in the dataset are not restricted to those that have a failing test case.
- Unit tested code does not appear to be associated with fewer failures while increased coverage is associated with more failures. 
- Commits in which the code compiles before and after the bug was located and repaired. 
- Commits which make a multiple-statement change at any single position are excluded. 
- Commits that make single-line modifications at more than one position in the same file are included. 
- Changes to comments, blank lines and formatting changes are excluded. 
- Some refactorings produce small changes: variable, method, or class renaming and any used of them across modified files are excluded. 

## Possible research questions
- How long does the bug stay in the code? 
- How long before the bug is found? 
- Why are those bugs being introduced? 
- Is the code affected by the bug covered by any test case? 
- Could CI capture those bugs? 
- How many of the bugs were captured by CI? 
- What is the reason for introducing those bugs? (Refactoring, another bug fix, fixing a failing test, fixing CI failure...) 
- If the bug was caught by CI, was it fixed? 
- How many commits are there between the bug fix and when it was first introduced? 
