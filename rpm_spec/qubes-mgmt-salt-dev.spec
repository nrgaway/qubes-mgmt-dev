%{!?version: %define version %(make get-version)}
%{!?rel: %define rel %(make get-release)}
%{!?package_name: %define package_name %(make get-package_name)}
%{!?package_summary: %define package_summary %(make get-summary)}
%{!?package_description: %define package_description %(make get-description)}

%{!?formula_name: %define formula_name %(make get-formula_name)}
%{!?state_name: %define state_name %(make get-state_name)}
%{!?saltenv: %define saltenv %(make get-saltenv)}
%{!?pillar_dir: %define pillar_dir %(make get-pillar_dir)}
%{!?formula_dir: %define formula_dir %(make get-formula_dir)}

Name:      %{package_name}
Version:   %{version}
Release:   %{rel}%{?dist}
Summary:   %{package_summary}
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
%{package_description}

%build

%install
make install DESTDIR=%{buildroot} LIBDIR=%{_libdir} BINDIR=%{_bindir} SBINDIR=%{_sbindir} SYSCONFDIR=%{_sysconfdir}

%post
# Update Salt Configuration
qubesctl state.sls config -l quiet --out quiet > /dev/null || true
qubesctl saltutil.clear_cache -l quiet --out quiet > /dev/null || true
qubesctl saltutil.sync_all refresh=true -l quiet --out quiet > /dev/null || true

# Enable States
#qubesctl topd.enable bind saltenv=%{saltenv} -l quiet --out quiet > /dev/null || true

%files
%defattr(-,root,root)
%attr(750, root, root) %dir /srv/formulas/dev/development-tools-formula
/srv/formulas/dev/development-tools-formula/bind/init.sls
/srv/formulas/dev/development-tools-formula/bind/init.top
/srv/formulas/dev/development-tools-formula/dev-tools/bind-qubes-src-to-srv
/srv/formulas/dev/development-tools-formula/LICENSE
/srv/formulas/dev/development-tools-formula/_modules/bind.py*
/srv/formulas/dev/development-tools-formula/README.rst

%changelog
