import duckdb
import os

# 1. Veritabanı bağlantısını oluşturma
# olist.db dosyası bu kodla aynı klasörde yaratılacak.
db_name = "olist.db"
conn = duckdb.connect(db_name)

print("Veritabanı bağlantısı başarılı. İçeri aktarma (ingestion) başlıyor...")

# 2. Hangi CSV dosyalarını, hangi isimle tabloya çevireceğimizi belirtiyoruz.
tables = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "products": "olist_products_dataset.csv"  # YENİ EKLENEN SATIR
}

# 3. Her bir tablo için döngü
for table_name, file_name in tables.items():
    # Dosyalar ingest.py ile aynı klasörde olduğu için yol belirtmemize gerek yok, 
    # direkt dosya adını (file_name) kullanıyoruz.
    file_path = file_name 
    
    if os.path.exists(file_path):
        print(f"[{table_name}] tablosu oluşturuluyor...")
        
        sql_query = f"""
            CREATE OR REPLACE TABLE {table_name} AS 
            SELECT * FROM read_csv_auto('{file_path}');
        """
        
        conn.execute(sql_query)
        print(f"✓ [{table_name}] başarıyla aktarıldı.")
    else:
        print(f"HATA: '{file_path}' bulunamadı. Lütfen dosyanın kod ile aynı klasörde olduğundan emin ol.")

# 4. Bağlantıyı kapatıyoruz.
conn.close()
print("Tüm işlemler tamamlandı! Artık SQL sorguları yazmaya hazırız.")