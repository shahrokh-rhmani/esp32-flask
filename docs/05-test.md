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

<p dir="rtl" align="justify">1. بدون ESP32 (تست با curl):</p>

<p dir="rtl" align="justify">
  <ul dir="rtl">
    <li>می‌توانید یک درخواست POST به آدرس http://localhost/api/location با این محتوا ارسال کنید:</li>
  </ul>
</p>

```json
{
    "latitude": 35.7749,
    "longitude": 51.4194,
    "timestamp": "2023-05-20 14:30:00"
}
```

<p dir="rtl" align="justify">
  <ul dir="rtl">
    <li>سپس با یک درخواست GET می‌توانید بررسی کنید که داده ذخیره شده است.</li>
  </ul>
</p>

<p dir="rtl" align="justify">برای تست کردن سرور Flask با curl، می‌توانید از دستورات زیر استفاده کنید. این دستورات یک درخواست POST با داده‌های JSON به سرور ارسال می‌کنند و سپس با یک درخواست GET نتیجه را بررسی می‌کنند.</p>

<p dir="rtl" align="justify">1. ارسال داده با curl (POST):</p>

```sh
curl -X POST \
  http://localhost/api/location \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 35.7749,
    "longitude": 51.4194,
    "timestamp": "2023-05-20 14:30:00"
  }'
```

<p dir="rtl" align="justify">خروجی مورد انتظار (اگر موفق باشد):</p>

```json
{"message":"Location updated","status":"success"}
```

<p dir="rtl" align="justify">2. دریافت داده ذخیره شده (GET):</p>

```sh
curl -X GET http://localhost/api/location
```

<p dir="rtl" align="justify">خروجی مورد انتظار (پس از ارسال POST):</p>

```json
{
  "city": "Tehran",
  "latitude": 35.7749,
  "longitude": 51.4194,
  "message": "موقعیت به روز شده از دستگاه GPS",
  "timestamp": "2023-05-20 14:30:00"
}
```

<p dir="rtl" align="justify">2. با ESP32:</p>

<p dir="rtl" align="justify">
  <ul dir="rtl">
    <li>مطمئن شوید ESP32 به شبکه متصل است و آدرس سرور Flask را به درستی تنظیم کرده‌اید.</li>
	<li>کد ESP32 باید داده‌های GPS را به صورت POST به همان آدرس ارسال کند.</li>
  </ul>
</p>

# <p dir="rtl" align="justify">اگر داده از ESP32 دریافت نشود:</p>

<p dir="rtl" align="justify">
  <ul dir="rtl">
    <li>اگر ESP32 داده ارسال نکند یا ارتباط برقرار نشود، سرور همچنان دسته تستی تهران را نمایش می‌دهد.</li>
	<li>برای اطمینان از دریافت داده از ESP32، می‌توانید در تابع handle_location یک print(data) اضافه کنید تا ببینید داده دریافت می‌شود یا خیر.</li>
  </ul>
</p>
