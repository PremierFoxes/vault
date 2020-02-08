# `Vault x IC Hack 2020`

### What is Vault?
Vault is a Core Banking Engine. Vault is at the centre of a bank's tech stack: it maintains the state of customers' accounts and moves funds between them. Vault is designed around "Smart Contracts": Python programs that model the behaviour of a banking product.

Contracts can model any product such as a credit card, mortgage, or current account. They define the logic for accepting or rejecting payments, charging fees, paying interest, and so on.

Vault can run and simulate any product, in any currency. What will you build with it?


### Getting Started
Our team will issue you with some credentials to access IC Hack 20's dedicated instance.
Follow their instructions to set the credentials up.

This repository includes a CLI tool, `vault-stonks`, to perform some common operations on Vault.
You must have a `python3` binary in your `$PATH` which points to python3.6 or later to use this.
Let us know if you need a hand with installing Python.
To install the Python dependencies:
```
pip3 install --user --requirement requirements.txt
```

Ensure `~/.local/bin` is in your $PATH:
```
export PATH=$PATH:~/.local/bin
```

To connect to Vault, open a new terminal tab or window and enter:
```
vault-stonks --connect /path/to/ssh-key
```
This sets up a proxy to the network Vault is located in. This must be running in the background to be able to interact with Vault.


### Interacting with Vault
You can interact with Vault through its synchronous HTTP REST APIs. You can find the documentation for these here
```
https://documentation.ichack.tmachine.io
```

You can also use our Streaming API (Kafka message queues) to react to Vault events in your application:
```
apt install kafkacat  # https://github.com/edenhill/kafkacat

kafkacat -b kafka.ichack.tmachine.io -t vault.xpl_api.v1.transactions.transaction.events -C
```
You can write your own Smart Contracts. We suggest you start with one of the basic contracts provided and build on top of it.
You can find the Contracts documentation here:
```
https://documentation.ichack.tmachine.io/reference/contracts/
```
Add the `vault-config.json` file that our team provided you to the `data/` folder, as this is used by the `vault-stonks` tool.

After you've cloned the repo you can use the `vault-stonks` tool to:
- Generate test customers and accounts
    ```
    vault-stonks --create-customer --product_id product_id --num_customer 50
    ```
    This will generate a `customers.json` in the `data/` directory.

- Generate random payments on the accounts you created
    ```
    vault-stonks --payment-bot --customers_file_path /path/to/customers.json
    ```
    This will randomly generate payments between the specified accounts in `customers.json` until it is manually killed with Ctrl+C.

You can view customers, accounts, products and payments in the `Ops-Dash` dashboard:

```
https://ops.ichack.tmachine.io
```

When presented with a pop-up Sign In box, please enter your `basic_auth` credentials. Afterwards when presented with the dashboard login page, click the `Log in with SSO` option and enter:
```
superuser@bytegun.com
1234
```


### Ideas for Vault projects

##### Round Up For Good
An app that rounds up every transaction for charitable donation.
Possible extensions: daily cap, saving + charity split, etc.

##### Vault Swear Jar
Want to hack with some hardware? Create a swear jar that moves money between accounts in Vaults whenever a button is pressed, and displays the balance on screen.
Feeling ambitious? Do away with the button and connect a microphone for speech-triggered payments.

##### Just Keep Running Bank
An app that uploads your step count to Vault - and a Smart Contract that rewards you handsomely for staying active!
Want to push further? Challenge your friends, whoever's step count is highest at the end of the day wins everyone else's bets!

### Bug Bounty Program
We are running a bug bounty program throughout with prizes for critical security bugs found within Vault. Think you found something? Reach out to us on Slack in [#sp-thought-machine](https://ichack20.slack.com/messages/sp-thought-machine) and we'll evaluate your submission.

### Rules for Shared Access Vault instance
For the purposes of this hackathon, we provide you with an instance of Vault shared by all the participating teams.
In order to keep things running smoothly for you and other teams we ask that you:
- Only interact with Vault customers/accounts that you create.
- Do not delete or disable smart contracts created by other teams.
- Don't apply restrictions to other teams' customers/accounts/payment devices.
- Don't put unreasonable load onto Vault that would keep other teams from working smoothly (this includes load originated from Smart Contract schedule execution).
-  If you are unsure of the effects on Vault of anything you're thinking of doing, please ask a member of Thought Machine staff and they will be happy to advise.

Failure to observe these rules may lead to your keys being revoked, and your access to Vault may be withdrawn at any time.

### FAQ

##### What languages can I use?
We offer some Python libraries so that you can hit the ground running.
We recommend using the bundled libraries as we will be better placed to provide support to you during the hackathon.

However, both our HTTP REST API and Streaming API use the JSON message format, so you can interact with these with any language you prefer.

##### What projects can I work on?
Anything you can think of! Remember, our prize category is Money for Good - but even if your project doesn't fit in the brief we are more than happy to support you!

##### What if I find a bug?
You are using a pre-release Vault version so that you can use the latest and greatest features. It's pretty solid but should you find any bugs, please get in touch in the [#sp-thought-machine](https://ichack20.slack.com/messages/sp-thought-machine) Slack channel and let us know. In addition, any crticial security bugs will be eligible for our bug bounty program throughout IC Hack 20!

##### How can I win prizes?
At IC Hack 20 we are giving you 3 ways to win prizes:
- **Money for Good**: for the best hack that uses money to promote personal health, mental health, charitable causes, or societal improvement. Note that this is not restricted to Vault projects!
- **Swag Challenge**: got some of our swag, but don't know what to do with it? The best pictures at IC Hack 20 featuring you showing off our swag sent to [#sp-thought-machine](https://ichack20.slack.com/messages/sp-thought-machine) will be eligible to win **cat lamps**!
- **Bug Bounty Program**: as mentioned above, we have prizes for any critical security bugs found in Vault. Please note that our security team will review these after the event and prizes will be distributed shortly afterwards.

##### I like this and I want to do this... as a job...?
Awesome! Reach out to one of our team or email recruitment@thoughtmachine.net and please mention that you worked on a Vault project at IC Hack 20!
All Thought Machiners attending IC Hack 20 are engineers and can answer any questions about what the job is all about.

We offer summer internships, 6 month placements, and full time positions.


**Good Luck! - The TM team**
