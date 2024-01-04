"""
Enhanced version @author: Mehmet Çağrı Aksoy https://github.com/mcagriaksoy
"""
import subprocess
import ui

VERSION_DEBUG = False
VERSION_RELEASE = True


def main():
    """ Main function """

    if VERSION_DEBUG:
        def install_requirements():
            ''' Install the requirements from requirements.txt '''
            subprocess.check_call(
                ["python", "-m", "pip", "install", "-r", "requirements.txt"])

        # Call the function to install the requirements
        install_requirements()

    # Call the main function
    ui.__main__()


if __name__ == "__main__":
    main()
