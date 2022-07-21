### How to build zfs-release RPMs:
```
sudo yum -y install rpm-build
mkdir -p ~/rpmbuild/{BUILDROOT,SPECS,RPMS,SRPMS,SOURCES,BUILD}
cp RPM-GPG-KEY-openzfs* *.repo ~/rpmbuild/SOURCES
cp zfs-release.spec ~/rpmbuild/SPECS/
rpmbuild -ba ~/rpmbuild/SPECS/zfs-release.spec
```
The built RPMs are in `~/rpmbuild/RPMS/noarch/` and `~/rpmbuild/SRPMS/`.

The released zfs-release RPMs should be checked into the top level
`fedora/` and `epel/` directories in this repo.  Remember to build
the Fedora RPMs on Fedora, and the EPEL RPMs on a RHEL derivative, as
the SPEC file does different things depending on the OS it's built upon.

### Keys ###
`RPM-GPG-KEY-openzfs-key1` - Older key used to sign packages for Fedora 36
(and older) and EL 6-8.  It's header is encoded with SHA1, and thus is not
supported by default on EL 9.

`RPM-GPG-KEY-openzfs-key2` - Newer key used to sign EL 9 (and newer) and
Fedora 37 (and newer).  It's header is encoded with SHA512.
