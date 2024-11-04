#!/usr/bin/env bash

######################################################################
# 4) configure and build openzfs modules
######################################################################

set -eu

cd zfsonlinux.github.com/zfs-release
sudo yum -y install rpm-build
mkdir -p ~/rpmbuild/{BUILDROOT,SPECS,RPMS,SRPMS,SOURCES,BUILD}
cp RPM-GPG-KEY-openzfs* *.repo ~/rpmbuild/SOURCES
cp zfs-release.spec ~/rpmbuild/SPECS/
rpmbuild -ba ~/rpmbuild/SPECS/zfs-release.spec

# building the zfs module was ok
echo 0 > /var/tmp/build-exitcode.txt

# reset cloud-init configuration and poweroff
sudo cloud-init clean --logs
exit 0
