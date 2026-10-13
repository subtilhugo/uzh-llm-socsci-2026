# Installation guide and verification test

You need three things before Session 1: a terminal with `git` and Python, an editor, and an agent that runs inside a folder. Thirty minutes if everything goes well. If the verification test at the end fails, write to Hugo before the session, with the error message.

## 1. Terminal, git, Python

**macOS.** Open Terminal (Spotlight, type "Terminal"). Run `git --version`. If macOS offers to install the command line tools, accept. Then install Python 3.11 or later from python.org, or with Homebrew (`brew install python`).

**Windows.** Install [Git for Windows](https://git-scm.com/downloads/win) (keep the defaults; it gives you Git Bash). Install Python 3.11 or later from python.org and tick "Add Python to PATH". Use Git Bash or PowerShell as your terminal.

**Linux.** You already have a terminal. `sudo apt install git python3 python3-pip` or your distribution's equivalent.

Check: `git --version` and `python3 --version` (on Windows, `python --version`) both print a version number.

## 2. An editor

[VS Code](https://code.visualstudio.com/) or [Cursor](https://cursor.com/). Either is fine. You will open your project folder in it, and run the agent in its integrated terminal (menu Terminal > New Terminal).

## 3. An agent

The workshop uses **Claude Code** as the example. The point is the way of working, not the brand: Gemini CLI and Codex CLI follow the same logic and are accepted. What matters is that the agent runs *inside your project folder*, reads and writes files there, and can run commands.

**Claude Code** (requires a Claude subscription, Pro or above). Three equivalent ways to run it; choose one:

- *Desktop app.* Install the Claude desktop app, sign in, click the **Code** tab, open your project folder. Nothing else to install. Simplest option.
- *Terminal.* macOS/Linux: `curl -fsSL https://claude.ai/install.sh | bash`. Windows PowerShell: `irm https://claude.ai/install.ps1 | iex`. Then open a new terminal, `cd` into your folder, run `claude`, and log in when asked.
- *VS Code or Cursor extension.* In the Extensions view, search "Claude Code", install, then open the Command Palette and choose "Claude Code: Open in New Tab".

Official instructions: https://code.claude.com/docs/en/overview

**Gemini CLI** (free with a Google account, daily quota). `npm install -g @google/gemini-cli`, then `gemini` in your folder. Requires Node.js 20 or later (nodejs.org).

**Codex CLI** (requires a ChatGPT subscription). `npm install -g @openai/codex`, then `codex` in your folder.

## 4. Verification test (do this one)

1. Create an empty folder anywhere, for example `agent-test/`.
2. Open a terminal in that folder (or open the folder in the desktop app, or in your editor and start the agent there).
3. Start the agent.
4. Type: `Create a file named hello.md containing today's date and the name of this folder.`
5. The agent will ask permission to write a file. Accept.
6. Look in the folder.

**Pass:** `hello.md` exists and contains today's date. You are ready.

**Fail:** send Hugo a screenshot of the error. Common fixes:

- "command not found": close and reopen the terminal, the installer added a path that the old terminal does not see.
- Login loop: log out of the agent, log in again in a browser, then restart.
- Permission prompt never answered: look for a prompt in the terminal asking "Allow?"; type `y`.

## 5. What to bring on 14 October

- Your laptop with the test passed, and the charger.
- Your project idea in a few lines (a research question, even rough).
- Three to five PDFs of papers your project builds on.
- Your dataset if you already have one (not needed before 28 October).

If you have none of these, you will work on the example project. You lose nothing.

## Costs, said plainly

Claude Code needs a paid Claude subscription (about 20 CHF per month; two months cover the workshop). Gemini CLI is free with a daily quota. From Session 3 on, we will call models through an API, for about 5 to 10 USD of credits over the rest of the workshop. Instructions will come a week before.
