import React, { useState } from "react";

export default function Step4({ dados, atualizarDados }: any) {
  const [gestorNome, setGestorNome] = useState("");
  const [gestorCargo, setGestorCargo] = useState("");
  const [fiscalNome, setFiscalNome] = useState("");
  const [fiscalCargo, setFiscalCargo] = useState("");

  const handleAddGestor = () => {
    if (!gestorNome) return;
    const novo = { nome: gestorNome, cargo: gestorCargo };
    atualizarDados({ gestores: [...dados.gestores, novo] });
    setGestorNome("");
    setGestorCargo("");
  };

  const handleAddFiscal = () => {
    if (!fiscalNome) return;
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

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "32px" }}>
      <div>
        <h2 style={{ fontSize: "16px", margin: "0 0 8px 0", color: "#111827" }}>Gestores do Contrato</h2>
        <p style={{ color: "#6B7280", margin: "0 0 16px 0", fontSize: "13px" }}>Adicione os responsáveis pelo contrato e mantenha o histórico de gestores disponíveis.</p>
        
        <div style={{ background: "#F9FAFB", border: "1px solid #E5E7EB", borderRadius: "14px", padding: "20px" }}>
          <div style={{ display: "flex", gap: "16px", marginBottom: "20px", alignItems: "flex-end" }}>
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
            <button 
              onClick={handleAddGestor}
              style={{ padding: "10px 24px", height: "40px", background: "#2563EB", color: "white", border: "none", borderRadius: "10px", fontWeight: "bold", fontSize: "13px", cursor: "pointer" }}
            >
              Adicionar Gestor
            </button>
          </div>

          <div style={{ background: "white", borderRadius: "10px", border: "1px solid #E5E7EB", minHeight: "80px", maxHeight: "150px", overflowY: "auto", padding: "8px", display: "flex", flexDirection: "column", gap: "4px" }}>
            {dados.gestores.length === 0 && (
              <div style={{ padding: "20px", textAlign: "center", color: "#9CA3AF", fontSize: "13px" }}>Nenhum gestor adicionado.</div>
            )}
            {dados.gestores.map((gestor: any, index: number) => (
              <div key={index} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "#F9FAFB", padding: "8px 16px", borderRadius: "8px", border: "1px solid #D1D5DB" }}>
                <span style={{ fontSize: "13px", color: "#111827", fontWeight: "500" }}>{gestor.nome} — {gestor.cargo}</span>
                <button 
                  onClick={() => handleRemoveGestor(index)}
                  style={{ padding: "6px 12px", background: "#DC2626", color: "white", border: "none", borderRadius: "6px", fontWeight: "bold", fontSize: "11px", cursor: "pointer" }}
                >
                  Remover
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div>
        <h2 style={{ fontSize: "16px", margin: "0 0 8px 0", color: "#111827" }}>Fiscais do Contrato</h2>
        <p style={{ color: "#6B7280", margin: "0 0 16px 0", fontSize: "13px" }}>Registre os fiscais responsáveis pela fiscalização e pelo acompanhamento do processo.</p>
        
        <div style={{ background: "#F9FAFB", border: "1px solid #E5E7EB", borderRadius: "14px", padding: "20px" }}>
          <div style={{ display: "flex", gap: "16px", marginBottom: "20px", alignItems: "flex-end" }}>
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
            <button 
              onClick={handleAddFiscal}
              style={{ padding: "10px 24px", height: "40px", background: "#2563EB", color: "white", border: "none", borderRadius: "10px", fontWeight: "bold", fontSize: "13px", cursor: "pointer" }}
            >
              Adicionar Fiscal
            </button>
          </div>

          <div style={{ background: "white", borderRadius: "10px", border: "1px solid #E5E7EB", minHeight: "80px", maxHeight: "150px", overflowY: "auto", padding: "8px", display: "flex", flexDirection: "column", gap: "4px" }}>
            {dados.fiscais.length === 0 && (
              <div style={{ padding: "20px", textAlign: "center", color: "#9CA3AF", fontSize: "13px" }}>Nenhum fiscal adicionado.</div>
            )}
            {dados.fiscais.map((fiscal: any, index: number) => (
              <div key={index} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "#F9FAFB", padding: "8px 16px", borderRadius: "8px", border: "1px solid #D1D5DB" }}>
                <span style={{ fontSize: "13px", color: "#111827", fontWeight: "500" }}>{fiscal.nome} — {fiscal.cargo}</span>
                <button 
                  onClick={() => handleRemoveFiscal(index)}
                  style={{ padding: "6px 12px", background: "#DC2626", color: "white", border: "none", borderRadius: "6px", fontWeight: "bold", fontSize: "11px", cursor: "pointer" }}
                >
                  Remover
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}