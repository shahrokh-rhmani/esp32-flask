# <p dir="rtl" align="justify">1. داده تستی پیش‌فرض:</p>


<p dir="rtl" align="justify">
  <ul dir="rtl">
    <li>در متغیر last_location یک موقعیت پیش‌فرض برای تهران قرار داده شده است:</li>
  </ul>
</p>

```python
last_location = {
    'latitude': 35.6892,
    'longitude': 51.3890,
    'timestamp': datetime.now().isoformat(),
    'city': 'Tehran',
    'message': 'تهران - پایتخت ایران'
}
```

<p dir="rtl" align="justify">این داده فقط برای آزمایش اولیه سرور است و وقتی سرور Flask را اجرا می‌کنید، بدون دریافت هیچ داده‌ای از ESP32، این مقدار را نمایش می‌دهد.</p>

# <p dir="rtl" align="justify">2. دریافت داده از ESP32:</p>

<p dir="rtl" align="justify">
  <ul dir="rtl">
    <li>وقتی ESP32 یک درخواست POST با داده‌های GPS به آدرس /api/location ارسال کند، سرور Flask آن را دریافت و ذخیره می‌کند:</li>
  </ul>
</p>

```python
if request.method == 'POST':
    data = request.get_json()  # Receiving data from ESP32
    
    last_location = {
        'latitude': data.get('latitude', 35.6892),  # اگر داده دریافت نشد، از مقدار پیش‌فرض استفاده کن
        'longitude': data.get('longitude', 51.3890),
        'timestamp': data.get('timestamp', datetime.now().isoformat()),
        'city': 'Tehran',
        'message': 'موقعیت به روز شده از دستگاه GPS'
    }
```

# <p dir="rtl" align="justify">نحوه تست کردن:</p>



<p dir="rtl" align="justify">برای تست کردن سرور Flask با curl، می‌توانید از دستورات زیر استفاده کنید. این دستورات یک درخواست POST با داده‌های JSON به سرور ارسال می‌کنند و سپس با یک درخواست GET نتیجه را بررسی می‌کنند.</p>

<p dir="rtl" align="justify"> ارسال داده با curl (POST):</p>

```sh
curl --unix-socket /root/esp32-flask/backend/flaskapp.sock -X POST \
  http://localhost/api/location \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 36.2605,
    "longitude": 59.6168,
    "timestamp": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'",
    "city": "Mashhad",
    "message": "موقعیت جدید در مشهد"
  }'
```

<p dir="rtl" align="justify">خروجی مورد انتظار (اگر موفق باشد):</p>

```json
{"message":"Location updated","status":"success"}
```



