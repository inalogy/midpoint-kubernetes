#!/bin/bash
echo "opening /mnt"
cd /mnt/


echo "Adding wget to image"

apt-get update && apt-get install wget -y
wget https://download.evolveum.com/dummy-hr-and-addressbook-for-live-demo/addressbook.war
wget https://download.evolveum.com/dummy-hr-and-addressbook-for-live-demo/hr.war


echo "creating directory /mnt/WEB-INF/classes"
ls -la 
mkdir -p /mnt/WEB-INF/classes

ls -la /mnt/


echo "copy of properties to /mnt/WEB-INF/classes"
ls -la /tmp/hr/
cp /tmp/hr/jdbc.properties /mnt/WEB-INF/classes/

ls -la /tmp/add/
cp /tmp/add/application.properties /mnt/WEB-INF/classes/

echo "packing configurations to war files"
cd /mnt/
jar uvf addressbook.war WEB-INF/classes/application.properties
jar uvf hr.war WEB-INF/classes/jdbc.properties

echo "deleting configurations"
rm -rf WEB-INF/
