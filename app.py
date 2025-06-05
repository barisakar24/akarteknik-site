from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# 🔐 OpenAI API Anahtarınızı buraya yapıştırın:

# 🔹 Ana Sayfa
@app.route("/")
def home():
    return render_template("index.html")

# 🔹 ChatGPT API'ye POST isteği (Chatbot)
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    if user_input == "":
        return jsonify({"reply": "Sorunuzu girin lütfen."})

    try:
        # 📌 Arıza kodları kontrol etmek isterseniz burada sabit bir sözlük ekleyebilirsiniz.
        # Örneğin:
        # ariza_kodlari = { "E1": "Hatalı faz sırası", "E2": "İç ünite ve Master ünite arasında iletişim hatası", ... }
        # for kod, aciklama in ariza_kodlari.items():
        #     if kod in user_input.upper():
        #         return jsonify({"reply": f"{kod} arıza kodu: {aciklama}"})

        response = openai.ChatCompletion.create(
            model="gpt-4",  # GPT-4 kullanmak için API key’inizin erişimi olması gerekir
            messages=[
                {
                    "role": "system",
                    "content": "Sen bir Erzincan teknik servis destek uzmanısın. Bosch/Buderus kombi, Tefal ütü ve kettle arızalarına yönelik doğru ve kısa çözümler sun. " 
                               "Eğer kullanıcının mesajında 'E1', 'E2', 'E4' gibi bir Bosch arıza kodu varsa, sabit verilmiş bir arıza kodu sözlüğünden doğrudan çıkarım yap ve sadece kodun açıklamasını ver."
                },
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Sunucu hatası: {str(e)}"})

if __name__ == "__main__":
    # debug=True yerel geliştirme içindir. Production ortamında False yapın.
    app.run(debug=True)
