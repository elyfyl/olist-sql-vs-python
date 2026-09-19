import duckdb

# 1. Veritabanına bağlantı kuruyoruz
# Daha önce oluşturduğumuz olist.db dosyamıza bağlanıyoruz.
conn = duckdb.connect("olist.db")

# 2. SQL Sorgumuzu hazırlıyoruz
# Üç tırnak arasına SQL komutlarımızı yazıyoruz.
sql_query = """
    SELECT 
        p.product_category_name AS kategori_adi,
        COUNT(oi.product_id) AS satis_adedi
        
    FROM order_items oi -- order_items tablosuna 'oi' kısaltmasını verdik
    
    -- Hangi ürünün hangi kategoriye ait olduğunu bulmak için INNER JOIN yapıyoruz
    -- Ortak kolonumuz: product_id
    JOIN products p ON oi.product_id = p.product_id
    
    -- Kategori adına göre verileri grupluyoruz
    GROUP BY p.product_category_name
    
    -- Satış adedine göre büyükten küçüğe (DESC - Descending) sıralıyoruz
    ORDER BY satis_adedi DESC
    
    -- Listenin sadece ilk 10 satırını getiriyoruz
    LIMIT 10;
"""

# 3. Sorguyu çalıştırıp sonucu terminale yazdırıyoruz
print("En Çok Satan 10 Ürün Kategorisi (SQL Çözümü):")
print("-" * 55)

# conn.sql().show() fonksiyonu DuckDB'nin veriyi düzenli bir tablo olarak basmasını sağlar.
conn.sql(sql_query).show()

# 4. Bağlantıyı kapatıyoruz (Kaynakları serbest bırakmak iyi bir alışkanlıktır)
conn.close()