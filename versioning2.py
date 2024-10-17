import subprocess

def kör_git_kommando(kommando):
    try:
        resultat = subprocess.run(kommando)
        return resultat.stdout
    except Exception as error:
        return f"Ett fel uppstod: {error}"

def öppna_versions_fil():
    with open("release.txt", "r") as fil:
        currentVersion = fil.read()
        currentVersion = currentVersion.split(".") # ["1", "0", "0"]
        newVersion = int(currentVersion[1]) + 1
        return f"{newVersion}.0.0"

def spara_versions_fil(version):
    with open("release.txt", "w") as fil:
        fil.write(version)

version = öppna_versions_fil()
print(f"Nuvarande version: {version}")

spara_versions_fil(version)

print(f"Kör 'branch release-{version}':")
output = kör_git_kommando(f"git branch release-{version}")
print(output)

output = kör_git_kommando(f"git push origin release-{version}")
print(output)
