# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Tar(AutotoolsPackage, GNUMirrorPackage):
    """GNU Tar provides the ability to create tar archives, as well as various
    other kinds of manipulation."""

    homepage = "https://www.gnu.org/software/tar/"
    gnu_mirror_path = "tar/tar-1.32.tar.gz"

    executables = [r'^tar$']

    tags = ['core-packages']

    version('1.34', sha256='03d908cf5768cfe6b7ad588c921c6ed21acabfb2b79b788d1330453507647aed')
    version('1.32', sha256='b59549594d91d84ee00c99cf2541a3330fed3a42c440503326dab767f2fbb96c')
    version('1.31', sha256='b471be6cb68fd13c4878297d856aebd50551646f4e3074906b1a74549c40d5a2')
    version('1.30', sha256='4725cc2c2f5a274b12b39d1f78b3545ec9ebb06a6e48e8845e1995ac8513b088')
    version('1.29', sha256='cae466e6e58c7292355e7080248f244db3a4cf755f33f4fa25ca7f9a7ed09af0')
    version('1.28', sha256='6a6b65bac00a127a508533c604d5bf1a3d40f82707d56f20cefd38a05e8237de')

    # A saner default than gzip?
    variant('zip', default='pigz', values=('gzip', 'pigz'), description='Default compression program for tar -z')

    depends_on('iconv')

    # Compression
    depends_on('gzip', type='run', when='zip=gzip')
    depends_on('pigz', type='run', when='zip=pigz')
    depends_on('zstd+programs', type='run', when='@1.31:')
    depends_on('xz', type='run')  # for xz/lzma
    depends_on('bzip2', type='run')

    patch('tar-pgi.patch',    when='@1.29')
    patch('config-pgi.patch', when='@:1.29')
    patch('se-selinux.patch', when='@:1.29')
    patch('argp-pgi.patch',   when='@:1.29')
    patch('gnutar-configure-xattrs.patch', when='@1.28')
    # The NVIDIA compilers do not currently support some GNU builtins.
    # Detect this case and use the fallback path.
    patch('nvhpc-1.30.patch', when='@1.30:1.32 %nvhpc')
    patch('nvhpc-1.34.patch', when='@1.34 %nvhpc')
    # Workaround bug where __LONG_WIDTH__ is not defined
    patch('nvhpc-long-width.patch', when='@1.34 %nvhpc')

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'tar \(GNU tar\) (\S+)', output)
        return match.group(1) if match else None

    def configure_args(self):
        # Note: compression programs are passed by abs path,
        # so that tar can locate them when invoked without spack load.
        args = [
            '--with-libiconv-prefix={0}'.format(self.spec['iconv'].prefix),
            '--with-xz={0}'.format(self.spec['xz'].prefix.bin.xz),
            '--with-lzma={0}'.format(self.spec['xz'].prefix.bin.lzma),
            '--with-bzip2={0}'.format(self.spec['bzip2'].prefix.bin.bzip2),
        ]

        if '^zstd' in self.spec:
            args.append('--with-zstd={0}'.format(self.spec['zstd'].prefix.bin.zstd))

        # Choose gzip/pigz
        zip = self.spec.variants['zip'].value
        if zip == 'gzip':
            gzip_path = self.spec['gzip'].prefix.bin.gzip
        elif zip == 'pigz':
            gzip_path = self.spec['pigz'].prefix.bin.pigz
        args.append('--with-gzip={}'.format(gzip_path))

        spec=self.spec
        # Pre-OneAPI Intel compilers search for a local copy of gcc and
        # degrade their feature set to match what was found.  In the
        # case where that gcc compiler is version < 5.0, m4@1.4.19 fails
        # to build.
        #
        # Passing in the -no-gcc option works in the following cases.
        #
        #       intel@14.0.3    intel@16.0.4
        #       intel@17.0.2    intel@18.0.2    
        #
        # These versions fail:
        #
        #       intel@15.0.6
        #
        # Passing in -gcc-name=/path/to/preferred/gcc works in this case.
        # This is not portable and will need to be hardcoded.
        #       intel@19.1.2.254
        #
        # No modifications are necessary for these versions.
        #       oneapi@2021.2.0 oneapi@2022.1.0
        #
        if spec.satisfies('%intel@14:18'):
            args.append('CFLAGS=-no-gcc')
        # Uncomment and modify if you are using icc v19 and the default
        # gcc in your environment is < gcc5.
        # elif spec.satisfies('%intel@19'):
        #    args.append('CFLAGS=-gcc-name=/usr/tce/packages/gcc/gcc-10.2.1/bin/gcc')
        return args
