# 🔄 Git Repo Updater

A Python script to automatically find all Git repositories under the current directory, optionally convert GitHub remotes from HTTPS to SSH **for pulling**, and pull the latest changes using a fast-forward strategy.

Ideal for managing a large number of local GitHub repositories.

---

## 📋 Features

* 🔍 Recursively finds all Git repositories from the **current directory**
* 🔐 Uses **SSH for GitHub remotes** during pull if original remote is HTTPS
* ⬇️ Pulls updates using `git pull --ff-only` (or `git pull <ssh-url> <branch>`)
* 🎨 Color-coded terminal output for clarity:

  * **Cyan** – Info (e.g., repo names, pull source)
  * **Green** – Success messages
  * **Yellow** – Summary of changes (files changed, insertions, deletions)
  * **Red** – Deletions
  * **Magenta** – (reserved for SSH conversion – not actively used now)

---

## 🔐 Why Pull Using SSH?

GitHub **disabled password authentication** for HTTPS in **August 2021**.

Instead of managing personal access tokens (PATs), SSH provides:

✅ Token-free authentication

✅ Seamless automation

✅ Better integration with CI/CD and scripts

The script pulls using:

```plaintext
git@github.com:username/repo.git
```

Even if your remote is:

```plaintext
https://github.com/username/repo.git
```

Your actual remote is **not modified**—SSH is only used during the pull process.

---

## 🚀 Usage

### 🏗️ 1. Move to Your Projects Directory

This script operates on the **current working directory** and all its subdirectories.
You should either:

* Move the script to the directory containing your GitHub repositories, or
* Navigate to that directory before running it

### ▶️ 2. Run the Script

```bash
python git_repo_updater.py
```

---

## 🛠 Requirements

* **Python 3** (tested with **Python 3.13.4**)
* **Git** must be installed and available in your system’s PATH
* **SSH key** must be configured and added to your GitHub account
  ➤ Test with: `ssh -T git@github.com`

---

## ✅ Example Output

```plaintext
🔄 Processing ./project-one
⬇️  Pulling latest changes...
From github.com:user/project-one
Updating abc123..def456
 Fast-forward
  file.py | 10 +++++-----
✅ Up to date.

✅ All repositories processed.
```

---

## 📎 Notes

* Only repositories with a remote named `origin` are processed.
* Only GitHub HTTPS remotes are pulled via SSH (converted temporarily).
* Uses `git pull --ff-only` to avoid accidental merge commits.
* Does **not** modify or rewrite the actual remote URL in `.git/config`.

---

## 📄 License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for full details.
