# AlertManager WebHook for Telegram notifications

This is a small gateway between OKD / OpenShift AlertManager (prometheus) and telegram written in python (flask).

It should be run in a separate namespace and uses only two secrets for configuration.

## First: create a telegram bot

- Login to telegram (web or app)
- search @BotFather
- `/newbot`
- give it a name aka `myfamoustest`
- give it a username aka `MyFamousTestBot` (must end with bot or Bot)
- now you get an API token like this one back: `1334834688:AAH8qx8nu-GR9thPnxxXXt7h1iPLTJJh6jYs` <- remember this!
- go to 'tg://resolve?domain=MyFamousTestBot' and start your bot

Great you now have a bot. A bot is like a normal telegram user for automation (with some restrictions).

## Second: create a private channel for your alerts

- create a new group in telegram with you and your bot
- look at the URL if you are in the group while in telegram web. The number at the end (something like `/im?p=g12345678` => 12345678) is your chat_id!
- now you have:
  - your API token: `1334834688:AAH8qx8nu-GR9thPnxxXXt7h1iPLTJJh6jYs`
  - your chat_id: `12345678`

Send a test message to your alert channel:

`curl -vv "https://api.telegram.org/bot[Your API token]/sendMessage?chat_id=-[your chat_id]&text=Hoooray, it is working"`

## Third: establish your gateway

The webhook-telegram-python gateway makes the translation between the JSON alertmanager output (example in ./default.json) and the telegram bot.

- Deploy the pod (examples are in the directory ./openshift)
- put your bot-config from above in the secret ./openshift/Secret_bot-config.yaml (base64 encoded: `echo 12345678 | base64`for ex.)
- establish a username / password combo for your gateway and put it in ./openshift/Secret_alertmanager-login.yaml
- create a route like in ./openshift/Route_alertmanager-telegram.yaml

Test your work with

```shell
curl -vv -k -XPOST --data @example.json https://myusernameforgateway:mypasswordforgateway@webhook-telegram-alertmanager-telegram.apps.myfamous-cluster.net/alert
```

You should get a well formated warnning now!

## Fourth: use this as alert receiver in OKD / OpenShift (4)

-  log in the web console of OKD / OpenShift as admin user
- Administration -> Cluster Settings -> Global Configuration -> Alertmanager
- for example edit the "Default" receiver:
  - Receiver Type: "Webhook"
	- URL: "https://myusernameforgateway:mypasswordforgateway@webhook-telegram-alertmanager-telegram.apps.myfamous-cluster.net/alert"
	- Save

Your set!

# Cudos

This work is derived from: https://github.com/qq516249940/alertmanager-webhook-telegram-python



---
Peter Pflaeging <peter@pflaeging.net>