### How to build zfs-release RPMs:
```
sudo yum -y install rpm-build
mkdir -p ~/rpmbuild/{BUILDROOT,SPECS,RPMS,SRPMS,SOURCES,BUILD}
cp RPM-GPG-KEY-zfsonlinux zfs-el.repo zfs-fedora.repo ~/rpmbuild/SOURCES
cp zfs-release.spec ~/rpmbuild/SPECS/
rpmbuild -ba ~/rpmbuild/SPECS/zfs-release.spec
```
The built RPMs are in `~/rpmbuild/RPMS/noarch/` and `~/rpmbuild/SRPMS/`.

The released zfs-release RPMs should be checked into the top level
`fedora/` and `epel/` directories in this repo.  Remember to build
the Fedora RPMs on Fedora, and the EPEL RPMs on a RHEL derivative, as
the SPEC file does different things depending on the OS it's built upon.
