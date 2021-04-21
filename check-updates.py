from __future__ import annotations
import pathlib
import requests
from pathlib import Path
import json
import re

packages: dict[str, int] = {"dsnet": 194004, "xp-pen": 194013}


def get_anitya_version(id: int) -> str:
    response = requests.get(
        f"https://release-monitoring.org/api/v2/versions/?project_id={id}",
    )
    if response.status_code != 200:
        raise RuntimeError("Error requesting version")

    version = json.loads(response.content.decode()).get("latest_version", "")
    if not version:
        raise RuntimeError("Error requesting version")

    return version


RE_PKGBUILD = re.compile(r"^\s*pkgver\s*=\s*(.+)$")


def get_pkgbuild_version(package: str) -> str:
    with open(Path(package) / "PKGBUILD", "r") as fptr:
        for line in fptr:
            m = RE_PKGBUILD.match(line)
            if m:
                return m.group(1).strip()

    raise RuntimeError("Failed to extract version from PKGBUILD")


retval = 0
for package in packages:
    pkgbuild_version = get_pkgbuild_version(package)
    anitya_version = get_anitya_version(packages[package])
    if pkgbuild_version == anitya_version:
        print(f"{package}: {pkgbuild_version} == {anitya_version} ✓")
    else:
        print(f"{package}: {pkgbuild_version} != {anitya_version} ✗")
        retval += 1

exit(retval)