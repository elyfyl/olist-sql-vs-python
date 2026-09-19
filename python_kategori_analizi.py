import duckdb
import pandas as pd

# 1. Veritabanı Bağlantısı ve Veri Çekme
# 'olist.db' dosyasına bağlanıp analiz edeceğimiz tabloları Python'a alıyoruz.
conn = duckdb.connect("olist.db")

items_df = conn.sql("SELECT * FROM order_items").df()
products_df = conn.sql("SELECT * FROM products").df()

# Veriyi çektikten sonra bağlantıyı kapatmak kaynakları serbest bırakır.
conn.close()

# 2. Tabloları Birleştirme (Merge / Join İşlemi)
# Hangi ürünün hangi kategoriye ait olduğunu görmek için iki tabloyu birleştiriyoruz.
# 'on' parametresi: Hangi kolon üzerinden birleşeceklerini söyler.
# 'how=inner' parametresi: Sadece her iki tabloda da karşılığı olan ürünleri getirir.
merged_df = pd.merge(items_df, products_df, on='product_id', how='inner')

# 3. Gruplama ve Sayma (Group By & Count İşlemi)
# Kategorilere göre gruplayıp, o kategorinin kaç kez sipariş edildiğini sayıyoruz.
# .size() fonksiyonu, gruptaki satır sayısını (yani satılan ürün adedini) verir.
# reset_index(name='satis_adedi') ile bu sayım sonucuna yeni ve temiz bir kolon adı atıyoruz.
kategori_satis = merged_df.groupby('product_category_name').size().reset_index(name='satis_adedi')

# 4. Sıralama ve Filtreleme (Order By & Limit İşlemi)
# Satış adedine göre büyükten küçüğe sıralıyoruz (ascending=False büyükten küçüğe demektir).
en_cok_satanlar = kategori_satis.sort_values(by='satis_adedi', ascending=False)

# head(10) fonksiyonu ile listenin sadece en üstteki 10 satırını kesip alıyoruz.
ilk_10_kategori = en_cok_satanlar.head(10)

# 5. Sonuçları Gösterme
print("En Çok Satan 10 Ürün Kategorisi (Satış Adedine Göre - Python):")
print("-" * 65)
# index=False ile sol baştaki anlamsız sıra numaralarını (0, 1, 2...) gizliyoruz.
print(ilk_10_kategori.to_string(index=False))