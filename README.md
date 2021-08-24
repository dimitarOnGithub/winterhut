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
```bash
pip3 install <list later lol>
```
