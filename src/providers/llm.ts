export async function validarChaveGemini(apiKey: string): Promise<boolean> {
  try {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;
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
    return response.ok;
  } catch {
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
        model: "openai/gpt-4o-mini",
        max_tokens: 1,
        messages: [{ role: "user", content: "teste" }]
      })
    });
    return response.ok;
  } catch {
    return false;
  }
}

export async function gerarTextoGemini(prompt: string, apiKey: string, model: string = "gemini-1.5-flash"): Promise<any> {
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
    textoFinal = textoFinal.replace(/```json/gi, "").replace(/```/g, "").trim();
    return JSON.parse(textoFinal);
  } catch (err) {
    throw new Error("Resposta inesperada da API do Gemini. Estrutura de dados ou JSON inválidos.");
  }
}

export async function gerarTextoOpenRouter(prompt: string, apiKey: string, model: string = "openai/gpt-4o"): Promise<any> {
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
      response_format: { type: "json_object" },
      messages: [{ role: "user", content: prompt }]
    })
  });

  if (!response.ok) {
    const errorData = await response.text();
    throw new Error(`Erro na API do OpenRouter (HTTP ${response.status}): ${errorData}`);
  }

  const data = await response.json();

  try {
    let textoFinal = data.choices[0].message.content;
    textoFinal = textoFinal.replace(/```json/gi, "").replace(/```/g, "").trim();
    return JSON.parse(textoFinal);
  } catch (err) {
    throw new Error("Resposta inesperada da API do OpenRouter. Estrutura de dados ou JSON inválidos.");
  }
}