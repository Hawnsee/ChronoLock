import customtkinter as ctk
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
import core
import clipboard
import os
from locales import translator, t, LANGUAGES

MAX_LOCK_MINUTES = core.MAX_LOCK_MINUTES

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ChronoLockApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title(t("title_main"))
        self.geometry("600x520")
        self.resizable(False, False)
        
        core.initialize_system()
        
        self.timer_running = False
        self.remaining_seconds = 0
        self.vault_to_unlock = ""
        self._clipboard_clear_id = None
        
        # Selector de idioma
        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.pack(fill="x", padx=20, pady=(10, 0))
        
        self.lang_selector = ctk.CTkOptionMenu(
            self.frame_top, 
            values=list(LANGUAGES.keys()), 
            command=self.on_language_change,
            width=100
        )
        self.lang_selector.set(translator.get_current_language_name())
        self.lang_selector.pack(side="right")
        
        self.tabview = ctk.CTkTabview(self, width=550, height=430)
        self.tabview.pack(padx=20, pady=(0, 20))
        
        # Pestañas
        self.tab_new_name = t("tab_new")
        self.tab_unlock_name = t("tab_unlock")
        self.tabview.add(self.tab_new_name)
        self.tabview.add(self.tab_unlock_name)
        self.tabview.set(self.tab_new_name)
        
        self.setup_generate_tab()
        self.setup_unlock_tab()
        
        self.tabview.configure(command=self.on_tab_change)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_language_change(self, choice):
        translator.set_language(choice)
        self.update_ui_texts()

    def update_ui_texts(self):
        self.title(t("title_main"))
        
        new_tab_new = t("tab_new")
        if getattr(self, 'tab_new_name', '') != new_tab_new:
            try:
                self.tabview.rename(self.tab_new_name, new_tab_new)
                self.tab_new_name = new_tab_new
            except Exception:
                pass
                
        new_tab_unlock = t("tab_unlock")
        if getattr(self, 'tab_unlock_name', '') != new_tab_unlock:
            try:
                self.tabview.rename(self.tab_unlock_name, new_tab_unlock)
                self.tab_unlock_name = new_tab_unlock
            except Exception:
                pass
        
        self.title_gen.configure(text=t("title_new_vault"))
        self.lbl_name_gen.configure(text=t("lbl_name"))
        self.lbl_time_gen.configure(text=t("lbl_time"))
        self.btn_generate.configure(text=t("btn_generate"))
        self.btn_limpiar_gen.configure(text=t("btn_clear"))
        self.btn_copy_gen.configure(text=t("btn_copy"))
        
        if self.lbl_result.cget("text") != "":
            self.lbl_result.configure(text=t("msg_gen_success"))
            
        self.unlock_title.configure(text=t("title_unlock") if not self.timer_running else t("unlocking", self.combo_vaults.get()))
        
        if not self.timer_running and not self.entry_unlocked.winfo_ismapped():
            val = self.combo_vaults.get()
            # Reset dropdown strings gracefully
            if val in ["No hay bóvedas", "No vaults available", "Нет доступных хранилищ", "Aucun coffre disponible", "ボルトがありません", "没有可用的金库", t("msg_no_vaults")]:
                self.combo_vaults.set(t("msg_no_vaults"))
                self.lbl_lock_info.configure(text=t("lbl_select_vault"))
            else:
                self.on_vault_select(val) 
                
        self.btn_unlock.configure(text=t("btn_start_unlock"))
        self.btn_volver.configure(text=t("btn_back"))
        self.btn_change_time.configure(text=t("btn_change_time"))
        self.btn_delete_vault.configure(text=t("btn_delete_vault"))
        self.btn_copy_unlock.configure(text=t("btn_copy"))
        
        if self.entry_unlocked.winfo_ismapped():
            self.unlock_title.configure(text=t("title_unlocked"))
            
        if self.tabview.get() == self.tab_unlock_name:
            self.refresh_vault_list()
            
    def setup_generate_tab(self):
        tab = self.tabview.tab(self.tab_new_name)
        
        self.title_gen = ctk.CTkLabel(tab, text=t("title_new_vault"), font=ctk.CTkFont(size=20, weight="bold"))
        self.title_gen.pack(pady=20)
        
        frame = ctk.CTkFrame(tab, fg_color="transparent")
        frame.pack(pady=10)
        
        self.lbl_name_gen = ctk.CTkLabel(frame, text=t("lbl_name"))
        self.lbl_name_gen.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_name = ctk.CTkEntry(frame, width=200)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)
        
        self.lbl_time_gen = ctk.CTkLabel(frame, text=t("lbl_time"))
        self.lbl_time_gen.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_time = ctk.CTkEntry(frame, width=200)
        self.entry_time.insert(0, "30")
        self.entry_time.grid(row=1, column=1, padx=10, pady=10)
        
        self.btn_generate = ctk.CTkButton(tab, text=t("btn_generate"), command=self.generate_password)
        self.btn_generate.pack(pady=20)
        
        self.lbl_result = ctk.CTkLabel(tab, text="", text_color="#2ecc71", font=ctk.CTkFont(weight="bold"))
        self.lbl_result.pack(pady=5)
        
        self.entry_result = ctk.CTkEntry(tab, width=400, justify="center", state="disabled", text_color="#2ecc71")
        self.entry_result.pack(pady=5)
        
        self.frame_gen_actions = ctk.CTkFrame(tab, fg_color="transparent")
        
        self.btn_copy_gen = ctk.CTkButton(self.frame_gen_actions, text=t("btn_copy"), command=self.copy_generated_password, width=140, fg_color="#2980b9", hover_color="#1a5276")
        self.btn_copy_gen.pack(side="left", padx=5)
        
        self.btn_limpiar_gen = ctk.CTkButton(self.frame_gen_actions, text=t("btn_clear"), command=self.reset_generate_tab, width=140)
        self.btn_limpiar_gen.pack(side="left", padx=5)
        
        self.lbl_copy_status_gen = ctk.CTkLabel(tab, text="", text_color="#f39c12", font=ctk.CTkFont(size=12))

    def setup_unlock_tab(self):
        self.tab_unlock = self.tabview.tab(self.tab_unlock_name)
        
        self.unlock_title = ctk.CTkLabel(self.tab_unlock, text=t("title_unlock"), font=ctk.CTkFont(size=20, weight="bold"))
        self.unlock_title.pack(pady=20)
        
        self.combo_vaults = ctk.CTkComboBox(self.tab_unlock, values=[], width=250)
        self.combo_vaults.pack(pady=15)
        
        self.lbl_lock_info = ctk.CTkLabel(self.tab_unlock, text=t("lbl_select_vault"))
        self.lbl_lock_info.pack(pady=5)
        
        self.combo_vaults.configure(command=self.on_vault_select)
        
        self.btn_unlock = ctk.CTkButton(self.tab_unlock, text=t("btn_start_unlock"), command=self.start_unlock, fg_color="#C21807", hover_color="#8A0303")
        self.btn_unlock.pack(pady=10)
        
        # Frame para botones de gestión (se mostrará solo tras desbloquear)
        self.frame_vault_actions = ctk.CTkFrame(self.tab_unlock, fg_color="transparent")
        
        self.btn_change_time = ctk.CTkButton(self.frame_vault_actions, text=t("btn_change_time"), command=self.change_vault_time, width=140, fg_color="#2980b9", hover_color="#1a5276")
        self.btn_change_time.pack(side="left", padx=5)
        
        self.btn_delete_vault = ctk.CTkButton(self.frame_vault_actions, text=t("btn_delete_vault"), command=self.delete_vault, width=140, fg_color="#7f1d1d", hover_color="#450a0a")
        self.btn_delete_vault.pack(side="left", padx=5)
        
        self.lbl_timer = ctk.CTkLabel(self.tab_unlock, text="00:00:00", font=ctk.CTkFont(size=60, weight="bold"))
        
        self.entry_unlocked = ctk.CTkEntry(self.tab_unlock, width=400, justify="center", state="disabled", text_color="#2ecc71", font=ctk.CTkFont(size=18, weight="bold"))
        
        self.btn_copy_unlock = ctk.CTkButton(self.tab_unlock, text=t("btn_copy"), command=self.copy_unlocked_password, width=160, fg_color="#2980b9", hover_color="#1a5276")
        
        self.lbl_copy_status_unlock = ctk.CTkLabel(self.tab_unlock, text="", text_color="#f39c12", font=ctk.CTkFont(size=12))
        
        self.btn_volver = ctk.CTkButton(self.tab_unlock, text=t("btn_back"), command=self.reset_unlock_tab)

    def on_tab_change(self):
        if self.tabview.get() == self.tab_unlock_name:
            self.refresh_vault_list()

    def refresh_vault_list(self):
        vaults = core.list_vaults()
        if vaults:
            self.combo_vaults.configure(values=vaults)
            
            if self.combo_vaults.get() not in vaults:
                self.combo_vaults.set(vaults[0])
                
            self.on_vault_select(self.combo_vaults.get())
        else:
            self.combo_vaults.configure(values=[t("msg_no_vaults")])
            self.combo_vaults.set(t("msg_no_vaults"))
            self.lbl_lock_info.configure(text="")
            self.btn_unlock.configure(state="disabled")

    def on_vault_select(self, choice):
        if choice in ["No hay bóvedas", "No vaults available", "Нет доступных хранилищ", "Aucun coffre disponible", "ボルトがありません", "没有可用的金库", t("msg_no_vaults")]: return
        try:
            data = core.load_vault_info(choice)
            mins = data.get("lock_time_minutes", 30)
            self.lbl_lock_info.configure(text=t("msg_time_req", mins))
            self.btn_unlock.configure(state="normal")
        except Exception:
            self.lbl_lock_info.configure(text=t("msg_err_read_vault"))
            self.btn_unlock.configure(state="disabled")

    def generate_password(self):
        name = self.entry_name.get().strip()
        time_str = self.entry_time.get().strip()
        
        if not name:
            messagebox.showwarning(t("notice_title"), t("err_empty_name"))
            return
            
        try:
            lock_time = int(time_str)
            if lock_time <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(t("notice_title"), t("err_time_format"))
            return

        # MED-1: Límite de tiempo máximo
        if lock_time > MAX_LOCK_MINUTES:
            messagebox.showwarning(t("notice_title"), t("err_time_max", MAX_LOCK_MINUTES))
            return
            
        try:
            password = core.generate_password(name, lock_time)
            self.lbl_result.configure(text=t("msg_gen_success"))
            
            self.entry_result.configure(state="normal")
            self.entry_result.delete(0, "end")
            self.entry_result.insert(0, password)
            self.entry_result.configure(state="disabled")
            
            self.entry_name.delete(0, "end")
            self.frame_gen_actions.pack(pady=10)
            self.lbl_copy_status_gen.pack(pady=2)
            
        except Exception as e:
            messagebox.showerror(t("err_title"), str(e))

    def start_unlock(self):
        name = self.combo_vaults.get()
        if not name or name == t("msg_no_vaults"): return
        
        try:
            data = core.load_vault_info(name)
            mins = data.get("lock_time_minutes", 30)
            # HIGH-3: Validar que la contraseña existe antes de iniciar
            password = data.get("password")
            if not password:
                messagebox.showerror(t("err_title"), t("err_vault_corrupt"))
                return
        except Exception as e:
            messagebox.showerror(t("err_title"), str(e))
            return
            
        confirm = messagebox.askyesno(t("conf_title"), t("conf_start", mins))
        if not confirm: return
        
        # HIGH-1: Solo guardar el nombre, NO la contraseña desencriptada
        self.vault_to_unlock = name
        
        self.combo_vaults.pack_forget()
        self.lbl_lock_info.pack_forget()
        self.btn_unlock.pack_forget()
        
        self.unlock_title.configure(text=t("unlocking", name))
        self.lbl_timer.pack(pady=40)
        
        self.remaining_seconds = mins * 60
        self.timer_running = True
        
        self.update_timer()

    def update_timer(self):
        if not self.timer_running: return
        
        if self.remaining_seconds > 0:
            m, s = divmod(self.remaining_seconds, 60)
            h, m = divmod(m, 60)
            time_str = f"{h:02d}:{m:02d}:{s:02d}"
            self.lbl_timer.configure(text=time_str)
            self.remaining_seconds -= 1
            self.after(1000, self.update_timer)
        else:
            self.timer_running = False
            self.lbl_timer.configure(text="00:00:00", text_color="#2ecc71")
            
            # HIGH-1: Desencriptar SOLO ahora, al finalizar el temporizador
            try:
                data = core.load_vault_info(self.vault_to_unlock)
                password = data.get("password", "")
                if not password:
                    messagebox.showerror(t("err_title"), t("err_vault_corrupt"))
                    self.reset_unlock_tab()
                    return
            except Exception as e:
                messagebox.showerror(t("err_title"), str(e))
                self.reset_unlock_tab()
                return
            
            self.unlock_title.configure(text=t("title_unlocked"))
            self.entry_unlocked.configure(state="normal")
            self.entry_unlocked.delete(0, "end")
            self.entry_unlocked.insert(0, password)
            self.entry_unlocked.configure(state="disabled")
            self.entry_unlocked.pack(pady=10)
            
            self.btn_copy_unlock.pack(pady=5)
            self.lbl_copy_status_unlock.pack(pady=2)
            self.frame_vault_actions.pack(pady=5)
            self.btn_volver.pack(pady=10)

    def reset_generate_tab(self):
        self.lbl_result.configure(text="")
        self.entry_result.configure(state="normal")
        self.entry_result.delete(0, "end")
        self.entry_result.configure(state="disabled")
        self.entry_name.delete(0, "end")
        self.entry_time.delete(0, "end")
        self.entry_time.insert(0, "30")
        self.frame_gen_actions.pack_forget()
        self.lbl_copy_status_gen.configure(text="")
        self.lbl_copy_status_gen.pack_forget()

    def reset_unlock_tab(self):
        self.lbl_timer.pack_forget()
        self.entry_unlocked.pack_forget()
        self.btn_copy_unlock.pack_forget()
        self.lbl_copy_status_unlock.configure(text="")
        self.lbl_copy_status_unlock.pack_forget()
        self.frame_vault_actions.pack_forget()
        self.btn_volver.pack_forget()
        
        self.unlock_title.configure(text=t("title_unlock"))
        self.lbl_timer.configure(text_color=["black", "white"])
        self.vault_to_unlock = ""
        
        self.combo_vaults.pack(pady=15)
        self.lbl_lock_info.pack(pady=5)
        self.btn_unlock.pack(pady=10)
        self.refresh_vault_list()

    def delete_vault(self):
        """Elimina la bóveda seleccionada con doble confirmación."""
        name = self.vault_to_unlock
        if not name: return
        
        # Primera confirmación
        confirm1 = messagebox.askyesno(t("warn_title"), t("conf_delete_1", name))
        if not confirm1: return
        
        # Segunda confirmación
        confirm2 = messagebox.askyesno(t("warn_title"), t("conf_delete_2", name))
        if not confirm2: return
        
        try:
            core.delete_vault(name)
            messagebox.showinfo(t("notice_title"), t("msg_deleted", name))
            self.reset_unlock_tab()
        except Exception as e:
            messagebox.showerror(t("err_title"), str(e))

    def change_vault_time(self):
        """Cambia el tiempo de bloqueo de la bóveda seleccionada."""
        name = self.vault_to_unlock
        if not name: return
        
        new_time = simpledialog.askinteger(
            t("btn_change_time"),
            t("dlg_new_time"),
            parent=self,
            minvalue=1,
            maxvalue=MAX_LOCK_MINUTES
        )
        
        if new_time is None: return
        
        try:
            core.update_vault_time(name, new_time)
            messagebox.showinfo(t("notice_title"), t("msg_time_updated", name, new_time))
        except Exception as e:
            messagebox.showerror(t("err_title"), str(e))

    def copy_generated_password(self):
        """Copia la contraseña generada al portapapeles sin historial."""
        password = self.entry_result.get()
        if password:
            if clipboard.secure_copy(password):
                self.lbl_copy_status_gen.configure(text=t("msg_copied"))
                self._schedule_clipboard_clear(self.lbl_copy_status_gen)
            else:
                self.lbl_copy_status_gen.configure(text=t("msg_copy_fail"))

    def copy_unlocked_password(self):
        """Copia la contraseña desbloqueada al portapapeles sin historial."""
        password = self.entry_unlocked.get()
        if password:
            if clipboard.secure_copy(password):
                self.lbl_copy_status_unlock.configure(text=t("msg_copied"))
                self._schedule_clipboard_clear(self.lbl_copy_status_unlock)
            else:
                self.lbl_copy_status_unlock.configure(text=t("msg_copy_fail"))

    def _schedule_clipboard_clear(self, status_label):
        """Programa la limpieza del portapapeles en 30 segundos."""
        if self._clipboard_clear_id:
            self.after_cancel(self._clipboard_clear_id)
        
        def clear():
            clipboard.clear_clipboard()
            try:
                status_label.configure(text=t("msg_clipboard_cleared"))
            except Exception:
                pass
            self._clipboard_clear_id = None
        
        self._clipboard_clear_id = self.after(30000, clear)

    def on_closing(self):
        if self.timer_running:
            if messagebox.askokcancel(t("warn_title"), t("warn_close")):
                self.destroy()
        else:
            self.destroy()

if __name__ == "__main__":
    app = ChronoLockApp()
    app.mainloop()
