LC_ALL=C

clear:
	python3 cli cleanup

commit: clear
	LC_ALL=C git status | grep 'Untracked files:' | wc -l | xargs 
	git add -A
	git commit -m "A"
	/bin/sh -c 'eval $$(ssh-agent); ssh-add ~/.ssh/id_rsa_1; git push || true'
	killall -9 ssh-agent

merge: clear
	ssh-add ~/.ssh/id_rsa_1
	git add -A
	git commit -m "A"
	git pull
