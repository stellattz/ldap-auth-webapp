from flask import Flask, render_template, request
from ldap3 import Server, Connection, ALL, SIMPLE, Server, Tls
import ssl

app = Flask(__name__)

LDAP_SERVER = '192.168.17.144'
LDAP_PORT = 636  # LDAPS typically uses port 636
LDAP_CERT = '../../Downloads/cert.pem'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    dn = request.form['dn']
    password = request.form['password']

    if validate_credentials(dn, password):
        return f'Welcome, {dn}!'
    else:
        return f'Invalid credentials DN = \"{dn}\". Please try again.'

def validate_credentials(dn, password):
    tls_configuration = Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLS)

    server = Server(LDAP_SERVER, port=LDAP_PORT, use_ssl=True, tls=tls_configuration)
    user_dn = dn

    try:
        conn = Connection(server, user=user_dn, password=password, authentication=SIMPLE)
        print("conn")
        print(conn)
        return conn.bind()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == '__main__':
    app.run(debug=True)
