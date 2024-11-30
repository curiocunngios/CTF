# Install essential tools
sudo apt-get update
sudo apt-get install -y build-essential
sudo apt-get install -y gdb
sudo apt-get install -y python3
sudo apt-get install -y python3-pip
sudo apt-get install -y pwntools
sudo apt-get install -y checksec

# Install GDB-Pwndbg (better GDB interface)
git clone https://github.com/pwndbg/pwndbg
cd pwndbg
./setup.sh