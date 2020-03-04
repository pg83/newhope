LC_ALL=C

clear:
	python3 cli cleanup

commit: clear
	ssh-add ~/.ssh/id_rsa_1
	LC_ALL=C git status | grep 'Untracked files:' | wc -l | xargs 
	git add -A
	git commit -m "A"
	git push

merge: clear
	ssh-add ~/.ssh/id_rsa_1
	git add -A
	git commit -m "A"
	git pull
