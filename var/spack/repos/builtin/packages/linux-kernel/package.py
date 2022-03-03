# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import llnl.util.tty as tty

class LinuxKernel(Package):
    """Useful for installing Linux kernel source, generating kernel header files and building out-of tree kernel modules."""

    homepage = "https://www.kernel.org/"
    url      = "https://www.kernel.org/pub/linux/kernel/v4.x/linux-4.9.10.tar.xz"
    list_url = "https://www.kernel.org/pub/linux/kernel"
    list_depth = 2

    maintainers = ['rountree']

    variant( 'headers_install', default=False, description='Installs Linux header files.' )
    variant( 'defconfig', default=False, description='Source install + make defconfig.')
    variant( 'modules_prepare', default=False, description='Source install + make defconfig + make modules_prepare' )

    version('4.9.10', sha256='bd6e05476fd8d9ea4945e11598d87bc97806bbc8d03556abbaaf809707661525')

    # Totally ripped of from kernel-headers/package.py
    def setup_build_environment(self, env):
        # This variable is used in the Makefile. If it is defined on the
        # system, it can break the build if there is no build recipe for
        # that specific ARCH
        env.unset('ARCH')

    def install(self, spec, prefix):
        tty.msg("QQQ: install")
        if '+headers_install' in self.spec:
            make('headers_install', 'INSTALL_HDR_PATH={0}'.format(prefix))
        if '+defconfig' in self.spec or '+modules_prepare' in self.spec:
            make('defconfig')
        if '+modules_prepare' in self.spec:
            make('modules_prepare')

    # Totally ripped off from lcio/package.py
    @run_after('install')
    def install_source(self):
        tty.msg("QQQ: install_tree")
        install_tree('.',self.prefix + '/linux')
