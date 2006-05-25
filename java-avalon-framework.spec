Summary:	The Avalon Framework
#Summary(pl):	
Name:		avalon-framework
Version:	4.3
Release:	0.1
License:	Apache v2.0
Group:		Libraries
Source0:	http://www.apache.org/dist/excalibur/avalon-framework/source/%{name}-api-%{version}-src.tar.gz
# Source0-md5:	9dd92ffe60d3375eb386cde18039acf1
Source1:	http://www.apache.org/dist/excalibur/avalon-framework/source/%{name}-impl-%{version}-src.tar.gz
# Source1-md5:	8b792355d6719ab4f02dc6a59fc21dcc
URL:		http://excalibur.apache.org/framework/
BuildRequires:	ant >= 1.5
BuildRequires:	jpackage-utils
BuildRequires:	rpmbuild(macros) >= 1.300
BuildArch:	noarch
ExclusiveArch:	i586 i686 pentium3 pentium4 athlon %{x8664} noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Avalon Framework consists of interfaces that define relationships
between commonly used application components, best-of-practice pattern
enforcements, and several lightweight convenience implementations of
the generic components.

#%description -l pl

%prep
%setup -q -c -T
# double gzip... sigh.
zcat %{SOURCE0} | tar xz
zcat %{SOURCE1} | tar xz

%build
required_jars='junit'
export CLASSPATH="`/usr/bin/build-classpath $required_jars`"
export JAVA_HOME=%{java_home}
export JAVAC=%{javac}
export JAVA=%{java}

# nope.  doesn't work.  nooo-way.
cd %{name}-api-%{version}
%{ant}
cd ..

cd %{name}-impl-%{version}
%{ant}
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

# XXX

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar
