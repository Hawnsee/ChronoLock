import json
import os
import sys

# MED-2: Rutas absolutas ancladas al directorio del ejecutable
if getattr(sys, 'frozen', False):
    _BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(_BASE_DIR, "config.json")

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
        "msg_gen_success": "¡Bóveda creada exitosamente! Cópiala ahora (se ocultará en 30s):",
        "btn_clear": "Limpiar Pantalla",
        "title_unlock": "Desbloquear Bóveda",
        "lbl_select_vault": "Selecciona una bóveda.",
        "btn_start_unlock": "Iniciar Desbloqueo",
        "msg_no_vaults": "No hay bóvedas",
        "msg_time_req": "Tiempo de espera requerido: {} minutos.",
        "msg_err_read_vault": "Error leyendo esta bóveda.",
        "title_unlocked": "¡Bóveda Abierta! (se ocultará en 30s)",
        "btn_back": "Volver al Menú",
        "warn_title": "Advertencia",
        "err_title": "Error",
        "conf_title": "Confirmación",
        "notice_title": "Aviso",
        "err_empty_name": "El nombre no puede estar vacío.",
        "err_time_format": "El tiempo de bloqueo debe ser un número entero positivo (minutos).",
        "conf_start": "¿Estás seguro de iniciar la cuenta atrás de {} minutos?\n\nSi cierras la ventana el progreso se perderá.",
        "warn_close": "Hay una cuenta atrás en progreso. Si sales ahora, perderás el progreso y tendrás que esperar de nuevo. ¿Seguro que quieres salir?",
        "unlocking": "Desbloqueando '{}'",
        "err_time_max": "El tiempo máximo de bloqueo es {} minutos (24 horas).",
        "err_vault_corrupt": "La bóveda está corrupta o no contiene una contraseña válida.",
        "btn_delete_vault": "Eliminar Bóveda",
        "btn_change_time": "Cambiar Tiempo",
        "conf_delete_1": "¿Estás seguro de que quieres eliminar la bóveda '{}'?\n\nLa contraseña se perderá PARA SIEMPRE.",
        "conf_delete_2": "ÚLTIMA OPORTUNIDAD: ¿Eliminar definitivamente '{}'?\n\nEsta acción NO se puede deshacer.",
        "msg_deleted": "La bóveda '{}' ha sido eliminada.",
        "dlg_new_time": "Nuevo tiempo de bloqueo (minutos):",
        "msg_time_updated": "Tiempo de bloqueo de '{}' actualizado a {} minutos.",
        "btn_copy": "📋 Copiar Seguro",
        "msg_copied": "✅ Copiada (se borrará del portapapeles en 30s)",
        "msg_copy_fail": "❌ Error al copiar al portapapeles.",
        "msg_clipboard_cleared": "🔒 Portapapeles limpiado automáticamente.",
        "msg_password_hidden": "🔒 Contraseña oculta por seguridad.",
        "msg_hide_warning": "⚠️ Se ocultará en 30 segundos."
    },
    "en": {
        "title_main": "ChronoLock - Time Vault",
        "tab_new": "New Vault",
        "tab_unlock": "Unlock",
        "title_new_vault": "Create New Secure Password",
        "lbl_name": "Name (e.g. App1):",
        "lbl_time": "Lock time (minutes):",
        "btn_generate": "Generate & Lock",
        "msg_gen_success": "Vault created successfully! Copy it now (hides in 30s):",
        "btn_clear": "Clear Screen",
        "title_unlock": "Unlock Vault",
        "lbl_select_vault": "Select a vault.",
        "btn_start_unlock": "Start Unlock",
        "msg_no_vaults": "No vaults available",
        "msg_time_req": "Required wait time: {} minutes.",
        "msg_err_read_vault": "Error reading this vault.",
        "title_unlocked": "Vault Unlocked! (hides in 30s)",
        "btn_back": "Back to Menu",
        "warn_title": "Warning",
        "err_title": "Error",
        "conf_title": "Confirmation",
        "notice_title": "Notice",
        "err_empty_name": "The name cannot be empty.",
        "err_time_format": "The lock time must be a positive integer (minutes).",
        "conf_start": "Are you sure you want to start the {} minute countdown?\n\nIf you close the window, progress will be lost.",
        "warn_close": "There is a countdown in progress. If you exit now, you will lose your progress and have to wait again. Are you sure you want to exit?",
        "unlocking": "Unlocking '{}'",
        "err_time_max": "Maximum lock time is {} minutes (24 hours).",
        "err_vault_corrupt": "The vault is corrupt or does not contain a valid password.",
        "btn_delete_vault": "Delete Vault",
        "btn_change_time": "Change Time",
        "conf_delete_1": "Are you sure you want to delete the vault '{}'?\n\nThe password will be lost FOREVER.",
        "conf_delete_2": "LAST CHANCE: Permanently delete '{}'?\n\nThis action CANNOT be undone.",
        "msg_deleted": "The vault '{}' has been deleted.",
        "dlg_new_time": "New lock time (minutes):",
        "msg_time_updated": "Lock time of '{}' updated to {} minutes.",
        "btn_copy": "📋 Secure Copy",
        "msg_copied": "✅ Copied (clipboard clears in 30s)",
        "msg_copy_fail": "❌ Failed to copy to clipboard.",
        "msg_clipboard_cleared": "🔒 Clipboard cleared automatically.",
        "msg_password_hidden": "🔒 Password hidden for security.",
        "msg_hide_warning": "⚠️ Will hide in 30 seconds."
    },
    "ru": {
        "title_main": "ChronoLock - Хранилище Времени",
        "tab_new": "Новое хранилище",
        "tab_unlock": "Разблокировать",
        "title_new_vault": "Создать новый надежный пароль",
        "lbl_name": "Имя (напр. App1):",
        "lbl_time": "Время блокировки (минуты):",
        "btn_generate": "Сгенерировать и Заблокировать",
        "msg_gen_success": "Хранилище создано! Скопируйте сейчас (скроется через 30с):",
        "btn_clear": "Очистить экран",
        "title_unlock": "Разблокировать хранилище",
        "lbl_select_vault": "Выберите хранилище.",
        "btn_start_unlock": "Начать разблокировку",
        "msg_no_vaults": "Нет хранилищ",
        "msg_time_req": "Требуемое время ожидания: {} минут.",
        "msg_err_read_vault": "Ошибка чтения хранилища.",
        "title_unlocked": "Хранилище Открыто! (скроется через 30с)",
        "btn_back": "Вернуться в меню",
        "warn_title": "Предупреждение",
        "err_title": "Ошибка",
        "conf_title": "Подтверждение",
        "notice_title": "Уведомление",
        "err_empty_name": "Имя не может быть пустым.",
        "err_time_format": "Время блокировки должно быть целым положительным числом (в минутах).",
        "conf_start": "Вы уверены, что хотите начать обратный отсчет на {} минут?\n\nЕсли вы закроете окно, прогресс будет потерян.",
        "warn_close": "Идет обратный отсчет. Если вы выйдете сейчас, прогресс будет потерян. Вы уверены, что хотите выйти?",
        "unlocking": "Разблокировка '{}'",
        "err_time_max": "Максимальное время блокировки — {} минут (24 часа).",
        "err_vault_corrupt": "Хранилище повреждено или не содержит действительного пароля.",
        "btn_delete_vault": "Удалить хранилище",
        "btn_change_time": "Изменить время",
        "conf_delete_1": "Вы уверены, что хотите удалить хранилище '{}'?\n\nПароль будет потерян НАВСЕГДА.",
        "conf_delete_2": "ПОСЛЕДНИЙ ШАНС: Удалить '{}' окончательно?\n\nЭто действие НЕВОЗМОЖНО отменить.",
        "msg_deleted": "Хранилище '{}' удалено.",
        "dlg_new_time": "Новое время блокировки (минуты):",
        "msg_time_updated": "Время блокировки '{}' обновлено до {} минут.",
        "btn_copy": "📋 Безопасное копирование",
        "msg_copied": "✅ Скопировано (буфер очистится через 30с)",
        "msg_copy_fail": "❌ Ошибка копирования в буфер обмена.",
        "msg_clipboard_cleared": "🔒 Буфер обмена автоматически очищен.",
        "msg_password_hidden": "🔒 Пароль скрыт в целях безопасности.",
        "msg_hide_warning": "⚠️ Скроется через 30 секунд."
    },
    "fr": {
        "title_main": "ChronoLock - Coffre-fort temporel",
        "tab_new": "Nouveau Coffre",
        "tab_unlock": "Déverrouiller",
        "title_new_vault": "Créer un nouveau mot de passe",
        "lbl_name": "Nom (ex: App1):",
        "lbl_time": "Temps de blocage (minutes):",
        "btn_generate": "Générer & Bloquer",
        "msg_gen_success": "Coffre-fort créé avec succès! Copiez-le maintenant (masqué dans 30s):",
        "btn_clear": "Effacer l'écran",
        "title_unlock": "Déverrouiller le coffre-fort",
        "lbl_select_vault": "Sélectionnez un coffre-fort.",
        "btn_start_unlock": "Démarrer le déverrouillage",
        "msg_no_vaults": "Aucun coffre-fort",
        "msg_time_req": "Temps d'attente requis : {} minutes.",
        "msg_err_read_vault": "Erreur de lecture de ce coffre-fort.",
        "title_unlocked": "Coffre-fort Ouvert ! (masqué dans 30s)",
        "btn_back": "Retour au Menu",
        "warn_title": "Avertissement",
        "err_title": "Erreur",
        "conf_title": "Confirmation",
        "notice_title": "Avis",
        "err_empty_name": "Le nom ne peut pas être vide.",
        "err_time_format": "Le temps de blocage doit être un entier positif (minutes).",
        "conf_start": "Êtes-vous sûr de vouloir commencer le compte à rebours de {} minutes ?\n\nSi vous fermez la fenêtre, la progression sera perdue.",
        "warn_close": "Un compte à rebours est en cours. Si vous quittez maintenant, la progression sera perdue. Êtes-vous sûr de vouloir quitter ?",
        "unlocking": "Déverrouillage de '{}'",
        "err_time_max": "Le temps de blocage maximum est de {} minutes (24 heures).",
        "err_vault_corrupt": "Le coffre est corrompu ou ne contient pas de mot de passe valide.",
        "btn_delete_vault": "Supprimer le coffre",
        "btn_change_time": "Modifier le temps",
        "conf_delete_1": "Êtes-vous sûr de vouloir supprimer le coffre '{}' ?\n\nLe mot de passe sera perdu POUR TOUJOURS.",
        "conf_delete_2": "DERNIÈRE CHANCE : Supprimer définitivement '{}' ?\n\nCette action est IRRÉVERSIBLE.",
        "msg_deleted": "Le coffre '{}' a été supprimé.",
        "dlg_new_time": "Nouveau temps de blocage (minutes) :",
        "msg_time_updated": "Temps de blocage de '{}' mis à jour à {} minutes.",
        "btn_copy": "📋 Copie sécurisée",
        "msg_copied": "✅ Copié (le presse-papiers sera vidé dans 30s)",
        "msg_copy_fail": "❌ Échec de la copie dans le presse-papiers.",
        "msg_clipboard_cleared": "🔒 Presse-papiers vidé automatiquement.",
        "msg_password_hidden": "🔒 Mot de passe masqué par sécurité.",
        "msg_hide_warning": "⚠️ Sera masqué dans 30 secondes."
    },
    "ja": {
        "title_main": "ChronoLock - タイムボルト",
        "tab_new": "新しいボルト",
        "tab_unlock": "ロック解除",
        "title_new_vault": "新しい安全なパスワードを作成",
        "lbl_name": "名前 (例: App1):",
        "lbl_time": "ロック時間 (分):",
        "btn_generate": "生成とロック",
        "msg_gen_success": "ボルトが作成されました！今すぐコピーしてください（30秒後に非表示）:",
        "btn_clear": "画面をクリア",
        "title_unlock": "ボルトのロック解除",
        "lbl_select_vault": "ボルトを選択してください。",
        "btn_start_unlock": "ロック解除を開始",
        "msg_no_vaults": "ボルトがありません",
        "msg_time_req": "必要な待機時間: {} 分。",
        "msg_err_read_vault": "このボルトの読み取りエラー。",
        "title_unlocked": "ボルトが開きました！（30秒後に非表示）",
        "btn_back": "メニューに戻る",
        "warn_title": "警告",
        "err_title": "エラー",
        "conf_title": "確認",
        "notice_title": "通知",
        "err_empty_name": "名前を空にすることはできません。",
        "err_time_format": "ロック時間は正の整数（分）である必要があります。",
        "conf_start": "{} 分のカウントダウンを開始してもよろしいですか？\n\nウィンドウを閉じると進行状況が失われます。",
        "warn_close": "カウントダウンが進行中です。 今終了すると進行状況が失われます。 本当に終了しますか？",
        "unlocking": "'{}' をロック解除中",
        "err_time_max": "最大ロック時間は {} 分（24時間）です。",
        "err_vault_corrupt": "ボルトが破損しているか、有効なパスワードが含まれていません。",
        "btn_delete_vault": "ボルトを削除",
        "btn_change_time": "時間を変更",
        "conf_delete_1": "ボルト '{}' を削除してもよろしいですか？\n\nパスワードは永久に失われます。",
        "conf_delete_2": "最後の確認: '{}' を完全に削除しますか？\n\nこの操作は元に戻せません。",
        "msg_deleted": "ボルト '{}' が削除されました。",
        "dlg_new_time": "新しいロック時間（分）:",
        "msg_time_updated": "'{}' のロック時間が {} 分に更新されました。",
        "btn_copy": "📋 安全コピー",
        "msg_copied": "✅ コピー済み（30秒後にクリップボードを消去）",
        "msg_copy_fail": "❌ クリップボードへのコピーに失敗しました。",
        "msg_clipboard_cleared": "🔒 クリップボードが自動的に消去されました。",
        "msg_password_hidden": "🔒 セキュリティのためパスワードを非表示にしました。",
        "msg_hide_warning": "⚠️ 30秒後に非表示になります。"
    },
    "zh": {
        "title_main": "ChronoLock - 时间金库",
        "tab_new": "新金库",
        "tab_unlock": "解锁",
        "title_new_vault": "创建新的安全密码",
        "lbl_name": "名称 (例如: App1):",
        "lbl_time": "锁定时间 (分钟):",
        "btn_generate": "生成并锁定",
        "msg_gen_success": "金库创建成功！立即复制（30秒后隐藏）：",
        "btn_clear": "清屏",
        "title_unlock": "解锁金库",
        "lbl_select_vault": "选择一个金库。",
        "btn_start_unlock": "开始解锁",
        "msg_no_vaults": "没有金库",
        "msg_time_req": "需要等待时间：{} 分钟。",
        "msg_err_read_vault": "读取此金库时出错。",
        "title_unlocked": "金库已打开！（30秒后隐藏）",
        "btn_back": "返回菜单",
        "warn_title": "警告",
        "err_title": "错误",
        "conf_title": "确认",
        "notice_title": "注意",
        "err_empty_name": "名称不能为空。",
        "err_time_format": "锁定时间必须是正整数 (分钟)。",
        "conf_start": "您确定要开始 {} 分钟的倒计时吗？\n\n如果您关闭窗口，进度将会丢失。",
        "warn_close": "倒计时正在进行中。 如果您现在退出，进度将会丢失。 确定要退出吗？",
        "unlocking": "正在解锁 '{}'",
        "err_time_max": "最大锁定时间为 {} 分钟（24小时）。",
        "err_vault_corrupt": "金库已损坏或不包含有效密码。",
        "btn_delete_vault": "删除金库",
        "btn_change_time": "更改时间",
        "conf_delete_1": "您确定要删除金库 '{}'吗？\n\n密码将永久丢失。",
        "conf_delete_2": "最后机会：永久删除 '{}'？\n\n此操作无法撤消。",
        "msg_deleted": "金库 '{}' 已删除。",
        "dlg_new_time": "新锁定时间（分钟）:",
        "msg_time_updated": "'{}' 的锁定时间已更新为 {} 分钟。",
        "btn_copy": "📋 安全复制",
        "msg_copied": "✅ 已复制（30秒后清除剪贴板）",
        "msg_copy_fail": "❌ 复制到剪贴板失败。",
        "msg_clipboard_cleared": "🔒 剪贴板已自动清除。",
        "msg_password_hidden": "🔒 为安全起见密码已隐藏。",
        "msg_hide_warning": "⚠️ 将在30秒后隐藏。"
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
