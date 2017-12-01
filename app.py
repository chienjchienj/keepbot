import urllib
import os
from fbmq import Page,Attachment
from flask import Flask, request

app = Flask(__name__)
page = Page(os.getenv('PAGE_TOKEN',''))



@app.route("/")
def hello():
    return "Hello World!"


@app.route('/webhook', methods=['GET'])
def webhook_get():
    print(request.get_data(as_text=True))
    mode=request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode=='subscribe' and token==os.getenv('SECRET',''):
        return challenge
    else:
        return "wrong token"



@app.route('/webhook', methods=['POST'])
def webhook():

    page.handle_webhook(request.get_data(as_text=True))
    return "ok"


@page.handle_message
def message_handler(event):
    """:type event: fbmq.Event"""
    sender_id = event.sender_id
    message = event.message_text
    attachments = event.message_attachments;
    print(attachments)
    if attachments:
        for attachment_item in attachments:
            print(attachment_item)
            print(type(attachment_item))
            if  attachment_item.get('type',None)=='image':
                file_url=attachment_item.get('payload').get('url');
                testfile = urllib.URLopener()
                testfile.retrieve(file_url, "image.jpg")
                page.send(sender_id, Attachment.Image(file_url))
                print("saved==>"+file_url)

    else:
        page.send(sender_id, "thank you! your message is '%s'" % message)


@page.after_send
def after_send(payload, response):
    """:type payload: fbmq.Payload"""
    print("complete")

if __name__ == '__main__':
    app.run(debug=True,port=80,host="0.0.0.0")