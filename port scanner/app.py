from flask import Flask, render_template, request
import socket
from datetime import datetime

app = Flask(__name__)

# List of top 20 common ports
TOP_20_PORTS = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389, 8080, 8443, 3306, 1723, 5900, 111, 515, 993]

# Mapping ports to their services and descriptions
PORT_DETAILS = {
    21: ("FTP", "File Transfer Protocol"),
    22: ("SSH", "Secure Shell"),
    23: ("Telnet", "Telnet Protocol"),
    25: ("SMTP", "Simple Mail Transfer Protocol"),
    53: ("DNS", "Domain Name System"),
    80: ("HTTP", "HyperText Transfer Protocol"),
    110: ("POP3", "Post Office Protocol 3"),
    139: ("NetBIOS", "NetBIOS Session Service"),
    143: ("IMAP", "Internet Message Access Protocol"),
    443: ("HTTPS", "HyperText Transfer Protocol Secure"),
    445: ("SMB", "Server Message Block"),
    3389: ("RDP", "Remote Desktop Protocol"),
    8080: ("HTTP-ALT", "Alternative HTTP Protocol"),
    8443: ("HTTPS-ALT", "Alternative HTTPS Protocol"),
    3306: ("MySQL", "MySQL Database Service"),
    1723: ("PPTP", "Point-to-Point Tunneling Protocol"),
    5900: ("VNC", "Virtual Network Computing"),
    111: ("rpcbind", "RPC Portmapper"),
    515: ("LPR", "Line Printer Daemon"),
    993: ("IMAPS", "IMAP Secure")
}

def port_scanner(target, ports):
    results = []
    target_ip = socket.gethostbyname(target)
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            status = 'Open'
        else:
            status = 'Closed'
        service, description = PORT_DETAILS.get(port, ("Unknown", "No description available"))
        results.append((port, status, service, description))
        sock.close()
    return results

@app.route('/')
def index():
    return render_template('index.html', ports=TOP_20_PORTS)

@app.route('/scan', methods=['POST'])
def scan():
    target_host = request.form['target']
    selected_ports = request.form.getlist('ports')
    selected_ports = [int(port) for port in selected_ports]

    start_time = datetime.now()
    scan_results = port_scanner(target_host, selected_ports)
    end_time = datetime.now()

    return render_template('results.html', target=target_host, results=scan_results, time_taken=end_time - start_time)

if __name__ == '__main__':
    app.run(debug=True)
