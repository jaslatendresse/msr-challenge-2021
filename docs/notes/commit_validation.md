# Commit Validation
In this document, I manually validate the commits by verifying if they contain single statements changes. 

An example of what I look for if I validate for CHANGE_OPERATOR: 

![](https://i.imgur.com/cpKUY44.png)

## Remarks
- Some commits contain multiple statements with one line change that do not belong do the category being validated. For example: 
![](https://i.imgur.com/dEDDA6k.png)

- Some commits belong to multiple bugType category, meaning they contain multiple kinds of changes. For example, a commit may contain a CHANGE_OPERATOR bugType and a CHANGE_IDENTIFIER bugType. 

### Requirements
- Commits which make a multiple-statement change at any single position are **excluded**.
- Commits that make single-line modifications at more than one position in the same file are **included**.
- Changes to comments, blank lines and formatting changes are **excluded**.
- Some refactorings produce small changes: variable, method, or class renaming and any used of them across modified files are **excluded**.

## Validation

`SELECT bugType, projectName FROM msr_table`

Not all commits are unique. One commit can have multiple bugType. Hence, one commit will be verified once against all bugType. 

### Potential Exclusions
