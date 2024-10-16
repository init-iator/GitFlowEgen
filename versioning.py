import subprocess


def get_current_version():
    try:
        with open('version.txt', 'r') as f:
            version = f.read().strip()
    except FileNotFoundError:
        version = '0.0.0'
    return version

def increment_version(version):
    major, minor, patch = map(int, version.split('.'))
    # Här kan du välja vilken del du vill öka, t.ex. major, minor, eller patch
    major += 1  # Ökar major versionen
    new_version = f"{major}.0.0"
    return new_version

def genrelease(new_version):
    subprocess.run(["git", "checkout", "-b", f"relese-{new_version}"])
    update_version_file(new_version)
    subprocess.run(["git", "add", ".",])
    subprocess.run(["git", "commit", "-m", f"relese-{new_version}"])
    subprocess.run(["git", "push"])

def update_version_file(new_version):
    with open('version.txt', 'w') as f:
        f.write(new_version)

if __name__ == "__main__":
    current_version = get_current_version()
    print(f"Nuvarande version: {current_version}")

    new_version = increment_version(current_version)
    print(f"Ny version: {new_version}")

    genrelease(new_version)

    
    print(f"Versionen har uppdaterats till {new_version} i version.txt")