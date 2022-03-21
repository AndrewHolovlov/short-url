## General info
RESTful API made with Flask

**API Docs:** https://short-url-task.herokuapp.com/doc/


### Local Setup
Configure your environment.
Activate virtualenv: (venv - your virtual environment name).
```shell
source venv/bin/activate
```
Then copy env.example to .env file and set up environment variables.
To start server go to the project root and run:
```shell
python3 run.py
```


# Deployment
Production: https://short-url-task.herokuapp.com/

If you are sure that your changes won't break anything on the server: 
1. Push your changes to the **develop** branch
2. Checkout **master** branch
3. Merge **develop** branch and push to **master**

If not, please, follow the instructions below

**Deploy To Production Instructions**
1. Commit and push changes to your working branch
2. Create a Pull Request (PR) from your working branch to master
3. If there are any errors and PR can't be merged, resolve the issues locally and then push again to your branch
4. Merge PR