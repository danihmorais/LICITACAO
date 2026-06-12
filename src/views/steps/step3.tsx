import React, { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/core";

const SECRETARIAS_DEFAULT = [
  "Gabinete do Prefeito",
  "Fundo Social de Solidariedade",
  "Secretaria de Administração",
  "Secretaria de Educação, Cultura, Esporte e Lazer",
  "Secretaria de Desenvolvimento e Promoção Social",
  "Secretaria de Saúde",
  "Secretaria de Obras e Serviços Públicos",
  "Secretaria de Agricultura, Meio Ambiente, Industria e Comércio",
];

export default function Step3({ dados = { secretarias: [], contatosSecretarias: {} }, atualizarDados }: any) {
  const [emailsTemp, setEmailsTemp] = useState<Record<string, string>>({});
  const [telsTemp, setTelsTemp] = useState<Record<string, string>>({});
  const [contatosSalvos, setContatosSalvos] = useState<any[]>([]);
  const [modalSecAberto, setModalSecAberto] = useState<string | null>(null);

  const secretarias = dados.secretarias || [];
  const contatosSecretarias = dados.contatosSecretarias || {};

  const secretariasStr = JSON.stringify(secretarias);
  const contatosStr = JSON.stringify(contatosSecretarias);

  useEffect(() => {
    invoke("ler_dados_usuario").then((dadosSalvos: any) => {
      if (dadosSalvos && dadosSalvos.contatos_salvos) {
        setContatosSalvos(dadosSalvos.contatos_salvos);
      }
    }).catch(console.error);
  }, []);

  const salvarContatosNoBackend = async (novosContatos: any[]) => {
    try {
      const dados_usuario: any = await invoke("ler_dados_usuario") || {};
      dados_usuario.contatos_salvos = novosContatos;
      await invoke("salvar_dados_usuario", { dados: dados_usuario });
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    const isValido = secretarias.length > 0 && secretarias.every((sec: string) => contatosSecretarias[sec] && contatosSecretarias[sec].length > 0);
    if (dados.step3Valido !== isValido) {
      atualizarDados({ ...dados, step3Valido: isValido });
    }
  }, [secretariasStr, contatosStr, dados.step3Valido]);

  const handleToggleSecretaria = (sec: string) => {
    let novasSecs = [...secretarias];
    let novosContatos = { ...contatosSecretarias };

    if (novasSecs.includes(sec)) {
      novasSecs = novasSecs.filter(s => s !== sec);
      delete novosContatos[sec];
    } else {
      novasSecs.push(sec);
    }

    atualizarDados({ 
      ...dados, 
      secretarias: novasSecs, 
      contatosSecretarias: novosContatos
    });
  };

  const handleAddContato = (sec: string) => {
    const email = emailsTemp[sec] || "";
    const tel = telsTemp[sec] || "";
    
    if (!email && !tel) return;

    const atuais = contatosSecretarias[sec] || [];
    const novosContatos = { ...contatosSecretarias, [sec]: [...atuais, { email, tel }] };

    atualizarDados({ ...dados, contatosSecretarias: novosContatos });
    setEmailsTemp({ ...emailsTemp, [sec]: "" });
    setTelsTemp({ ...telsTemp, [sec]: "" });
  };

  const handleRemoveContato = (sec: string, index: number) => {
    const atuais = contatosSecretarias[sec] || [];
    const novos = atuais.filter((_: any, i: number) => i !== index);
    const novosContatos = { ...contatosSecretarias, [sec]: novos };
    atualizarDados({ ...dados, contatosSecretarias: novosContatos });
  };

  const handleSalvarContatoIndiv = (contato: any) => {
    const jaExiste = contatosSalvos.some(c => c.email === contato.email && c.tel === contato.tel);
    
    if (jaExiste) {
      alert("Este contato já está salvo na sua lista.");
      return;
    }

    const novosSalvos = [...contatosSalvos, contato];
    setContatosSalvos(novosSalvos);
    salvarContatosNoBackend(novosSalvos);
    alert("Contato salvo com sucesso!");
  };

  const handleUsarContatoSalvo = (sec: string, contato: any) => {
    const atuais = contatosSecretarias[sec] || [];
    const novosContatos = { ...contatosSecretarias, [sec]: [...atuais, contato] };
    atualizarDados({ ...dados, contatosSecretarias: novosContatos });
    setModalSecAberto(null);
  };

  const handleRemoverContatoSalvo = (index: number) => {
    const novosSalvos = contatosSalvos.filter((_, i) => i !== index);
    setContatosSalvos(novosSalvos);
    salvarContatosNoBackend(novosSalvos);
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
      <div>
        <h2 style={{ fontSize: "16px", margin: "0 0 8px 0", color: "#111827" }}>
          Secretarias Demandantes <span style={{ color: "#DC2626" }}>*</span>
        </h2>
        <p style={{ color: "#6B7280", margin: 0, fontSize: "13px" }}>Escolha as unidades demandantes e registre os contatos responsáveis por cada uma.</p>
        {secretarias.length === 0 && <span style={{ color: "#DC2626", fontSize: "12px", display: "block", marginTop: "4px", fontWeight: "bold" }}>Selecione pelo menos uma secretaria.</span>}
      </div>

      <div style={{ background: "#F9FAFB", border: secretarias.length === 0 ? "1px solid #DC2626" : "1px solid #E5E7EB", borderRadius: "14px", padding: "16px", display: "flex", flexDirection: "column", gap: "12px" }}>
        {SECRETARIAS_DEFAULT.map((sec) => (
          <label key={sec} style={{ display: "flex", alignItems: "center", gap: "12px", cursor: "pointer", fontSize: "14px", color: "#374151" }}>
            <input 
              type="checkbox" 
              checked={secretarias.includes(sec)} 
              onChange={() => handleToggleSecretaria(sec)} 
              style={{ width: "18px", height: "18px", cursor: "pointer" }}
            />
            {sec}
          </label>
        ))}
      </div>

      {secretarias.length > 0 && (
        <div>
          <h2 style={{ fontSize: "16px", margin: "0 0 16px 0", color: "#111827" }}>Dados de Contato por Secretaria</h2>
          <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
            {secretarias.map((sec: string) => {
              const contatos = contatosSecretarias[sec] || [];
              const faltaContato = contatos.length === 0;

              return (
                <div key={sec} style={{ background: "white", border: faltaContato ? "1px solid #DC2626" : "1px solid #D1D5DB", borderRadius: "12px", padding: "16px" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "16px", flexWrap: "wrap" }}>
                    <strong style={{ fontSize: "14px", color: "#111827", minWidth: "150px" }}>{sec}</strong>
                    <input 
                      type="email" 
                      placeholder="E-mail" 
                      value={emailsTemp[sec] || ""}
                      onChange={(e) => setEmailsTemp({ ...emailsTemp, [sec]: e.target.value })}
                      style={{ flex: 1, minWidth: "140px", padding: "8px", borderRadius: "8px", border: "1px solid #D1D5DB", fontSize: "12px" }} 
                    />
                    <input 
                      type="text" 
                      placeholder="Telefone" 
                      value={telsTemp[sec] || ""}
                      onChange={(e) => setTelsTemp({ ...telsTemp, [sec]: e.target.value })}
                      style={{ width: "120px", padding: "8px", borderRadius: "8px", border: "1px solid #D1D5DB", fontSize: "12px" }} 
                    />
                    <div style={{ display: "flex", gap: "4px" }}>
                      <button 
                        onClick={() => handleAddContato(sec)}
                        disabled={!emailsTemp[sec] && !telsTemp[sec]}
                        style={{ padding: "8px 12px", background: (!emailsTemp[sec] && !telsTemp[sec]) ? "#9CA3AF" : "#2563EB", color: "white", border: "none", borderRadius: "8px", fontWeight: "bold", fontSize: "12px", cursor: (!emailsTemp[sec] && !telsTemp[sec]) ? "not-allowed" : "pointer" }}
                      >
                        + Adicionar
                      </button>
                      <button 
                        onClick={() => setModalSecAberto(sec)}
                        style={{ padding: "8px 12px", background: "#E5E7EB", color: "#374151", border: "1px solid #D1D5DB", borderRadius: "8px", fontWeight: "bold", fontSize: "12px", cursor: "pointer", display: "flex", alignItems: "center", gap: "4px" }}
                      >
                        Usar dados salvos ▼
                      </button>
                    </div>
                  </div>

                  <div style={{ background: "#F3F4F6", borderRadius: "8px", border: "1px solid #E5E7EB", padding: "8px", minHeight: "60px", maxHeight: "120px", overflowY: "auto", display: "flex", flexDirection: "column", gap: "4px" }}>
                    {faltaContato && (
                      <div style={{ fontSize: "12px", color: "#DC2626", textAlign: "center", padding: "8px", fontWeight: "bold" }}>
                        Obrigatório adicionar pelo menos um contato
                      </div>
                    )}
                    {contatos.map((contato: any, idx: number) => (
                      <div key={idx} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "white", padding: "6px 12px", borderRadius: "6px", border: "1px solid #D1D5DB" }}>
                        <span style={{ fontSize: "12px", color: "#111827" }}>{contato.email || "—"} | {contato.tel || "—"}</span>
                        <div style={{ display: "flex", gap: "6px" }}>
                          <div style={{ display: "flex", gap: "6px" }}>
                            <button 
                              onClick={() => handleSalvarContatoIndiv(contato)}
                              disabled={contatosSalvos.some(s => s.email === contato.email && s.tel === contato.tel)}
                              style={{ 
                                padding: "4px 8px", 
                                background: contatosSalvos.some(s => s.email === contato.email && s.tel === contato.tel) ? "#9CA3AF" : "#10B981", 
                                color: "white", 
                                border: "none", 
                                borderRadius: "6px", 
                                fontWeight: "bold", 
                                fontSize: "11px", 
                                cursor: contatosSalvos.some(s => s.email === contato.email && s.tel === contato.tel) ? "default" : "pointer" 
                              }}
                            >
                              {contatosSalvos.some(s => s.email === contato.email && s.tel === contato.tel) ? "Já Salvo" : "Salvar Contato"}
                            </button>
                          </div>
                          <button 
                            onClick={() => handleRemoveContato(sec, idx)}
                            style={{ padding: "4px 8px", background: "#DC2626", color: "white", border: "none", borderRadius: "6px", fontWeight: "bold", fontSize: "11px", cursor: "pointer" }}
                          >
                            Remover
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {modalSecAberto && (
        <div style={{ position: "fixed", top: 0, left: 0, width: "100%", height: "100%", backgroundColor: "rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 9999 }}>
          <div style={{ background: "white", padding: "24px", borderRadius: "16px", width: "100%", maxWidth: "450px", boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.1)" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
              <h3 style={{ margin: 0, color: "#111827", fontSize: "18px" }}>Contatos Salvos</h3>
              <button onClick={() => setModalSecAberto(null)} style={{ background: "none", border: "none", fontSize: "20px", cursor: "pointer", color: "#6B7280" }}>×</button>
            </div>
            
            <div style={{ display: "flex", flexDirection: "column", gap: "8px", maxHeight: "300px", overflowY: "auto" }}>
              {contatosSalvos.length === 0 ? (
                <p style={{ color: "#6B7280", fontSize: "14px", textAlign: "center" }}>Nenhum contato salvo ainda.</p>
              ) : (
                contatosSalvos.map((contato, i) => {
                  const contatosAtuais = contatosSecretarias[modalSecAberto] || [];
                  const emUso = contatosAtuais.some((c: any) => c.email === contato.email && c.tel === contato.tel);

                  return (
                    <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px", border: "1px solid #E5E7EB", borderRadius: "8px", background: "#F9FAFB" }}>
                      <div style={{ fontSize: "13px", color: "#374151" }}>
                        <div style={{ fontWeight: "bold" }}>{contato.email || "Sem E-mail"}</div>
                        <div>{contato.tel || "Sem Telefone"}</div>
                      </div>
                      <div style={{ display: "flex", gap: "8px" }}>
                        <button 
                          onClick={() => handleUsarContatoSalvo(modalSecAberto, contato)} 
                          disabled={emUso}
                          style={{ padding: "6px 12px", background: emUso ? "#9CA3AF" : "#2563EB", color: "white", border: "none", borderRadius: "6px", fontSize: "12px", fontWeight: "bold", cursor: emUso ? "not-allowed" : "pointer" }}
                        >
                          {emUso ? "Em uso" : "Usar"}
                        </button>
                        <button onClick={() => handleRemoverContatoSalvo(i)} style={{ padding: "6px 8px", background: "#FEE2E2", color: "#DC2626", border: "none", borderRadius: "6px", fontSize: "12px", fontWeight: "bold", cursor: "pointer" }}>Apagar</button>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
            
            <div style={{ marginTop: "20px", textAlign: "right" }}>
              <button onClick={() => setModalSecAberto(null)} style={{ padding: "8px 16px", background: "#E5E7EB", color: "#374151", border: "none", borderRadius: "8px", fontWeight: "bold", cursor: "pointer" }}>Fechar</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}