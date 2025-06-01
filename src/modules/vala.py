from modules.utils import execute, info, write_and_replace_name

import pathlib
import os

ROOT_MESON_TEMPLATE = """
project('%PROJECT_NAME%', ['c', 'vala'],
          version: '0.1.0',
    meson_version: '>= 0.62.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

i18n = import('i18n')
gnome = import('gnome')

subdir('src')
subdir('po')

gnome.post_install(
     glib_compile_schemas: true,
    gtk_update_icon_cache: true,
  update_desktop_database: true,
)
"""

ROOT_MESON_TEMPLATE_BARE = """
project('%PROJECT_NAME%', ['c', 'vala'],
  version : '0.1')

subdir('src')
"""

SOURCE_MESON_TEMPLATE = """
%PROJECT_NAME%_sources = [
  'App.vala',
]

%PROJECT_NAME%_deps = [
  dependency('gtk4'),
  dependency('glib-2.0'),
  dependency('libadwaita-1', version: '>= 1.4'),
]

blueprints = custom_target('blueprints',
  input: files(
    # LIST YOUR BLUEPRINT FILES HERE
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

%PROJECT_NAME%_sources += gnome.compile_resources('%PROJECT_NAME%-resources',
  '%PROJECT_NAME%.gresource.xml',
  dependencies: blueprints,
  c_name: '%PROJECT_NAME%'
)

executable('%PROJECT_NAME%', %PROJECT_NAME%_sources,
  dependencies: %PROJECT_NAME%_deps,
       install: true,
)
"""

SOURCE_MESON_TEMPLATE_BARE = """
dependencies = [
    # dependencies
]

sources = [
    # source files
]

executable('%PROJECT_NAME%', dependencies : dependencies, install : true)
"""

PO_MESON_TEMPLATE = """
i18n.gettext('%PROJECT_NAME%', preset: 'glib')
"""

DIRENV_CONTENT = "use flake"

FLAKE_TEMPLATE = """
{
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
    nativeBuildInputs = with pkgs; [
      meson
      ninja
      vala
      gcc
      pkg-config
      gobject-introspection
    ];
    buildInputs = with pkgs; [];
  in {
    devShells.${system}.default = pkgs.mkShell {
      inherit nativeBuildInputs buildInputs;
      packages = [
        pkgs.vala-language-server
    };

    packages.${system}.default = pkgs.stdenv.mkDerivation {
      name = "%PROJECT_NAME%";
      version = "0.1";
      src = ./.;

      inherit nativeBuildInputs buildInputs;
    };
  };
}
"""


def create_nix_files(root, p_name):
    write_and_replace_name(root / "flake.nix", FLAKE_TEMPLATE, p_name)
    (root / ".envrc").write_text(DIRENV_CONTENT)
    execute("direnv", "allow", str(root))


def create_vala_project(args):
    root = pathlib.Path(args.directory)
    p_name = args.project_name.lower()

    info("Creating project root...")
    (root / "src").mkdir(parents=True, exist_ok=True)

    if args.nix:
        info("Generating nix files...")
        create_nix_files(root, p_name)

    info("Creating main vala file...")
    open(root / "src" / "main.vala", "x").close()

    info("Creating meson files...")
    if args.minimal:
        write_and_replace_name(root / "meson.build", ROOT_MESON_TEMPLATE_BARE, p_name)
        write_and_replace_name(
            root / "src" / "meson.build", SOURCE_MESON_TEMPLATE_BARE, p_name
        )
    else:
        (root / "po").mkdir(exist_ok=True)
        (root / "src" / "ui").mkdir(exist_ok=True)
        write_and_replace_name(root / "meson.build", ROOT_MESON_TEMPLATE, p_name)
        write_and_replace_name(
            root / "src" / "meson.build", SOURCE_MESON_TEMPLATE, p_name
        )
        write_and_replace_name(root / "po" / "meson.build", PO_MESON_TEMPLATE, "")

    info("Done")
