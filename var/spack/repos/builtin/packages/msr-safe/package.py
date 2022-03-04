# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class MsrSafe(Package):
    """Linux kernel module for safer access to model-specific registers."""

    homepage = "https://github.com/LLNL/msr-safe"
    url      = "https://github.com/LLNL/msr-safe/archive/v1.6.0.tar.gz"

    maintainers = ['rountree']

    version('1.6.0', sha256='defe9d12e2cdbcb1a9aa29bb09376d4156c3dbbeb7afc33315ca4b0b6859f5bb')

    def install(self, spec, prefix):
        make()

    # Totally ripped off from lcio/package.py
    @run_after('install')
    def install_source(self):
        install_tree('.',self.prefix + '/build')

# Ponder this:
rountree@ruby961 /dev/shm$ spack install msr-safe
==> Installing msr-safe-1.6.0-niwbdz7kjayo5v5izodfsxo63a2jphhw
==> No binary for msr-safe-1.6.0-niwbdz7kjayo5v5izodfsxo63a2jphhw found: installing from source
==> Fetching https://github.com/LLNL/msr-safe/archive/v1.6.0.tar.gz
==> No patches needed for msr-safe
==> msr-safe: Executing phase: 'install'
==> Error: ProcessError: Command exited with status 2:
    'make' '-j16'

4 errors found in build log:
     3     /dev/shm/spack/lib/spack/env/gcc/gcc  -DVERSION=\"1.6.0\" -fPIC -shared -c msrsave/msrsave_main.c -o msrsave/msrsave_main.o
     4     /dev/shm/spack/lib/spack/env/gcc/gcc  -DVERSION=\"1.6.0\" -fPIC -shared -c msrsave/msrsave.c -o msrsave/msrsave.o
     5     /dev/shm/spack/lib/spack/env/gcc/gcc  -DVERSION=\"1.6.0\" msrsave/msrsave_main.o msrsave/msrsave.o -o msrsave/msrsave
     6     make -C /lib/modules/3.10.0-1160.53.1.1chaos.ch6.x86_64/build M=/dev/shm modules
     7     make[1]: Entering directory `/usr/src/kernels/3.10.0-1160.53.1.1chaos.ch6.x86_64'
     8     make[1]: warning: jobserver unavailable: using -j1.  Add `+' to parent make rule.
  >> 9     scripts/Makefile.build:44: /dev/shm/Makefile: No such file or directory
  >> 10    make[2]: *** No rule to make target `/dev/shm/Makefile'.  Stop.
  >> 11    make[1]: *** [_module_/dev/shm] Error 2
     12    make[1]: Leaving directory `/usr/src/kernels/3.10.0-1160.53.1.1chaos.ch6.x86_64'
  >> 13    make: *** [all] Error 2

See build log for details:
  /dev/shm/spack/var/spack/stage/rountree/spack-stage-msr-safe-1.6.0-niwbdz7kjayo5v5izodfsxo63a2jphhw/spack-build-out.txt
