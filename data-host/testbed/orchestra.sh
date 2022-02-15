# shutdown command
pssh -i -h shut_hosts.txt -A -l root -x '-tt' init 0

# telegraf halt
pssh -i -h all-nodes.txt -A -l root -x '-tt' systemctl stop telegraf

# telegraf start
pssh -i -h all-nodes.txt -A -l root -x '-tt' systemctl start telegraf