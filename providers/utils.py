import json
import re

def extrair_json(texto):
    texto = texto.strip()
    padrao = "`" * 3 + r"(?:json)?\s*([\s\S]*?)\s*" + "`" * 3
    match = re.search(padrao, texto)
    if match:
        texto = match.group(1).strip()
    
    try:
        return json.loads(texto)
    except json.JSONDecodeError as e:
        inicio = texto.find('{')
        fim = texto.rfind('}')
        if inicio != -1 and fim != -1:
            try:
                return json.loads(texto[inicio:fim+1])
            except Exception:
                pass
        raise ValueError(f"O modelo de IA não retornou um formato de dados válido. Resposta bruta cortada:\n{texto[:200]}...") from e