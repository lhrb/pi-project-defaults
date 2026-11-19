import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
from tempfile import NamedTemporaryFile


TEMPLATE = Path(__file__).resolve().parent
REGISTRY = TEMPLATE / ".template-installs.json"
FILES = ("architecture.md", "AGENTS.md", ".pi/settings.json")
DIRECTORIES = (".pi/agents", ".pi/prompts", ".pi/skills")


def regular_file(root, relative):
    """Check each path component before reading or replacing a managed file."""
    path = root
    for part in relative.parts[:-1]:
        path /= part
        if path.is_symlink() or (path.exists() and not path.is_dir()):
            raise ValueError(f"Expected a real directory: {path}")
    path = root / relative
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise ValueError(f"Expected a regular file: {path}")
    return path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def template_files(*, include_all, include_settings, selected):
    paths = [Path(name) for name in FILES
             if include_all or (include_settings and name == ".pi/settings.json")]
    for directory in DIRECTORIES:
        paths.extend(
            path.relative_to(TEMPLATE)
            for path in sorted((TEMPLATE / directory).rglob("*"))
            if path.is_file() or path.is_symlink()
        )
    sources = {path: digest(source) for path in paths
               if (not selected or path in selected)
               and (source := regular_file(TEMPLATE, path)).exists()}
    if missing := selected - sources.keys():
        raise ValueError("Not managed template files: " + ", ".join(map(str, sorted(missing))))
    return sources


def replace_file(path, write):
    with NamedTemporaryFile(dir=path.parent, delete=False) as temp:
        staged = Path(temp.name)
    try:
        write(staged)
        os.replace(staged, path)
    finally:
        staged.unlink(missing_ok=True)


def sync(project, baseline, sources, *, installing=False, overwrite=False):
    if not project.is_dir() or project.resolve() != project:
        print(f"Skipped project (missing or moved): {project}", file=sys.stderr)
        return False

    ok = True
    for relative, expected in sources.items():
        key = relative.as_posix()
        target = project / relative
        try:
            target = regular_file(project, relative)
            current = digest(target) if target.exists() else None
            if current != expected:
                previous = baseline.get(key)
                safe = current == previous and (not installing or current is None)
                if not (safe or overwrite):
                    print(f"Skipped local change: {target}", file=sys.stderr)
                    ok = False
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                replace_file(target, lambda staged: shutil.copy(TEMPLATE / relative, staged))
                print(f"Copied: {target}")
            baseline[key] = expected
        except (OSError, ValueError) as error:
            print(f"Skipped {target}: {error}", file=sys.stderr)
            ok = False
    return ok


def named_projects(registry, names):
    projects = {}
    for name in map(str.strip, names.split(",")):
        matches = [path for path in registry if Path(path).name == name]
        if not matches:
            raise ValueError(f"No registered project named {name!r}")
        if len(matches) > 1:
            raise ValueError(f"Ambiguous project name {name!r}: " + ", ".join(matches))
        path = matches[0]
        projects[path] = registry[path]
    return projects


def main():
    parser = argparse.ArgumentParser(description="Sync Pi project defaults.")
    commands = parser.add_subparsers(dest="command", required=True)
    install = commands.add_parser("install")
    install.add_argument("project", type=Path)
    update = commands.add_parser("update")
    update.add_argument("--name", metavar="NAME[,NAME...]", help="Update only these registered project names")
    update.add_argument("--overwrite", nargs="*", metavar="FILE", type=Path,
                        help="Replace managed .pi/ files by default, or pass exact template-relative file paths")
    update.add_argument("--all", action="store_true", help="Overwrite all managed files; requires --overwrite")
    args = parser.parse_args()
    installing = args.command == "install"
    overwrite = not installing and args.overwrite is not None
    selected = set(args.overwrite or ()) if overwrite else set()
    if not installing and args.all and (not overwrite or selected):
        update.error("Use --all with --overwrite and without file paths")

    try:
        if REGISTRY.is_symlink() or (REGISTRY.exists() and not REGISTRY.is_file()):
            raise ValueError(f"Expected a regular registry file: {REGISTRY}")
        registry = json.loads(REGISTRY.read_text()) if REGISTRY.exists() else {}
        if not isinstance(registry, dict) or any(
            not Path(project).is_absolute() or not isinstance(baseline, dict)
            for project, baseline in registry.items()
        ):
            raise ValueError(f"Invalid registry: {REGISTRY}")

        if installing:
            project = args.project.resolve(strict=True)
            if not project.is_dir() or project == TEMPLATE or TEMPLATE in project.parents:
                raise ValueError("Use an existing project directory outside the template")
            projects = {str(project): registry.setdefault(str(project), {})}
        else:
            projects = named_projects(registry, args.name) if args.name is not None else registry

        sources = template_files(include_all=installing or args.all or bool(selected),
                                 include_settings=overwrite, selected=selected)
        if not projects:
            print("No registered projects. Run install.sh first.")
            return 0
        if not sources:
            raise ValueError("No template files found")

        ok = True
        for path, baseline in projects.items():
            print(f"{'Registering' if installing else 'Updating'}: {path}", flush=True)
            if not sync(Path(path), baseline, sources, installing=installing, overwrite=overwrite):
                ok = False
        replace_file(REGISTRY, lambda staged: staged.write_text(json.dumps(registry, indent=2) + "\n"))
        return 0 if ok else 1
    except (OSError, ValueError, RuntimeError) as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
