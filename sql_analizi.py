import duckdb

# 1. Veritabanına bağlanıyoruz
db_name = "olist.db"
conn = duckdb.connect(db_name)

# 2. SQL Sorgumuzu üç tırnak (multi-line string) arasına yazıyoruz.
# Böylece SQL kodumuzu alt alta, okunaklı bir şekilde yazabiliriz.
sql_query = """
    SELECT 
        -- Tarihi 'ay' seviyesine yuvarla (Örn: 2017-10-15 -> 2017-10-01 olur)
        -- STRFTIME fonksiyonu ile tarihi 'Yıl-Ay' (YYYY-MM) metnine çeviriyoruz ki daha şık görünsün.
        STRFTIME(DATE_TRUNC('month', o.order_purchase_timestamp), '%Y-%m') AS siparis_ayi,
        
        -- O aydaki tüm ürün fiyatlarını topla ve ondalık kısmı 2 haneye yuvarla (ROUND)
        ROUND(SUM(oi.price), 2) AS toplam_ciro
        
    FROM orders o  -- orders tablosuna 'o' kısaltmasını verdik
    
    -- orders (o) ile order_items (oi) tablolarını order_id üzerinden birleştir
    JOIN order_items oi ON o.order_id = oi.order_id
    
    -- Sadece teslim edilmiş (delivered) siparişleri hesaba kat
    WHERE o.order_status = 'delivered'
    
    -- Hesaplamayı 'siparis_ayi' kolonuna göre grupla
    GROUP BY siparis_ayi
    
    -- Sonuçları kronolojik olarak aya göre sırala
    ORDER BY siparis_ayi;
"""

# 3. Sorguyu veritabanında çalıştır ve sonucunu ekrana yazdır
print("Aylık Ciro Trendi (SQL Çözümü):")
print("-" * 40)

# duckdb.sql().show() komutu, sonucu terminalde güzel bir tablo formatında gösterir
conn.sql(sql_query).show()

# 4. İşlem bitince bağlantıyı kapatıyoruz
conn.close()