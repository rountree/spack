# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import llnl.util.filesystem as fs

class Linux(Package):
    """Linux kernel source from kernel.org."""

    homepage = "https://kernel.org"
    url      = "https://mirrors.edge.kernel.org/pub/linux/kernel/v5.x/linux-5.15.3.tar.gz"

    maintainers = ['rountree']

    version('5.15.3', sha256='e2e780e3d75e9d1223c57cd218680c58637a45bc02b1cb02a7174f8a01682180')

    def url_for_version(self, version):
        if( version.up_to(1) >= Version(3) ):
            return "https://mirrors.edge.kernel.org/pub/linux/kernel/v{0}.x/linux-{1}.tar.gz".format(version.up_to(1), version)
        else:
            return "https://mirrors.edge.kernel.org/pub/linux/kernel/v{0}/linux-{1}.tar.gz".format(version.up_to(2), version)

    # FIXME: Add dependencies if required.
    # depends_on('foo')
    def install(self, spec, prefix):
        if not os.path.isdir(self.stage.source_path):
            return
        src_target = os.path.join(prefix, 'share', spec.name, 'src')
        fs.install_tree(self.stage.source_path, src_target)
