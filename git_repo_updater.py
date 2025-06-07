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

def set_remote_url(repo_path, ssh_url):
    subprocess.run(
        ['git', '-C', repo_path, 'remote', 'set-url', 'origin', ssh_url],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

def pull_repo(repo_path):
    process = subprocess.Popen(
        ['git', '-C', repo_path, 'pull', '--ff-only'],
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
            # Colorize + (green) and - (red) signs within the line
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

def convert_https_to_ssh(url):
    if url.startswith('https://github.com/'):
        path_part = url[len('https://github.com/'):]
        return f'git@github.com:{path_part}'
    return None

def main():
    repos = find_git_dirs()
    for repo in repos:
        rel_path = os.path.relpath(repo).replace("\\", "/")
        print(f"{CYAN}🔄 Processing {BOLD}./{rel_path}{RESET}")

        current_url = get_remote_url(repo)
        if not current_url:
            print(f"{YELLOW}⚠️  Warning: no remote 'origin' found in {rel_path}{RESET}")
            print()
            continue

        if current_url.startswith('https://github.com/'):
            ssh_url = convert_https_to_ssh(current_url)
            if ssh_url:
                print(f"{MAGENTA}🔧 Updating remote URL to SSH: {ssh_url}{RESET}")
                set_remote_url(repo, ssh_url)

        print(f"{CYAN}⬇️  Pulling latest changes...{RESET}")
        pull_output = pull_repo(repo)

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

