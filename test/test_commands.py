#
# Copyright (c) 2017-2019 NVIDIA CORPORATION. All rights reserved.
# This file is part of webloader (see TBD).
# See the LICENSE file for licensing terms (BSD-style).
#

import os
import subprocess
import re


PYTHON3 = os.environ.get("PYTHON3", "python3")
PREFIX = os.environ.get("PREFIX", ".")
PY = f"{PYTHON3} {PREFIX}/"


def run(script, *args, **kw):
    result = subprocess.check_output(
        ["/bin/bash", "-c", script], stderr=subprocess.STDOUT
    ).decode("utf-8")
    for arg in args:
        print(result)
        assert re.search(arg, result), (arg, result)


def test_lines2tar(tmpdir):
    run(f"{PY}lines2tar --help", "Create a tar file")
    run(f"(echo a; echo b; echo c) > {tmpdir}/lines.txt")
    run(f"{PY}lines2tar < {tmpdir}/lines.txt | tar tf -", "000000.txt")


def test_tar2json(tmpdir):
    run(f"{PY}tar2json --help", "Extract parts")
    run(f"(echo a; echo b; echo c) > {tmpdir}/lines.txt")
    run(f"{PY}lines2tar < {tmpdir}/lines.txt | {PY}tar2json -k txt", "txt: a")


def test_tarcats(tmpdir):
    run(f"{PY}tarcats --help", "Concatenate")


def test_tarcats_2(tmpdir):
    run(f"(echo a; echo b; echo c) | {PY}lines2tar > {tmpdir}/tar1.tar")
    run(f"(echo d; echo e; echo f) | {PY}lines2tar > {tmpdir}/tar2.tar")
    run(f"{PY}tarcats {tmpdir}/tar1.tar {tmpdir}/tar2.tar > {tmpdir}/tar12.tar")
    run(f"{PY}tar2json -k txt < {tmpdir}/tar12.tar", "txt: a", "txt: e")


def test_tarproc(tmpdir):
    run(f"{PY}tarproc --help", "Each sample is extracted")


def test_tarproc_2():
    tmpdir = "."
    run(f"(echo a; echo b; echo c) | {PY}lines2tar > {tmpdir}/tar1.tar")
    run(f"{PY}tarproc -c 'cp sample.txt sample.x.txt' {tmpdir}/tar1.tar -o {tmpdir}/tar2.tar")
    run(f"{PY}tar2json -k x.txt < {tmpdir}/tar2.tar", 'x.txt: a')


def test_tarshow(tmpdir):
    run(f"{PY}tarshow --help", "Show data inside")


def test_tarshow_2(tmpdir):
    run(f"{PY}tarshow testdata/imagenet-000000.tar", "b'746'", "n07734744")
    run(f"(echo a; echo b; echo c) | {PY}lines2tar > {tmpdir}/tar1.tar")
    run(f"{PY}tarshow {tmpdir}/tar1.tar", "txt.*b'b'")


def test_tarsort(tmpdir):
    run(f"{PY}tarsort --help", "Sort the samples inside")
    run(f"(echo c; echo b; echo a) | {PY}lines2tar > {tmpdir}/tar1.tar")
    run(f"{PY}tarsort {tmpdir}/tar1.tar -o {tmpdir}/tar2.tar -s txt")
    run(f"{PY}tar2json -k txt < {tmpdir}/tar2.tar", 'txt: a')
    # TODO check for actually sorted

def test_tarsplit(tmpdir):
    run(f"{PY}tarsplit --help", "Split a tar")
