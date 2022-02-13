# install influxdb
wget https://dl.influxdata.com/influxdb/releases/influxdb2-2.1.1-amd64.deb
dpkg -i influxdb2-2.1.1-amd64.deb
cp influxdb.conf /etc/influxdb/influxdb.conf
service influxdb start

# install influx client (database management portal)
apt install influxdb-client

# install grafana
apt-get install -y adduser libfontconfig1
wget https://dl.grafana.com/oss/release/grafana_8.3.6_amd64.deb
dpkg -i grafana_8.3.6_amd64.deb