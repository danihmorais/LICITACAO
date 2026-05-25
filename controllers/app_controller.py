import os
import json
import threading
import logging
import urllib.request
import urllib.error
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import config
from models.dados_model import DadosModel
from gerador_ia import processar_dados_ia
from montador_variaveis import montar_variaveis_fixas, filtrar_chaves_docx
from processador_docx import modificar_documento, extrair_placeholders_modelos

PLACEHOLDERS_PODEM_FICAR_VAZIOS = {
    "{{PRORROGA_CLAUS}}",
}

try:
    import keyring
except ImportError:
    keyring = None
log_dir = os.path.join(os.getenv("LOCALAPPDATA"), "MeuApp")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "app.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class AppController:
    def __init__(self):
        self.dados_model = DadosModel()
        self.api_key = ""
        self.provedor = config.DEFAULT_PROVIDER
        self.pasta_saida = os.path.join(
            config.EXECUTABLE_DIR, config.DEFAULT_OUTPUT_FOLDER_NAME
        )
        self.app = None
        self.view = None
        logging.info("Aplicação inicializada.")

    def get_tema_atual(self):
        if os.path.exists(config.ARQUIVO_DADOS):
            try:
                with open(config.ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    return dados.get("tema", "System")
            except Exception:
                return "System"
        return "System"

    def alternar_tema(self, novo_tema):
        ctk.set_appearance_mode(novo_tema)
        dados = {}
        if os.path.exists(config.ARQUIVO_DADOS):
            try:
                with open(config.ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                    dados = json.load(f)
            except Exception:
                pass
        dados["tema"] = novo_tema
        try:
            with open(config.ARQUIVO_DADOS, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=4)
            logging.info(f"Tema alterado e salvo: {novo_tema}")
        except Exception as e:
            logging.error(f"Erro ao salvar o tema no json: {str(e)}")

    def _pasta_base(self):
        return config.BASE_DIR

    def _pasta_modelos(self):
        return config.PASTA_MODELOS

    def placeholders_modelos(self):
        pasta = self._pasta_modelos()
        if not os.path.exists(pasta):
            logging.warning(f"Pasta de modelos não encontrada: {pasta}")
            return set()
        arquivos = [f for f in os.listdir(pasta) if f.endswith(".docx")]
        return extrair_placeholders_modelos(pasta, arquivos)

    def _valor_vazio(self, valor):
        if valor is None:
            return True
        texto = str(valor).strip()
        if not texto:
            return True
        texto_lower = texto.lower()
        vazio_por_texto = (
            "não informado" in texto_lower
            or "nã£o informado" in texto_lower
            or "n?o informado" in texto_lower
            or "nao informado" in texto_lower
            or texto_lower == "[não informado]"
            or texto_lower == "[nao informado]"
            or texto_lower == "[n?o informado]"
        )
        return vazio_por_texto

    def _mes_atual_extenso(self):
        meses = [
            "janeiro", "fevereiro", "março", "abril", "maio", "junho",
            "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
        ]
        return meses[datetime.now().month - 1]

    def montar_modificacoes_preliminares(self, dados_ia, dados_usuario):
        modificacoes = filtrar_chaves_docx(montar_variaveis_fixas(dados_usuario))

        for chave, valor in dados_ia.items():
            chave_docx = chave if chave.startswith("{{") and chave.endswith("}}") else f"{{{{{chave}}}}}"
            modificacoes[chave_docx] = valor

        aliases = [
            ("{{ESTIMATIVA}}", "{{ESTIMATIVA_QUANTIDADES}}"),
            ("{{RESULTADOS}}", "{{RESULTADOS_ESPERADOS}}"),
            ("{{OBRIG_CONTRATADA}}", "{{OBRIGACOES_CONTRATADA}}"),
            ("{{SOLUCAO}}", "{{ESPECIFICACAO_TECNICA}}"),
            ("{{PARCELAMENTO}}", "{{CRITERIOS_JUSTIFICATIVA_ETP}}"),
            ("{{IMPAC_AMB}}", "{{CRITERIOS_SUSTENTABILIDADE}}"),
        ]

        for chave1, chave2 in aliases:
            val1 = modificacoes.get(chave1)
            val2 = modificacoes.get(chave2)
            vazio1 = self._valor_vazio(val1)
            vazio2 = self._valor_vazio(val2)

            if not vazio1 and vazio2:
                modificacoes[chave2] = val1
            elif not vazio2 and vazio1:
                modificacoes[chave1] = val2
            elif vazio1 and vazio2:
                logging.warning(
                    f"Alias sem valor disponível: '{chave1}' e '{chave2}' estão ambos vazios."
                )

        if self._valor_vazio(modificacoes.get("{{MES_INICIO}}")):
            modificacoes["{{MES_INICIO}}"] = self._mes_atual_extenso()
        if not self._valor_vazio(modificacoes.get("{{ITENS}}")):
            try:
                itens_json = modificacoes["{{ITENS}}"]

                if isinstance(itens_json, str):
                    itens = json.loads(itens_json)
                else:
                    itens = itens_json

                colunas_remover = {
                    "Vlr Unit. (R$)",
                    "Vlr Unit",
                    "Valor Unitário",
                    "Valor Unitario",
                    "Total",
                    "Valor Total",
                }

                itens_sem_valor = []

                for item in itens:
                    novo_item = {
                        k: v
                        for k, v in item.items()
                        if k not in colunas_remover
                    }
                    itens_sem_valor.append(novo_item)

                modificacoes["{{ITENS_SEMVALOR}}"] = json.dumps(
                    itens_sem_valor,
                    ensure_ascii=False
                )

            except Exception as e:
                logging.error(
                    f"Erro ao gerar {{ITENS_SEMVALOR}}: {str(e)}",
                    exc_info=True
                )
                modificacoes["{{ITENS_SEMVALOR}}"] = ""

        return modificacoes

    def placeholders_pendentes(self, modificacoes):
        return sorted(
            chave for chave in self.placeholders_modelos()
            if chave not in PLACEHOLDERS_PODEM_FICAR_VAZIOS
            and self._valor_vazio(modificacoes.get(chave))
        )

    def iniciar(self):
        logging.info("Iniciando interface gráfica da aplicação.")
        self.app = ctk.CTk()
        self.app.title(config.APP_NAME)
        self.app.geometry("1000x800")
        self.app.minsize(850, 700)
        self.app.after(100, lambda: self.app.state("zoomed"))

        icon_path = os.path.join(config.BASE_DIR, "assets", "logo.ico")
        if os.path.exists(icon_path):
            try:
                self.app.iconbitmap(icon_path)
            except Exception as e:
                logging.warning(f"Não foi possível carregar o ícone: {str(e)}")

        from views.login_view import LoginView
        self.view = LoginView(self.app, self)
        self.view.pack(fill="both", expand=True)
        self.app.mainloop()

    def carregar_chave_keyring(self, provedor):
        if keyring is None:
            logging.warning("Módulo keyring não está disponível.")
            return None
        try:
            chave = keyring.get_password(config.APP_NAME, provedor)
            if chave:
                logging.info(f"Chave carregada do keyring para o provedor: {provedor}")
            return chave
        except Exception as e:
            logging.error(f"Erro ao carregar chave do keyring: {str(e)}")
            return None

    def salvar_chave_keyring(self, provedor, key):
        if keyring is None:
            return
        try:
            keyring.set_password(config.APP_NAME, provedor, key)
            logging.info(f"Chave salva no keyring para o provedor: {provedor}")
        except Exception as e:
            logging.error(f"Erro ao salvar chave no keyring: {str(e)}")

    def validar_chave_api(self, provedor, chave):
        chave_limpa = chave.strip()
        logging.info(f"Iniciando validação de chave na API para o provedor: {provedor}")

        if provedor == "openrouter":
            url = "https://openrouter.ai/api/v1/models"
            req = urllib.request.Request(url)
        elif provedor == "gemini":
            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={chave_limpa}"
            req = urllib.request.Request(url)
        else:
            logging.error(f"Provedor desconhecido durante validação: {provedor}")
            return False, "Provedor desconhecido."

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() == 200:
                    logging.info(f"Chave do provedor {provedor} validada com sucesso via API.")
                    return True, "Chave válida."
        except urllib.error.HTTPError as e:
            erro_msg = f"Acesso negado (HTTP {e.code}). Verifique a chave."
            logging.warning(f"Falha na validação HTTP ({provedor}): {e.code} - {e.reason}")
            if e.code in [400, 401, 403]:
                return False, erro_msg
            else:
                return False, f"Erro no provedor (HTTP {e.code})."
        except urllib.error.URLError as e:
            logging.error(f"Erro de conexão ao validar chave ({provedor}): {e.reason}")
            return False, "Erro de conexão com a internet."
        except Exception as e:
            logging.error(f"Erro inesperado ao validar chave ({provedor}): {str(e)}")
            return False, f"Erro inesperado: {str(e)}"

        return False, "Erro desconhecido na validação."

    def realizar_login(self, provedor, chave):
        logging.info(f"Tentativa de login iniciada para o provedor: {provedor}")
        if not chave:
            logging.warning("Tentativa de login falhou: Chave de API vazia.")
            messagebox.showwarning("Autenticação Necessária", "Insira a chave de API para continuar.")
            return False

        try:
            self.app.config(cursor="watch")
            self.app.update()
        except Exception:
            pass

        valida, mensagem = self.validar_chave_api(provedor, chave)

        try:
            self.app.config(cursor="")
        except Exception:
            pass

        if not valida:
            logging.warning(f"Login bloqueado. Motivo: {mensagem}")
            messagebox.showerror("Erro de Autenticação", f"Não foi possível validar a chave.\nMotivo: {mensagem}")
            return False

        self.salvar_chave_keyring(provedor, chave)

        try:
            dados = {}
            if os.path.exists(config.ARQUIVO_DADOS):
                with open(config.ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                    dados = json.load(f)
            dados["ultimo_provedor"] = provedor
            with open(config.ARQUIVO_DADOS, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=4)
            logging.info("Provedor salvo no arquivo JSON de configurações.")
        except Exception as e:
            logging.error(f"Erro ao salvar o provedor no json: {str(e)}")

        self.api_key = chave
        self.provedor = provedor

        logging.info("Login finalizado com sucesso. Redirecionando para o WizardView.")

        self.view.pack_forget()
        from views.wizard_view import WizardView
        self.view = WizardView(self.app, self)
        self.view.pack(fill="both", expand=True)
        return True

    def executar_geracao(self, dados_usuario, meepp_exclusivo, progresso_callback, fim_callback, erro_callback):
        logging.info(f"Iniciando thread de processamento da IA. Objeto: {dados_usuario.get('{{OBJETO}}', 'Não informado')}")
        threading.Thread(
            target=self._processar_thread,
            args=(dados_usuario, meepp_exclusivo, progresso_callback, fim_callback, erro_callback),
            daemon=True
        ).start()

    def _processar_thread(self, dados_usuario, meepp_exclusivo, progresso_callback, fim_callback, erro_callback):
        try:
            dados_ia = {}
            etapas_ia = [
                ("DFD", "Processando Documento de Formalização de Demanda (DFD)..."),
                ("ETP", "Analisando e gerando Estudo Técnico Preliminar (ETP)..."),
                ("TR", "Estruturando Termo de Referência (TR)..."),
            ]

            for etapa, mensagem in etapas_ia:
                progresso_callback(mensagem)
                logging.info(f"Solicitando geração da etapa IA: {etapa}")
                etapa_dados = processar_dados_ia(
                    dados_usuario, self.api_key, self.provedor, meepp_exclusivo, etapa
                )
                dados_ia.update(etapa_dados)
                logging.info(f"Etapa {etapa} concluída com sucesso.")

            progresso_callback("Consolidando artefatos e revisando resultados...")
            logging.info("Processamento de IA finalizado sem erros.")
            fim_callback(dados_ia, dados_usuario)

        except Exception as e:
            logging.error(f"Erro severo durante o processamento da IA: {str(e)}", exc_info=True)
            erro_callback(str(e))

    def salvar_documentos(self, dados_ia, dados_usuario, preenchimentos_manuais=None):
        logging.info("Iniciando rotina de salvamento de documentos.")
        modificacoes = self.montar_modificacoes_preliminares(dados_ia, dados_usuario)
        if preenchimentos_manuais:
            modificacoes.update(preenchimentos_manuais)

        pendentes = self.placeholders_pendentes(modificacoes)
        if pendentes:
            msg_erro = "Ainda existem campos obrigatórios sem preenchimento: " + ", ".join(pendentes)
            logging.error(msg_erro)
            raise ValueError(msg_erro)

        todos_placeholders = self.placeholders_modelos()
        for ph in todos_placeholders:
            if ph not in modificacoes or self._valor_vazio(modificacoes.get(ph)):
                modificacoes[ph] = "" if ph in PLACEHOLDERS_PODEM_FICAR_VAZIOS else "[Não informado]"

        pasta_modelos = self._pasta_modelos()
        if not os.path.exists(self.pasta_saida):
            os.makedirs(self.pasta_saida, exist_ok=True)
            logging.info(f"Pasta de saída criada: {self.pasta_saida}")

        arquivos_base = config.BASE_FILES
        arquivos_gerados = []
        for arq in arquivos_base:
            cam_origem = os.path.join(pasta_modelos, arq)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            cam_destino = os.path.join(self.pasta_saida, f"Pronto_{timestamp}_{arq}")

            if not os.path.exists(cam_origem):
                logging.error(f"Modelo não encontrado para modificação: {cam_origem}")
                continue

            try:
                modificar_documento(cam_origem, cam_destino, modificacoes)
                arquivos_gerados.append(cam_destino)
                logging.info(f"Documento salvo com sucesso: {cam_destino}")
            except Exception as e:
                logging.error(f"Erro ao modificar documento {cam_origem}: {str(e)}", exc_info=True)

        logging.info(
            f"Lote de artefatos concluído com êxito. "
            f"Secretaria: {dados_usuario.get('{{SECRETARIA}}', '')} | "
            f"Vigência: {dados_usuario.get('{{VIGENCIA}}', '')} | "
            f"Instrumento: {dados_usuario.get('{{INSTRUMENTO}}', '')}"
        )
        return self.pasta_saida