Name     : jdk-atinject
Version  : 1
Release  : 4
URL      : https://github.com/javax-inject/javax-inject/archive/1.tar.gz
Source0  : https://github.com/javax-inject/javax-inject/archive/1.tar.gz
Source1  : http://repo1.maven.org/maven2/javax/inject/javax.inject-tck/1/javax.inject-tck-1.pom
Patch0   : atinject-target-1.5.patch
Summary  : No detailed summary available
Group    : Development/Tools
License  : Apache-2.0
BuildRequires : openjdk-dev
BuildRequires : javapackages-tools
BuildRequires : jdk-junit4
BuildRequires : python3-dev
BuildRequires : six
BuildRequires : lxml
BuildRequires : xmvn

%description
No detailed description available

%prep
%setup -q -n javax-inject-1
mv %{SOURCE1} tck-pom.xml
ln -s /usr/share/java lib

%patch0 -p1

# Fix dep in TCK pom
sed -i -e 's/pom\.groupId/project.groupId/' tck-pom.xml

# J2EE API symlinks
python3 /usr/share/java-utils/mvn_file.py :javax.inject atinject javax.inject/atinject

# TCK sub-package
python3 /usr/share/java-utils/mvn_file.py :javax.inject-tck atinject-tck
python3 /usr/share/java-utils/mvn_package.py :javax.inject-tck tck

%build
alias rm=:
alias xargs=:
alias javadoc='javadoc -Xdoclint:none'
. ./build.sh

python3 /usr/share/java-utils/mvn_artifact.py pom.xml build/dist/javax.inject.jar
python3 /usr/share/java-utils/mvn_artifact.py tck-pom.xml build/tck/dist/javax.inject-tck.jar

%install
xmvn-install  -R .xmvn-reactor -n atinject -d %{buildroot}

%files
%defattr(-,root,root,-)
/usr/share/java/atinject-tck.jar
/usr/share/java/atinject.jar
/usr/share/java/javax.inject/atinject.jar
/usr/share/maven-metadata/atinject-tck.xml
/usr/share/maven-metadata/atinject.xml
/usr/share/maven-poms/atinject-tck.pom
/usr/share/maven-poms/atinject.pom
/usr/share/maven-poms/javax.inject/atinject.pom
