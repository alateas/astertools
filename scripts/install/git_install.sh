yum -y install git
cd /opt
git clone git://github.com/alateas/astertools.git astertools
sh astertools/scripts/install/install.sh $*
