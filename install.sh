cd /opt
sudo mkdir -p bibbox/
sudo chmod -R 777 bibbox/
cd bibbox/
git clone https://github.com/bibbox/sys-bibbox.git
cd sys-bibbox
mkdir -p log
cd log
touch system.log
cd /opt/bibbox/sys-bibbox
cd sys-proxy/proxyconfig
mkdir -p sites/
cd /opt/bibbox/sys-bibbox
source CLIFunctions.sh
mkdir -p application-instance
docker-compose up -d
cd /opt
sudo chmod -R 777 bibbox 
grep -qxF "source /opt/bibbox/sys-bibbox/CLIFunctions.sh" ~/.bashrc || echo "source /opt/bibbox/sys-bibbox/CLIFunctions.sh" >> ~/.bashrc
#echo "source /opt/bibbox/sys-bibbox/CLIFunctions.sh" >> ~/.bashrc


