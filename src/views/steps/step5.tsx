import React from "react";
import { open } from "@tauri-apps/api/dialog";

export default function Step5({ dados, atualizarDados }: any) {
  const handleAnexarImagem = async () => {
    try {
      const selected = await open({
        filters: [{ name: 'Imagens', extensions: ['png', 'jpg', 'jpeg'] }]
      });
      if (selected && !Array.isArray(selected)) {
        atualizarDados({ caminhoImagemDotacao: selected });
      }
    } catch (err) {
      alert("Erro ao selecionar imagem: " + err);
    }
  };

  const decrementarVigencia = () => {
    if (dados.vigenciaNum > 1) {
      atualizarDados({ vigenciaNum: dados.vigenciaNum - 1 });
    }
  };

  const incrementarVigencia = () => {
    atualizarDados({ vigenciaNum: dados.vigenciaNum + 1 });
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "28px" }}>
      <div>
        <h2 style={{ fontSize: "16px", margin: "0 0 16px 0", color: "#111827" }}>Tipo de Instrumento</h2>
        <div style={{ display: "flex", flexDirection: "column", gap: "12px", marginBottom: "16px" }}>
          <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer", fontSize: "14px", color: "#374151" }}>
            <input type="radio" value="CONTRATO" checked={dados.instrumento === "CONTRATO"} onChange={(e) => atualizarDados({ instrumento: e.target.value, prorrogar: dados.prorrogar })} />
            CONTRATO (Certeza da quantidade)
          </label>
          <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer", fontSize: "14px", color: "#374151" }}>
            <input type="radio" value="ATA" checked={dados.instrumento === "ATA"} onChange={(e) => atualizarDados({ instrumento: e.target.value, prorrogar: dados.prorrogar })} />
            ATA DE REGISTRO DE PREÇOS (Sem certeza da quantidade)
          </label>
          <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer", fontSize: "14px", color: "#374151" }}>
            <input type="radio" value="SEM_CONTRATO" checked={dados.instrumento === "SEM_CONTRATO"} onChange={(e) => atualizarDados({ instrumento: e.target.value, prorrogar: false })} />
            SEM CONTRATO (Dispensa pequeno valor)
          </label>
        </div>
        <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: dados.instrumento === "SEM_CONTRATO" ? "not-allowed" : "pointer", fontSize: "14px", color: "#374151", opacity: dados.instrumento === "SEM_CONTRATO" ? 0.5 : 1 }}>
          <input 
            type="checkbox" 
            checked={dados.prorrogar} 
            disabled={dados.instrumento === "SEM_CONTRATO"}
            onChange={(e) => atualizarDados({ prorrogar: e.target.checked })} 
          />
          Permitir prorrogação?
        </label>
      </div>

      <div>
        <h2 style={{ fontSize: "16px", margin: "0 0 16px 0", color: "#111827" }}>Participação ME/EPP</h2>
        <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
          <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer", fontSize: "14px", color: "#374151" }}>
            <input type="radio" value="SIM" checked={dados.meepp === "SIM"} onChange={(e) => atualizarDados({ meepp: e.target.value })} />
            Exclusiva para ME/EPP (Até R$ 80.000,00)
          </label>
          <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer", fontSize: "14px", color: "#374151" }}>
            <input type="radio" value="NAO" checked={dados.meepp === "NAO"} onChange={(e) => atualizarDados({ meepp: e.target.value })} />
            Não Exclusiva (Maior que R$ 80.000,00 ou ampla participação)
          </label>
        </div>
      </div>

      <div>
        <h2 style={{ fontSize: "16px", margin: "0 0 4px 0", color: "#111827" }}>Critério de Julgamento</h2>
        <p style={{ color: "#6B7280", margin: "0 0 16px 0", fontSize: "13px", fontStyle: "italic" }}>Regra geral da Lei 14.133/21: A adjudicação deve ser preferencialmente por ITEM para ampliar a concorrência.</p>
        <div style={{ display: "flex", flexDirection: "column", gap: "12px", marginBottom: "16px" }}>
          <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer", fontSize: "14px", color: "#374151" }}>
            <input type="radio" value="ITEM" checked={dados.criterio === "ITEM"} onChange={(e) => atualizarDados({ criterio: e.target.value })} />
            Menor preço por item
          </label>
          <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer", fontSize: "14px", color: "#374151" }}>
            <input type="radio" value="GLOBAL" checked={dados.criterio === "GLOBAL"} onChange={(e) => atualizarDados({ criterio: e.target.value })} />
            Menor preço global
          </label>
          <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer", fontSize: "14px", color: "#374151" }}>
            <input type="radio" value="LOTE" checked={dados.criterio === "LOTE"} onChange={(e) => atualizarDados({ criterio: e.target.value })} />
            Menor preço por lote
          </label>
        </div>
        {(dados.criterio === "GLOBAL" || dados.criterio === "LOTE") && (
          <div style={{ background: "#F9FAFB", padding: "16px", borderRadius: "12px", border: "1px solid #E5E7EB" }}>
            <label style={{ fontWeight: "bold", fontSize: "13px", color: "#374151", display: "block", marginBottom: "8px" }}>Motivação simples para o agrupamento (Global/Lote):</label>
            <textarea 
              value={dados.motivoCriterio}
              onChange={(e) => atualizarDados({ motivoCriterio: e.target.value })}
              style={{ width: "100%", padding: "12px", borderRadius: "8px", border: "1px solid #D1D5DB", fontSize: "13px", minHeight: "60px", resize: "vertical", boxSizing: "border-box" }}
            />
          </div>
        )}
      </div>

      <div>
        <h2 style={{ fontSize: "16px", margin: "0 0 4px 0", color: "#111827" }}>Modalidade</h2>
        <p style={{ color: "#6B7280", margin: "0 0 16px 0", fontSize: "13px", fontStyle: "italic" }}>Regra geral da Lei 14.133/21: O Pregão Eletrônico é a modalidade obrigatória padrão.</p>
        <div style={{ display: "flex", flexDirection: "column", gap: "12px", marginBottom: "16px" }}>
          <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer", fontSize: "14px", color: "#374151" }}>
            <input type="radio" value="PREGAO_ELETRONICO" checked={dados.modalidade === "PREGAO_ELETRONICO"} onChange={(e) => atualizarDados({ modalidade: e.target.value })} />
            Pregão Eletrônico
          </label>
          <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer", fontSize: "14px", color: "#374151" }}>
            <input type="radio" value="DISPENSA_EMAIL" checked={dados.modalidade === "DISPENSA_EMAIL"} onChange={(e) => atualizarDados({ modalidade: e.target.value })} />
            Dispensa por e-mail
          </label>
          <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer", fontSize: "14px", color: "#374151" }}>
            <input type="radio" value="DISPENSA_BLL" checked={dados.modalidade === "DISPENSA_BLL"} onChange={(e) => atualizarDados({ modalidade: e.target.value })} />
            Dispensa com lances na BLL
          </label>
          <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer", fontSize: "14px", color: "#374151" }}>
            <input type="radio" value="PREGAO_PRESENCIAL" checked={dados.modalidade === "PREGAO_PRESENCIAL"} onChange={(e) => atualizarDados({ modalidade: e.target.value })} />
            Pregão Presencial
          </label>
        </div>
        {dados.modalidade !== "PREGAO_ELETRONICO" && (
          <div style={{ background: "#F9FAFB", padding: "16px", borderRadius: "12px", border: "1px solid #E5E7EB" }}>
            <label style={{ fontWeight: "bold", fontSize: "13px", color: "#374151", display: "block", marginBottom: "8px" }}>
              {dados.modalidade === "PREGAO_PRESENCIAL" ? "Justificativa simples (Atenção: Válido para municípios com até 20k habitantes até abril de 2027):" : "Justificativa (Atenção: Limite legal de até 65k ao todo ao longo do ano):"}
            </label>
            <textarea 
              value={dados.motivoModalidade}
              onChange={(e) => atualizarDados({ motivoModalidade: e.target.value })}
              style={{ width: "100%", padding: "12px", borderRadius: "8px", border: "1px solid #D1D5DB", fontSize: "13px", minHeight: "60px", resize: "vertical", boxSizing: "border-box" }}
            />
          </div>
        )}
      </div>

      <div>
        <h2 style={{ fontSize: "16px", margin: "0 0 16px 0", color: "#111827" }}>Vigência do Contrato/Ata (Máximo 1 ano)</h2>
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <button onClick={decrementarVigencia} style={{ width: "40px", height: "40px", borderRadius: "10px", background: "#F3F4F6", border: "1px solid #D1D5DB", fontSize: "18px", fontWeight: "bold", cursor: "pointer", color: "#374151" }}>-</button>
          <input 
            type="text" 
            value={dados.vigenciaNum} 
            readOnly 
            style={{ width: "60px", height: "40px", textAlign: "center", borderRadius: "10px", border: "1px solid #D1D5DB", fontSize: "16px", fontWeight: "bold" }} 
          />
          <button onClick={incrementarVigencia} style={{ width: "40px", height: "40px", borderRadius: "10px", background: "#F3F4F6", border: "1px solid #D1D5DB", fontSize: "18px", fontWeight: "bold", cursor: "pointer", color: "#374151" }}>+</button>
          <select 
            value={dados.vigenciaUnidade} 
            onChange={(e) => atualizarDados({ vigenciaUnidade: e.target.value })}
            style={{ height: "40px", padding: "0 12px", borderRadius: "10px", border: "1px solid #D1D5DB", fontSize: "14px", background: "white", marginLeft: "8px", cursor: "pointer" }}
          >
            <option value="Dias">Dias</option>
            <option value="Meses">Meses</option>
            <option value="Ano(s)">Ano(s)</option>
          </select>
        </div>
      </div>

      <div>
        <h2 style={{ fontSize: "16px", margin: "0 0 16px 0", color: "#111827" }}>Dotação Orçamentária (Texto ou Imagem)</h2>
        <div style={{ display: "flex", gap: "16px", alignItems: "flex-start" }}>
          <textarea 
            value={dados.dotacao}
            onChange={(e) => atualizarDados({ dotacao: e.target.value })}
            placeholder="Descreva a dotação orçamentária..."
            style={{ flex: 1, padding: "12px", borderRadius: "12px", border: "1px solid #D1D5DB", minHeight: "80px", fontSize: "14px", resize: "vertical", boxSizing: "border-box" }}
          />
          <button 
            onClick={handleAnexarImagem} 
            style={{ padding: "0 24px", height: "44px", background: dados.caminhoImagemDotacao ? "#10B981" : "#2563EB", color: "white", border: "none", borderRadius: "12px", fontWeight: "bold", fontSize: "14px", cursor: "pointer", whiteSpace: "nowrap" }}
          >
            {dados.caminhoImagemDotacao ? "Imagem Anexada ✓" : "Anexar Imagem"}
          </button>
        </div>
      </div>

      <div>
        <h2 style={{ fontSize: "16px", margin: "0 0 16px 0", color: "#111827" }}>Plano Anual de Contratações (PAC)</h2>
        <div style={{ display: "flex", flexDirection: "column", gap: "12px", marginBottom: "16px" }}>
          <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer", fontSize: "14px", color: "#374151" }}>
            <input type="radio" value="SIM" checked={dados.pac === "SIM"} onChange={(e) => atualizarDados({ pac: e.target.value })} />
            Sim, previsto no PAC
          </label>
          <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer", fontSize: "14px", color: "#374151" }}>
            <input type="radio" value="NAO" checked={dados.pac === "NAO"} onChange={(e) => atualizarDados({ pac: e.target.value })} />
            Não previsto no PAC
          </label>
        </div>
        {dados.pac === "NAO" && (
          <div style={{ background: "#F9FAFB", padding: "16px", borderRadius: "12px", border: "1px solid #E5E7EB" }}>
            <label style={{ fontWeight: "bold", fontSize: "13px", color: "#374151", display: "block", marginBottom: "8px" }}>Justificativa simples para a não inclusão no PAC:</label>
            <textarea 
              value={dados.motivoPac}
              onChange={(e) => atualizarDados({ motivoPac: e.target.value })}
              style={{ width: "100%", padding: "12px", borderRadius: "8px", border: "1px solid #D1D5DB", fontSize: "13px", minHeight: "60px", resize: "vertical", boxSizing: "border-box" }}
            />
          </div>
        )}
      </div>
    </div>
  );
}