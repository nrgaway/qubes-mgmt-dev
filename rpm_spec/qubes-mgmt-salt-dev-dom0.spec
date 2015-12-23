%{!?version: %define version %(cat version)}

Name:      qubes-mgmt-salt-dev-dom0
Version:   %{version}
Release:   1%{?dist}
Summary:   All Qubes+Salt Management formulas available for dom0.
License:   GPL 2.0
URL:	   http://www.qubes-os.org/

Group:     System administration tools
BuildArch: noarch
Requires:  qubes-mgmt-salt-dev
Requires:  qubes-mgmt-salt-dom0
Requires:  qubes-mgmt-salt-dom0-fix-permissions
Requires:  qubes-mgmt-salt-dom0-policy-qubesbuilder
Requires:  qubes-mgmt-salt-dom0-template-upgrade
Requires:  qubes-mgmt-salt-dom0-formulas
BuildRequires: PyYAML
BuildRequires: tree
Requires(post): /usr/bin/qubesctl

%define _builddir %(pwd)

%description
Summary:   All Qubes+Salt Management formulas available for dom0.

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
