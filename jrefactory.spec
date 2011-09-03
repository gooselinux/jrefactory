# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define	section	devel

Name:		jrefactory
Version:	2.8.9
Release:	9.10%{?dist}
Epoch:		0
Summary:	JRefactory and Pretty Print
License:	BSD and ASL 1.1 and GPL+
Group:		Development/Libraries
Source0:	http://downloads.sourceforge.net/project/jrefactory/JRefactory/2.8.9%20_%202.8.10%20%28Final%29/jrefactory-2.8.9-source.zip
Patch0:	jrefactory-2.8.9-fixcrlf.patch
Patch1: jrefactory-savejpg.patch
Patch2: %{name}-%{version}-source14.patch

URL:		http://jrefactory.sourceforge.net/
BuildRequires:	ant
BuildRequires:	jpackage-utils >= 0:1.5
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
JRefactory provides a variety of refactoring and pretty printing tools

%prep
%setup -q -c -n %{name}
find . -name "*.class" -exec rm {} \;
find . -name "*.jar" -exec rm {} \;

mv settings/.Refactory settings/sample
%patch0 -p0 -b .fixcrlf
%patch1 -p1
%patch2 -p1

rm -f src/org/acm/seguin/pmd/swingui/PMDLookAndFeel.java

# remove classes that don't build without said jarfiles
find -name '*.java' | \
    xargs grep -l '^import \(edu\|org\.\(jaxen\|saxpath\)\)\.' | \
        xargs rm

%build
perl -p -i -e 's|^Class-Path:.*||' \
	src/meta-inf/refactory.mf
ant jar

%install
rm -rf $RPM_BUILD_ROOT
# jar
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 ant.build/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar

(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} ${jar/-%{version}/}; done)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0664,root,root,0755)
%doc docs2/{*.html,*.jpg,*.gif,*.txt} settings/sample
%{_javadir}/*

%changelog
* Wed Jan 13 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.8.9-9.10
- Remove buildrood in install section.

* Sat Jan 9 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.8.9-9.9
- Use upstream sources.
- Drop gcj_support.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0:2.8.9-9.8
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.8.9-9.7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 20 2009 Deepak Bhole <dbhole@redhat.com> - 0:2.8.9-8.7
- Add patch to set source to 1.4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.8.9-8.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:2.8.9-7.6
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:2.8.9-7jpp.5
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:2.8.9-7jpp.4
- Autorebuild for GCC 4.3

* Thu Sep 20 2007 Deepak Bhole <dbhole@redhat.com> - 0:2.8.9-6jpp.4
- Add %%{?dist} as per new policy

* Thu Aug 10 2006 Deepak Bhole <dbhole@redhat.com> - 0:2.8.9-6jpp.3
- Changed release to match new spec.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:2.8.9-6jpp_2fc
- Rebuilt

* Thu Jul 20 2006 Deepak Bhole <dbhole@redhat.com> - 0:2.8.9-6jpp_1fc
- Added conditional native compilation.
- From gbenson@redhat:
-    Remove classes that don't build without said jarfiles.
-    Avoid Sun-specific classes.

* Fri Apr 28 2006 Fernando Nasser <fnasser@redhat.com> - 0:2.8.9-5jpp
- First JPP 1.7 build

* Tue Apr 19 2005 Ralph Apel <r.apel at r-apel.de> - 0:2.8.9-4jpp
- Patch to fix CRLF problem; THX to Richard Bullington-McGuire

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:2.8.9-3jpp
- Rebuild with ant-1.6.2

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:2.8.9-2jpp
- Upgrade to Ant 1.6.X

* Wed Jan 21 2004 David Walluck <david@anti-microsoft.org> 0:2.8.9-1jpp
- 2.8.9
- remove Class-Path from manifest

* Mon Dec 15 2003 Paul Nasrat <pauln at truemesh.com> 0:2.6.40-1jpp
- Initial Release
