# Git Commit Instructions

Please follow these guidelines for writing commit messages:

## Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) and structure your commit messages as follows:

```
<type>(<scope>): <short description>

[optional body]
```

- **type**: feat, fix, docs, style, refactor, test, chore, etc.
- **scope**: Use the file location in the format `chapterX: lessonY: quiz` or similar, based on the file path. For example:
  - `chapter1: lesson1: quiz` for changes in `chapter1/lesson1/quizzes/quiz1.txt`
  - `chapter2: lesson3: notes` for changes in `chapter2/lesson3/notes/<placeholder-name>.md`

## Examples

- `feat(chapter1: lesson1: quiz): add new question to quiz1`
- `fix(chapter2: lesson3: notes): correct typo in notes`
- `docs(chapter1: lesson2): update lesson overview`

## Additional Guidelines

- Use the imperative mood in the subject line (e.g., "add", "fix", "update").
- Keep the subject line under 72 characters.
- Add a body if more detail is needed.
- Reference issues or tasks if applicable.

For more details, see the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

