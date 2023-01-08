# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class E3smScream(Package):
    """Package for E3SMs Scream dependencies. Doesn't install anything other than dependencies."""

    homepage = "https://e3sm.org/"
    url      = "https://github.com/E3SM-Project/scream"
    git      = "https://github.com/E3SM-Project/scream.git"
    #maintainers = ['Jessicat-H','mtaylo12']

    #version('master',git="https://github.com/E3SM-Project/scream.git", branch='master',submodules=True)
    #version("v2.0.0-beta.3", submodules=True)
    version("master",branch="master", submodules=True)

    depends_on('cmake@3.18.0')
    #depends_on('mvapich2@2.3')
    depends_on('netcdf-fortran@4.4.4')
    depends_on('netcdf-c@4.4.1')
    depends_on('cuda')
    depends_on('parallel-netcdf@1.10.0')

    #depends_on('rust', type=("build","link","run"))
    #depends_on('python@3.10.8', type=("build", "link", "run"))
    depends_on('py-poetry', type=("build","link","run"))
    depends_on('py-pip', type=("build","link","run"))
    depends_on('py-pyyaml',type=("build", "link", "run"))
    depends_on('py-pylint',type=("build","link","run"))

    depends_on('py-psutil',type=("build", "link", "run"))
    depends_on('perl-xml-libxml',type=("build", "link", "run"))

    depends_on('util-linux-uuid@:2.36.2',when='%intel')
    depends_on('intel-mkl@2020.0.166',when='%intel',type=("build", "link", "run"))

    conflicts('diffutils@3.8:',when='%intel')
    conflicts('netcdf-c@4.5:')

    def install(self, spec, prefix):
        # sanity_check_prefix requires something in the install directory
        mkdirp(prefix.lib)
