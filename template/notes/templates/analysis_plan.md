# Analysis plan: <short title>

Written on YYYY-MM-DD by <your name>, with the agent (prompt 06). Status: draft / settled.

## Question

One sentence: what the first table or figure should answer.

## Data

For each file: path, source, what one row is, period or wave, geography (which year's boundaries), identifier.

## Sample

Who is in, who is out, and why. One rule per line, with the number of rows it removes if known.

## Variables

- Outcome: definition, and denominator.
- Explanatory variables: definitions, and how they are built (difference, ratio, log, scale).
- Missing values: the codes in each file and what happens to each. Survey data: refusal, don't know, not asked are three different things.

## Merges

For each merge: the two files, the key and its format (text, length), the join type, the rule for rows that do not match on each side, the number of rows expected after.

## Estimation

What the first output is: a descriptive table, a figure, or a regression (equation, estimator, fixed effects, clustering). Weights: which variable, and for which statistics. "Descriptive only at this stage" is a valid answer.

## Expected outputs

File names in `data/processed/` and `outputs/`.

## Checks

What would tell us it went right: a known total, a known value for one unit, a number of rows.

## Open questions

What is not decided yet. Prompt 07 asks about these before writing code.
