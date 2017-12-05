from app import app

app.run(debug=True,host='0.0.0.0',port=8085,ssl_context=('./ssl.crt', './ssl.key'),threaded=True)