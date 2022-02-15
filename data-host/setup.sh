# REDHAT INSTALLS
# install influxdb
wget https://dl.influxdata.com/influxdb/releases/influxdb2-2.1.1-amd64.rpm
yum -y localinstall -i influxdb2-2.1.1-amd64.rpm
cp influxdb.conf /etc/influxdb/influxdb.conf
sudo systemctl enable influxdb
sudo systemctl start influxdb

# install influx client (database management portal)
apt install influxdb-client

# install grafana
wget https://dl.grafana.com/enterprise/release/grafana-enterprise-8.3.6-1.x86_64.rpm
yum -y install grafana-enterprise-8.3.6-1.x86_64.rpm
systemctl enable grafana-server
systemctl start grafana-server