import os
import subprocess
import venv

def create_venv():
    venv.create('venv', with_pip=True)
    # Create activation scripts
    with open("venv.ps1", "w") as f:
        f.write("venv\\Scripts\\Activate.ps1")

    with open("venv.bat", "w") as f:
        f.write("venv\\Scripts\\activate")

def create_uninstall_scripts():
    # Create uninstall scripts for PowerShell and Batch
    with open("uninstall.ps1", "w") as f:
        f.write("Remove-Item -Recurse -Force venv\n")
        f.write("Remove-Item venv.ps1\n")
        f.write("Remove-Item venv.bat\n")

    with open("uninstall.bat", "w") as f:
        f.write("rd /s /q venv\n")
        f.write("del venv.bat\n")
        f.write("del venv.ps1\n")

def install_requirements():
    subprocess.check_call(["python", '-m', 'pip', 'install', '-r', 'requirements.txt'])

def install_requirements_in_venv():
    subprocess.check_call([os.path.join('venv', 'Scripts', 'pip'), 'install', '-r', 'requirements.txt'])

if __name__ == "__main__":
    create_venv_choice = input("Do you want to create a virtual environment and install the packages there? (y/N) [Default: No] ")
    if create_venv_choice.lower() == 'y':
        print("Creating virtual environment...")
        create_venv()
        print("Installing packages in the virtual environment...")
        install_requirements_in_venv()
        print("Creating uninstall scripts...")
        create_uninstall_scripts()
    else:
        print("Installing packages globally...")
        install_requirements()
    print("Installation complete.")
