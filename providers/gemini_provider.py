import os
import ctypes
import urllib.request
import urllib.error
import json
import logging
import config


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


def gerar_texto_gemini(prompt, api_key, model=None):
    if model is None:
        model = config.MODEL_GEMINI

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "responseMimeType": "application/json"
        }
    }

    logger.debug(f"Iniciando requisicao Gemini - Modelo: {model}")
    logger.debug(f"Prompt enviado: {prompt}")

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode("utf-8")
            logger.debug(f"Resposta bruta Gemini: {response_body}")
            result = json.loads(response_body)
            try:
                texto_final = result["candidates"][0]["content"]["parts"][0]["text"]
                logger.info("Requisicao Gemini concluida com sucesso")
                return texto_final
            except KeyError:
                logger.error("Estrutura de dados invalida na resposta do Gemini")
                raise RuntimeError("Resposta inesperada da API do Gemini. Estrutura de dados inválida.")
    except urllib.error.HTTPError as e:
        error_info = e.read().decode("utf-8")
        logger.error(f"Erro HTTP Gemini ({e.code}): {error_info}")
        raise RuntimeError(f"Erro na API do Gemini (HTTP {e.code}): {error_info}")
    except urllib.error.URLError as e:
        logger.error(f"Erro de conexao Gemini: {e.reason}")
        raise RuntimeError(f"Erro de conexão com a API do Gemini: {e.reason}")
    except json.JSONDecodeError:
        logger.error("Erro ao decodificar JSON do Gemini")
        raise RuntimeError("Erro ao decodificar a resposta JSON do Gemini.")
