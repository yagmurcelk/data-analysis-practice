#############################################
# Kural Tabanlı Sınıflandırma ile Potansiyel Müşteri Getirisi Hesaplama
#############################################

#############################################
# İş Problemi
#############################################
# Gezinomi yaptığı satışların bazı özelliklerini kullanarak seviye tabanlı (level based) yeni satış tanımları
# oluşturmak ve bu yeni satış tanımlarına göre segmentler oluşturup bu segmentlere göre yeni gelebilecek müşterilerin şirkete
# ortalama ne kadar kazandırabileceğini tahmin etmek istemektedir.
# Örneğin: Antalya’dan Herşey Dahil bir otele yoğun bir dönemde gitmek isteyen bir müşterinin ortalama ne kadar kazandırabileceği belirlenmek isteniyor.
#############################################
# PROJE GÖREVLERİ
#############################################

#############################################
# GÖREV 1: Aşağıdaki soruları yanıtlayınız.
#############################################
#Soru 1: miuul_gezinomi.xlsx dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.

import pandas as pd
df = pd.read_excel('datasets/miuul_gezinomi.xlsx') #excel dosyasını okuma
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x:'%.2f' % x)
df.info()
df.shape

#Soru 2: Kaç unique şehir vardır? Frekansları nedir?

df["SaleCityName"].nunique() #6
df["SaleCityName"].value_counts()
#output:
#SaleCityName
#Antalya    31649
#Muğla      10662
#Aydın      10646
#Diğer       3245
#İzmir       2507
#Girne        455

#Soru 3: Kaç unique Concept vardır?

df["ConceptName"].nunique() #3

#Soru 4: Hangi Concept'dan kaçar tane satış gerçekleşmiş?

df["ConceptName"].value_counts()
#output:
#ConceptName
#Herşey Dahil      53186
#Yarım Pansiyon     3559
#Oda + Kahvaltı     2419

#Soru 5: Şehirlere göre satışlardan toplam ne kadar kazanılmış?

df.groupby("SaleCityName").agg({"Price": "sum"})
###Out[29]:
#                  Price
#SaleCityName
#Antalya      2041911.10
#Aydın         573296.01
#Diğer         154572.29
#Girne          27065.03
#Muğla         665842.21
#İzmir         165934.83

# Soru 6: Concept türlerine göre göre ne kadar kazanılmış?

df.groupby("ConceptName").agg({"Price": "sum"})
#Out[30]:
#                    Price
#ConceptName
#Herşey Dahil   3332910.77
#Oda + Kahvaltı  121308.35
#Yarım Pansiyon  174402.35

# Soru 7: Şehirlere göre PRICE ortalamaları nedir?
df.groupby("SaleCityName").agg({"Price": "mean"})
#Out[32]:
#              Price
#SaleCityName
#Antalya       64.52
#Aydın         53.86
#Diğer         47.71
#Girne         59.48
#Muğla         62.46
#İzmir         66.27

# Soru 8: Conceptlere  göre PRICE ortalamaları nedir?
df.groupby("ConceptName").agg({"Price": "mean"})
#Out[33]:
#                Price
#ConceptName
#Herşey Dahil    62.67
#Oda + Kahvaltı  50.25
#Yarım Pansiyon  49.03

# Soru 9: Şehir-Concept kırılımında PRICE ortalamaları nedir?

df.pivot_table("SaleCityName", "ConceptName").agg({"Price": "mean"})


#############################################
# GÖREV 2: satis_checkin_day_diff değişkenini EB_Score adında yeni bir kategorik değişkene çeviriniz.
#############################################

bins = [-1, 7, 30, 90, df["SaleCheckInDayDiff"].max()] 	#bins listesi, SaleCheckInDayDiff değişkeninin hangi aralıklarla kategorilere ayrılacağını belirler.
labels = ["Last Minuters", "Potential Planners", "Planners", "Early Bookers"]#	•	Bu liste, bins ile belirlenen aralıklar için kullanılacak kategori isimlerini içerir.

df["EB_Score"] = pd.cut(df["SaleCheckInDayDiff"], bins, labels=labels)
df.head(50).to_excel("eb_scorew.xlsx", index=False)

#############################################
# GÖREV 3: Şehir,Concept, [EB_Score,Sezon,CInday] kırılımında ücret ortalamalarına ve frekanslarına bakınız
#############################################

# Şehir-Concept-EB Score kırılımında ücret ortalamaları

df.groupby(by= ["SaleCityName", "ConceptName", "EB_Score"]).agg({"Price": "mean"})

# Şehir-Concept-Sezon kırılımında ücret ortalamaları

df.groupby(by=["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": "mean"})

# Şehir-Concept-CInday kırılımında ücret ortalamaları

df.groupby(by= ["SaleCityName", "ConceptName", "CInDay"]).agg({"Price": "mean"})

#############################################
# GÖREV 4: City-Concept-Season kırılımın çıktısını PRICE'a göre sıralayınız.
#############################################
# Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE'a uygulayınız.
# Çıktıyı agg_df olarak kaydediniz.

agg_df = df.groupby(by= ["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": "mean"}).sort_values("Price", ascending=False)

#############################################
# GÖREV 5: Indekste yer alan isimleri değişken ismine çeviriniz.
#############################################
# Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir.
# Bu isimleri değişken isimlerine çeviriniz.
# İpucu: reset_index()

agg_df.reset_index(inplace=True)

#############################################
# GÖREV 6: Yeni level based satışları tanımlayınız ve veri setine değişken olarak ekleyiniz.
#############################################
# sales_level_based adında bir değişken tanımlayınız ve veri setine bu değişkeni ekleyiniz.

agg_df['sales_level_based'] = agg_df[["SaleCityName", "ConceptName", "Seasons"]].agg(lambda x: '_'.join(x).upper(), axis=1)


#############################################
# GÖREV 7: Personaları segmentlere ayırınız.
#############################################
# PRICE'a göre segmentlere ayırınız,
# segmentleri "SEGMENT" isimlendirmesi ile agg_df'e ekleyiniz
# segmentleri betimleyiniz

agg_df["SEGMENT"] = pd.qcut(agg_df["Price"], 4, labels=["D", "C", "B", "A"])
#qcut, pandas kütüphanesinde kullanılan bir fonksiyondur ve veriyi belirli sayıda eşit büyüklükteki gruba bölmek için kullanılır.

agg_df.groupby("SEGMENT").agg({"Price": ["max", "min", "mean"]})

#############################################
# GÖREV 8: Oluşan son df'i price değişkenine göre sıralayınız.
# "ANTALYA_HERŞEY DAHIL_HIGH" hangi segmenttedir ve ne kadar ücret beklenmektedir?
#############################################

agg_df.sort_values(by="Price")

new = "ANTALYA_HERŞEY DAHIL_HIGH"
agg_df[agg_df["sales_level_based"] == new]
#Out[28]:
#  SaleCityName   ConceptName Seasons  Price          sales_level_based SEGMENT
#9      Antalya  Herşey Dahil    High  64.92  ANTALYA_HERŞEY DAHIL_HIGH       B