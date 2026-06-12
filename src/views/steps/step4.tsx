import React, { useState, useEffect } from "react";

export default function Step4({ dados, atualizarDados }: any) {
  const [gestorNome, setGestorNome] = useState("");
  const [gestorCargo, setGestorCargo] = useState("");
  const [fiscalNome, setFiscalNome] = useState("");
  const [fiscalCargo, setFiscalCargo] = useState("");

  const [gestoresSalvos, setGestoresSalvos] = useState<any[]>([]);
  const [fiscaisSalvos, setFiscaisSalvos] = useState<any[]>([]);

  const [modalGestorAberto, setModalGestorAberto] = useState(false);
  const [modalFiscalAberto, setModalFiscalAberto] = useState(false);

  useEffect(() => {
    const gSalvos = localStorage.getItem("licita_gestores_salvos");
    const fSalvos = localStorage.getItem("licita_fiscais_salvos");
    if (gSalvos) setGestoresSalvos(JSON.parse(gSalvos));
    if (fSalvos) setFiscaisSalvos(JSON.parse(fSalvos));
  }, []);

  const handleAddGestor = () => {
    if (!gestorNome || !gestorCargo) return;
    const novo = { nome: gestorNome, cargo: gestorCargo };
    atualizarDados({ gestores: [...dados.gestores, novo] });
    setGestorNome("");
    setGestorCargo("");
  };

  const handleAddFiscal = () => {
    if (!fiscalNome || !fiscalCargo) return;
    const novo = { nome: fiscalNome, cargo: fiscalCargo };
    atualizarDados({ fiscais: [...dados.fiscais, novo] });
    setFiscalNome("");
    setFiscalCargo("");
  };

  const handleRemoveGestor = (index: number) => {
    atualizarDados({ gestores: dados.gestores.filter((_: any, i: number) => i !== index) });
  };

  const handleRemoveFiscal = (index: number) => {
    atualizarDados({ fiscais: dados.fiscais.filter((_: any, i: number) => i !== index) });
  };

  const handleSalvarGestor = (gestor: any) => {
    const jaExiste = gestoresSalvos.some(g => g.nome === gestor.nome && g.cargo === gestor.cargo);
    if (jaExiste) {
      alert("Este gestor já está salvo na sua lista.");
      return;
    }
    const novosSalvos = [...gestoresSalvos, gestor];
    setGestoresSalvos(novosSalvos);
    localStorage.setItem("licita_gestores_salvos", JSON.stringify(novosSalvos));
    alert("Gestor salvo com sucesso!");
  };

  const handleSalvarFiscal = (fiscal: any) => {
    const jaExiste = fiscaisSalvos.some(f => f.nome === fiscal.nome && f.cargo === fiscal.cargo);
    if (jaExiste) {
      alert("Este fiscal já está salvo na sua lista.");
      return;
    }
    const novosSalvos = [...fiscaisSalvos, fiscal];
    setFiscaisSalvos(novosSalvos);
    localStorage.setItem("licita_fiscais_salvos", JSON.stringify(novosSalvos));
    alert("Fiscal salvo com sucesso!");
  };

  const handleUsarGestorSalvo = (gestor: any) => {
    atualizarDados({ gestores: [...dados.gestores, gestor] });
    setModalGestorAberto(false);
  };

  const handleUsarFiscalSalvo = (fiscal: any) => {
    atualizarDados({ fiscais: [...dados.fiscais, fiscal] });
    setModalFiscalAberto(false);
  };

  const handleApagarGestorSalvo = (index: number) => {
    const novosSalvos = gestoresSalvos.filter((_, i) => i !== index);
    setGestoresSalvos(novosSalvos);
    localStorage.setItem("licita_gestores_salvos", JSON.stringify(novosSalvos));
  };

  const handleApagarFiscalSalvo = (index: number) => {
    const novosSalvos = fiscaisSalvos.filter((_, i) => i !== index);
    setFiscaisSalvos(novosSalvos);
    localStorage.setItem("licita_fiscais_salvos", JSON.stringify(novosSalvos));
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "32px" }}>
      
      <div>
        <h2 style={{ fontSize: "16px", margin: "0 0 8px 0", color: "#111827" }}>
          Gestores do Contrato <span style={{ color: "#DC2626" }}>*</span>
        </h2>
        <p style={{ color: "#6B7280", margin: "0 0 16px 0", fontSize: "13px" }}>Adicione pelo menos um responsável pelo contrato.</p>
        
        <div style={{ background: "#F9FAFB", border: dados.gestores.length === 0 ? "1px solid #DC2626" : "1px solid #E5E7EB", borderRadius: "14px", padding: "20px" }}>
          <div style={{ display: "flex", gap: "12px", marginBottom: "20px", alignItems: "flex-end" }}>
            <div style={{ flex: 1 }}>
              <label style={{ fontSize: "13px", fontWeight: "bold", color: "#374151", display: "block", marginBottom: "6px" }}>Nome</label>
              <input 
                type="text" 
                value={gestorNome}
                onChange={(e) => setGestorNome(e.target.value)}
                style={{ width: "100%", padding: "10px", borderRadius: "10px", border: "1px solid #D1D5DB", fontSize: "13px", boxSizing: "border-box" }}
              />
            </div>
            <div style={{ flex: 1 }}>
              <label style={{ fontSize: "13px", fontWeight: "bold", color: "#374151", display: "block", marginBottom: "6px" }}>Cargo</label>
              <input 
                type="text" 
                value={gestorCargo}
                onChange={(e) => setGestorCargo(e.target.value)}
                style={{ width: "100%", padding: "10px", borderRadius: "10px", border: "1px solid #D1D5DB", fontSize: "13px", boxSizing: "border-box" }}
              />
            </div>
            <div style={{ display: "flex", gap: "6px" }}>
              <button 
                onClick={handleAddGestor}
                disabled={!gestorNome || !gestorCargo}
                style={{ padding: "0 16px", height: "40px", background: (!gestorNome || !gestorCargo) ? "#9CA3AF" : "#2563EB", color: "white", border: "none", borderRadius: "10px", fontWeight: "bold", fontSize: "13px", cursor: (!gestorNome || !gestorCargo) ? "not-allowed" : "pointer" }}
              >
                Adicionar Gestor
              </button>
              <button 
                onClick={() => setModalGestorAberto(true)}
                style={{ padding: "0 12px", height: "40px", background: "#E5E7EB", color: "#374151", border: "1px solid #D1D5DB", borderRadius: "10px", fontWeight: "bold", fontSize: "12px", cursor: "pointer", display: "flex", alignItems: "center", gap: "4px" }}
              >
                Usar dados salvos ▼
              </button>
            </div>
          </div>

          <div style={{ background: "white", borderRadius: "10px", border: "1px solid #E5E7EB", minHeight: "80px", maxHeight: "150px", overflowY: "auto", padding: "8px", display: "flex", flexDirection: "column", gap: "4px" }}>
            {dados.gestores.length === 0 && (
              <div style={{ padding: "20px", textAlign: "center", color: "#9CA3AF", fontSize: "13px" }}>Nenhum gestor adicionado.</div>
            )}
            {dados.gestores.map((gestor: any, index: number) => (
              <div key={index} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "#F9FAFB", padding: "8px 16px", borderRadius: "8px", border: "1px solid #D1D5DB" }}>
                <span style={{ fontSize: "13px", color: "#111827", fontWeight: "500" }}>{gestor.nome} — {gestor.cargo}</span>
                <div style={{ display: "flex", gap: "6px" }}>
                  <div style={{ display: "flex", gap: "6px" }}>
  <button 
    onClick={() => handleSalvarGestor(gestor)}
    disabled={gestoresSalvos.some(g => g.nome === gestor.nome && g.cargo === gestor.cargo)}
    style={{ 
      padding: "6px 12px", 
      background: gestoresSalvos.some(g => g.nome === gestor.nome && g.cargo === gestor.cargo) ? "#9CA3AF" : "#10B981", 
      color: "white", 
      border: "none", 
      borderRadius: "6px", 
      fontWeight: "bold", 
      fontSize: "11px", 
      cursor: gestoresSalvos.some(g => g.nome === gestor.nome && g.cargo === gestor.cargo) ? "default" : "pointer" 
    }}
  >
    {gestoresSalvos.some(g => g.nome === gestor.nome && g.cargo === gestor.cargo) ? "Já Salvo" : "Salvar Gestor"}
  </button>
  </div>
                  <button 
                    onClick={() => handleRemoveGestor(index)}
                    style={{ padding: "6px 12px", background: "#DC2626", color: "white", border: "none", borderRadius: "6px", fontWeight: "bold", fontSize: "11px", cursor: "pointer" }}
                  >
                    Remover
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div>
        <h2 style={{ fontSize: "16px", margin: "0 0 8px 0", color: "#111827" }}>
          Fiscais do Contrato <span style={{ color: "#DC2626" }}>*</span>
        </h2>
        <p style={{ color: "#6B7280", margin: "0 0 16px 0", fontSize: "13px" }}>Registre pelo menos um fiscal responsável pelo acompanhamento.</p>
        
        <div style={{ background: "#F9FAFB", border: dados.fiscais.length === 0 ? "1px solid #DC2626" : "1px solid #E5E7EB", borderRadius: "14px", padding: "20px" }}>
          <div style={{ display: "flex", gap: "12px", marginBottom: "20px", alignItems: "flex-end" }}>
            <div style={{ flex: 1 }}>
              <label style={{ fontSize: "13px", fontWeight: "bold", color: "#374151", display: "block", marginBottom: "6px" }}>Nome</label>
              <input 
                type="text" 
                value={fiscalNome}
                onChange={(e) => setFiscalNome(e.target.value)}
                style={{ width: "100%", padding: "10px", borderRadius: "10px", border: "1px solid #D1D5DB", fontSize: "13px", boxSizing: "border-box" }}
              />
            </div>
            <div style={{ flex: 1 }}>
              <label style={{ fontSize: "13px", fontWeight: "bold", color: "#374151", display: "block", marginBottom: "6px" }}>Cargo</label>
              <input 
                type="text" 
                value={fiscalCargo}
                onChange={(e) => setFiscalCargo(e.target.value)}
                style={{ width: "100%", padding: "10px", borderRadius: "10px", border: "1px solid #D1D5DB", fontSize: "13px", boxSizing: "border-box" }}
              />
            </div>
            <div style={{ display: "flex", gap: "6px" }}>
              <button 
                onClick={handleAddFiscal}
                disabled={!fiscalNome || !fiscalCargo}
                style={{ padding: "0 16px", height: "40px", background: (!fiscalNome || !fiscalCargo) ? "#9CA3AF" : "#2563EB", color: "white", border: "none", borderRadius: "10px", fontWeight: "bold", fontSize: "13px", cursor: (!fiscalNome || !fiscalCargo) ? "not-allowed" : "pointer" }}
              >
                Adicionar Fiscal
              </button>
              <button 
                onClick={() => setModalFiscalAberto(true)}
                style={{ padding: "0 12px", height: "40px", background: "#E5E7EB", color: "#374151", border: "1px solid #D1D5DB", borderRadius: "10px", fontWeight: "bold", fontSize: "12px", cursor: "pointer", display: "flex", alignItems: "center", gap: "4px" }}
              >
                Usar dados salvos ▼
              </button>
            </div>
          </div>

          <div style={{ background: "white", borderRadius: "10px", border: "1px solid #E5E7EB", minHeight: "80px", maxHeight: "150px", overflowY: "auto", padding: "8px", display: "flex", flexDirection: "column", gap: "4px" }}>
            {dados.fiscais.length === 0 && (
              <div style={{ padding: "20px", textAlign: "center", color: "#9CA3AF", fontSize: "13px" }}>Nenhum fiscal adicionado.</div>
            )}
            {dados.fiscais.map((fiscal: any, index: number) => (
              <div key={index} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "#F9FAFB", padding: "8px 16px", borderRadius: "8px", border: "1px solid #D1D5DB" }}>
                <span style={{ fontSize: "13px", color: "#111827", fontWeight: "500" }}>{fiscal.nome} — {fiscal.cargo}</span>
                <div style={{ display: "flex", gap: "6px" }}>
                  <div style={{ display: "flex", gap: "6px" }}>
  <button 
    onClick={() => handleSalvarFiscal(fiscal)}
    disabled={fiscaisSalvos.some(f => f.nome === fiscal.nome && f.cargo === fiscal.cargo)}
    style={{ 
      padding: "6px 12px", 
      background: fiscaisSalvos.some(f => f.nome === fiscal.nome && f.cargo === fiscal.cargo) ? "#9CA3AF" : "#10B981", 
      color: "white", 
      border: "none", 
      borderRadius: "6px", 
      fontWeight: "bold", 
      fontSize: "11px", 
      cursor: fiscaisSalvos.some(f => f.nome === fiscal.nome && f.cargo === fiscal.cargo) ? "default" : "pointer" 
    }}
  >
    {fiscaisSalvos.some(f => f.nome === fiscal.nome && f.cargo === fiscal.cargo) ? "Já Salvo" : "Salvar Fiscal"}
  </button>
  </div>
                  <button 
                    onClick={() => handleRemoveFiscal(index)}
                    style={{ padding: "6px 12px", background: "#DC2626", color: "white", border: "none", borderRadius: "6px", fontWeight: "bold", fontSize: "11px", cursor: "pointer" }}
                  >
                    Remover
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {modalGestorAberto && (
        <div style={{ position: "fixed", top: 0, left: 0, width: "100%", height: "100%", backgroundColor: "rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 9999 }}>
          <div style={{ background: "white", padding: "24px", borderRadius: "16px", width: "100%", maxWidth: "450px", boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.1)" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
              <h3 style={{ margin: 0, color: "#111827", fontSize: "18px" }}>Gestores Salvos</h3>
              <button onClick={() => setModalGestorAberto(false)} style={{ background: "none", border: "none", fontSize: "20px", cursor: "pointer", color: "#6B7280" }}>×</button>
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: "8px", maxHeight: "300px", overflowY: "auto" }}>
              {gestoresSalvos.length === 0 ? (
                <p style={{ color: "#6B7280", fontSize: "14px", textAlign: "center" }}>Nenhum gestor salvo ainda.</p>
              ) : (
                gestoresSalvos.map((g, i) => {
                  const emUso = dados.gestores.some((dg: any) => dg.nome === g.nome && dg.cargo === g.cargo);

                  return (
                    <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px", border: "1px solid #E5E7EB", borderRadius: "8px", background: "#F9FAFB" }}>
                      <div style={{ fontSize: "13px", color: "#374151" }}>
                        <div style={{ fontWeight: "bold" }}>{g.nome}</div>
                        <div>{g.cargo}</div>
                      </div>
                      <div style={{ display: "flex", gap: "8px" }}>
                        <button 
                          onClick={() => handleUsarGestorSalvo(g)} 
                          disabled={emUso}
                          style={{ padding: "6px 12px", background: emUso ? "#9CA3AF" : "#2563EB", color: "white", border: "none", borderRadius: "6px", fontSize: "12px", fontWeight: "bold", cursor: emUso ? "not-allowed" : "pointer" }}
                        >
                          {emUso ? "Em uso" : "Usar"}
                        </button>
                        <button onClick={() => handleApagarGestorSalvo(i)} style={{ padding: "6px 8px", background: "#FEE2E2", color: "#DC2626", border: "none", borderRadius: "6px", fontSize: "12px", fontWeight: "bold", cursor: "pointer" }}>Apagar</button>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
            <div style={{ marginTop: "20px", textAlign: "right" }}>
              <button onClick={() => setModalGestorAberto(false)} style={{ padding: "8px 16px", background: "#E5E7EB", color: "#374151", border: "none", borderRadius: "8px", fontWeight: "bold", cursor: "pointer" }}>Fechar</button>
            </div>
          </div>
        </div>
      )}

      {modalFiscalAberto && (
        <div style={{ position: "fixed", top: 0, left: 0, width: "100%", height: "100%", backgroundColor: "rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 9999 }}>
          <div style={{ background: "white", padding: "24px", borderRadius: "16px", width: "100%", maxWidth: "450px", boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.1)" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
              <h3 style={{ margin: 0, color: "#111827", fontSize: "18px" }}>Fiscais Salvos</h3>
              <button onClick={() => setModalFiscalAberto(false)} style={{ background: "none", border: "none", fontSize: "20px", cursor: "pointer", color: "#6B7280" }}>×</button>
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: "8px", maxHeight: "300px", overflowY: "auto" }}>
              {fiscaisSalvos.length === 0 ? (
                <p style={{ color: "#6B7280", fontSize: "14px", textAlign: "center" }}>Nenhum fiscal salvo ainda.</p>
              ) : (
                fiscaisSalvos.map((f, i) => {
                  const emUso = dados.fiscais.some((df: any) => df.nome === f.nome && df.cargo === f.cargo);

                  return (
                    <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px", border: "1px solid #E5E7EB", borderRadius: "8px", background: "#F9FAFB" }}>
                      <div style={{ fontSize: "13px", color: "#374151" }}>
                        <div style={{ fontWeight: "bold" }}>{f.nome}</div>
                        <div>{f.cargo}</div>
                      </div>
                      <div style={{ display: "flex", gap: "8px" }}>
                        <button 
                          onClick={() => handleUsarFiscalSalvo(f)} 
                          disabled={emUso}
                          style={{ padding: "6px 12px", background: emUso ? "#9CA3AF" : "#2563EB", color: "white", border: "none", borderRadius: "6px", fontSize: "12px", fontWeight: "bold", cursor: emUso ? "not-allowed" : "pointer" }}
                        >
                          {emUso ? "Em uso" : "Usar"}
                        </button>
                        <button onClick={() => handleApagarFiscalSalvo(i)} style={{ padding: "6px 8px", background: "#FEE2E2", color: "#DC2626", border: "none", borderRadius: "6px", fontSize: "12px", fontWeight: "bold", cursor: "pointer" }}>Apagar</button>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
            <div style={{ marginTop: "20px", textAlign: "right" }}>
              <button onClick={() => setModalFiscalAberto(false)} style={{ padding: "8px 16px", background: "#E5E7EB", color: "#374151", border: "none", borderRadius: "8px", fontWeight: "bold", cursor: "pointer" }}>Fechar</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}