from invoke import task
import os
import re
import sys
import tempfile
import shutil
import glob

ACTIVATE = ". ./venv/bin/activate;"
PACKAGE = "tarproc"
VENV = "venv"
PYTHON3 = f"{VENV}/bin/python3"
PIP = f"{VENV}/bin/pip"
TEMP = "tarproc.yaml tarproc.yml"
DOCKER = "tarproctest"

commands = (
    "tar2tsv tarcats tarfirst tarmix tarpcat tarproc tarshow tarsort tarsplit tsv2tar"
).split()


@task
def virtualenv(c):
    "Build the virtualenv."
    c.run(f"git config core.hooksPath .githooks")
    c.run(f"test -d {VENV} || python3 -m venv {VENV}")
    c.run(f"{ACTIVATE}{PIP} install -r requirements.dev.txt")
    c.run(f"{ACTIVATE}{PIP} install -r requirements.txt")


@task(virtualenv)
def test(c):
    "Run the tests."
    c.run(f"{PYTHON3} -m pytest")


@task
def newversion(c):
    "Increment the version number."
    assert "working tree clean" in c.run("git status").stdout
    text = open("setup.py").read()
    version = re.search('version *= *"([0-9.]+)"', text).group(1)
    print("old version", version)
    text = re.sub(
        r'(version *= *"[0-9]+[.][0-9]+[.])([0-9]+)"',
        lambda m: f'{m.group(1)}{1+int(m.group(2))}"',
        text,
    )
    version = re.search('version *= *"([0-9.]+)"', text).group(1)
    print("new version", version)
    with open("setup.py", "w") as stream:
        stream.write(text)
    with open("VERSION", "w") as stream:
        stream.write(version)
    c.run(f"grep 'version *=' setup.py")
    c.run(f"git add VERSION setup.py")
    c.run(f"git commit -m 'incremented version'")
    # the git push will do a test
    c.run(f"git push")


@task
def release(c):
    "Tag the current version as a release on Github."
    assert "working tree clean" in c.run("git status").stdout
    version = open("VERSION").read().strip()
    os.system(f"hub release create {version}")  # interactive


pydoc_template = """
# Module `{module}`

```
{text}
```
"""

command_template = """
# Command `{command}`

```
{text}
```
"""


@task
def gendocs(c):
    "Generate docs."
    document = ""
    for fname in glob.glob("tarproclib/*.py"):
        module, ext = os.path.splitext(fname)
        module = re.sub("/", ".", module)
        with os.popen(f"{ACTIVATE}{PYTHON3} -m pydoc {module}") as stream:
            text = stream.read()
        document += pydoc_template.format(text=text, module=module)
    with open("docs/pydoc.md", "w") as stream:
        stream.write(document)
    document = ""
    for command in commands:
        with os.popen(f"{ACTIVATE}{PYTHON3}{command} --help ") as stream:
            text = stream.read()
        text = re.sub("```", "", text)
        document = command_template.format(text=text, command=command)
    with open("docs/commands.md", "w") as stream:
        stream.write(document)


@task(gendocs)
def pubdocs(c):
    "Generate and publish docs."
    modified = os.popen("git status").readlines()
    for line in modified:
        if "modified:" in line and ".md" not in line:
            print("non-documentation file modified; commit manually", file=sys.stderr)
    c.run("git add docs/*.md README.md")
    c.run("git commit -a -m 'documentation update'")
    c.run("git push")


@task
def clean(c):
    "Remove temporary files."
    c.run(f"rm -rf {TEMP}")
    c.run(f"rm -rf build dist")


@task
def cleanall(c):
    "Remove temporary files and virtualenv."
    c.run(f"rm -rf {TEMP}")
    c.run(f"rm -rf venv build dist")


@task(test)
def twine_pypi_release(c):
    "Manually push to PyPI via Twine."
    c.run("rm -f dist/*")
    c.run("$(PYTHON3) setup.py sdist bdist_wheel")
    c.run("twine check dist/*")
    c.run("twine upload dist/*")


base_container = f"""
FROM ubuntu:19.10
ENV LC_ALL=C
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -qqy update
RUN apt-get install -qqy git
RUN apt-get install -qqy python3
RUN apt-get install -qqy python3-pip
RUN apt-get install -qqy python3-venv
RUN apt-get install -qqy curl
WORKDIR /tmp
RUN python3 -m venv venv
RUN . venv/bin/activate; pip install --no-cache-dir pytest
"""

github_test = f"""
FROM tarproctest-base
ENV SHELL=/bin/bash
RUN git clone https://git@github.com/tmbdev/tarproc.git /tmp/tarproc
WORKDIR /tmp/tarproc
RUN python3 -m venv venv
RUN . venv/bin/activate; pip install --no-cache-dir pytest
RUN . venv/bin/activate; pip install --no-cache-dir -r requirements.txt
RUN . venv/bin/activate; python3 -m pytest
"""

pypi_test = f"""
FROM tarproctest-base
ENV SHELL=/bin/bash
RUN git clone https://git@github.com/tmbdev/tarproc.git /tmp/tarproc
WORKDIR /tmp/tarproc
RUN python3 -m venv venv
RUN . venv/bin/activate; pip install --no-cache-dir pytest
RUN . venv/bin/activate; pip install --no-cache-dir -r requirements.txt
RUN . venv/bin/activate; python3 -m pytest
"""


def docker_build(c, instructions, files=[], nocache=False):
    with tempfile.TemporaryDirectory() as dir:
        with open(dir + "/Dockerfile", "w") as stream:
            stream.write(instructions)
        for fname in files:
            shutil.copy(fname, dir + "/.")
        flags = "--no-cache" if nocache else ""
        c.run(f"cd {dir} && docker build {flags} .")


def here(s):
    return f"<<EOF\n{s}\nEOF\n"


@task
def dockerbase(c):
    "Build a base container."
    docker_build(c, base_container)


@task(dockerbase)
def githubtest(c):
    "Test the latest version on Github in a docker container."
    docker_build(c, github_test, nocache=True)


@task
def pypitest(c):
    "Test the latest version on PyPI in a docker container."
    docker_build(c, pypi_test, nocache=True)


required_files = f"""
.github/workflows/pypi.yml
.github/workflows/test.yml
.github/workflows/testpip.yml
.githooks/pre-push
.gitignore
mkdocs.yml
""".strip().split()


@task
def checkall(c):
    "Check for existence of required files."
    for (root, dirs, files) in os.walk(f"./{PACKAGE}"):
        if "/__" in root:
            continue
        assert "__init__.py" in files, (root, dirs, files)
    assert os.path.isdir("./docs")
    for fname in required_files:
        assert os.path.exists(fname), fname
    assert "run: make" not in open(".github/workflows/test.yml").read()

