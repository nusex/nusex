import json

from nusex import CONFIG_DIR


def _update_config(**kwargs):
    print("⌛ Updating config...", end="")
    with open(CONFIG_DIR / "user.nsc") as f:
        data = json.load(f)

    for k, v in kwargs.items():
        if v:
            data[k] = v

    with open(CONFIG_DIR / "user.nsc", "w") as f:
        json.dump(data, f, ensure_ascii=False)
    print(" done")


def config(**kwargs):
    _update_config(**kwargs)
    print("🎉 User config updated!")
