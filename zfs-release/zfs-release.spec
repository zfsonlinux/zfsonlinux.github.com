%if 0%{?fedora}
%global osname      fedora
%endif

%if 0%{?rhel}
%global osname      el
%endif

Name:           zfs-release-%{osname}
Version:        2
Release:        1
Summary:        OpenZFS Repository Configuration

Group:          System Environment/Base
License:        BSD
URL:            http://zfsonlinux.org
Source0:        zfs-el.repo
Source1:        zfs-fedora.repo
Source10:       RPM-GPG-KEY-zfsonlinux
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

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
%{__install} -Dp -m644 \
    %{SOURCE10} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg

# Yum .repo files
%{__install} -p -m644 zfs-%{osname}.repo \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/zfs.repo

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_sysconfdir}/pki/rpm-gpg/*
%config(noreplace) %{_sysconfdir}/yum.repos.d/*

%post
# We only need to import the key on RHEL 7 and below
# https://github.com/zfsonlinux/zfsonlinux.github.com/pull/63
%if 0%{?rhel} && 0%{?rhel} < 8
rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-zfsonlinux
%endif

%changelog
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
