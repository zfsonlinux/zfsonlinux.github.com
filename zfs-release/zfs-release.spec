%if 0%{?fedora}
%global osname      fedora
%endif

%if 0%{?rhel}
%global osname      el
%endif

Name:           zfs-release
Version:        3
Release:        3%{dist}
Summary:        OpenZFS Repository Configuration

Group:          System Environment/Base
License:        BSD
URL:            http://zfsonlinux.org
Source0:        zfs-el.repo
Source1:        zfs-fedora.repo
Source10:       RPM-GPG-KEY-openzfs-key1
Source11:       RPM-GPG-KEY-openzfs-key2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Obsoletes:      zfs-release-%{osname} <= 2-1
Provides:       zfs-release = %{version}-%{release}

# We have two GPG keys -
#
# RPM-GPG-KEY-openzfs-key1:
#     Older, SHA1-encoded key used on RHEL 6-8 and Fedora 36 and older.
#
# RPM-GPG-KEY-openzfs-key2:
#     Newer, SHA512-encoded key used on RHEL 9+ and Fedora 37+.  RHEL 9
#     no longer allows SHA1 RPM keys by default.

# RHEL 9 defaults to using zstd for RPM compression.  Unfortunately, CentOS 7
# does not support zstd, so force gzip compression for compatibility.
%define _source_payload w9.gzdio
%define _binary_payload w9.gzdio

%description
OpenZFS repository for Fedora and RHEL variants.

%prep
%setup -c -n %{name} -T
cp -a %{SOURCE0} %{SOURCE1} .

%build
echo "Nothing to build"

%install
rm -rf $RPM_BUILD_ROOT

# Create dirs
install -d -m755 \
  $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg  \
  $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

# GPG Key
%{__install} -Dp -m644 %{SOURCE10} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-openzfs-2013
%{__install} -Dp -m644 %{SOURCE11} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-openzfs-2022

# Create symlinks to the appropriate keys
%if 0%{?rhel}
ln -s RPM-GPG-KEY-openzfs-2013 \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-openzfs-el-6
ln -s RPM-GPG-KEY-openzfs-2013 \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-openzfs-el-7
ln -s RPM-GPG-KEY-openzfs-2013 \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-openzfs-el-8
ln -s RPM-GPG-KEY-openzfs-2022 \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-openzfs-el-9
ln -s RPM-GPG-KEY-openzfs-2022 \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-openzfs-el-10
%endif
%if 0%{?fedora}
ln -s RPM-GPG-KEY-openzfs-2022 \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-openzfs-fedora-38
ln -s RPM-GPG-KEY-openzfs-2022 \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-openzfs-fedora-39
ln -s RPM-GPG-KEY-openzfs-2022 \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-openzfs-fedora-40
ln -s RPM-GPG-KEY-openzfs-2022 \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-openzfs-fedora-41
ln -s RPM-GPG-KEY-openzfs-2022 \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-openzfs-fedora-42
ln -s RPM-GPG-KEY-openzfs-2022 \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-openzfs-fedora-43
ln -s RPM-GPG-KEY-openzfs-2022 \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-openzfs-fedora-44
ln -s RPM-GPG-KEY-openzfs-2022 \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-openzfs-fedora-45
%endif

# Yum .repo files
%{__install} -p -m644 zfs-%{osname}.repo \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/zfs.repo

%if 0%{?rhel} >= 10
# EL10 has an x86-64-v2 variant (AlmaLinux) whose packages cannot be installed
# alongside the x86-64-v3 ones, so it gets its own repo directory.  Replace
# $basearch with a dnf variable that the %post scriptlet sets to the right
# architecture for the host.
sed -i 's|\$basearch/|$zfs_basearch/|g' \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/zfs.repo
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_sysconfdir}/pki/rpm-gpg/*
%config(noreplace) %{_sysconfdir}/yum.repos.d/*
%if 0%{?rhel} >= 10
%ghost %attr(0644,root,root) %{_sysconfdir}/yum/vars/zfs_basearch
%endif

%if 0%{?rhel} >= 10
%post
# Set $zfs_basearch, the architecture zfs.repo uses for this host.  This is
# normally the system architecture, but the AlmaLinux 10 x86-64-v2 variant
# needs 'x86_64_v2'.  That variant's almalinux-release package defines the
# %%x86_64_v2 macro, so use that to detect it.
arch="$(rpm --eval '%%{_arch}' 2>/dev/null)"
if [ "$(rpm --eval '%%{?x86_64_v2}' 2>/dev/null)" = "1" ] ; then
    arch="x86_64_v2"
fi
mkdir -p %{_sysconfdir}/yum/vars
echo "$arch" > %{_sysconfdir}/yum/vars/zfs_basearch
%endif

%changelog
* Tue Nov 10 2026 FingerlessGlov3s <me@fingerlessgloves.me> - 3-3
- Add support for the AlmaLinux 10 x86-64-v2 variant.  On EL10, zfs.repo now
  uses a $zfs_basearch dnf variable in place of $basearch, which is set to
  'x86_64_v2' on x86-64-v2 hosts and to the normal architecture otherwise.
* Tue Nov 03 2026 Tony Hutter <hutter2@llnl.gov> - 3-2
- Add signing key for Fedora 45
* Fri May 01 2026 Tony Hutter <hutter2@llnl.gov> - 3-1
- Add signing key for Fedora 44
* Wed Nov 12 2025 Tony Hutter <hutter2@llnl.gov> - 3-0
- Add new repos for specific versions
* Wed Oct 01 2025 Ralf Ertzinger <ralf@skytale.net> - 2-9
- Add signing key for Fedora 43
* Sat Mar 22 2025 Ralf Ertzinger <ralf@skytale.net> - 2-8
- Add signing key for Fedora 42
* Thu Dec 26 2024 James Reilly <jreilly1821@gmail.com> - 2-7
- Add signing key for EL10
* Wed Oct 16 2024 Ralf Ertzinger <ralf@skytale.net> - 2-6
- Add signing key for Fedora 41, drop link for Fedora 37
* Thu Mar 28 2024 Ralf Ertzinger <ralf@skytale.net> - 2-5
- Add signing key for Fedora 40, drop link for Fedora 36
* Thu Jul 27 2023 Ralf Ertzinger <ralf@skytale.net> - 2-4
- Add signing key for Fedora 39, drop link for Fedora 35
* Tue Jan 03 2023 Ralf Ertzinger <ralf@skytale.net> - 2-3
- Rework key and repo files to allow dynamic (by $releasever variable)
  selection of correct signing keys. This allows major version upgrades
* Mon Jul 25 2022 Tony Hutter <hutter2@llnl.gov> - 2-2
- Add newer, SHA512-encoded, RPM-GPG-KEY-openzfs-key2 key.
- Add "Obsoletes" and "Provides" sections.
* Wed Jun 22 2022 Todd Zullinger <tmz@pobox.com> - 2-1
- Build Fedora and EL packages from the same source
* Wed Jun 22 2022 Tony Hutter <hutter2@llnl.gov> - 2-1
- Switch to a universal zfs-release RPM for all RHEL versions
- Don't import GPG key on RHEL 8 or newer:
  https://github.com/zfsonlinux/zfsonlinux.github.com/pull/63
* Wed Jan 15 2020 Tony Hutter <hutter2@llnl.gov> - 1-8.1
- Default repository updated for 8.1 compatible kmod packages
* Fri Aug 25 2017 Brian Behlendorf <behlendorf1@llnl.gov> - 1-5
- Default repository updated for 7.4 compatible kmod packages
* Mon Dec 12 2016 Brian Behlendorf <behlendorf1@llnl.gov> - 1-4
- Default repository updated for 7.3 compatible kmod packages
* Thu Aug 25 2016 Brian Behlendorf <behlendorf1@llnl.gov> - 1-3
- Changed repository from archive.zfsonlinux.org to download.zfsonlinux.org
- Added kmod repository to zfs.repo
* Thu Aug 7 2014 Brian Behlendorf <behlendorf1@llnl.gov> - 1-2
- Changed '$releasever' to '7' in zfs.repo for RHEL/CentOS compatibility
* Wed Jul 23 2014 Brian Behlendorf <behlendorf1@llnl.gov> - 1-1
- Initial zfs-release package.
