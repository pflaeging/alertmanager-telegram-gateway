import telegram, json, logging, sys
from dateutil import parser
from flask import Flask
from flask import request
from flask_basicauth import BasicAuth


app = Flask(__name__)
app.secret_key = 'lAlAlA123'
basic_auth = BasicAuth(app)

# Yes need to have -, change it!
chatID = "-xchatIDx"

# Authentication conf, change it!
app.config['BASIC_AUTH_FORCE'] = True
app.config['BASIC_AUTH_USERNAME'] = 'XXXUSERNAME'
app.config['BASIC_AUTH_PASSWORD'] = 'XXXPASSWORD'

# Bot token, change it!
bot = telegram.Bot(token="botToken")

@app.route('/alert', methods = ['POST'])
def postAlertmanager():

    try:
        app.logger.setLevel(logging.DEBUG)
        content = json.loads(request.get_data())
        app.logger.debug(json.dumps(content, indent=2))
        for alert in content['alerts']:
            message = "Status: "+alert['status']+"\n"
            if 'resource' in alert['labels']:
                message += "Alert: "+alert['labels']['alertname']+"("+alert['labels']['resource']+")\n"
            else:
                message += "Alert: "+alert['labels']['alertname']+"\n"
            if 'message' in alert['annotations']:
                message += "Message: "+alert['annotations']['message']+"\n"
            if 'summary' in alert['annotations']:
                message += "Summary: "+alert['annotations']['summary']+"\n"                
            if 'description' in alert['annotations']:
                message += "Description: "+alert['annotations']['description']+"\n"
            if alert['status'] == "resolved":
                correctDate = parser.parse(alert['endsAt']).strftime('%Y-%m-%d %H:%M:%S')
                message += "Resolved: "+correctDate
            elif alert['status'] == "firing":
                correctDate = parser.parse(alert['startsAt']).strftime('%Y-%m-%d %H:%M:%S')
                message += "Started: "+correctDate
            bot.sendMessage(chat_id=chatID, text=message)
            return "Alert OK", 200
    except Exception as error:       
        bot.sendMessage(chat_id=chatID, text="Error to read json: "+str(error))
        app.logger.info("\t%s",error)
        return "Alert fail", 200
