LC_ALL=C
THRS?=3

tests: test_coro test_self test_pslic test_offload test_ctx test_queue test_pubsub test_template test_wait test_green	test_preproc

test_coro:
	./cli test coro

test_self:
	./cli test self

test pslice:
	./cli test pslice

test_offload:
	./cli test offload

test_ctx:
	./cli test ctx

test_queue:
	./cli test queue

test_pubsub:
	./cli test pubsub

test_template:
	./cli test template

test_wait:
	./cli test wait

test_green:
	./cli test green

test_preproc:
	./clit test preproc

make:
	./cli make -j16 -v

make-debug:
	./cli make --install-dir /pkg -j1 -vm ll=debug

linux:
	./cli makefile --os linux | ./cli make -f - -j$(THRS)

clear:
	./cli cleanup

commit:
	./cli cleanup
	ssh-add ~/.ssh/id_rsa_1
	LC_ALL=C git status | grep 'Untracked files:' | wc -l | xargs 
	git add -A
	git commit -m "A"
	git push

merge:
	ssh-add ~/.ssh/id_rsa_1
	git add -A
	git commit -m "A"
	git pull

all: tests make make-debug clear
