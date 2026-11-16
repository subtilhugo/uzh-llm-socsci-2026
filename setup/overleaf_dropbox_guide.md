# Your paper and your data, connected: Overleaf and Dropbox

The agent works in one folder. This guide brings the paper (Overleaf) and the shared data (Dropbox) to that folder. What Hugo showed in Session 4. Checked on 16 November 2026 against the Overleaf documentation: https://docs.overleaf.com

## Overleaf at UZH

UZH members have Overleaf's premium features: go to https://www.overleaf.com/edu/uzh and log in with SSO. Git integration and Dropbox sync are premium features; for Git, it is the project **owner** who needs them.

## Way 1. Git: the paper as a repository

1. In the project: menu, **Integrations**, **Git**. It shows the clone command.
2. Create a Git authentication token in **Account Settings**. It is your password when git asks.
3. Clone it next to your project, not inside its git repository:

```bash
git clone https://git.overleaf.com/<project-id> paper
```

4. The loop, every time:

```bash
cd paper
git pull                                  # before the agent works: your coauthors' edits
# ... the agent edits sections, writes tables/t2.tex, figures/f1.pdf ...
git add -A && git commit -m "Table 2 from 50_estimate.py" && git push
```

Limits: no branches, no tags, no Git LFS. A rename is a delete and a create on the Overleaf side. A push can displace or lose tracked changes and comments: agree with your coauthors on who writes where.

## Way 2. Dropbox sync: the paper as a synced folder

**Account Settings**, link Dropbox. Every project you own or can edit appears in `Dropbox/Apps/Overleaf/<project name>`, and syncs in both directions. "Sync this project now" in the project menu forces it.

Limits: you cannot choose the location; the Apps folder cannot be shared with other Dropbox users; compiled files (`.aux`, `.log`, the PDF) written locally cause conflicts, so compile on Overleaf or send local outputs elsewhere; two projects with the same name can unlink Dropbox.

**One route per project**: Git or Dropbox, not both.

## From a script to the paper, without a copy-paste

Scripts write LaTeX fragments; the paper includes them:

```
code/50_estimate.py   ->  paper/tables/t2.tex      \input{tables/t2}
code/51_figure.py     ->  paper/figures/f1.pdf     \includegraphics{figures/f1}
```

In your project's `CLAUDE.md`: *"The paper is in `paper/` (Overleaf through Git). Pull before editing, never rename files, write tables to `paper/tables/` and figures to `paper/figures/`, and stop before `git push`: I push."*

## "Overleaf connectors"

The Overleaf MCP servers you find online are community projects, not Overleaf's. Several work by reusing your browser session. Read what one asks for before you install it; the Git route above needs none.

## Dropbox: the synced folder

The agent reads and writes the local copy; Dropbox carries it to your coauthors.

- **Online-only files are empty.** A file that is not downloaded is a placeholder of 0 bytes: the agent reads nothing, and may not tell you. Right click, "Make available offline", before the session.
- **No git repository inside Dropbox.** Two machines syncing `.git` corrupt it. Code in git (outside Dropbox), data in Dropbox, and the path to the data in one config file or in `.env`.
- **Raw data read-only.** What the agent deletes is deleted for everyone. Dropbox keeps deleted files for a period that depends on the plan: know yours.
- **Your coauthors see every file the agent writes.** One folder for its outputs.
- **The Dropbox connector** (an MCP server, Session 3) searches and reads files without syncing them. It creates files; it does not edit one in place.

## What leaves your machine

The agent sends what it reads to its provider: the paper, with its unpublished results, and any data file it opens. Confidential data: keep it out of the agent's folder, or use a local model (Session 3).
