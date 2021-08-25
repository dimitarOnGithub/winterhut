# winterhut

Hey y'all :) This is the source code of my personal website over at <TODO: add domain here>. The site is using Flask, one of Python's web frameworks, and a bunch of other packages from the same ecosystem. That's really there is to it, only reason I'm adding a README is because Github keeps complaining and I also need a shared place to note down useful commands and list dependencies.

Useful Bash function to avoid having to constantly export stuff
```bash
prep() {
	cd <path to repo checkout>
	export FLASK_APP=winterhut
	export FLASK_ENV=development
	export APP_CONFIG_PATH=<path to config>
}
```

Dependencies
CentOS 8:
```bash
yum groupinstall "Development Tools"
yum install libffi-devel zlib zlib-devel bzip2-devel openssl-devel sqlite-devel readline-devel
```
After the installation fo libffi-devel, we need to load the new libffi.so
```bash
ldconfig
```

Install PyENV as per https://github.com/pyenv/pyenv#installation
Install Python 3.9.2
```bash
pyenv install 3.9.2
```
Set it as local version for the project
```bash
pyenv local 3.9.2
```

Install Flask and its dependencies 
```bash
pip3 install flask flask_wtf flask-bcrypt flask-login flask_mail pymsql flask-sqlalchemy email_validator
```
