LC_ALL=C


clear:
	python3 cli cleanup


commit: clear
	git add -A
	git commit -m "A"
	/bin/sh -c 'eval $$(ssh-agent); ssh-add ~/.ssh/id_rsa_1; (git push || true); killall -9 ssh-agent'


merge: clear
	git add -A
	git commit -m "A"
	/bin/sh -c 'eval $$(ssh-agent); ssh-add ~/.ssh/id_rsa_1; (git pull || true); killall -9 ssh-agent'
