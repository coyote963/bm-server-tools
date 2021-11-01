# How to set up your own dedicated server on the cloud using Boring Man Server Tools

Setting up dedicated servers used to be only accessible to the computer literate. Users needed to know how to navigate the command line, understand networking, as well as manage configuration files. With the inclusion of bm-server-tools, this ability is given to everyone. The following is a guide on how to set up your own dedicated server. It is geared towards those that are trying to set up a free dedicated server, but this can easily be extended to paid VPS.

## Why use a dedicated server?

There's quite a few reasons:

 - It's completely free. With certain caveats, the server you host is free. You don't need to keep your computer on all the time and waste electricity, and you don't need to pay for internet to keep it connected. The cloud provider will handle all that for you. The caveats are that you abuse the generous free trials that companies such as Amazon provide you

 - It can be put in any location as long as it is offered by the cloud provider. This means that you can host a server for a friend who lives on the other side of the world, or provide a server that is at the midpoint of a group of players for the lowest collective latency. 

 - BM Server Tools provides a simple interface for managing Boring Man servers. As you will see, the installation and usage is foolproof.

 - It's pretty fun, and you get to learn a lot about the command line.

## What are the Caveats?

I am only speaking about Amazon Web Services (AWS), but from my quick perusal of the offerings of the other cloud providers (Google, Amazon and Micro$oft), AWS has the best free plan out of the three. For 12 months you can use their services as long as you stay below certain usage limits. After which you will be charged the normal rate (which is about 5$ a month). Therefore the rest of this guide is written with the assumption that you are using AWS. If you are not you can probably adapt the instructions for your choice of Operating System and Cloud Provider. 

Ever since Spasman added server sleeping, servers that are idle use around 4% CPU. Because of this, in MOST cases, the server will not exceed the allotted CPU time. But just in case you are afraid of getting charged money, you can set up alerts that tell you when you are nearing the limit, and you can just terminate the server. 

The other caveat is that you will need a Credit / Debit card. I am well aware that a lot of the community is underage and this will be a show stopper :)

## Installation

Without further ado, the first step is acquiring an AWS account. 

### Getting an AWS Account

 - First open up the [AWS Console](https://console.aws.amazon.com/)
 - Click "Create a new AWS account." 
 - Fill in your email, password and username.
 - Fill in personal details
 - Fill in payment information
 - Set up phone verification
 - Select Basic Plan (Free Tier)
 - Put whatever you want for "Personalize your Experience"

### Creating a server

Now you have an account, click on the big orange "Sign into Console" on the top right, and sign in with the account details you provided. Go to the [instances page](https://console.aws.amazon.com/ec2) and click the big orange "Launch Instances" button. 
 - Select the Amazon Linux 2 AMI. 
 - Select t2.micro (Should be preselected) 
 - Click Review and Launch
 - *VERY IMPORTANT!* There will be a popup that says "Select an existing key pair." Make sure you select "create a new keypair and give it the name bm and save bm.pem somewhere. This is very important file that you will need to sign into your server. After saving you are good to launch the instance

### Entering your server and installing docker

Open your terminal (CTRL+SHIFT+P) and issue the following command `ssh -i <path/to/your/bm.pem> ec2_user@<public_ipv4_dns>` and this will connect you to the server. If it asks something about keyprint, type `y`. 

Now that you are in, you need to install docker. There's pretty clear instructions on [their website](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html) but I'll repeat them:

`sudo yum update -y`

`sudo amazon-linux-extras install docker`

`sudo yum install docker`

`sudo service docker start`

`sudo usermod -a -G docker ec2-user`

`exit`

### Installing boring man tools

Log back into your server

`ssh -i <path/to/your/bm.pem> ec2_user@<public_ipv4_dns>`

`pip install bm-cli`

And that's it, you now have the boring man server tools, which are issued by typing bmcli followed by a command

To get started use 

`bmcli start`

This will hang for a while on the first run, but be patient. It takes about 30 seconds. What this does is initialize the tools and gets it ready to launch servers.

`bmcli status`

This will say there are no servers running. This is because `bmcli start` doesn't start any servers by itself, it starts the service that spawns servers, you will still need to start servers separately

`bmcli add tdm`

This will create a team deathmatch server

`bmcli status`

You should see now the TDM server with information about it's game_id and used ports. Try opening Boring Man, you should see a server called "Team Deathmatch." That is your server.

`bmcli add tdm`

Creates a second TDM server. It automatically updates the ports. By default the boring man tools can have 3 concurrent servers running. However this can easily be adjusted.

`bmcli add-custom /path/to/custom_settings.ini`

Creates a server with the settings from your custom_settings. Note: It will overwrite the port and rcon_port you give it.

`bmcli status`

Should show you the second server running. What if you want to stop a server? (For example to update its settings)

`bmcli remove 0`

This will stop the first server you created. What if you wanted to stop the entire boring man server tools and all the servers it is managing? Just issue:

`bmcli stop`

This will stop the tool and you will need to start it again to use it.