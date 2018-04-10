# pwnhub
Binary porn for those who do



apt-get install python2.7 python-pip python-dev git libssl-dev libffi-dev build-essential python-capstone
pip install --upgrade pip
pip install --upgrade pwntools

git clone https://github.com/longld/peda.git ~/.peda
alias switch-peda='echo "source ~/.peda/peda.py" > ~/.gdbinit'

wget -O ~/.gdbinit-gef.py -q https://github.com/hugsy/gef/raw/master/gef.py
alias switch-gef='echo "source ~/.gdbinit-gef.py" > ~/.gdbinit'
