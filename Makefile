LC_ALL=C


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
	./cli make -j1 -vm ll=debug

clear:
	./cli cleanup

commit:
	ssh-add ~/.ssh/id_rsa
	ssh-add ~/.ssh/id_rsa_1
	LC_ALL=C git status | grep 'Untracked files:' | wc -l | xargs 
	git add -A
	git commit -m "A"
	git push

all: tests make make-debug clear
