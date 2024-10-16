# import subprocess
# import sys

# def run_git_command(command):
#     """
#     Kör ett git-kommando och fånga eventuell output eller fel.
#     """
#     try:
#         result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         return result.stdout.strip()
#     except subprocess.CalledProcessError as e:
#         print(f"Error running command {' '.join(command)}: {e.stderr.strip()}")
#         sys.exit(1)

# def merge_branch(source_branch, target_branch):
#     """
#     Mergar source_branch in i target_branch.
#     """
#     print(f"Checking out {target_branch}...")
#     run_git_command(['git', 'checkout', target_branch])

#     print(f"Merging {source_branch} into {target_branch}...")
#     run_git_command(['git', 'merge', source_branch])

#     print(f"Successfully merged {source_branch} into {target_branch}.")

# def create_and_merge_rc_branch(source_branch, rc_branch):
#     """
#     Skapar och merga release-candidate branchen om den inte redan finns.
#     """
#     # Kolla om release-candidate branchen redan finns
#     existing_branches = run_git_command(['git', 'branch', '-r'])
#     if f"origin/{rc_branch}" in existing_branches:
#         print(f"{rc_branch} already exists, checking it out...")
#         run_git_command(['git', 'checkout', rc_branch])
#     else:
#         print(f"{rc_branch} does not exist, creating it from {source_branch}...")
#         run_git_command(['git', 'checkout', source_branch])
#         run_git_command(['git', 'checkout', '-b', rc_branch])

#     # Mergar source_branch in i release-candidate
#     print(f"Merging {source_branch} into {rc_branch}...")
#     run_git_command(['git', 'merge', source_branch])

#     print(f"Successfully merged {source_branch} into {rc_branch}.")

# def main():
#     main_branch = 'main'
#     develop_branch = 'develop'
#     rc_branch = 'release-candidate'

#     # Hämta senaste ändringar
#     print("Fetching latest changes...")
#     run_git_command(['git', 'fetch'])

#     # Merga main -> develop
#     merge_branch(main_branch, develop_branch)

#     # Skapa och merga main -> release-candidate om den inte finns
#     create_and_merge_rc_branch(main_branch, rc_branch)

# if __name__ == "__main__":
#     main()


import subprocess
import sys

def run_git_command(command):
    """
    Kör ett git-kommando och fånga eventuell output eller fel.
    """
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(command)}: {e.stderr.strip()}")
        sys.exit(1)

def ensure_branch_exists(branch_name):
    """
    Kontrollera om branchen finns lokalt, om inte - hämta den från origin.
    """
    local_branches = run_git_command(['git', 'branch'])
    if branch_name not in local_branches:
        print(f"{branch_name} does not exist locally. Fetching it from origin...")
        run_git_command(['git', 'fetch', 'origin', branch_name + ':' + branch_name, '-v'])

def merge_branch(source_branch, target_branch):
    """
    Mergar source_branch in i target_branch.
    """
    print(f"Checking out {target_branch}...")
    run_git_command(['git', 'checkout', target_branch, '-v'])

    print(f"Ensuring {source_branch} exists locally...")
    ensure_branch_exists(source_branch)

    print(f"Merging {source_branch} into {target_branch}...")
    run_git_command(['git', 'merge', f'origin/{source_branch}', '--allow-unrelated-histories', '-v'])

    print(f"Successfully merged {source_branch} into {target_branch}.")

def create_and_merge_rc_branch(source_branch, rc_branch):
    """
    Skapar och merga release-candidate branchen om den inte redan finns.
    """
    # Kolla om release-candidate branchen redan finns
    existing_branches = run_git_command(['git', 'branch', '-r'])
    if f"origin/{rc_branch}" in existing_branches:
        print(f"{rc_branch} already exists, checking it out...")
        run_git_command(['git', 'checkout', rc_branch, '-v'])
    else:
        print(f"{rc_branch} does not exist, creating it from {source_branch}...")
        run_git_command(['git', 'checkout', source_branch, '-v'])
        run_git_command(['git', 'checkout', '-b', rc_branch, '-v'])

    # Mergar source_branch in i release-candidate
    print(f"Merging {source_branch} into {rc_branch}...")
    run_git_command(['git', 'merge', source_branch, '-v'])

    print(f"Successfully merged {source_branch} into {rc_branch}.")

def main():
    main_branch = 'main'
    develop_branch = 'develop'
    rc_branch = 'release-candidate'

    # Hämta senaste ändringar
    print("Fetching latest changes...")
    run_git_command(['git', 'fetch', '--all', '-v'])

    # Merga main -> develop
    merge_branch(main_branch, develop_branch)

    # Skapa och merga main -> release-candidate om den inte finns
    create_and_merge_rc_branch(main_branch, rc_branch)

if __name__ == "__main__":
    main()
