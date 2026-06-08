import sys
import json
import os
from datetime import datetime
import traceback
from montador_variaveis import montar_variaveis_fixas, filtrar_chaves_docx
from processador_docx import modificar_documento, extrair_placeholders_modelos

def _valor_vazio(valor):
    if valor is None:
        return True
    texto_lower = str(valor).strip().lower()
    return not texto_lower or texto_lower in [
        "não informado", "nã£o informado", "n?o informado",
        "nao informado", "[não informado]", "[nao informado]", "[n?o informado]"
    ]

def processar():
    try:
        input_data = sys.stdin.read()
        if not input_data:
            return

        payload = json.loads(input_data)
        acao = payload.get("acao")

        if acao == "salvar_documentos":
            dados_ia = payload.get("dados_ia", {})
            dados_usuario = payload.get("dados_usuario", {})
            preenchimentos_manuais = payload.get("preenchimentos_manuais", {})
            pasta_saida = payload.get("pasta_saida", "saida")
            pasta_modelos = payload.get("pasta_modelos", "modelos")
            arquivos_base = payload.get("arquivos_base", [])

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
                val1, val2 = modificacoes.get(chave1), modificacoes.get(chave2)
                vazio1, vazio2 = _valor_vazio(val1), _valor_vazio(val2)
                if not vazio1 and vazio2:
                    modificacoes[chave2] = val1
                elif not vazio2 and vazio1:
                    modificacoes[chave1] = val2

            if _valor_vazio(modificacoes.get("{{MES_INICIO}}")):
                modificacoes["{{MES_INICIO}}"] = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"][datetime.now().month - 1]

            itens_json = modificacoes.get("{{ITENS}}")
            if not _valor_vazio(itens_json):
                try:
                    itens = json.loads(itens_json) if isinstance(itens_json, str) else itens_json
                    colunas_remover = {"Vlr Unit. (R$)", "Vlr Unit", "Valor Unitário", "Valor Unitario", "Total", "Valor Total"}
                    modificacoes["{{ITENS_SEMVALOR}}"] = json.dumps([{k: v for k, v in item.items() if k not in colunas_remover} for item in itens], ensure_ascii=False)
                except Exception:
                    modificacoes["{{ITENS_SEMVALOR}}"] = ""

            modificacoes.update(preenchimentos_manuais)

            placeholders_modelos = set()
            for arquivo in arquivos_base:
                caminho = os.path.join(pasta_modelos, arquivo)
                if os.path.exists(caminho):
                    placeholders_modelos.update(extrair_placeholders_modelos(pasta_modelos, [arquivo]))

            for ph in placeholders_modelos:
                if ph not in modificacoes or _valor_vazio(modificacoes.get(ph)):
                    modificacoes[ph] = "" if ph in {"{{PRORROGA_CLAUS}}"} else "[Não informado]"

            os.makedirs(pasta_saida, exist_ok=True)
            arquivos_gerados = []

            for arq in arquivos_base:
                cam_origem = os.path.join(pasta_modelos, arq)
                cam_destino = os.path.join(pasta_saida, f"Pronto_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{arq}")
                if os.path.exists(cam_origem):
                    modificar_documento(cam_origem, cam_destino, modificacoes)
                    arquivos_gerados.append(cam_destino)

            print(json.dumps({"sucesso": True, "arquivos": arquivos_gerados}))

    except Exception as e:
        print(json.dumps({"sucesso": False, "erro": str(e), "traceback": traceback.format_exc()}))

if __name__ == "__main__":
    processar()