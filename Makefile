.PHONY: run checkenv train test record clean-models clean-logs

run:
	python ./src/game.py

checkenv:
	python ./src/checkenv.py

train:
	-@ulimit -n 4096
	python ./src/train.py $(ARGS)

test:
	python ./src/test.py $(ARGS)

record:
	python ./src/record.py $(ARGS)

clean-models:
	rm -rf models/PPO

clean-logs:
	rm -rf wandb logs
