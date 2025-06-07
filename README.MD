# 🔄 Git Repo Updater

A Python script to automatically find all Git repositories under the current directory, convert their GitHub remotes from HTTPS to SSH (if needed), and pull the latest changes using a fast-forward strategy.

Ideal for managing a large number of local GitHub repositories.

---

## 📋 Features

* 🔍 Recursively finds all Git repositories from the **current directory**
* 🔄 Converts GitHub remotes from **HTTPS to SSH**
* ⬇️ Pulls updates using `git pull --ff-only`
* 🎨 Color-coded terminal output for clarity:

  * **Cyan** – Info
  * **Green** – Success
  * **Yellow** – Summary of changes
  * **Red** – Deletions
  * **Magenta** – SSH conversion

---

## 🔐 Why Convert HTTPS to SSH?

GitHub **disabled password authentication** for HTTPS in **August 2021**.

Instead of managing personal access tokens (PATs), SSH provides:

✅ Token-free authentication
✅ Seamless automation
✅ Better integration with CI/CD and scripts

The script converts:

```plaintext
https://github.com/username/repo.git
```

➡️ To:

```plaintext
git@github.com:username/repo.git
```

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
* **Git** must be installed and in your system’s PATH
* **SSH key** must be configured and added to your GitHub account
  ➤ Test with: `ssh -T git@github.com`

---

## ✅ Example Output

```MD
🔄 Processing ./project-one
🔧 Updating remote URL to SSH: git@github.com:user/project-one.git
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
* Only GitHub HTTPS remotes are converted to SSH.
* Uses `git pull --ff-only` to avoid accidental merge commits.

---

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for full details.
