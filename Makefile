LC_ALL=C

clear:
	python3 cli cleanup

commit: clear
	/bin/sh -c 'eval $$(ssh-agent); ssh-add ~/.ssh/id_rsa_1'
	LC_ALL=C git status | grep 'Untracked files:' | wc -l | xargs 
	git add -A
	git commit -m "A"
	-git push
	-killall -9 ssh-agent

merge: clear
	ssh-add ~/.ssh/id_rsa_1
	git add -A
	git commit -m "A"
	git pull
