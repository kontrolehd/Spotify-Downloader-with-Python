import subprocess
import sys
import os

def install_package(package):
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    print("Welcome to the SpotifyDownloaderWebsite first run setup!")
    print("This script will install all required dependencies and configure your Spotify API credentials.\n")

    # Install required packages
    required_packages = [
        "flask",
        "spotipy",
        "yt-dlp",
        "mutagen",
        "ffmpeg-python",
        "requests",
        "python-dotenv"
    ]

    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"{package} is already installed.")
        except ImportError:
            install_package(package)

    # Check if ffmpeg is installed and accessible
    print("\nChecking if ffmpeg is installed and accessible...")
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("ffmpeg is installed and accessible.")
    except Exception:
        print("ffmpeg is not installed or not in your PATH.")
        print("Please install ffmpeg manually from https://ffmpeg.org/download.html and ensure it is added to your system PATH.")
        input("Press Enter after installing ffmpeg to continue...")

    # Configure Spotify API credentials
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "config.py")
    print(f"\nConfiguring Spotify API credentials in {config_path}")

    client_id = input("Enter your Spotify Client ID: ").strip()
    client_secret = input("Enter your Spotify Client Secret: ").strip()

    config_content = f'''# Configuration file for Spotify API credentials
# Replace the placeholders with your own credentials

SPOTIFY_CLIENT_ID = "{client_id}"
SPOTIFY_CLIENT_SECRET = "{client_secret}"
'''

    with open(config_path, "w") as f:
        f.write(config_content)

    print("\nSetup complete! You can now run the app with:")
    print("cd app")
    print("python main.py")
    print("or use the console mode:")
    print('python main.py --console "SPOTIFY_TRACK_URL"')
    print("\nNote: The above commands assume you are now inside the 'app' directory.")

if __name__ == "__main__":
    main()
