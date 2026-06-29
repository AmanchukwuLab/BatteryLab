# Using the Terminal
Computers run either Windows, MacOS (Apple), or some distribution of Linux. BatteryLab's RaspberryPi (RPi) computers run Ubuntu, the most widely used Linux distribution. Historically, Linux systems were run entirely through the command line; this is still the case today in certain applications.

Ubuntu does have a Windows-like desktop you can use, so day-to-day use shouldn't feel that foreign. BatteryLab and GitHub are managed through the terminal, however, so you should at least know basic navigation and commands. The best way to get acquainted is to follow along with a tutorial; [this tutorial from Ubuntu](https://ubuntu.com/desktop/docs/en/latest/tutorial/the-linux-command-line-for-beginners/) is a very thorough introduction that contains everything you should need to be comfortable navigating. The *very* short list of essentials (exempting git commands, discussed further below) would be:

```bash
pwd            # "print working directory", shows the absolute path 
    # to your current location     
ls             # "list", shows the contents of your current directory
mkdir folder   # "make directory", creates a folder with the name you provide
cd folder      # "change directory", or move into the folder you specified
cd ..          # ".." is the relative path for the parent folder. For 
    # example, if you're currently in /home/user/docs/tutorials, 
    # "cd .." will land you in /home/user/docs
rmdir folder   # "remove directory", deletes the folder you specified
cd ~           # "~" is the home directory for your user.
touch filename # creates an empty file "filename"
    # There are several programs for editing files in the command line. 
    # One of the more historically popular ones is called 'vim', but 
    # it has a remarkably steep learning curve. It's a powerful tool and 
    # worth checking out if you anticipate using Linux often, but 
    # otherwise just know that those tools exist.
rm filename    # "remove", deletes the file "filename". Be careful: it is 
    # essentially impossible to undo this command.
python         # opens an interactive python session
python demo.py # runs the python script "demo.py"
```

# Setting up GitHub
If you aren't familiar with git or GitHub, the "[Start your journey](https://docs.github.com/en/get-started/start-your-journey)" tutorial from GitHub's documentation includes an overview of both softwares, how to create an account, a demonstration project, and some other useful info. For BatteryLab, you'll really only need the information in items 1-3 ("About GitHub", "Creating an account" and "Hello world"). GitHub is generally the default versioning/archival software for coding projects, so there are plenty of other tutorials and resources online if you're curious to learn more. 

Once you have an account, you'll need to get access to the AmanchukwuLab account and your information configured on BatteryLab's computer. Someone who is an AmanchukwuLab admin can give you editing rights to the remote [BatteryLab repository](https://github.com/AmanchukwuLab/BatteryLab/tree/main). This will allow you to edit files directly in GitHub and, more importantly, push changes you decide make to your local version of the files to the remote "master copy". 

Once you've been granted editing rights, you'll need to create a [Fine-grained personal access token (PAT)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token). A PAT is essentially a password that is unique to a specific set of functions/abilities. This is a clever security measure: not only can individual PATs be deactivated at any time, but someone getting access to one of your PATs means they only have access to whatever rights that PAT was configured for (editing BatteryLab, in this case). Your new PAT for BatteryLab should have (at least) read access to metadata, as well as read/write access to code.

Once your token is provided, you'll want to copy it to the machines on which you plan to edit BatteryLab's files. When you push your local changes to the remote repository (```git add .```, ```git commit -m "YOUR MESSAGE HERE"```, then ```git push```), you'll be prompted to provide your username, then a password. This is should NOT be your GitHub password: use your PAT. There are various ways of storing your PAT on your local machine. Find one that works for you, and be careful to never post your PAT online (e.g., accidentally include it in BatteryLab's files when pushing changes).

<!--
Written by Jared Porter (June 2026)
-->