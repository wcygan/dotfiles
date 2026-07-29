# Multiple-Choice Evaluation Protocol

Use this procedure whenever the requested answer is a choice letter, especially
for batched JSON evaluations.

## Silent working table

For every question, build a private four-column row:

| Question ID | Retrieved rule | Exact matching option text | Option letter |
| --- | --- | --- | --- |

Fill the columns from left to right. Determine the rule first. Then copy the
matching option text exactly from the current question. Only then copy the
letter printed beside that option.

Never choose a letter from memory, from a previous question, from the sample
output, or from the position of a similar answer.

## Two-way audit

Before emitting the response, audit every row in both directions:

1. Read the chosen letter back through the current question's options.
2. Confirm that its full option text is the text recorded in the row.
3. Confirm that this option text states the retrieved rule.
4. If either comparison fails, fix the letter before producing output.

For example, if the retrieved rule is `alpha/beta` and the options label
`alpha/beta` as `D`, the answer is `D` even if an earlier draft or sample used
`A`.

## Output audit

- Include every required question ID exactly once.
- Use only allowed uppercase choice letters.
- Preserve the requested ID order when practical.
- When compact JSON is requested, return exactly one single-line JSON object.
- Do not expose the working table, reasoning, headings, or Markdown fences.
