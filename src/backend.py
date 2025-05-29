from flask import Flask, request, jsonify
import error_codes as ErrCodes
import Control
import DriverGet
import DriverSetting
import Rota
import TelegramMsg

app = Flask(__name__)

@app.route('/api/search', methods=['POST'])
def search_ticket():
    data = request.json
    nereden = data.get('nereden')
    nereye = data.get('nereye')
    tarih = data.get('tarih')
    saat = data.get('saat')
    telegram_msg = data.get('telegram_msg', False)
    bot_token = data.get('bot_token', '')
    chat_id = data.get('chat_id', '')
    ses = data.get('ses', False)

    try:
        driver = DriverSetting.DriverSetting().driver_init()
        DriverGet.DriverGet(driver).driver_get()
        Rota.Rota(driver, nereden, nereye, tarih).dataInput()
        response = Control.Control(driver, saat).sayfa_kontrol()

        if response == ErrCodes.BASARILI:
            if telegram_msg:
                TelegramMsg.TelegramMsg().send_telegram_message(bot_token, chat_id)
            return jsonify({"status": "success", "message": "Bilet bulundu!"})
        elif response == ErrCodes.TEKRAR_DENE:
            return jsonify({"status": "retry", "message": "Tekrar deneyin."})
        elif response == ErrCodes.TIMEOUT_HATASI:
            return jsonify({"status": "timeout", "message": "Zaman aşımı hatası."})
        else:
            return jsonify({"status": "error", "message": "Bilinmeyen bir hata oluştu."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
