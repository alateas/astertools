if [ ! -n "$1" ] 
then
    echo 'Missed argument : MySQL password'
    exit 1
fi
    
#folder structure
cd /home/astertools
mkdir tmp tmp/python_eggs logs protected_media protected_media/faxes

#nginx
cd scripts/install
yum -y install nginx
rm -f /etc/nginx/nginx.conf
cp nginx.conf /etc/nginx/
cp virtual.conf /etc/nginx/conf.d/django.conf
cp fastcgi.conf /etc/nginx/django_fastcgi.conf

#python
yum -y install python-setuptools python-devel python-flup python-sqlite2
easy_install MySQL-python

#django
cd /tmp
wget http://www.djangoproject.com/download/1.3/tarball/
tar xzvf Django-1.3.tar.gz
cd Django-1.3
python setup.py install

#mysql
mysql -u root --password=$1 -e "create database astertools";


#setup
cd /home/astertools/src
cat /home/astertools/scripts/install/db_settings.py | sed -e "s/<password>/$1/" > db_settings.py
python manage.py syncdb --noinput
python hylafax/scripts/fax_devs_init.py
python manage.py createsuperuser --username admin --email dmitrymashkin@gmail.com --noinput
python manage.py changepassword admin

#adding to hylafax faxrcvd script
cd /var/spool/hylafax/bin
mv -f faxrcvd-elastix.php faxrcvd-elastix.php.bak
cp /home/astertools/scripts/install/faxrcvd-elastix.php faxrcvd-elastix.php

#permissions
cd /home/astertools
chmod -R 777 tmp logs protected_media

#adding to startup
chkconfig nginx on
echo -e "sh /home/astertools/scripts/runfcgi.sh" >> /etc/rc.d/rc.local

#start
sh /home/astertools/scripts/nginx_run.sh
