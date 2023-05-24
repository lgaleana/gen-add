# Ads generation tool
Give an URL, generate headlines and images for ads.

# Installation
1. Install python (make sure to add the environment variables and install pip).
  - Windows: https://www.digitalocean.com/community/tutorials/install-python-windows-10#step-1-downloading-the-python-installer.
2. Test python with `python -v`.
3. Download: https://github.com/lgaleana/gen-ads/zipball/master.
4. Get an OpenAI key.
5. Set up a project for Google Vision and download the service key https://cloud.google.com/vision/docs/setup.
6. Rename the file .env.example to .env and add your OpenAI key and the path to your Google Vision service key.

# Execution
1. Open the command line and navigate to the `gen-ads` folder.
2. Run `python main.py`.
3. Enter an URL and hit enter.
4. Get ad headlines and images for the URL.

# How it works
The program executes the AI and code tasks in: https://github.com/lgaleana/gen-ads/blob/main/control_flow/main.py

# How to tune
Update the prompts of the [AI tasks](https://github.com/lgaleana/gen-ads/tree/main/ai_tasks).