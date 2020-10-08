cd /opt
sudo mkdir -p bibbox/
sudo chmod -R 777 bibbox/
cd bibbox/
git clone https://github.com/bibbox/sys-bibbox.git
cd sys-bibbox
mkdir -p log
cd log
touch system.log
cd ..
cd sys-proxy/proxyconfig
mkdir -p sites/
source CLIFunctions.sh
mkdir -p application-instance
docker-compose up -d
cd ..
cd ..
sudo chmod -R 777 bibbox 
