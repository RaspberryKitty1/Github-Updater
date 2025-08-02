import os
import subprocess

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"

def find_git_dirs(root='.'):
    git_dirs = []
    for dirpath, dirnames, filenames in os.walk(root):
        if '.git' in dirnames:
            git_dirs.append(os.path.abspath(dirpath))
            dirnames.remove('.git')  # Don't recurse into .git dirs
    return git_dirs

def get_remote_url(repo_path):
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'remote', 'get-url', 'origin'],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def convert_https_to_ssh(url):
    if url.startswith('https://github.com/'):
        path_part = url[len('https://github.com/'):]
        return f'git@github.com:{path_part}'
    return None

def pull_repo(repo_path, remote_url, use_ssh=False):
    if use_ssh:
        # Get current branch name
        try:
            branch_result = subprocess.run(
                ['git', '-C', repo_path, 'rev-parse', '--abbrev-ref', 'HEAD'],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, check=True
            )
            current_branch = branch_result.stdout.strip()
        except subprocess.CalledProcessError:
            current_branch = 'main'  # fallback default branch

        ssh_url = convert_https_to_ssh(remote_url)
        if not ssh_url:
            ssh_url = remote_url  # fallback if conversion fails

        cmd = ['git', '-C', repo_path, 'pull', ssh_url, current_branch]
    else:
        cmd = ['git', '-C', repo_path, 'pull', '--ff-only']

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    output_lines = []
    for line in process.stdout:
        stripped = line.strip()
        if stripped.startswith("From github.com:"):
            print(f"{CYAN}{line.rstrip()}{RESET}")
        elif stripped.startswith("Updating") or stripped == "Fast-forward":
            print(f"{GREEN}{line.rstrip()}{RESET}")
        elif '|' in line and ('+' in line or '-' in line):
            colored_line = (
                line.replace('+', f"{GREEN}+{RESET}")
                    .replace('-', f"{RED}-{RESET}")
            )
            print(f"{YELLOW}{colored_line.rstrip()}{RESET}")
        elif "files changed" in line or "insertions" in line or "deletions" in line:
            print(f"{YELLOW}{line.rstrip()}{RESET}")
        else:
            print(line, end='')
        output_lines.append(line)
    process.wait()
    return ''.join(output_lines)

def main():
    repos = find_git_dirs()
    for repo in repos:
        rel_path = os.path.relpath(repo).replace("\\", "/")
        print(f"{CYAN}🔄 Processing {BOLD}./{rel_path}{RESET}")

        current_url = get_remote_url(repo)
        if not current_url:
            print(f"{YELLOW}⚠️  Warning: no remote 'origin' found in {rel_path}{RESET}\n")
            continue

        use_ssh_pull = current_url.startswith('https://github.com/')

        print(f"{CYAN}⬇️  Pulling latest changes...{RESET}")
        pull_output = pull_repo(repo, current_url, use_ssh=use_ssh_pull)

        if "Already up to date." in pull_output:
            print(f"{GREEN}✅ Up to date.{RESET}")
        elif pull_output.strip() == '':
            print(f"{YELLOW}⚠️  No output from pull command.{RESET}")
        else:
            print(f"{GREEN}⬆️  Updated with new commits.{RESET}")

        print()  # Blank line between repos

    print(f"{GREEN}✅ All repositories processed.{RESET}")

if __name__ == '__main__':
    main()
