import json
import os

CONFIG_FILE = "config.json"

LANGUAGES = {
    "Español": "es",
    "English": "en",
    "Русский": "ru",
    "Français": "fr",
    "日本語": "ja",
    "中文": "zh"
}

TRANSLATIONS = {
    "es": {
        "title_main": "ChronoLock - Bóveda de Tiempo",
        "tab_new": "Nueva Bóveda",
        "tab_unlock": "Desbloquear",
        "title_new_vault": "Crear Nueva Contraseña Segura",
        "lbl_name": "Nombre (ej. App1):",
        "lbl_time": "Bloqueo (minutos):",
        "btn_generate": "Generar y Bloquear",
        "msg_gen_success": "¡Bóveda creada exitosamente! Cópiala ahora:",
        "btn_clear": "Limpiar Pantalla",
        "title_unlock": "Desbloquear Bóveda",
        "lbl_select_vault": "Selecciona una bóveda.",
        "btn_start_unlock": "Iniciar Desbloqueo",
        "msg_no_vaults": "No hay bóvedas",
        "msg_time_req": "Tiempo de espera requerido: {} minutos.",
        "msg_err_read_vault": "Error leyendo esta bóveda.",
        "title_unlocked": "¡Bóveda Abierta!",
        "btn_back": "Volver al Menú",
        "warn_title": "Advertencia",
        "err_title": "Error",
        "conf_title": "Confirmación",
        "notice_title": "Aviso",
        "err_empty_name": "El nombre no puede estar vacío.",
        "err_time_format": "El tiempo de bloqueo debe ser un número entero positivo (minutos).",
        "conf_start": "¿Estás seguro de iniciar la cuenta atrás de {} minutos?\n\nSi cierras la ventana el progreso se perderá.",
        "warn_close": "Hay una cuenta atrás en progreso. Si sales ahora, perderás el progreso y tendrás que esperar de nuevo. ¿Seguro que quieres salir?",
        "unlocking": "Desbloqueando '{}'"
    },
    "en": {
        "title_main": "ChronoLock - Time Vault",
        "tab_new": "New Vault",
        "tab_unlock": "Unlock",
        "title_new_vault": "Create New Secure Password",
        "lbl_name": "Name (e.g. App1):",
        "lbl_time": "Lock time (minutes):",
        "btn_generate": "Generate & Lock",
        "msg_gen_success": "Vault created successfully! Copy it now:",
        "btn_clear": "Clear Screen",
        "title_unlock": "Unlock Vault",
        "lbl_select_vault": "Select a vault.",
        "btn_start_unlock": "Start Unlocking",
        "msg_no_vaults": "No vaults available",
        "msg_time_req": "Required wait time: {} minutes.",
        "msg_err_read_vault": "Error reading this vault.",
        "title_unlocked": "Vault Unlocked!",
        "btn_back": "Back to Menu",
        "warn_title": "Warning",
        "err_title": "Error",
        "conf_title": "Confirmation",
        "notice_title": "Notice",
        "err_empty_name": "The name cannot be empty.",
        "err_time_format": "The lock time must be a positive integer (minutes).",
        "conf_start": "Are you sure you want to start the {} minute countdown?\n\nIf you close the window, progress will be lost.",
        "warn_close": "There is a countdown in progress. If you exit now, you will lose your progress and have to wait again. Are you sure you want to exit?",
        "unlocking": "Unlocking '{}'"
    },
    "ru": {
        "title_main": "ChronoLock - Хранилище Времени",
        "tab_new": "Новое хранилище",
        "tab_unlock": "Разблокировать",
        "title_new_vault": "Создать новый надежный пароль",
        "lbl_name": "Имя (напр. App1):",
        "lbl_time": "Время блокировки (минуты):",
        "btn_generate": "Сгенерировать и Заблокировать",
        "msg_gen_success": "Хранилище успешно создано! Скопируйте пароль:",
        "btn_clear": "Очистить экран",
        "title_unlock": "Разблокировать хранилище",
        "lbl_select_vault": "Выберите хранилище.",
        "btn_start_unlock": "Начать разблокировку",
        "msg_no_vaults": "Нет доступных хранилищ",
        "msg_time_req": "Требуемое время ожидания: {} минут.",
        "msg_err_read_vault": "Ошибка чтения этого хранилища.",
        "title_unlocked": "Хранилище открыто!",
        "btn_back": "Вернуться в меню",
        "warn_title": "Предупреждение",
        "err_title": "Ошибка",
        "conf_title": "Подтверждение",
        "notice_title": "Уведомление",
        "err_empty_name": "Имя не может быть пустым.",
        "err_time_format": "Время блокировки должно быть целым положительным числом (в минутах).",
        "conf_start": "Вы уверены, что хотите начать обратный отсчет на {} минут?\n\nЕсли вы закроете окно, прогресс будет потерян.",
        "warn_close": "Идет обратный отсчет. Если вы выйдете сейчас, прогресс будет потерян. Вы уверены, что хотите выйти?",
        "unlocking": "Разблокировка '{}'"
    },
    "fr": {
        "title_main": "ChronoLock - Coffre-fort temporel",
        "tab_new": "Nouveau Coffre",
        "tab_unlock": "Déverrouiller",
        "title_new_vault": "Créer un nouveau mot de passe",
        "lbl_name": "Nom (ex: App1):",
        "lbl_time": "Temps de blocage (minutes):",
        "btn_generate": "Générer & Bloquer",
        "msg_gen_success": "Coffre créé avec succès ! Copiez-le maintenant :",
        "btn_clear": "Effacer l'écran",
        "title_unlock": "Déverrouiller le coffre",
        "lbl_select_vault": "Sélectionnez un coffre.",
        "btn_start_unlock": "Démarrer le déverrouillage",
        "msg_no_vaults": "Aucun coffre disponible",
        "msg_time_req": "Temps d'attente requis : {} minutes.",
        "msg_err_read_vault": "Erreur lors de la lecture du coffre.",
        "title_unlocked": "Coffre Ouvert !",
        "btn_back": "Retour au Menu",
        "warn_title": "Avertissement",
        "err_title": "Erreur",
        "conf_title": "Confirmation",
        "notice_title": "Avis",
        "err_empty_name": "Le nom ne peut pas être vide.",
        "err_time_format": "Le temps de blocage doit être un entier positif (minutes).",
        "conf_start": "Êtes-vous sûr de vouloir commencer le compte à rebours de {} minutes ?\n\nSi vous fermez la fenêtre, la progression sera perdue.",
        "warn_close": "Un compte à rebours est en cours. Si vous quittez maintenant, la progression sera perdue. Êtes-vous sûr de vouloir quitter ?",
        "unlocking": "Déverrouillage de '{}'"
    },
    "ja": {
        "title_main": "ChronoLock - タイムボルト",
        "tab_new": "新しいボルト",
        "tab_unlock": "ロック解除",
        "title_new_vault": "新しい安全なパスワードを作成",
        "lbl_name": "名前 (例: App1):",
        "lbl_time": "ロック時間 (分):",
        "btn_generate": "生成とロック",
        "msg_gen_success": "ボルトが正常に作成されました！ 今すぐコピー:",
        "btn_clear": "画面をクリア",
        "title_unlock": "ボルトのロック解除",
        "lbl_select_vault": "ボルトを選択してください。",
        "btn_start_unlock": "ロック解除を開始",
        "msg_no_vaults": "ボルトがありません",
        "msg_time_req": "必要な待機時間: {} 分。",
        "msg_err_read_vault": "このボルトの読み取りエラー。",
        "title_unlocked": "ボルト解除！",
        "btn_back": "メニューに戻る",
        "warn_title": "警告",
        "err_title": "エラー",
        "conf_title": "確認",
        "notice_title": "通知",
        "err_empty_name": "名前を空にすることはできません。",
        "err_time_format": "ロック時間は正の整数（分）である必要があります。",
        "conf_start": "{} 分のカウントダウンを開始してもよろしいですか？\n\nウィンドウを閉じると進行状況が失われます。",
        "warn_close": "カウントダウンが進行中です。 今終了すると進行状況が失われます。 本当に終了しますか？",
        "unlocking": "'{}' をロック解除中"
    },
    "zh": {
        "title_main": "ChronoLock - 时间金库",
        "tab_new": "新金库",
        "tab_unlock": "解锁",
        "title_new_vault": "创建新的安全密码",
        "lbl_name": "名称 (例如: App1):",
        "lbl_time": "锁定时间 (分钟):",
        "btn_generate": "生成并锁定",
        "msg_gen_success": "金库创建成功！ 立即复制:",
        "btn_clear": "清除屏幕",
        "title_unlock": "解锁金库",
        "lbl_select_vault": "选择一个金库。",
        "btn_start_unlock": "开始解锁",
        "msg_no_vaults": "没有可用的金库",
        "msg_time_req": "需要等待时间: {} 分钟。",
        "msg_err_read_vault": "读取此金库时出错。",
        "title_unlocked": "金库已打开！",
        "btn_back": "返回菜单",
        "warn_title": "警告",
        "err_title": "错误",
        "conf_title": "确认",
        "notice_title": "注意",
        "err_empty_name": "名称不能为空。",
        "err_time_format": "锁定时间必须是正整数 (分钟)。",
        "conf_start": "您确定要开始 {} 分钟的倒计时吗？\n\n如果您关闭窗口，进度将会丢失。",
        "warn_close": "倒计时正在进行中。 如果您现在退出，进度将会丢失。 确定要退出吗？",
        "unlocking": "正在解锁 '{}'"
    }
}

class Translator:
    def __init__(self):
        self.current_lang = "es"
        self.load_config()
        
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get('lang') in TRANSLATIONS:
                        self.current_lang = data['lang']
            except Exception:
                pass
                
    def save_config(self):
        data = {'lang': self.current_lang}
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f)
        except Exception:
            pass

    def set_language(self, language_name):
        code = LANGUAGES.get(language_name, "es")
        if code in TRANSLATIONS:
            self.current_lang = code
            self.save_config()
            
    def get_current_language_name(self):
        for name, code in LANGUAGES.items():
            if code == self.current_lang:
                return name
        return "Español"

    def t(self, key):
        return TRANSLATIONS[self.current_lang].get(key, key)

translator = Translator()

def t(key, *args):
    text = translator.t(key)
    if args:
        text = text.format(*args)
    return text
