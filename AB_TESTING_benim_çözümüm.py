#####################################################
# AB Testi ile BiddingYöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

#####################################################
# İş Problemi
#####################################################

# Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
# bu yeni özelliği test etmeye karar verdi veaveragebidding'in maximumbidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için bir A/B testi yapmak istiyor. A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchase metriğine odaklanılmalıdır.




#####################################################
# Veri Seti Hikayesi
#####################################################

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır. Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleri ab_testing.xlsx excel’inin ayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna AverageBidding uygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç

#####################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################

import numpy as np
import pandas as pd
import seaborn as sns

pd.set_option("display.max_columns", None)
#pd.set_option("display.max_rows", None)
pd.set_option('display.width', 200)

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

df = pd.read_excel(r"ab_testing.xlsx")
df.head()

#Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

control_df = pd.read_excel("ab_testing.xlsx", sheet_name="Control Group")
test_df = pd.read_excel("ab_testing.xlsx", sheet_name="Test Group")

print(control_df.head())
print(test_df.head())

# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.

control_df.describe().T
test_df.describe().T

# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

control_df["Group"] = "Control"
test_df["Group"] = "Test"

df = pd.concat([control_df, test_df], axis=0, ignore_index=True)
print(df.head())

print(df["Group"].value_counts())

#####################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################

# Adım 1: Hipotezi tanımlayınız.

H0: M1 = M2 (Maximum Bidding ve AverageBidding uygulamaları arasında ortalama kazanç açısından anlamlı bir fark yoktur.)
H1: M1 != M2 (Maximum Bidding ve AverageBidding uygulamaları arasında ortalama kazanç açısından anlamlı bir fark vardır.)

# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz

control_df["Purchase"].mean()
test_df["Purchase"].mean()

#####################################################
# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# ADIM 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.

## Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz

#   - 1. Normallik Varsayımı (shapiro)

from scipy.stats import shapiro

H0: Normal dağılım varsayımı sağlanmaktadır.
H1: Normal dağılım varsayımı sağlanmamaktadır.

test_stat, pvalue = shapiro(control_df["Purchase"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

##Test Stat = 0.9773, p-value = 0.5891
##p-value = 0.5891 > 0.05. H0 reddedilemez. Bu control grubunun normal dağıldığını gösterir.

test_stat, pvalue = shapiro(test_df["Purchase"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

##Test Stat = 0.9589, p-value = 0.1541
##p-value = 0.1541 > 0.05. H0 reddedilemez. Bu test grubunun normal dağıldığını gösterir.

##İki grup da normal dağılmıştır, birinci varsayım sağlanmıştır.


#   - 2. Varyans Homojenliği (levene)

from scipy.stats import levene

H0: Varyanslar homojendir
H1: Varyanslar homojen değildir

test_stat, pvalue = levene(control_df["Purchase"], test_df["Purchase"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

##Test Stat = 2.6393, p-value = 0.1083
##p-value = 0.1083 > 0.05. H0 reddedilemez. Bu control ve test grubunun varyanslarının homojen olduğunu gösterir.

# ADIM 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz

#   - 1. Varsayımlar sağlanıyor t testi (Parametrik test)

from scipy.stats import ttest_ind

test_stat, pvalue = ttest_ind(control_df["Purchase"], test_df["Purchase"], equal_var = True)
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi

##Varsayımlar sağlandı. Bu kullanılmaz!

##from scipy.stats import mannwhitneyu

##test_stat, pvalue = mannwhitneyu(control_df["Purchase"], test_df["Purchase"], equal_var = True)
##print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))


# ADIM 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

Test Stat = -0.9416, p-value = 0.3493
p-value = 0.3493 > 0.05. H0 reddedilemez.
Maximum Bidding ve AverageBidding uygulamaları arasında ortalama kazanç açısından anlamlı bir fark yoktur.

##############################################################
# GÖREV 4 : Sonuçların Analizi
##############################################################

# Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.

Parametrik T testini kullandım çünkü iki grup arasındaki ortalama kazanca bakıyorum. Bu iki grup normal dağılmış ve
varyansları eşit, yani varsayımları sağlıyor.

# Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.

Maximum Bidding ve Average Bidding uygulamaları arasında ortalama kazanç açısından anlamlı bir fark vardır. Maximum Bidding
grubunun kazanç ortalaması 550 iken Average Bidding uygulamalarının ortalama kazancı 582 çıkmıştır. Testler sonucunda
Average Bidding anlamlı bir şekilde daha çok kazandırıyor diyebiliriz.