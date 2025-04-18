from flask import Flask, render_template
from flask_mysqldb import MySQL
import config

app = Flask(__name__)

# MySQL Config
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)

@app.route('/')
def home():
    return 'URL Shortener Home Page'

if __name__ == '__main__':
    app.run(debug=True)
