import tkinter as tk
from tkinter import messagebox
import time
import json
import os

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor de Atendimento")

        # Variáveis para armazenamento de dados
        self.total_atendimentos = 0
        self.total_tempo = 0
        self.inicio_atendimento = [0, 0, 0]
        self.tempo_decorrido = [0, 0, 0]

        # Carregar dados salvos
        self.carregar_dados()

        # Layout - Título
        self.label_title = tk.Label(root, text="Monitor de Atendimentos", font=('Helvetica', 16))
        self.label_title.pack(pady=10)

        # Layout para cada chat
        self.chat_frames = []
        for i in range(3):
            frame = tk.Frame(root, borderwidth=2, relief="groove", padx=10, pady=10)
            frame.pack(pady=10)

            label_cronometro = tk.Label(frame, text=f"Tempo Decorrido: 00:00:00", font=('Helvetica', 12), fg='blue')
            label_cronometro.pack(pady=5)

            btn_iniciar = tk.Button(frame, text=f"Iniciar Chat {i+1}", command=lambda i=i: self.iniciar_atendimento(i))
            btn_iniciar.pack(pady=5)

            btn_finalizar = tk.Button(frame, text=f"Finalizar Chat {i+1}", command=lambda i=i: self.finalizar_atendimento(i))
            btn_finalizar.pack(pady=5)

            self.chat_frames.append({
                'label_cronometro': label_cronometro,
                'btn_iniciar': btn_iniciar,
                'btn_finalizar': btn_finalizar
            })

        # Média total de tempo e quantidade total de atendimentos
        self.label_media_total = tk.Label(root, text="Média de Tempo Total: 00:00:00", font=('Helvetica', 12))
        self.label_media_total.pack(pady=5)

        self.label_total_atendimentos = tk.Label(root, text=f"Total de Atendimentos: {self.total_atendimentos}", font=('Helvetica', 12))
        self.label_total_atendimentos.pack(pady=10)

        # Botão para resetar todos os dados
        self.btn_reset = tk.Button(root, text="Resetar Todos os Dados", command=self.resetar_dados)
        self.btn_reset.pack(pady=10)

        # Atualiza o cronômetro a cada segundo
        self.update_cronometro()

        # Atualizar a interface após carregar os dados
        self.atualizar_interface()

    def iniciar_atendimento(self, chat_index):
        if self.inicio_atendimento[chat_index] != 0:
            messagebox.showwarning("Erro", f"O Chat {chat_index + 1} já está em andamento.")
            return

        self.inicio_atendimento[chat_index] = time.time()
        self.tempo_decorrido[chat_index] = 0  # Reseta o cronômetro
        messagebox.showinfo("Início", f"Atendimento do Chat {chat_index + 1} iniciado.")

    def finalizar_atendimento(self, chat_index):
        if self.inicio_atendimento[chat_index] == 0:
            messagebox.showwarning("Erro", f"O Chat {chat_index + 1} não foi iniciado.")
            return

        fim_atendimento = time.time()
        duracao = fim_atendimento - self.inicio_atendimento[chat_index]
        self.total_tempo += duracao
        self.inicio_atendimento[chat_index] = 0
        self.tempo_decorrido[chat_index] = 0  # Para o cronômetro

        self.total_atendimentos += 1
        self.atualizar_interface()
        self.salvar_dados()  # Salvar dados após finalizar o atendimento
        
        self.chat_frames[chat_index]['label_cronometro'].config(fg='blue')

    def atualizar_interface(self):
        # Calcula e exibe a média de tempo total
        if self.total_atendimentos > 0:
            media_total = self.total_tempo / self.total_atendimentos
            media_hhmmss = self.converter_para_hhmmss(media_total)
            self.label_media_total.config(text=f"Média de Tempo Total: {media_hhmmss}")
        else:
            self.label_media_total.config(text="Média de Tempo Total: 00:00:00")

        # Atualiza o número total de atendimentos
        self.label_total_atendimentos.config(text=f"Total de Atendimentos: {self.total_atendimentos}")

    def resetar_dados(self):
        # Reseta dados de todos os chats e variáveis de total
        self.total_atendimentos = 0
        self.total_tempo = 0
        self.inicio_atendimento = [0, 0, 0]
        self.tempo_decorrido = [0, 0, 0]
        
        # Atualiza a interface e salva os dados
        self.atualizar_interface()
        self.salvar_dados()
        messagebox.showinfo("Reset", "Dados de todos os chats foram resetados com sucesso.")

    def update_cronometro(self):
        # Atualiza o cronômetro de cada chat
        for i in range(3):
            if self.inicio_atendimento[i] != 0:
                self.tempo_decorrido[i] = time.time() - self.inicio_atendimento[i]
                tempo_hhmmss = self.converter_para_hhmmss(self.tempo_decorrido[i])

                # Alteração de cor do tempo de atendimento
                if self.tempo_decorrido[i] > 45 * 60:  # 45 minutos
                    self.chat_frames[i]['label_cronometro'].config(fg='red')
                elif self.tempo_decorrido[i] > 30 * 60:  # 30 minutos
                    self.chat_frames[i]['label_cronometro'].config(fg='#FFA500')
                elif self.tempo_decorrido[i] < 30 * 60:
                    self.chat_frames[i]['label_cronometro'].config(fg='green')
                else:
                    self.chat_frames[i]['label_cronometro'].config(fg='blue')

                self.chat_frames[i]['label_cronometro'].config(text=f"Tempo Decorrido: {tempo_hhmmss}")
            else:
                self.chat_frames[i]['label_cronometro'].config(text=f"Tempo Decorrido: 00:00:00")

        # Chama esta função a cada 1 segundo
        self.root.after(1000, self.update_cronometro)

    def converter_para_hhmmss(self, segundos):
        horas = int(segundos // 3600)
        minutos = int((segundos % 3600) // 60)
        segundos = int(segundos % 60)
        return f"{horas:02}:{minutos:02}:{segundos:02}"

    def salvar_dados(self):
        """Salvar os dados de atendimentos em um arquivo JSON."""
        dados = {
            'total_atendimentos': self.total_atendimentos,
            'total_tempo': self.total_tempo
        }
        with open('dados_atendimentos.json', 'w') as f:
            json.dump(dados, f)
        print("Dados salvos com sucesso.")

    def carregar_dados(self):
        """Carregar os dados de atendimentos de um arquivo JSON, se existir."""
        if os.path.exists('dados_atendimentos.json'):
            with open('dados_atendimentos.json', 'r') as f:
                dados = json.load(f)
                self.total_atendimentos = dados.get('total_atendimentos', 0)
                self.total_tempo = dados.get('total_tempo', 0)
            print("Dados carregados com sucesso.")
        else:
            print("Nenhum dado anterior encontrado.")

# Inicializa a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
