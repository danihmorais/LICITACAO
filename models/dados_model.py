import json
import os
import logging
import config


class DadosModel:
    def __init__(self):
        self.arquivo = config.ARQUIVO_DADOS
        self.dados = self.carregar()

    def carregar(self):
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, "r", encoding="utf-8") as f:
                    dados = json.load(f)

                gestores = dados.get("gestores", [])
                dados["gestores"] = [
                    g if isinstance(g, dict)
                    else {"nome": g.split(" | ")[0].strip(), "cargo": g.split(" | ")[1].strip()}
                    if " | " in g else {"nome": g, "cargo": ""}
                    for g in gestores
                ]

                fiscais = dados.get("fiscais", [])
                dados["fiscais"] = [
                    f if isinstance(f, dict)
                    else {"nome": f.split(" | ")[0].strip(), "cargo": f.split(" | ")[1].strip()}
                    if " | " in f else {"nome": f, "cargo": ""}
                    for f in fiscais
                ]

                dados.setdefault("contatos_secretarias", {})
                return dados
            except json.JSONDecodeError as erro:
                logging.error(f"Erro ao decodificar {self.arquivo}: {erro}")
            except OSError as erro:
                logging.error(f"Erro ao abrir {self.arquivo}: {erro}")
            except Exception as erro:
                logging.error(f"Erro inesperado ao carregar dados: {erro}")
        return {
            "gestores": [],
            "fiscais": [],
            "contatos_secretarias": {}
        }

    def salvar(self):
        # FIX #15 — salvar() agora captura erros de I/O e serialização em vez
        # de propagar exceções não tratadas para a UI, causando crash silencioso.
        try:
            os.makedirs(os.path.dirname(self.arquivo), exist_ok=True)
            # Serializa primeiro em memória para detectar erros antes de abrir o arquivo.
            conteudo = json.dumps(self.dados, indent=4, ensure_ascii=False)
            with open(self.arquivo, "w", encoding="utf-8") as f:
                f.write(conteudo)
        except (OSError, TypeError, ValueError) as e:
            logging.error(f"Erro ao salvar dados em {self.arquivo}: {e}")

    def adicionar_gestor(self, nome, cargo):
        if not nome or not cargo:
            return None
        novo = {"nome": nome, "cargo": cargo}
        gestores = self.dados.setdefault("gestores", [])
        existe = any(g.get("nome") == nome and g.get("cargo") == cargo for g in gestores)
        if not existe:
            gestores.append(novo)
            self.salvar()
            return novo
        return None

    def adicionar_fiscal(self, nome, cargo):
        if not nome or not cargo:
            return None
        novo = {"nome": nome, "cargo": cargo}
        fiscais = self.dados.setdefault("fiscais", [])
        existe = any(f.get("nome") == nome and f.get("cargo") == cargo for f in fiscais)
        if not existe:
            fiscais.append(novo)
            self.salvar()
            return novo
        return None

    def adicionar_contato_secretaria(self, secretaria: str, email: str, telefone: str):
        if not secretaria:
            return None
        contatos = self.dados.setdefault("contatos_secretarias", {})
        lista = contatos.setdefault(secretaria, [])
        novo = {"email": email, "tel": telefone}
        if novo not in lista:
            lista.append(novo)
            self.salvar()
            return novo
        return None

    def remover_contato_secretaria(self, secretaria: str, email: str, telefone: str):
        contatos = self.dados.get("contatos_secretarias", {})
        lista = contatos.get(secretaria, [])
        contatos[secretaria] = [
            c for c in lista
            if not (isinstance(c, dict) and c.get("email") == email and c.get("tel") == telefone)
        ]
        self.salvar()
