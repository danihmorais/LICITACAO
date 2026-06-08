import React, { useState } from "react";

const SECRETARIAS_DEFAULT = [
  "Gabinete do Prefeito",
  "Secretaria de Administração",
  "Secretaria de Saúde",
  "Secretaria de Educação",
  "Secretaria de Obras e Serviços Públicos",
  "Secretaria de Assistência Social",
  "Secretaria de Finanças"
];

export default function Step3({ dados, atualizarDados }: any) {
  const [emailsTemp, setEmailsTemp] = useState<Record<string, string>>({});
  const [telsTemp, setTelsTemp] = useState<Record<string, string>>({});

  const handleToggleSecretaria = (sec: string) => {
    let novasSecs = [...dados.secretarias];
    if (novasSecs.includes(sec)) {
      novasSecs = novasSecs.filter(s => s !== sec);
      const novosContatos = { ...dados.contatosSecretarias };
      delete novosContatos[sec];
      atualizarDados({ secretarias: novasSecs, contatosSecretarias: novosContatos });
    } else {
      novasSecs.push(sec);
      atualizarDados({ secretarias: novasSecs });
    }
  };

  const handleAddContato = (sec: string) => {
    const email = emailsTemp[sec] || "";
    const tel = telsTemp[sec] || "";
    
    if (!email && !tel) return;

    const atuais = dados.contatosSecretarias[sec] || [];
    atualizarDados({
      contatosSecretarias: {
        ...dados.contatosSecretarias,
        [sec]: [...atuais, { email, tel }]
      }
    });

    setEmailsTemp({ ...emailsTemp, [sec]: "" });
    setTelsTemp({ ...telsTemp, [sec]: "" });
  };

  const handleRemoveContato = (sec: string, index: number) => {
    const atuais = dados.contatosSecretarias[sec] || [];
    const novos = atuais.filter((_: any, i: number) => i !== index);
    atualizarDados({
      contatosSecretarias: {
        ...dados.contatosSecretarias,
        [sec]: novos
      }
    });
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
      <div>
        <h2 style={{ fontSize: "16px", margin: "0 0 8px 0", color: "#111827" }}>
          Secretarias Demandantes <span style={{ color: "#DC2626" }}>*</span>
        </h2>
        <p style={{ color: "#6B7280", margin: 0, fontSize: "13px" }}>Escolha as unidades demandantes e registre os contatos responsáveis por cada uma.</p>
        {dados.secretarias.length === 0 && <span style={{ color: "#DC2626", fontSize: "12px", display: "block", marginTop: "4px" }}>Selecione pelo menos uma secretaria.</span>}
      </div>

      <div style={{ background: "#F9FAFB", border: dados.secretarias.length === 0 ? "1px solid #DC2626" : "1px solid #E5E7EB", borderRadius: "14px", padding: "16px", maxHeight: "230px", overflowY: "auto", display: "flex", flexDirection: "column", gap: "12px" }}>
        {SECRETARIAS_DEFAULT.map((sec) => (
          <label key={sec} style={{ display: "flex", alignItems: "center", gap: "12px", cursor: "pointer", fontSize: "14px", color: "#374151" }}>
            <input 
              type="checkbox" 
              checked={dados.secretarias.includes(sec)} 
              onChange={() => handleToggleSecretaria(sec)} 
              style={{ width: "18px", height: "18px", cursor: "pointer" }}
            />
            {sec}
          </label>
        ))}
      </div>

      {dados.secretarias.length > 0 && (
        <div>
          <h2 style={{ fontSize: "16px", margin: "0 0 16px 0", color: "#111827" }}>Dados de Contato por Secretaria</h2>
          <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
            {dados.secretarias.map((sec: string) => (
              <div key={sec} style={{ background: "white", border: "1px solid #D1D5DB", borderRadius: "12px", padding: "16px" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "16px", flexWrap: "wrap" }}>
                  <strong style={{ fontSize: "14px", color: "#111827", minWidth: "200px" }}>{sec}</strong>
                  <input 
                    type="email" 
                    placeholder="E-mail" 
                    value={emailsTemp[sec] || ""}
                    onChange={(e) => setEmailsTemp({ ...emailsTemp, [sec]: e.target.value })}
                    style={{ width: "180px", padding: "8px", borderRadius: "8px", border: "1px solid #D1D5DB", fontSize: "12px" }} 
                  />
                  <input 
                    type="text" 
                    placeholder="Telefone" 
                    value={telsTemp[sec] || ""}
                    onChange={(e) => setTelsTemp({ ...telsTemp, [sec]: e.target.value })}
                    style={{ width: "140px", padding: "8px", borderRadius: "8px", border: "1px solid #D1D5DB", fontSize: "12px" }} 
                  />
                  <button 
                    onClick={() => handleAddContato(sec)}
                    disabled={!emailsTemp[sec] && !telsTemp[sec]}
                    style={{ padding: "8px 16px", background: (!emailsTemp[sec] && !telsTemp[sec]) ? "#9CA3AF" : "#2563EB", color: "white", border: "none", borderRadius: "8px", fontWeight: "bold", fontSize: "12px", cursor: (!emailsTemp[sec] && !telsTemp[sec]) ? "not-allowed" : "pointer" }}
                  >
                    + Adicionar
                  </button>
                </div>

                <div style={{ background: "#F3F4F6", borderRadius: "8px", border: "1px solid #E5E7EB", padding: "8px", minHeight: "60px", maxHeight: "120px", overflowY: "auto", display: "flex", flexDirection: "column", gap: "4px" }}>
                  {(!dados.contatosSecretarias[sec] || dados.contatosSecretarias[sec].length === 0) && (
                    <div style={{ fontSize: "12px", color: "#9CA3AF", textAlign: "center", padding: "8px" }}>Nenhum contato adicionado</div>
                  )}
                  {(dados.contatosSecretarias[sec] || []).map((contato: any, idx: number) => (
                    <div key={idx} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "white", padding: "6px 12px", borderRadius: "6px", border: "1px solid #D1D5DB" }}>
                      <span style={{ fontSize: "12px", color: "#111827" }}>{contato.email || "—"} | {contato.tel || "—"}</span>
                      <button 
                        onClick={() => handleRemoveContato(sec, idx)}
                        style={{ padding: "4px 8px", background: "#DC2626", color: "white", border: "none", borderRadius: "6px", fontWeight: "bold", fontSize: "11px", cursor: "pointer" }}
                      >
                        Remover
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}