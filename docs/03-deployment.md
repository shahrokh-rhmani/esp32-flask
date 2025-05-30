# Deployment Guide

# 1. Server Connection & System Update

```
ssh root@your-server-ip
apt update && apt upgrade -y
```

# 2. Install Prerequisites

```
# Python and pip
apt install python3 python3-pip python3-venv -y

# Node.js 
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs 

# Nginx and tools
apt install nginx git build-essential -y
```

# 3. Clone Project

```
https://github.com/shahrokh-rhmani/esp32-flask.git
cd esp32-flask
```

# 4. Backend Setup (Flask)

```
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create systemd service file:

```
sudo nano /etc/systemd/system/flaskapp.service
```

Paste this configuration:

```
[Unit]
Description=Gunicorn Flask App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/root/esp32-flask/backend
Environment="PATH=/root/esp32-flask/backend/venv/bin"
ExecStart=/root/esp32-flask/backend/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:flaskapp.sock \
          --timeout 120 \
          app:app

[Install]
WantedBy=multi-user.target
```

Start and enable service:

```
sudo systemctl start flaskapp
sudo systemctl enable flaskapp
sudo systemctl status flaskapp
sudo systemctl restart flaskapp
```

# 5. Frontend Setup (React)

```
cd ../frontend
npm install
npm run build

sudo mkdir -p /var/www/esp32-flask
sudo cp -r build/* /var/www/esp32-flask/
```

# 6. Nginx Configuration

```
sudo nano /etc/nginx/sites-available/esp32-flask
```

Paste this configuration:

```
server {
    listen 80;
    server_name your-ip-or-domain;

    root /var/www/esp32-flask;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        include proxy_params;
        proxy_pass http://unix:/root/esp32-flask/backend/flaskapp.sock;
    }
}
```

Enable configuration:

```
sudo ln -s /etc/nginx/sites-available/esp32-flask /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

# 7. Permissions Setup

```
sudo chown -R www-data:www-data /root/esp32-flask/backend
sudo chmod 660 /root/esp32-flask/backend/flaskapp.sock
sudo chmod 755 /root /root/esp32-flask /root/esp32-flask/backend
```

# 8. Verification Steps

Check Gunicorn installation:

```
source /root/esp32-flask/backend/venv/bin/activate
pip list | grep gunicorn
```

Test Unix socket:

```
curl --unix-socket /root/esp32-flask/backend/flaskapp.sock http://localhost/api/location | jq
```

Expected output: 

```
{
  "city": "Tehran",
  "latitude": 35.6892,
  "longitude": 51.389,
  "message": "تهران - پایتخت ایران",
  "timestamp": "2025-05-30T06:41:40.575927"
}

```
















