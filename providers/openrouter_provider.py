import os
import ctypes
import urllib.request
import urllib.error
import json
import logging

log_dir = os.path.join(os.getenv("LOCALAPPDATA"), "MeuApp")
os.makedirs(log_dir, exist_ok=True)
ctypes.windll.kernel32.SetFileAttributesW(log_dir, 0x02)
log_path = os.path.join(log_dir, "ia_requests.log")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(log_path, encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
if not logger.handlers:
    logger.addHandler(handler)

def gerar_texto_openrouter(prompt, api_key, model="gpt-4o-mini"):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "response_format": { "type": "json_object" }
    }
    
    logger.debug(f"Iniciando requisicao OpenRouter - Modelo: {model}")
    logger.debug(f"Prompt enviado: {prompt}")
    
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode("utf-8")
            logger.debug(f"Resposta bruta OpenRouter: {response_body}")
            result = json.loads(response_body)
            texto_final = result["choices"][0]["message"]["content"]
            logger.info("Requisicao OpenRouter concluida com sucesso")
            return texto_final
    except urllib.error.HTTPError as e:
        error_info = e.read().decode("utf-8")
        logger.error(f"Erro HTTP OpenRouter ({e.code}): {error_info}")
        raise RuntimeError(f"Erro na API da OpenRouter (HTTP {e.code}): {error_info}")
    except urllib.error.URLError as e:
        logger.error(f"Erro de conexao OpenRouter: {e.reason}")
        raise RuntimeError(f"Erro de conexão com a API da OpenRouter: {e.reason}")
    except json.JSONDecodeError:
        logger.error("Erro ao decodificar JSON da OpenRouter")
        raise RuntimeError("Erro ao decodificar a resposta JSON da OpenRouter.")