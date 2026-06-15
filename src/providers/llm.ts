import { writeTextFile, exists, mkdir, BaseDirectory } from '@tauri-apps/plugin-fs';

async function salvarLogErro(prefixo: string, erro: any, dadosCrus: any = null) {
  try {
    const logsDirExists = await exists("logs", { baseDir: BaseDirectory.AppData });
    if (!logsDirExists) {
      await mkdir("logs", { baseDir: BaseDirectory.AppData, recursive: true });
    }

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `logs/${prefixo}-${timestamp}.txt`;

    let conteudo = `=== ERRO REGISTRADO ===\nData: ${new Date().toISOString()}\n\n`;
    conteudo += `MENSAGEM DE ERRO:\n${erro instanceof Error ? erro.message : String(erro)}\n\n`;
    
    if (erro instanceof Error && erro.stack) {
      conteudo += `STACK TRACE:\n${erro.stack}\n\n`;
    }

    if (dadosCrus) {
      conteudo += `DADOS RECEBIDOS DA API (RAW):\n${typeof dadosCrus === 'string' ? dadosCrus : JSON.stringify(dadosCrus, null, 2)}\n`;
    }

    await writeTextFile(filename, conteudo, { baseDir: BaseDirectory.AppData });
    console.log(`Log de erro salvo em: AppData/logs/${filename}`);
  } catch (e) {
    console.error("Falha crítica ao tentar salvar log de erro no disco:", e);
  }
}

export async function validarChaveGemini(apiKey: string): Promise<boolean> {
  try {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`;
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        contents: [{ parts: [{ text: "teste" }] }],
        generationConfig: {
          maxOutputTokens: 1
        }
      })
    });
    
    if (!response.ok) {
      const errText = await response.text();
      await salvarLogErro("validacao-gemini", `HTTP ${response.status}`, errText);
    }
    
    return response.ok;
  } catch (error) {
    await salvarLogErro("excecao-validacao-gemini", error);
    return false;
  }
}

export async function validarChaveOpenRouter(apiKey: string): Promise<boolean> {
  try {
    const url = "https://openrouter.ai/api/v1/chat/completions";
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "openrouter/free",
        max_tokens: 1,
        messages: [{ role: "user", content: "teste" }]
      })
    });
    
    if (!response.ok) {
      const errText = await response.text();
      await salvarLogErro("validacao-openrouter", `HTTP ${response.status}`, errText);
    }
    
    return response.ok;
  } catch (error) {
    await salvarLogErro("excecao-validacao-openrouter", error);
    return false;
  }
}

export async function gerarTextoGemini(prompt: string, apiKey: string, model: string = "gemini-2.5-flash"): Promise<any> {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;
  
  let response;
  try {
    response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: {
          temperature: 0.3,
          maxOutputTokens: 8192,
          responseMimeType: "application/json"
        }
      })
    });
  } catch (networkError) {
    await salvarLogErro("gemini-network-error", networkError);
    throw new Error("Falha de rede ao conectar com a API do Gemini.");
  }

  if (!response.ok) {
    const errorData = await response.text();
    await salvarLogErro("gemini-http-error", `HTTP ${response.status}`, errorData);
    throw new Error(`Erro na API do Gemini (HTTP ${response.status}): ${errorData}`);
  }

  let data;
  try {
    data = await response.json();
  } catch (jsonError) {
    const rawText = await response.text();
    await salvarLogErro("gemini-response-not-json", jsonError, rawText);
    throw new Error("A API do Gemini não retornou um JSON válido na camada HTTP.");
  }
  
  let rawText = "";
  try {
    rawText = data.candidates[0].content.parts[0].text;
    let textoFinal = rawText;
    const inicioJSON = textoFinal.indexOf('{');
    const fimJSON = textoFinal.lastIndexOf('}');
    
    if (inicioJSON !== -1 && fimJSON !== -1) {
      textoFinal = textoFinal.substring(inicioJSON, fimJSON + 1);
    }
    
    return JSON.parse(textoFinal);
  } catch (err) {
    await salvarLogErro("gemini-parse-error", err, rawText || data);
    throw new Error("Resposta inesperada da API do Gemini. Estrutura de dados ou JSON inválidos.");
  }
}

export async function gerarTextoOpenRouter(prompt: string, apiKey: string, model: string = "openrouter/free"): Promise<any> {
  const url = "https://openrouter.ai/api/v1/chat/completions";

  let response;
  try {
    response = await fetch(url, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: model,
        temperature: 0.3,
        max_tokens: 8000,
        messages: [{ role: "user", content: prompt }]
      })
    });
  } catch (networkError) {
    await salvarLogErro("openrouter-network-error", networkError);
    throw new Error("Falha de rede ao conectar com a API do OpenRouter.");
  }

  if (!response.ok) {
    const errorData = await response.text();
    await salvarLogErro("openrouter-http-error", `HTTP ${response.status}`, errorData);
    throw new Error(`Erro na API do OpenRouter (HTTP ${response.status}): ${errorData}`);
  }

  let data;
  try {
    data = await response.json();
  } catch (jsonError) {
    const rawText = await response.text();
    await salvarLogErro("openrouter-response-not-json", jsonError, rawText);
    throw new Error("A API do OpenRouter não retornou um JSON válido na camada HTTP.");
  }

  if (!data.choices || !data.choices[0] || !data.choices[0].message) {
    await salvarLogErro("openrouter-empty-choices", "A resposta da API veio sem choices ou message", data);
    throw new Error("Resposta vazia ou bloqueada pela OpenRouter. Verifique o limite de requisições gratuitas.");
  }

  let rawText = "";
  try {
    rawText = data.choices[0].message.content;
    let textoFinal = rawText;
    const inicioJSON = textoFinal.indexOf('{');
    const fimJSON = textoFinal.lastIndexOf('}');
    
    if (inicioJSON !== -1 && fimJSON !== -1) {
      textoFinal = textoFinal.substring(inicioJSON, fimJSON + 1);
    }
    
    return JSON.parse(textoFinal);
  } catch (err) {
    await salvarLogErro("openrouter-parse-error", err, rawText || data);
    throw new Error("Resposta inesperada da API do OpenRouter. Estrutura de dados ou JSON inválidos.");
  }
}