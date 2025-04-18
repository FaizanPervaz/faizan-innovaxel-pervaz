from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import config
import string, random


app = Flask(__name__)

# MySQL Config
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')

    if not original_url:
        return jsonify({'error': 'URL is required'}), 400

    # Generate short code
    short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    # Save to DB
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO urls (original_url, short_code) VALUES (%s, %s)", (original_url, short_code))
    mysql.connection.commit()
    cur.close()

    return jsonify({
        'url': original_url,
        'shortCode': short_code
    }), 201

if __name__ == '__main__':
    app.run(debug=True)
