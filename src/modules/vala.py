from modules.utils import execute, info

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

PO_MESON_TEMPLATE = """
i18n.gettext('%PROJECT_NAME%', preset: 'glib')
"""

def create_vala_project(args):
    root = pathlib.Path(args.directory)

    info("Creating project root...")
    os.makedirs(str(root / "src" / "ui"),  exist_ok=True)
    os.mkdir(str(root / "po"))

    info("Creating main vala file...")
    open(root / "src" / "App.vala", 'x').close()

    info("Creating meson files...")
    (root / "meson.build").write_text(ROOT_MESON_TEMPLATE.replace("%PROJECT_NAME%", args.project_name.lower()))
    (root / "src" / "meson.build").write_text(SOURCE_MESON_TEMPLATE.replace("%PROJECT_NAME%", args.project_name.lower()))
    (root / "po" / "meson.build").write_text(PO_MESON_TEMPLATE)

    info("Done")
