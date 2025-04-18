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

@app.route('/shorten/<short_code>', methods=['GET'])
def get_original_url(short_code):
    cur = mysql.connection.cursor()
    cur.execute("SELECT original_url, access_count FROM urls WHERE short_code = %s", (short_code,))
    result = cur.fetchone()
    
    if not result:
        return jsonify({'error': 'Short URL not found'}), 404

    original_url, access_count = result

    # Increment access count
    cur.execute("UPDATE urls SET access_count = access_count + 1 WHERE short_code = %s", (short_code,))
    mysql.connection.commit()
    cur.close()

    return jsonify({
        'shortCode': short_code,
        'original_url': original_url,
        'accessCount': access_count + 1
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
