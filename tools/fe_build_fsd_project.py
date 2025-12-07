#!/usr/bin/env python3
"""
Scaffold a full Feature-Sliced Design (FSD) 7-layer structure and an optional feature.

Creates under {appname}/src/:

  app/
  processes/
  pages/
  widgets/
  features/
  entities/
  shared/
  test/
  types/

Subfolders:

- app/:       ui, router, providers, store, styles, config
- shared/:    ui, lib, api, config, hooks, styles, types
- processes/: ui, model, api, lib, config
- pages/:     ui, model, api, lib, config
- widgets/:   ui, model, api, lib, config
- entities/:  ui, model, api, lib, config

Optional feature slice:

  {appname}/src/features/{feature-name}/
    ui/
    model/
    api/
    lib/
    config/
    index.ts

Non-destructive behavior:

- Only creates folders that do NOT already exist.
- Does NOT overwrite existing files or folders.
- Creates index.ts for the feature only if it does not already exist.

Usage (from the directory that contains {appname}/):

    # Create base FSD structure only:
    python scaffold_fsd.py my-app

    # Create base FSD structure + a feature:
    python scaffold_fsd.py my-app "User Auth"
"""

import argparse
from pathlib import Path
import re
import sys
from typing import List, Tuple


def to_kebab_case(name: str) -> str:
    """
    Convert a feature name like 'User Auth' or 'user_auth'
    into kebab-case: 'user-auth'.
    """
    name = name.strip()
    # Replace non-alphanumeric with hyphens
    name = re.sub(r"[^A-Za-z0-9]+", "-", name)
    # Collapse multiple hyphens
    name = re.sub(r"-+", "-", name)
    return name.strip("-").lower()


def safe_mkdir(path: Path, created: List[Path], existing: List[Path]) -> None:
    """
    Create a directory only if it does not already exist.

    - If created, append to `created`.
    - If already exists, append to `existing`.
    """
    if path.exists():
        existing.append(path)
        return
    path.mkdir(parents=True, exist_ok=False)
    created.append(path)


def create_base_fsd_structure(app_root: Path) -> Tuple[List[Path], List[Path]]:
    """
    Create the base FSD 7-layer structure under {app_root}/src, non-destructively.

    Returns:
        (created_paths, existing_paths)
    """
    created: List[Path] = []
    existing: List[Path] = []

    # Ensure app_root exists
    if not app_root.exists():
        app_root.mkdir(parents=True, exist_ok=False)
        created.append(app_root)
    else:
        existing.append(app_root)

    src_root = app_root / "src"
    safe_mkdir(src_root, created, existing)

    # 7 layers + test/types
    layer_names = [
        "app",
        "processes",
        "pages",
        "widgets",
        "features",
        "entities",
        "shared",
        "test",
        "types",
    ]

    layers = {name: src_root / name for name in layer_names}
    for path in layers.values():
        safe_mkdir(path, created, existing)

    # app/ standard subfolders
    app_root_dir = layers["app"]
    for sub in ["ui", "router", "providers", "store", "styles", "config"]:
        safe_mkdir(app_root_dir / sub, created, existing)

    # shared/ standard subfolders
    shared_root_dir = layers["shared"]
    for sub in ["ui", "lib", "api", "config", "hooks", "styles", "types"]:
        safe_mkdir(shared_root_dir / sub, created, existing)

    # processes, pages, widgets, entities: create FSD segments (ui/model/api/lib/config)
    for layer_name in ["processes", "pages", "widgets", "entities"]:
        layer_root = layers[layer_name]
        for sub in ["ui", "model", "api", "lib", "config"]:
            safe_mkdir(layer_root / sub, created, existing)

    # features/ root is left as a container; per-feature segments are created separately

    return created, existing


def create_feature_structure(app_root: Path, feature_name: str) -> Tuple[List[Path], List[Path]]:
    """
    Safely create the FSD-style structure for a feature under {app_root}/src/features.

    - Only creates new folders (does not touch existing ones).
    - Only creates index.ts if it does not already exist.

    Returns:
        (created_paths, existing_paths)
    """
    created: List[Path] = []
    existing: List[Path] = []

    feature_folder_name = to_kebab_case(feature_name)

    src_root = app_root / "src"
    features_root = src_root / "features"
    safe_mkdir(features_root, created, existing)

    feature_root = features_root / feature_folder_name
    safe_mkdir(feature_root, created, existing)

    # Segments for the feature slice
    subfolders = ["ui", "model", "api", "lib", "config"]
    for sub in subfolders:
        safe_mkdir(feature_root / sub, created, existing)

    # Create a minimal index.ts if it doesn't exist
    index_file = feature_root / "index.ts"
    if not index_file.exists():
        index_file.write_text(
            f"// Public API for feature '{feature_folder_name}'\n"
            f"// export {{ ExampleComponent }} from './ui/ExampleComponent';\n"
        )
        created.append(index_file)
    else:
        existing.append(index_file)

    return created, existing


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Scaffold a full FSD 7-layer structure under {appname}/src "
            "and optionally create a feature slice under features/."
        )
    )
    parser.add_argument(
        "appname",
        help="App folder name (relative path), e.g. 'my-app'",
    )
    parser.add_argument(
        "feature_name",
        nargs="?",
        help="Optional feature name, e.g. 'User Auth' (will be converted to kebab-case)",
    )

    args = parser.parse_args()

    app_root = Path(args.appname)

    # 1) Create base FSD structure
    created_base, existing_base = create_base_fsd_structure(app_root)

    # 2) Optionally create a feature slice
    created_feature: List[Path] = []
    existing_feature: List[Path] = []

    if args.feature_name:
        feature_name = args.feature_name.strip()
        if not feature_name:
            print("Error: feature name cannot be empty.")
            sys.exit(1)

        created_feature, existing_feature = create_feature_structure(app_root, feature_name)

    # ---- Logging ----
    print(f"\nApp root: {app_root.resolve()}")

    if created_base:
        print("\nCreated base FSD folders/files:")
        for p in created_base:
            print(f"  + {p}")
    else:
        print("\nNo new base FSD folders/files were created.")

    if existing_base:
        print("\nBase FSD folders/files that already existed (left unchanged):")
        for p in existing_base:
            print(f"  = {p}")

    if args.feature_name:
        print(f"\nFeature: {args.feature_name} → '{to_kebab_case(args.feature_name)}'")
        if created_feature:
            print("\nCreated feature folders/files:")
            for p in created_feature:
                print(f"  + {p}")
        else:
            print("\nNo new feature folders/files were created.")

        if existing_feature:
            print("\nFeature folders/files that already existed (left unchanged):")
            for p in existing_feature:
                print(f"  = {p}")

    print("\nDone (non-destructive).")


if __name__ == "__main__":
    main()
