%{!?version: %define version %(cat version)}

Name:      qubes-mgmt-salt-dev
Version:   %{version}
Release:   1%{?dist}
Summary:   Various tools and scripts for qubes-mgmt-salt development
License:   GPL 2.0
URL:	   http://www.qubes-os.org/

Group:     System administration tools
BuildArch: noarch
Requires:  qubes-mgmt-salt
Requires:  qubes-mgmt-salt-template
Requires:  qubes-mgmt-salt-all-vim
Requires:  qubes-mgmt-salt-all-yamlscript-renderer
Requires:  qubes-mgmt-salt-all-gnugp

%define _builddir %(pwd)

%description
Various tools and scripts for qubes-mgmt-salt development

%build

%install
make install DESTDIR=%{buildroot} LIBDIR=%{_libdir} BINDIR=%{_bindir} SBINDIR=%{_sbindir} SYSCONFDIR=%{_sysconfdir}

%post
# Update Salt Configuration
qubesctl state.sls config -l quiet --out quiet > /dev/null || true
qubesctl saltutil.clear_cache -l quiet --out quiet > /dev/null || true
qubesctl saltutil.sync_all refresh=true -l quiet --out quiet > /dev/null || true

# Enable States
#qubesctl top.enable bind saltenv=%{saltenv} -l quiet --out quiet > /dev/null || true

%files
%defattr(-,root,root)
%doc LICENSE README.rst
%attr(750, root, root) %dir /srv/formulas/dev/development-tools-formula
/srv/formulas/dev/development-tools-formula/bind/init.sls
/srv/formulas/dev/development-tools-formula/bind/init.top
/srv/formulas/dev/development-tools-formula/dev-tools/bind-qubes-src-to-srv
/srv/formulas/dev/development-tools-formula/LICENSE
/srv/formulas/dev/development-tools-formula/_modules/bind.py*
/srv/formulas/dev/development-tools-formula/README.rst

%changelog
