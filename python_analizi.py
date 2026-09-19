import duckdb
import pandas as pd

# 1. Veri Çekme (Veritabanından Python'a)
# DuckDB veritabanımıza bağlanıp tabloları Pandas DataFrame formatında alıyoruz.
conn = duckdb.connect("olist.db")
orders_df = conn.sql("SELECT * FROM orders").df()
items_df = conn.sql("SELECT * FROM order_items").df()
conn.close()

# 2. Filtreleme ve Birleştirme (SQL'deki WHERE ve JOIN)
# Sadece 'delivered' (teslim edilmiş) olan siparişleri seçiyoruz
delivered_orders = orders_df[orders_df['order_status'] == 'delivered'].copy()

# 'order_id' ortak kolonu üzerinden iki tabloyu birleştiriyoruz (Inner Join)
merged_df = pd.merge(delivered_orders, items_df, on='order_id', how='inner')

# 3. Tarih İşlemleri (SQL'deki DATE_TRUNC)
# Sipariş tarihini metinden Python'ın anlayacağı 'datetime' formatına çeviriyoruz
merged_df['order_purchase_timestamp'] = pd.to_datetime(merged_df['order_purchase_timestamp'])

# Tarihi sadece 'Yıl-Ay' (YYYY-MM) formatında gruplanabilir bir metne dönüştürüyoruz
merged_df['siparis_ayi'] = merged_df['order_purchase_timestamp'].dt.to_period('M').astype(str)

# 4. Gruplama ve Toplama (SQL'deki GROUP BY ve SUM)
# Aya göre gruplayıp, fiyat (price) kolonunun toplamını alıyoruz
aylik_ciro = merged_df.groupby('siparis_ayi')['price'].sum().reset_index()

# Çıkan sonucu 2 ondalık haneye yuvarlayıp kolon adını SQL'deki gibi güncelliyoruz
aylik_ciro['price'] = aylik_ciro['price'].round(2)
aylik_ciro.rename(columns={'price': 'toplam_ciro'}, inplace=True)

# 5. Sıralama ve Gösterme (SQL'deki ORDER BY)
# Sonuçları kronolojik olarak sıralıyoruz
aylik_ciro = aylik_ciro.sort_values('siparis_ayi')

print("Aylık Ciro Trendi (Python Pandas Çözümü):")
print("-" * 40)
# index=False ile tablonun başındaki sıra numaralarını gizleyip daha temiz bir çıktı alıyoruz
print(aylik_ciro.to_string(index=False))