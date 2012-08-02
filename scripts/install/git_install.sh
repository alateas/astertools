yum -y install git
cd /home
git clone git://github.com/alateas/astertools.git astertools
sh astertools/scripts/install/install.sh $*
