# TODO
# - chicken-egg: who was first, avalon-framework or avalon-logkit?
#
# Conditional build:
%bcond_with	tests		# build and run tests
#
%include	/usr/lib/rpm/macros.java
Summary:	The Avalon Framework
Summary(pl.UTF-8):	Szkielet Avalon
Name:		avalon-framework
Version:	4.3
Release:	0.1
License:	Apache v2.0
Group:		Libraries
Source0:	http://www.apache.org/dist/excalibur/avalon-framework/source/%{name}-api-%{version}-src.tar.gz
# Source0-md5:	d4cffb4ba1d07bdc517ac6e322636495
Source1:	http://www.apache.org/dist/excalibur/avalon-framework/source/%{name}-impl-%{version}-src.tar.gz
# Source1-md5:	62499f9b32ac4d722a46a4f2cfbbf0d8
Patch0:		%{name}-tests.patch
URL:		http://excalibur.apache.org/framework/
BuildRequires:	ant >= 1.5
%{?with_tests:BuildRequires:	ant-junit}
BuildRequires:	ant-nodeps
BuildRequires:	avalon-logkit
BuildRequires:	jakarta-commons-logging
BuildRequires:	jpackage-utils
%{?with_tests:BuildRequires:	junit}
BuildRequires:	logging-log4j
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	sed >= 4.0
BuildArch:	noarch
ExclusiveArch:	i586 i686 pentium3 pentium4 athlon %{x8664} noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Avalon Framework consists of interfaces that define relationships
between commonly used application components, best-of-practice pattern
enforcements, and several lightweight convenience implementations of
the generic components.

%description -l pl.UTF-8
Avalon Framework składa się z interfejsów definiujących powiązania
między powszechnie używanymi komponentami aplikacji, najlepszymi
narzucanymi wzorami i kilkoma lekkimi wygodnymi implementacjami
ogólnych komponentów.

%prep
%setup -q -c -T
%{__tar} -xzf %{SOURCE0}
%{__tar} -xzf %{SOURCE1}
%patch0 -p1

# Fix for wrong-file-end-of-line-encoding problem
find '(' -name '*.html' -o -name '*.css' -o -name '*.xml' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

%build
required_jars="avalon-logkit %{?with_tests:junit}"
export CLASSPATH=$(build-classpath $required_jars)

%ant -f %{name}-api-%{version}/build.xml \
	-Dnoget=1 \
	dist %{?with_tests:test}

required_jars="avalon-logkit commons-logging log4j"
export CLASSPATH=$(build-classpath $required_jars):$(pwd)/avalon-framework-api-4.3/target/avalon-framework-api-4.3.jar
%ant -f %{name}-impl-%{version}/build.xml \
	-Dnoget=1 \
	dist %{?with_tests:test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a %{name}-api-%{version}/target/%{name}-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-api-%{version}.jar
ln -sf %{name}-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-api.jar

cp -a %{name}-impl-%{version}/target/%{name}-impl-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-impl-%{version}.jar
ln -sf %{name}-impl-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-impl.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar
