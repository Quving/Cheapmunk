build_cheapmunk:
	docker build -t telegram-cheapmunk . 

run_cheapmunk:
	docker run -it -d -v $(shell pwd):/cheapmunk --name telegram-cheapmunk telegram-cheapmunk 

start_cheapmunk:
	docker start telegram-cheapmunk

stop_cheapmunk:
	docker stop telegram-cheapmunk
