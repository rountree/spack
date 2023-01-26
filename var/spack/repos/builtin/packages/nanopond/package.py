# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class Nanopond(MakefilePackage):
    """nanopond is a minimal virtual life simulation created in C by
    Adam Ierymenko."""

    homepage="https://github.com/adamierymenko/nanopond"
    version("dev", branch="dev", git="https://github.com/rountree/nanopond.git")
    depends_on("sdl2", type=("build", "link", "run"))
    maintainer = ["rountree"]

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('nanopond', prefix.bin)

