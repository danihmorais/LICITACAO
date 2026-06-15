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
      console.error(response.status, errText);
    }
    
    return response.ok;
  } catch (error) {
    console.error(error);
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
      console.error(response.status, errText);
    }
    
    return response.ok;
  } catch (error) {
    console.error(error);
    return false;
  }
}

export async function gerarTextoGemini(prompt: string, apiKey: string, model: string = "gemini-2.5-flash"): Promise<any> {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;
  
  const response = await fetch(url, {
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

  if (!response.ok) {
    const errorData = await response.text();
    throw new Error(`Erro na API do Gemini (HTTP ${response.status}): ${errorData}`);
  }

  const data = await response.json();
  
  try {
    let textoFinal = data.candidates[0].content.parts[0].text;
    const inicioJSON = textoFinal.indexOf('{');
    const fimJSON = textoFinal.lastIndexOf('}');
    
    if (inicioJSON !== -1 && fimJSON !== -1) {
      textoFinal = textoFinal.substring(inicioJSON, fimJSON + 1);
    }
    
    return JSON.parse(textoFinal);
  } catch (err) {
    throw new Error("Resposta inesperada da API do Gemini. Estrutura de dados ou JSON inválidos.");
  }
}

export async function gerarTextoOpenRouter(prompt: string, apiKey: string, model: string = "openrouter/free"): Promise<any> {
  const url = "https://openrouter.ai/api/v1/chat/completions";

  const response = await fetch(url, {
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

  if (!response.ok) {
    const errorData = await response.text();
    throw new Error(`Erro na API do OpenRouter (HTTP ${response.status}): ${errorData}`);
  }

  const data = await response.json();

  if (!data.choices || !data.choices[0] || !data.choices[0].message) {
    throw new Error("Resposta vazia ou bloqueada pela OpenRouter. Verifique o limite de requisições gratuitas.");
  }

  try {
    let textoFinal = data.choices[0].message.content;
    const inicioJSON = textoFinal.indexOf('{');
    const fimJSON = textoFinal.lastIndexOf('}');
    
    if (inicioJSON !== -1 && fimJSON !== -1) {
      textoFinal = textoFinal.substring(inicioJSON, fimJSON + 1);
    }
    
    return JSON.parse(textoFinal);
  } catch (err) {
    throw new Error("Resposta inesperada da API do OpenRouter. Estrutura de dados ou JSON inválidos.");
  }
}