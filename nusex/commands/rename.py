import os

from nusex import CONFIG_DIR


def rename(old_name, new_name):
    os.rename(CONFIG_DIR / f"{old_name}.nsx", CONFIG_DIR / f"{new_name}.nsx")
    print(f"🎉 Template successfully renamed from '{old_name}' to '{new_name}'!")
