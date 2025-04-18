from flask import Flask, render_template, request, jsonify, redirect
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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')

    if not original_url:
        return jsonify({'error': 'URL is required'}), 400

    # Generating short code
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
    
@app.route('/shorten/<short_code>', methods=['PUT'])
def update_url(short_code):
    data = request.get_json()
    new_url = data.get('url')

    if not new_url:
        return jsonify({'error': 'New URL is required'}), 400

    # Checking from DB if the short code exists
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM urls WHERE short_code = %s", (short_code,))
    if not cur.fetchone():
        return jsonify({'error': 'Short URL not found'}), 404

    # Updating the original URL
    cur.execute("UPDATE urls SET original_url = %s WHERE short_code = %s", (new_url, short_code))
    mysql.connection.commit()
    cur.close()

    return jsonify({
        'message': 'URL updated successfully',
        'shortCode': short_code,
        'new_url': new_url
    }), 200
    
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

@app.route('/<short_code>')
def redirect_to_original(short_code):
    cur = mysql.connection.cursor()
    cur.execute("SELECT original_url FROM urls WHERE short_code = %s", (short_code,))
    result = cur.fetchone()
    
    if not result:
        return jsonify({'error': 'Short URL not found'}), 404

    original_url = result[0]

    # Updating Access Count
    cur.execute("UPDATE urls SET access_count = access_count + 1 WHERE short_code = %s", (short_code,))
    mysql.connection.commit()
    cur.close()

    return redirect(original_url)

@app.route('/shorten/<short_code>', methods=['DELETE'])
def delete_url(short_code):
    # Check if the short code exists
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM urls WHERE short_code = %s", (short_code,))
    if not cur.fetchone():
        return jsonify({'error': 'Short URL not found'}), 404

    # Delete the short URL
    cur.execute("DELETE FROM urls WHERE short_code = %s", (short_code,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Short URL deleted successfully'}), 200

@app.route('/shorten/<short_code>/stats', methods=['GET'])
def url_stats(short_code):
    cur = mysql.connection.cursor()
    cur.execute("SELECT access_count FROM urls WHERE short_code = %s", (short_code,))
    result = cur.fetchone()

    if not result:
        return jsonify({'error': 'Short URL not found'}), 404

    access_count = result[0]
    return jsonify({'shortCode': short_code, 'accessCount': access_count}), 200

if __name__ == '__main__':
    app.run(debug=True)
