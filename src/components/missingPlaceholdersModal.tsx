import React, { useState, useEffect } from "react";

interface MissingPlaceholdersModalProps {
  isOpen: boolean;
  placeholders: string[];
  onClose: () => void;
  onConfirm: (resultados: Record<string, string>) => void;
}

export default function MissingPlaceholdersModal({ isOpen, placeholders, onClose, onConfirm }: MissingPlaceholdersModalProps) {
  const [valores, setValores] = useState<Record<string, string>>({});

  useEffect(() => {
    // Inicializar o estado com chaves vazias sempre que os placeholders mudarem
    if (isOpen) {
      const inicial: Record<string, string> = {};
      placeholders.forEach(p => inicial[p] = "");
      setValores(inicial);
    }
  }, [isOpen, placeholders]);

  if (!isOpen) return null;

  const handleConfirmar = () => {
    const vazios = placeholders.filter(p => !valores[p]?.trim());
    if (vazios.length > 0) {
      alert(`Preencha todos os campos antes de continuar:\n\n${vazios.join("\n")}`);
      return;
    }
    onConfirm(valores);
  };

  return (
    <div style={{ position: "fixed", top: 0, left: 0, right: 0, bottom: 0, backgroundColor: "rgba(0,0,0,0.5)", display: "flex", justifyContent: "center", alignItems: "center", zIndex: 1000, padding: "24px" }}>
      <div style={{ background: "white", width: "100%", maxWidth: "720px", maxHeight: "90vh", display: "flex", flexDirection: "column", borderRadius: "24px", padding: "32px", boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.1)" }}>
        
        <h2 style={{ margin: "0 0 8px 0", fontSize: "20px", color: "#111827" }}>Dados pendentes para completar os documentos</h2>
        <p style={{ margin: "0 0 20px 0", fontSize: "14px", color: "#6B7280" }}>
          Preencha todos os campos abaixo para que as variáveis sejam substituídas corretamente no documento final.
        </p>

        <div style={{ flex: 1, overflowY: "auto", background: "#F9FAFB", border: "1px solid #E5E7EB", borderRadius: "18px", padding: "20px", marginBottom: "24px", display: "flex", flexDirection: "column", gap: "16px" }}>
          {placeholders.map((chave) => (
            <div key={chave}>
              <label style={{ display: "block", fontSize: "14px", fontWeight: "bold", color: "#111827", marginBottom: "8px" }}>
                {chave}
              </label>
              <textarea
                value={valores[chave] || ""}
                onChange={(e) => setValores({ ...valores, [chave]: e.target.value })}
                style={{ width: "100%", height: "78px", padding: "12px", borderRadius: "14px", border: "1px solid #D1D5DB", fontSize: "13px", resize: "vertical", boxSizing: "border-box" }}
              />
            </div>
          ))}
        </div>

        <div style={{ display: "flex", justifyContent: "flex-end", gap: "12px" }}>
          <button 
            onClick={onClose}
            style={{ width: "120px", height: "40px", borderRadius: "10px", border: "1px solid #D1D5DB", background: "transparent", color: "#374151", fontWeight: "bold", fontSize: "14px", cursor: "pointer" }}
          >
            Cancelar
          </button>
          <button 
            onClick={handleConfirmar}
            style={{ width: "130px", height: "40px", borderRadius: "10px", border: "none", background: "#22C55E", color: "white", fontWeight: "bold", fontSize: "14px", cursor: "pointer" }}
          >
            Continuar
          </button>
        </div>

      </div>
    </div>
  );
}