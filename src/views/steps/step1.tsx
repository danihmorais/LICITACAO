import React from "react";
import { open } from "@tauri-apps/api/dialog";
import { readBinaryFile } from "@tauri-apps/api/fs";
import * as XLSX from "xlsx";

export default function Step1({ dados, atualizarDados }: any) {
  const formatarMoeda = (valor: number) => {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor);
  };

  const parseMoeda = (texto: string) => {
    const num = texto.replace(/[^\d,.-]/g, "").replace(".", "").replace(",", ".");
    return Number(num) || 0;
  };

  const handleAdd = () => {
    const novosItens = [...dados.itens, { id: Date.now(), descricao: "", un: "UN", qtd: 1, valor: 0 }];
    atualizarDados({ itens: novosItens });
  };

  const handleRemove = (id: number) => {
    atualizarDados({ itens: dados.itens.filter((i: any) => i.id !== id) });
  };

  const handleChange = (id: number, field: string, value: any) => {
    const novosItens = dados.itens.map((i: any) => i.id === id ? { ...i, [field]: value } : i);
    atualizarDados({ itens: novosItens });
  };

  const handleMover = (index: number, direcao: number) => {
    const novoIndex = index + direcao;
    if (novoIndex < 0 || novoIndex >= dados.itens.length) return;
    const novosItens = [...dados.itens];
    const temp = novosItens[index];
    novosItens[index] = novosItens[novoIndex];
    novosItens[novoIndex] = temp;
    atualizarDados({ itens: novosItens });
  };

  const importarPlanilha = async () => {
    try {
      const selected = await open({
        filters: [{ name: 'Excel', extensions: ['xlsx', 'xls'] }]
      });
      
      if (!selected || Array.isArray(selected)) return;

      const data = await readBinaryFile(selected);
      const workbook = XLSX.read(data, { type: "array" });
      const firstSheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[firstSheetName];
      const json = XLSX.utils.sheet_to_json(worksheet, { defval: "" });

      const novosItens = json.map((row: any) => ({
        id: Date.now() + Math.random(),
        descricao: row["Descrição"] || row["Descricao"] || row["Nome"] || row["Produto"] || "",
        un: row["UN"] || row["Unidade"] || "UN",
        qtd: Number(row["Quantidade"] || row["Qtd"] || 1),
        valor: Number(row["Valor"] || row["Preço"] || row["Preco"] || 0)
      })).filter((i: any) => i.descricao !== "");

      atualizarDados({ itens: novosItens });
      alert("Planilha importada com sucesso.");
    } catch (error) {
      alert("Erro ao importar planilha: " + error);
    }
  };

  const totalGeral = dados.itens.reduce((acc: number, item: any) => acc + (item.qtd * item.valor), 0);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
      <div>
        <label style={{ fontWeight: "bold", fontSize: "16px", color: "#111827", display: "block", marginBottom: "8px" }}>Objeto da Licitação:</label>
        <p style={{ color: "#6B7280", fontSize: "13px", margin: "0 0 12px 0" }}>Descreva brevemente o objeto licitado para direcionar a geração de especificações.</p>
        <input 
          type="text" 
          value={dados.objeto} 
          onChange={(e) => atualizarDados({ objeto: e.target.value })}
          style={{ width: "100%", padding: "12px", borderRadius: "12px", border: "1px solid #D1D5DB", fontSize: "14px", boxSizing: "border-box" }}
        />
      </div>

      <div>
        <label style={{ fontWeight: "bold", fontSize: "16px", color: "#111827", display: "block", marginBottom: "8px" }}>Justificativa da Demanda:</label>
        <p style={{ color: "#6B7280", fontSize: "13px", margin: "0 0 12px 0" }}>Descreva brevemente a justificativa da demanda.</p>
        <textarea 
          value={dados.necessidade}
          onChange={(e) => atualizarDados({ necessidade: e.target.value })}
          style={{ width: "100%", padding: "12px", borderRadius: "12px", border: "1px solid #D1D5DB", fontSize: "14px", minHeight: "120px", resize: "vertical", boxSizing: "border-box" }}
        />
      </div>

      <div style={{ borderTop: "1px solid #E5E7EB", paddingTop: "24px" }}>
        <div style={{ display: "flex", gap: "12px", marginBottom: "16px" }}>
          <button onClick={handleAdd} style={{ width: "140px", height: "38px", background: "#2563EB", color: "white", border: "none", borderRadius: "12px", fontWeight: "bold", cursor: "pointer" }}>+ Novo Item</button>
          <button onClick={importarPlanilha} style={{ width: "140px", height: "38px", background: "#2563EB", color: "white", border: "none", borderRadius: "12px", fontWeight: "bold", cursor: "pointer" }}>Importar XLSX</button>
        </div>

        <div style={{ background: "#4B5563", color: "white", display: "flex", padding: "12px", borderRadius: "8px", fontWeight: "bold", fontSize: "13px" }}>
          <div style={{ width: "40px" }}>#</div>
          <div style={{ flex: 1, minWidth: "200px" }}>Descrição</div>
          <div style={{ width: "60px" }}>UN</div>
          <div style={{ width: "80px" }}>Qtd</div>
          <div style={{ width: "120px" }}>Vlr Unit.</div>
          <div style={{ width: "120px" }}>Total</div>
          <div style={{ width: "100px" }}></div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "8px", marginTop: "8px", maxHeight: "300px", overflowY: "auto", paddingRight: "4px" }}>
          {dados.itens.map((item: any, index: number) => (
            <div key={item.id} style={{ display: "flex", alignItems: "center", background: "#F3F4F6", padding: "8px 12px", borderRadius: "8px", gap: "8px" }}>
              <div style={{ width: "40px", fontWeight: "bold", color: "#374151" }}>{index + 1}</div>
              
              <input type="text" value={item.descricao} onChange={(e) => handleChange(item.id, "descricao", e.target.value)} style={{ flex: 1, minWidth: "200px", padding: "8px", borderRadius: "8px", border: "1px solid #D1D5DB" }} />
              
              <input type="text" value={item.un} onChange={(e) => handleChange(item.id, "un", e.target.value)} style={{ width: "60px", padding: "8px", borderRadius: "8px", border: "1px solid #D1D5DB" }} />
              
              <input type="number" value={item.qtd} onChange={(e) => handleChange(item.id, "qtd", Number(e.target.value))} style={{ width: "80px", padding: "8px", borderRadius: "8px", border: "1px solid #D1D5DB" }} />
              
              <input type="text" value={item.valor} onChange={(e) => handleChange(item.id, "valor", parseMoeda(e.target.value))} style={{ width: "120px", padding: "8px", borderRadius: "8px", border: "1px solid #D1D5DB" }} />
              
              <div style={{ width: "120px", fontWeight: "bold", color: "#111827", fontSize: "14px" }}>{formatarMoeda(item.qtd * item.valor)}</div>
              
              <div style={{ width: "100px", display: "flex", gap: "4px" }}>
                <button onClick={() => handleMover(index, -1)} style={{ width: "28px", height: "28px", borderRadius: "6px", border: "1px solid #D1D5DB", background: "white", cursor: "pointer" }}>↑</button>
                <button onClick={() => handleMover(index, 1)} style={{ width: "28px", height: "28px", borderRadius: "6px", border: "1px solid #D1D5DB", background: "white", cursor: "pointer" }}>↓</button>
                <button onClick={() => handleRemove(item.id)} style={{ width: "28px", height: "28px", borderRadius: "6px", border: "none", background: "#DC2626", color: "white", cursor: "pointer" }}>X</button>
              </div>
            </div>
          ))}
          {dados.itens.length === 0 && (
            <div style={{ padding: "20px", textAlign: "center", color: "#6B7280" }}>Nenhum item adicionado.</div>
          )}
        </div>

        <div style={{ textAlign: "right", marginTop: "16px", fontSize: "18px", fontWeight: "bold", color: "#111827" }}>
          TOTAL GERAL: {formatarMoeda(totalGeral)}
        </div>
      </div>
    </div>
  );
}