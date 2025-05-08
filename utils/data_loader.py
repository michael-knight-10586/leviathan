from pathlib import Path
import pandas as pd

def load_data(filename, subpath):
    """
    Loads a CSV file depending on whether running in Colab or locally.
    """
    try:
        import google.colab
        IS_COLAB = True
    except ImportError:
        IS_COLAB = False

    if IS_COLAB:
        github_user = "YOUR_GITHUB_USERNAME"  # ← Replace this
        base_url = f"https://raw.githubusercontent.com/{github_user}/Leviathan/main/"
        full_url = base_url + subpath + filename
        print(f"📡 Loading from GitHub: {full_url}")
        return pd.read_csv(full_url)
    else:
        base_dir = Path("C:/Users/mikek/One Drive New/OneDrive/Leviathan")
        full_path = base_dir / subpath / filename
        print(f"💾 Loading from local path: {full_path}")
        return pd.read_csv(full_path)
        