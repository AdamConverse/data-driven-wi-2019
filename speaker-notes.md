# Big Data Brainstorm

### Overview
1. Who am I
2. Problem definition
	- We want to build a system that can run daily, calculatinng optimal DFS lineups using monte carlo and our own scoring algorithm. Oh and it needs to be highly available and close to free because this is a hobby project
3. Walk through of accounts that need to be setup (Slack, Google Account and Heroku)
4. Docker needs to be installed on everyone's machine
5. Let's code


### Coding
Github Link: https://github.com/AdamConverse/data-driven-wi-2019

SlideDeck: https://docs.google.com/presentation/d/16FTUBHxrE7LS-XA2PoXtyZDRtEAmgphVuHxBCbYAlXs/edit#slide=id.g5df106cd25_0_64

**Step 1 (master):** Setup Repo make sure everyone can run the sample app

- Clone the repo
- Walkthrough the structure. `/app` will hold our application files. The root is docker files (i.e. build configuration)
- Let's create the app basics
	- inside `/app` create `__init__.py`
		- create 3 methods `create_app()`, `load_config(app)`, `redis_url()`
	- create `/app/config` directory
		- create `__init__.py`
		- create `default.py`
	- create `app.py`
		- include the correct imports
		- add the main method
		- add `index()` method to test with
- At this point we should have an example flask application running
	- `cd app`
	- `pip install -r requirements.txt`
	- `python app.py`
	- Open a browser to `http://127.0.0.1:8080/`
- Take a break to help others

**Step 2 (step-2):** Connect to Docker

- Edit `Dockerfile`
- Edit `docker-compose.yml`
	- create `web` service
	- add build command `build: .`
	- add `ports: - "8080:8080"` 
	- add `enviroment: DYNO: "true"`
- At this point you should be able to run `docker-compose up` from the root directory
- Navigate a browser to `localhost:8080`
- Take a break to help others

**Step 3 (step-3):** Setup worker

- Create `app/worker.py`
	- Basic worker setup with main method
- Edit `Dockerfile.worker`
	- Same as the other Dockerfile but this one runs `worker.py` on boot
- Add worker service to `docker-compose.yml`
	- similar to the web service but with `Dockerfile.worker`
	- add `REDIS_URL` to `environment`
	- add `redis` image to services
- `docker-compose up` Navigating to `localhost:8080` should still work

**Step 4 (step-4):** Create our first job

- create `tasks.py` with method `my_task()`
- inside `app.py	`
	- Connect to redis
	- import `tasks.py`
	- Create `job_id` route
- You should now be able to visit `localhost:8080/test-job` and see the `job_id`
- Visit `localhost:8080/job/<job_id>` to view job result


**Step 5 (step-5):** The interesting bits...

- Let's create a job to handle processing of daily fantasy sports data
- Create a new endpoint in `app.py`
	- `run_simulations(month, date, year)` method will queue our simulations job
- in `tasks.py` create `run_simulations(date)` that just returns date
- Test it to make sure the plumbing is working
- Create `draftkings_client.py` inside `app/clients`
	- make sure to include `__init__.py`
- Go back to `tasks.py` and edit `run_simulations()` to include simulation logic
	- Add `select_player()` method
- Now you should be able to run the job and see the simulation results

**Step 6 (step-6):** Integrations / UI / Heroku

- First Heroku
	- If you did not create an account you can now
	- open `heroku.yml` and edit
	- create new application in heroku
	- run `heroku login` from cli
	- run `heroku git:remote -a <your-project>` from cli. You might need to run `git init` first
	- run `heroku stack:set container` to tell heroku to use `heroku.yml`
	- then run `git push heroku master` to deploy. If not on master use `git push heroku yourbranch:master`
	- check the activity tab in heroku for errors
	- Turn on the worker in Resources tab and add Redis in the Add-ons section
	- Open the heroku app and you should see "Hello world!"
	- Run the test job and simulations to verify it's working
- Setup dropbox for automations
	- I highly recommend checking out Big Data Ball https://www.bigdataball.com/
	- Big Data Ball posts a csv of the results of how players performed after each game has been played. We can use this upload as an automation trigger for our app and maybe even as a data source ;)
	- Create a new method in `app.py` called `dropbox()`. This will handle the webhook request
	- Create another method called `dropbox_update()`. Dropbox will ping this endpoint when a change is made
	- Create a method in `tasks.py` called `post_to_slack()` we will edit this later.
	- Redeploy the app
	- Create a dropbox account or use an existing one
	- Go to https://www.dropbox.com/developers/apps/create to create a new app
		- Choose "Dropbox API" in step 1 and Full Dropbox in step 2
	- Setup Dropbox Webhook URIs to point to our app `/dropbox` and test
- Let's connect to slack for a UI
	- If you have an existing slack instance feel free to use it. If not you can create one now or follow along
	- create `clients/slack_client.py` and edit
	- go to https://api.slack.com/apps to create a new app
	- add 3 permissions `channels:history`, `chat:write:bot`, and `groups:history`
	- Install the app and copy the Oauth token. Create a new enviroment variable in heroku called `SLACK_API_TOKEN` and paste
	- Open your slack instance in a browser and go to the channel you want. The slack channel ID will be the last hash in the url. Create a new enviroment variable in heroku called `SLACK_CHANNEL_ID` and paste
	- add slack logic to our `post_to_slack()` method in `tasks.py`
