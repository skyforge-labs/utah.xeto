"""Build and smoke-test the six public Utah libraries in isolated directories."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
LIBS = ("utah", "utah.ahu", "utah.terminal", "utah.hotwater", "utah.chilledwater", "utah.meter")
HAXALL_VERSION = "4.0.6"
HAXALL_SHA256 = "b0d5347f3614f8d8bef317e28e51e66e7fcb6d6879c731549b90108eb3430dc8"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def runtime_home():
    """Cache the exact public runtime used by CI; never modify an installed runtime."""
    cache = ROOT / ".tools"
    cache.mkdir(exist_ok=True)
    archive = cache / f"haxall-{HAXALL_VERSION}.zip"
    if not archive.exists():
        url = f"https://github.com/haxall/haxall/releases/download/v{HAXALL_VERSION}/{archive.name}"
        print(f"Downloading {url}", flush=True)
        urllib.request.urlretrieve(url, archive)
    if digest(archive) != HAXALL_SHA256:
        raise RuntimeError(f"Runtime checksum mismatch: remove {archive} and retry")
    home = cache / f"haxall-{HAXALL_VERSION}"
    if not (home / "lib/java/sys.jar").exists():
        with zipfile.ZipFile(archive) as z:
            z.extractall(cache)
    return home


def run_xeto(home, work, *args):
    # Invoke Java directly so Windows and Linux use the same command and no shell.
    env = os.environ.copy()
    for name in ("FAN_HOME", "FAN_ENV", "FAN_ENV_PATH", "FAN_CP", "CLASSPATH"):
        env.pop(name, None)
    env.update(FAN_ENV="util::PathEnv", FAN_ENV_PATH=str(work))
    java = shutil.which("java")
    if not java:
        raise RuntimeError("Java 21+ must be on PATH")
    cp = os.pathsep.join(str(home / "lib/java" / jar) for jar in ("sys.jar", "jline.jar"))
    command = [java, "-cp", cp, f"-Dfan.home={home}", "fanx.tools.Fan", "xeto", *args]
    result = subprocess.run(command, cwd=work, env=env, text=True, encoding="utf-8", errors="replace", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode or "ERROR:" in result.stdout or "❌" in result.stdout:
        raise RuntimeError(result.stdout)
    return result.stdout


def init_work(work):
    work.mkdir(parents=True, exist_ok=True)
    (work / "fan.props").write_text("path=\n", encoding="utf-8")
    (work / "xeto.props").write_text("path=\n", encoding="utf-8")


def build(home, package=False):
    if package:
        status = subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=normal"], cwd=ROOT, text=True)
        if status.strip():
            raise RuntimeError("Commit source changes before packaging so the manifest identifies the exact source")
    props = dict(line.split("=", 1) for line in (ROOT / "build.props").read_text().splitlines() if "=" in line and not line.startswith("//"))
    version = props["utah.version"]
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise RuntimeError("utah.version must have three numeric components")
    if props["utah.license"] != "AFL-3.0":
        raise RuntimeError("Library license and repository LICENSE must agree")
    stage_parent = ROOT / ".build"
    stage_parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="check-", dir=stage_parent) as tmp:
        base = Path(tmp)
        work = base / "build"
        init_work(work)
        src = work / "src/xeto"
        src.mkdir(parents=True)
        shutil.copy2(ROOT / "build.props", src)
        for lib in LIBS:
            if not (ROOT / lib / "lib.xeto").is_file():
                raise RuntimeError(f"Missing library manifest: {lib}")
            shutil.copytree(ROOT / lib, src / lib)
        print(run_xeto(home, work, "build", *LIBS), flush=True)
        artifacts = [work / "lib/xeto" / f"{lib}.xetolib" for lib in LIBS]
        for artifact in artifacts:
            if not artifact.is_file() or artifact.stat().st_size == 0:
                raise RuntimeError(f"Build did not produce {artifact.name}")

        # Installation smoke test: no Utah source in this second environment.
        installed = base / "installed"
        init_work(installed)
        output = installed / "lib/xeto"
        output.mkdir(parents=True)
        for artifact in artifacts:
            shutil.copy2(artifact, output)
        listing = run_xeto(home, installed, "repo", *LIBS)
        (base / "repo.txt").write_text(listing, encoding="utf-8")
        dump_dir = base / "dump"
        dump_dir.mkdir()
        run_xeto(home, installed, "dump", *LIBS, "-outDir", str(dump_dir))
        for lib in LIBS:
            dump = dump_dir / f"{lib}-{version}.txt"
            if not dump.is_file() or not dump.stat().st_size:
                raise RuntimeError(f"Installed library could not be loaded: {lib}")
        print(f"PASS: all {len(LIBS)} compiled libraries load without Utah source", flush=True)
        if not package:
            return
        dest = ROOT / "dist" / f"v{version}"
        if dest.exists():
            raise RuntimeError(f"Refusing to mix release artifacts: move or remove {dest} first")
        dest.mkdir(parents=True)
        for artifact in artifacts:
            shutil.copy2(artifact, dest)
        for name in ("LICENSE", "README.md", "MIGRATION.md"):
            shutil.copy2(ROOT / name, dest)
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        manifest = {"version": version, "commit": commit, "toolchain": str(home), "libraries": list(LIBS)}
        # Keep release metadata portable: do not disclose the builder's local path.
        manifest["toolchain"] = HAXALL_VERSION if home.name == f"haxall-{HAXALL_VERSION}" else "external (see build log)"
        (dest / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        bundle = dest / f"utah-xeto-{version}-skyspark4.zip"
        with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as z:
            for artifact in artifacts:
                z.write(dest / artifact.name, f"lib/xeto/{artifact.name}")
            for name in ("LICENSE", "README.md", "MIGRATION.md", "manifest.json"):
                z.write(dest / name, name)
        hashes = "".join(f"{digest(p)}  {p.name}\n" for p in sorted(dest.iterdir()) if p.is_file())
        (dest / "SHA256SUMS").write_text(hashes, encoding="utf-8")
        print(f"Release assets: {dest}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", type=Path, help="Use an existing Haxall/SkySpark 4 runtime instead of downloading Haxall")
    parser.add_argument("--package", action="store_true", help="Create verified release assets in dist/vVERSION")
    options = parser.parse_args()
    build(options.runtime.resolve() if options.runtime else runtime_home(), options.package)
