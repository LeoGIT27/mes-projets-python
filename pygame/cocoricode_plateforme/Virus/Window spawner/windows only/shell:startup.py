from pathlib import Path
import subprocess
import sys

LABEL = "com.test.app"

launch_agents = Path.home() / "Library" / "LaunchAgents"
launch_agents.mkdir(parents=True, exist_ok=True)

plist = launch_agents / f"{LABEL}.plist"

python_path = Path(sys.executable).resolve()
script_path = Path(__file__).resolve()

# Fichiers de log pour voir les éventuelles erreurs
stdout_log = Path.home() / "test_app_stdout.log"
stderr_log = Path.home() / "test_app_stderr.log"

content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN"
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>

    <key>Label</key>
    <string>{LABEL}</string>

    <key>ProgramArguments</key>
    <array>
        <string>{python_path}</string>
        <string>{script_path}</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>StandardOutPath</key>
    <string>{stdout_log}</string>

    <key>StandardErrorPath</key>
    <string>{stderr_log}</string>

</dict>
</plist>
"""

plist.write_text(content, encoding="utf-8")

print("Python utilisé :", python_path)
print("Script lancé    :", script_path)
print("Plist           :", plist)

# Supprime une ancienne version si elle existe
subprocess.run(
    ["launchctl", "bootout", f"gui/{subprocess.check_output(['id', '-u']).decode().strip()}", str(plist)],
    capture_output=True
)

# Charge le LaunchAgent
uid = subprocess.check_output(["id", "-u"]).decode().strip()

result = subprocess.run(
    ["launchctl", "bootstrap", f"gui/{uid}", str(plist)],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print("ERREUR :", result.stderr)
else:
    print("✓ LaunchAgent installé et chargé !")

# Lance immédiatement pour tester
subprocess.run(
    ["launchctl", "kickstart", f"gui/{uid}/{LABEL}"],
    capture_output=True,
    text=True
)

print("✓ Test de lancement effectué.")