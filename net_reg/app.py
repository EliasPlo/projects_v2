import nmap
import socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import ssl
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Avoimien porttien skannaus nmap-kirjastolla
def scan_open_ports(target):
    open_ports = []
    for port in range(1, 65536):  # Skannaa portit 1-65535
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # Aseta aikaraja porttiskannaukselle
        result = s.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
        s.close()
    return open_ports

# Verkon yhteyksien tarkistus socket-kirjastolla
def check_port(target, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((target, port))
    if result == 0:
        return True
    else:
        return False

# SSL/TLS-sertifikaatin tarkistus cryptography-kirjastolla
def check_ssl_cert(domain):
    context = ssl.create_default_context()
    with socket.create_connection((domain, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            cert = ssock.getpeercert()
            cert_details = x509.load_pem_x509_certificate(cert['certificate'], default_backend())
            return cert_details

# Salausongelmien tarkistus salattujen tiedostojen osalta (esimerkki AES-salauksesta)
def decrypt_file(file_path, key, iv):
    with open(file_path, 'rb') as f:
        data = f.read()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(data) + decryptor.finalize()
    
    return decrypted_data

# Raportin luominen JSON-muodossa
def generate_report(open_ports, ssl_issues, encryption_issues):
    report = {
        "open_ports": open_ports,
        "ssl_issues": ssl_issues,
        "encryption_issues": encryption_issues
    }

    with open("vulnerability_report.json", "w") as f:
        json.dump(report, f, indent=4)

# Kokonaisvaltainen haavoittuvuustarkistus kohteelle
def vulnerability_scan(target):
    print(f"Scanning {target} for vulnerabilities...")

    # Skannaa avoimet portit
    open_ports = scan_open_ports(target)
    
    # Tarkista SSL/TLS-sertifikaatti
    ssl_issues = check_ssl_cert(target)
    
    # Tässä voi tarkistaa salausongelmia tiedostojen osalta
    encryption_issues = []  # Lisää tähän logiikkaa salausongelmista, kuten AES-avaimen heikkoudet

    # Generoi raportti
    generate_report(open_ports, ssl_issues, encryption_issues)

    print(f"Scan complete. Report generated as 'vulnerability_report.json'.")

# Testaa työkalua
if __name__ == "__main__":
    target = "elpw.com"  # Voit vaihtaa tämän kohteeksi, jonka haluat skannata
    vulnerability_scan(target)
