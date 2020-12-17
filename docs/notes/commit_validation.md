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
Some commits contain additional changes that don't fall in any of the templates in addition to the change they should contain. To be discussed. 

- contains a change in comment: https://github.com/graylog2/graylog2-server/commit/5b4979166050e553fd967e5094509de7975651ec
- contains a change in comment: https://github.com/graylog2/graylog2-server/commit/8cac34cb2fd489023a20702dabf24db38c64b3cf
- https://github.com/google/closure-compiler/commit/7e69b806137604da52bdded56b711041943a3893
- 2 bugTypes: DIFFERENT_METHOD_SAME_ARGS and CHANGE_IDENTIFIER but only contains one change https://github.com/redis/jedis/commit/03c0af2581386394637d83713efe6bfa8ab6e446
    - https://github.com/redis/jedis/commit/d7cd3a0af671b0fcf30b7cd4819fa9026f8d92f8
