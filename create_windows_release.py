import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import markdown as markdown

from randovania import VERSION, get_data_path
from randovania.cli import prime_database
from randovania.games.prime import default_data

zip_folder = "randovania-{}".format(VERSION)

package_folder = Path("dist", "randovania")
shutil.rmtree(package_folder, ignore_errors=True)

prime_database.export_as_binary(default_data.decode_default_prime2(),
                                get_data_path().joinpath("binary_data", "prime2.bin"))

subprocess.run([sys.executable, "-m", "PyInstaller", "randovania.spec"])

with zipfile.ZipFile("dist/{}.zip".format(zip_folder), "w", compression=zipfile.ZIP_DEFLATED) as release_zip:
    for f in package_folder.glob("**/*"):
        print("Adding", f)
        release_zip.write(f, "{}/{}".format(zip_folder, f.relative_to(package_folder)))

    with open("README.md") as readme_file:
        readme_html = markdown.markdown(readme_file.read())
        release_zip.writestr(zip_folder + "/README.html", readme_html)

    for subdir, _, files in os.walk("randovania-readme"):
        for file in files:
            path = os.path.join(subdir, file)
            release_zip.write(path, "{}/{}".format(zip_folder, path))
