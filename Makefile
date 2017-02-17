build:
	docker build -t telegram-cheapmunk . 

run:
	docker run -it -d  --restart=always -e BOT_TOKEN=$(BOT_TOKEN_CHEAPMUNK) -v $(shell pwd):/cheapmunk --name telegram-cheapmunk telegram-cheapmunk 


