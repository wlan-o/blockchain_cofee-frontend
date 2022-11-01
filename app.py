# -*- coding: utf-8 -*-
# coding: utf8

from flask import Flask, render_template, request
import requests
import random
import json

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def home():
    size_type = request.form.get('radioo')
    size = request.form.get('amount')
    send_date = request.form.get('send')
    delivery_date = request.form.get('delivery')

    error = False
    responce = "Заполните все поля"

    if size_type and send_date and delivery_date and size:
        responce = "Заказ принят"
        send_date = send_date.split('.')
        delivery_date = delivery_date.split('.')
        # date comparison
        for i in range(3):

            if delivery_date[2-i] >= send_date[2-i]:
                break
            else:
                responce = "Проверьте введенную информацию"
        if not size.isdigit():
            responce = "Проверьте введенную информацию"
    else:
        error = True

    status_button = request.form.get("status_button")
    status = ''
    if status_button == "Статус":
        status = requests.get("https://my-json-server.typicode.com/wlan-o/server-engineering/statuses")
        status = json.loads(status.text)
        # status = json.dumps(status, ensure_ascii=False)
        status = random.choice(status)['description']

    # print(status_button)

    return render_template("index.html", error=error, responce=responce, status=status, size=size_type)


# @app.route('/json')
# def json_check():
#     response = requests.get("https://my-json-server.typicode.com/wlan-o/server-engineering/statuses")
#     statuses = json.loads(response.text)
#     statuses = json.dumps(statuses, ensure_ascii=False)
#     # return [num for num.loads() in statuses]
#     # return render_template("index.html")
#     return statuses


if __name__ == "__main__":
    app.run(debug=True)
