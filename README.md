# Maximum New York Final Exam

The Cohort 16 final exam as a self-grading web page: 65 questions and 5 set pieces
("The New Colossus," the NYS Constitution, the U.S. Constitution, the political map,
and the five-borough map). Students get a score card they can download or share as a link.

The site is plain HTML, CSS and JavaScript with no build step, served by GitHub Pages
from the `main` branch.

## Files

| File | What it holds |
|---|---|
| `index.html` | Page shell and all styles |
| `exam-key.js` | The questions and the answer key: each answer, why it's right, and the phrases the grader accepts |
| `app.js` | Grading, the quiz screens, the score card and result links |
| `tools/build_artifact.py` | Builds the single-file Claude artifact version from these files |

## Editing the answer key

Each item in `exam-key.js` has:

- `answer`: what students see as the correct answer
- `why`: the explanation shown after grading
- `conf`: `"check"` marks an answer that still needs verifying
- `parts`: what the student fills in and how each part is graded

Accepted phrases match whole words after normalizing: lowercase, punctuation stripped,
number words turned into digits. A trailing `*` matches any ending (`statut*`), and
`/.../` is a regular expression. Small typos in longer phrases are forgiven.

The Claude artifact version also has an owner-only answer-key editor at `#key`. Edits made
there live in the artifact's database, not in this repo; copy them into `exam-key.js`
to update this site.

## What differs from the Claude artifact

The [Claude artifact](https://claude.ai/artifact/A6CrNFYv5Txt3z1WDzxXqV) adds a live
cohort board, the answer-key editor, and "Challenge the grade" (Claude re-reads a
disputed answer). Those need Claude's servers, so this static site leaves them out.
Students here are asked to send their result link to the instructor. Paste those links
into the artifact's "Add results from links" tab to count them in the cohort stats.

The answer key ships with the page, so anyone who reads the source can see it.

## Local preview

```bash
python -m http.server 8766
```

Then open <http://localhost:8766/>. Add `?dev` to that URL to try the owner tools,
which then save in your browser only.

## Rebuilding the Claude artifact

```bash
python tools/build_artifact.py path/to/mny-final-exam.html
```

Then publish that file to the existing artifact.
