#
# Conditional build:
%bcond_with	tests		# build and run tests
#
%define		srcname	avalon-framework
%include	/usr/lib/rpm/macros.java
Summary:	The Avalon Framework
Summary(pl.UTF-8):	Szkielet Avalon
Name:		java-avalon-framework
Version:	4.3
Release:	2
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://www.apache.org/dist/excalibur/avalon-framework/source/%{srcname}-api-%{version}-src.tar.gz
# Source0-md5:	d4cffb4ba1d07bdc517ac6e322636495
Source1:	http://www.apache.org/dist/excalibur/avalon-framework/source/%{srcname}-impl-%{version}-src.tar.gz
# Source1-md5:	62499f9b32ac4d722a46a4f2cfbbf0d8
Patch0:		%{name}-tests.patch
URL:		http://excalibur.apache.org/framework/
BuildRequires:	ant >= 1.5
%{?with_tests:BuildRequires:	ant-junit}
BuildRequires:	ant-nodeps
BuildRequires:	java-avalon-logkit
BuildRequires:	java-commons-logging
%{?with_tests:BuildRequires:	java-junit}
BuildRequires:	java-log4j
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.553
BuildRequires:	sed >= 4.0
BuildConflicts:	java-gcj-compat-devel
Requires:	jpackage-utils
Obsoletes:	avalon-framework
BuildArch:	noarch
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
%setup -q -c -a1

%patch0 -p1

# Fix for wrong-file-end-of-line-encoding problem
find '(' -name '*.html' -o -name '*.css' -o -name '*.xml' ')' -print0 | xargs -0 %undos

%build
required_jars="avalon-logkit %{?with_tests:junit}"
export CLASSPATH=$(build-classpath $required_jars)

%ant -f %{srcname}-api-%{version}/build.xml \
	-Dnoget=1 \
	dist %{?with_tests:test}

required_jars="avalon-logkit commons-logging log4j"
export CLASSPATH=$(build-classpath $required_jars):$(pwd)/avalon-framework-api-%{version}/target/avalon-framework-api-%{version}.jar
%ant -f %{srcname}-impl-%{version}/build.xml \
	-Dnoget=1 \
	dist %{?with_tests:test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a %{srcname}-api-%{version}/target/%{srcname}-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-api-%{version}.jar
ln -sf %{srcname}-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-api.jar
cp -a %{srcname}-impl-%{version}/target/%{srcname}-impl-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-impl-%{version}.jar
ln -sf %{srcname}-impl-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-impl.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_javadir}/%{srcname}-api.jar
%{_javadir}/%{srcname}-api-%{version}.jar
%{_javadir}/%{srcname}-impl.jar
%{_javadir}/%{srcname}-impl-%{version}.jar
