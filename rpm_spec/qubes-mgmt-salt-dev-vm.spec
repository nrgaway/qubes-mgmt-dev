%{!?version: %define version %(cat version)}

Name:      qubes-mgmt-salt-dev-vm
Version:   %{version}
Release:   1%{?dist}
Summary:   All Qubes+Salt Management formulas available for AppVM's.
License:   GPL 2.0
URL:	   http://www.qubes-os.org/

Group:     System administration tools
BuildArch: noarch
Requires:  qubes-mgmt-salt
Requires:  qubes-mgmt-salt-extra-formulas
Requires:  qubes-mgmt-salt-vm-formulas
BuildRequires: PyYAML
BuildRequires: tree
Requires(post): /usr/bin/qubesctl
Conflicts:  qubes-mgmt-salt-vm

%define _builddir %(pwd)

%description
Summary:   All Qubes+Salt Management formulas available for AppVM's.

%prep
# we operate on the current directory, so no need to unpack anything
# symlink is to generate useful debuginfo packages
rm -f %{name}-%{version}
ln -sf . %{name}-%{version}
%setup -T -D

%build

%install

%post

%files
%defattr(-,root,root)

%changelog
