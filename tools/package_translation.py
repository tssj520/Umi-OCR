"""Build clean Windows portable and v2.1.5 update ZIPs (standard library only)."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import zipfile


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE = "83173efc4f4453b41223ea96d63d44534bf0505c"
BLOCKED = {"__pycache__", ".git", ".settings", ".pre_settings", "themes.json", "logs", "temp", "temp_doc"}


def git_paths(*args):
    data = subprocess.check_output(["git", args[0], "-z", *args[1:]], cwd=str(ROOT))
    return [Path(p.decode("utf-8")) for p in data.split(b"\0") if p]


def allowed(path):
    return not any(part in BLOCKED for part in path.parts) and path.suffix not in {".pyc", ".pyo", ".log"}


def copy_file(relative, source_root, destination):
    source = source_root / relative
    target = destination / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(source), str(target))


def archive(directory, target, prefix=""):
    with zipfile.ZipFile(str(target), "w", zipfile.ZIP_DEFLATED, compresslevel=6) as output:
        for path in sorted(directory.rglob("*")):
            relative = path.relative_to(directory)
            if path.is_file() and allowed(relative):
                output.write(str(path), (Path(prefix) / relative).as_posix())
    with zipfile.ZipFile(str(target)) as output:
        bad = output.testzip()
        if bad:
            raise RuntimeError("Invalid archive member: " + bad)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "release")
    parser.add_argument("--runtime-root", type=Path, default=ROOT)
    parser.add_argument("--base", default=DEFAULT_BASE)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise SystemExit("Output already exists; use a new --output directory.")
    version_info = json.loads((ROOT / "UmiOCR-data/about.json").read_text(encoding="utf-8"))["version"]
    version = "{major}.{minor}.{patch}".format(**version_info)
    if version_info["prerelease"]:
        version += "-{prerelease}.{prereleaseNumber}".format(**version_info)
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(ROOT), text=True).strip()
    runtime_root = args.runtime_root.resolve()
    required = ["Umi-OCR.exe", "UmiOCR-data/runtime/python.exe",
                "UmiOCR-data/site-packages/PySide2/QtCore.pyd",
                "UmiOCR-data/plugins/win7_x64_RapidOCR-json/RapidOCR-json.exe"]
    for name in required:
        if not (runtime_root / name).is_file():
            raise SystemExit("Missing runtime dependency: " + name)
    output.mkdir(parents=True)
    full = output / ("Umi-OCR_Translation_Rapid_v" + version + "_Windows_x64")
    update = output / "update"
    full.mkdir()
    update.mkdir()
    tracked = git_paths("ls-files")
    docs = [Path(name) for name in ["README.md", "CHANGE_LOG.md", "LICENSE", "THIRD_PARTY_NOTICES.md"]]
    docs += [path for path in tracked if path.parts[0] == "docs"]
    sources = [path for path in tracked if path.parts[0] == "UmiOCR-data" and allowed(path)]
    for path in sources + docs:
        copy_file(path, ROOT, full)
    copy_file(Path("Umi-OCR.exe"), runtime_root, full)
    for name in ["runtime", "site-packages", "plugins/win7_x64_RapidOCR-json"]:
        relative = Path("UmiOCR-data") / name
        shutil.copytree(str(runtime_root / relative), str(full / relative),
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".git", "*.log"))
    changed = git_paths("diff", "--name-only", "--diff-filter=ACMR", args.base, "HEAD", "--", "UmiOCR-data")
    for path in changed + docs:
        if allowed(path):
            copy_file(path, ROOT, update)
    build_info = {"version": version, "revision": revision, "upstream_base": args.base,
                  "repository": "https://github.com/tssj520/Umi-OCR",
                  "platform": "Windows x64", "engine": "RapidOCR",
                  "runtime_source": "upstream Umi-OCR_Rapid_v2.1.5.7z"}
    for directory in [full, update]:
        (directory / "BUILD_INFO.json").write_text(json.dumps(build_info, indent=2) + "\n", encoding="utf-8")
    full_zip = output / (full.name + ".zip")
    update_zip = output / ("Umi-OCR_Translation_v" + version + "_Update_from_v2.1.5.zip")
    archive(full, full_zip, full.name)
    archive(update, update_zip)
    checksums = []
    for path in [full_zip, update_zip]:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        checksums.append(digest + "  " + path.name)
        print(path.name, path.stat().st_size, "bytes", digest, flush=True)
    (output / "SHA256SUMS.txt").write_text("\n".join(checksums) + "\n", encoding="utf-8")
    (output / "build-manifest.json").write_text(json.dumps(build_info, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
