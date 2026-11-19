# Chef Council in a chat app

Use this folder when your assistant is a chat app that cannot read this repository. You get the same council, the same rules, and the same editor check. What changes is that you carry the files in and out by hand, because the chat cannot save anything.

## What is here

- [`project-instructions.md`](project-instructions.md) is the text you paste into the app's instructions field. It is the one set of instructions for every chat app. The steps on this page only say where to paste it: they add nothing to it and change nothing in it. To change how your chat behaves, edit that file first, then paste it again everywhere you use it. It stays under 8,000 characters so that it fits an instructions field, and a test fails when it does not.
- [`bundle.md`](bundle.md) is the knowledge file you upload. It holds your kitchen files, the skills, the method pages, and the templates in one file. It is generated, so never edit it: run `scripts/build-chat-bundle.sh` from the repository root, which prints `chat bundle written:` and the number of files.

Your recipe cards and cook logs are not in the bundle, because they change more often than the rest. Upload or paste the ones you want the chat to work on.

## Set it up

These steps are the same in every app. The table below says what each app calls the two places.

1. Fill in the three files in [`kitchen/`](../kitchen/README.md), or leave them blank and let the chat interview you the first time you use it.
2. From the repository root, run `scripts/build-chat-bundle.sh`.
3. In the chat app, create a project, or whatever the app calls a saved set of instructions with files.
4. Paste the whole of `project-instructions.md` into the instructions field, from its first line to its last.
5. Upload `chat/bundle.md` as a knowledge file.
6. For each job, paste the recipe card and its most recent cook log into the chat. You can upload them as files instead, but an uploaded copy goes out of date the moment the card changes.
7. Try it. Ask it to save a card for a recipe you make up on the spot. A chat that is set up correctly returns the complete file under a line that starts `File to save:` and ends with the line `Nothing was saved: I cannot write files here.`

| App | Where the instructions go | Where the bundle goes | How this was checked |
|---|---|---|---|
| Claude Projects | "Set project instructions" on the project's page | The project knowledge base, with its "+" button | Read on 2026-11-19: [How can I create and manage projects?](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects) |
| ChatGPT Projects | The project's instructions | The project's files | Not checked. The help page could not be read on 2026-11-19, so these names may be wrong. |
| Gemini Gems | The instructions box of a new Gem | "Knowledge", then "Add files" | Read on 2026-11-19: [Tips for creating custom Gems](https://support.google.com/gemini/answer/15235603) |

Apps rename their screens. When a name above is not there, look for the place the app keeps instructions that apply to every chat, and the place it keeps files that every chat can read.

**The fallback, for an app with neither place.** Start a chat, paste `project-instructions.md` as your first message, and attach `chat/bundle.md` to it. If the app takes no file, paste from the bundle the files the job needs. Each one sits between a line that starts `===== FILE:` and a line that starts `===== END FILE:`. Say which files you left out, because the chat is told to treat a missing file as one it was not given.

## Keep it current

- After you change anything in `kitchen/`, a skill, `method/`, or `templates/`, run `scripts/build-chat-bundle.sh` again and upload the new `bundle.md` in place of the old one. The chat only knows the copy you uploaded.
- `scripts/build-chat-bundle.sh --check` prints `chat bundle checked:` when `bundle.md` matches the files it is built from, and `chat bundle is out of date:` when it does not. CI runs it on every pull request, so a change to one of those files without a rebuilt bundle fails the checks.
- After you change `project-instructions.md`, paste it again.
- If you uploaded a recipe card or a cook log as a file, replace it after every change to it, or remove it and paste the current one when you need it. The chat trusts the copy it has.

## Saving what the chat writes

The chat cannot write to your repository. When you ask it to save, it returns each file whole, under a line `File to save:` with the path, and tells you that nothing was saved. Saving is yours:

1. Put each file at the path given, replacing the whole file if it exists. Save it with plain line feeds, which some editors call Unix line endings. Git commits a card with line feeds, so a hash taken from a card saved with Windows line endings stops matching once the card is committed.
2. Run any command the chat gives after the files, such as `python3 scripts/build-index.py`.
3. Have the card checked, as the next section says.
4. Commit on a branch and open a pull request, as [`AGENTS.md`](../AGENTS.md) says under "Making changes".

A source packet goes under `.sources/`, which git ignores. Keep it there, and never commit one.

## The editor check, in a new chat

Every card that is added or changed is checked by an editor that did not write it. In a chat app the editor is a new chat: not the chat that wrote the card, and not a later message in it.

Open a new chat and follow [The editor prompt for a new chat](../method/recipe-qc.md#the-editor-prompt-for-a-new-chat). That section holds the prompt, the things to paste after it, and what to save from the reply. A new chat in the same project works: the instructions tell a chat that opens with that prompt to act as the editor and nothing else.

One of the things you paste is the card's hash line, which comes from a command. That step needs a copy of the repository and a terminal. Without them the report has no hash, and the editor gate in CI fails for that change, which is accurate: nothing shows which bytes were checked.

## What a chat cannot do

- Run a script. It gives you the command and says it did not run it. The index, the card linter, and the editor gate run in your terminal or in CI.
- See a file you changed after you built the bundle, until you upload a new one or paste the file.
- Open a web page, unless your app gives it a browsing tool. Without one it cannot research a source, and it is told to say so.
- Copy a card to a notes app. That is a job for an agent that works in the repository, under [`adapters/README.md`](../adapters/README.md).
