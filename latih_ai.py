from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# 1. Menyiapkan Data Latihan (Contoh kasus)
pesan_latihan = [
    "Saya HRD perusahaan, ingin menawarkan proyek IT",
    "Tolong buatkan website dan perbaiki jaringan kami",
    "Menang undian hadiah 100 juta klik link ini segera",
    "Situs judi online slot gacor deposit pulsa terpercaya",
    "Halo, salam kenal. Portofolionya bagus.",
    "Bagaimana cara belajar pemrograman dasar?"
]
# Kunci Jawabannya:
label_latihan = ["Penting", "Penting", "Spam", "Spam", "Biasa", "Biasa"]

# 2. Mengubah teks menjadi angka (karena komputer tidak paham huruf)
vectorizer = CountVectorizer()
pesan_angka = vectorizer.fit_transform(pesan_latihan)

# 3. Melatih Algoritma AI (Naive Bayes)
ai_model = MultinomialNB()
ai_model.fit(pesan_angka, label_latihan)

# 4. Menyimpan "Otak" AI yang sudah pintar ke dalam file permanen
with open('vektor_kata.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
with open('model_ai.pkl', 'wb') as f:
    pickle.dump(ai_model, f)

print("Sukses! Otak AI telah dilatih dan disimpan.")
