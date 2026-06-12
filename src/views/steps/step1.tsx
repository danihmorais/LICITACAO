import React, { useRef } from "react";
import * as XLSX from "xlsx";

export default function Step1({ dados = { itens: [], objeto: "", necessidade: "" }, atualizarDados }: any) {
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const itens = dados.itens || [];
  const objeto = dados.objeto || "";
  const necessidade = dados.necessidade || "";

  const formatarMoeda = (valor: number) => {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor);
  };

  const parseMoeda = (texto: string) => {
    const num = String(texto).replace(/[^\d]/g, "");
    return Number(num) / 100;
  };

  const handleAdd = () => {
    const novosItens = [
      ...itens, 
      { 
        id: Date.now() + Math.random(), 
        numero: itens.length + 1, 
        descricao: "", 
        un: "UN", 
        qtd: 1, 
        valor: 0 
      }
    ];
    atualizarDados({ ...dados, itens: novosItens });
  };

  const handleRemove = (id: number) => {
    atualizarDados({ ...dados, itens: itens.filter((i: any) => i.id !== id) });
  };

  const handleChange = (id: number, field: string, value: any) => {
    const novosItens = itens.map((i: any) => i.id === id ? { ...i, [field]: value } : i);
    atualizarDados({ ...dados, itens: novosItens });
  };

  const handleMover = (index: number, direcao: number) => {
    const novoIndex = index + direcao;
    if (novoIndex < 0 || novoIndex >= itens.length) return;
    const novosItens = [...itens];
    const temp = novosItens[index];
    novosItens[index] = novosItens[novoIndex];
    novosItens[novoIndex] = temp;
    atualizarDados({ ...dados, itens: novosItens });
  };

  const dispararImportacao = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const extrairNumero = (val: any) => {
    if (typeof val === "number") return val;
    const str = String(val || "0").replace(/[^\d,.-]/g, "").replace(/\.(?=\d{3})/g, "").replace(",", ".");
    return Number(str) || 0;
  };

  const processarArquivo = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();

    reader.onload = (evt) => {
      try {
        const data = evt.target?.result;
        const workbook = XLSX.read(data, { type: "array" });
        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];
        
        const rows = XLSX.utils.sheet_to_json(worksheet, {
          header: 1,
          defval: ""
        }) as any[][];

        const headerIndex = rows.findIndex(
          (row: any[]) =>
            row.some((c) => String(c).trim() === "Item") &&
            row.some((c) => String(c).trim() === "Nome")
        );

        if (headerIndex === -1) {
          alert("Cabeçalho da planilha não encontrado (linhas com 'Item' e 'Nome').");
          return;
        }

        const header = rows[headerIndex].map(c => String(c).trim());

        if (!header.includes("Nome") || !header.includes("Quantidade") || !header.includes("Unidade")) {
          alert("A planilha não possui as colunas obrigatórias (Nome, Quantidade, Unidade).");
          return;
        }

        const novosItens = rows
          .slice(headerIndex + 1)
          .map((row) => ({
            id: Date.now() + Math.random(),
            numero: Number(row[0]) || 0,
            descricao: String(row[1] || "").trim(),
            qtd: Math.floor(extrairNumero(row[7])) || 0,
            un: String(row[8] || "UN").trim(),
            valor: extrairNumero(row[6])
          }))
          .filter((item) => item.descricao);

        atualizarDados({ ...dados, itens: novosItens });
        alert("Planilha importada com sucesso: " + novosItens.length + " itens.");
      } catch (error: any) {
        alert("Erro crítico ao importar: " + error.message);
      } finally {
        if (fileInputRef.current) {
          fileInputRef.current.value = "";
        }
      }
    };

    reader.readAsArrayBuffer(file);
  };

  const totalGeral = itens.reduce((acc: number, item: any) => acc + (Number(item.qtd) * Number(item.valor)), 0);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
      <input 
        type="file" 
        accept=".xlsx, .xls" 
        ref={fileInputRef} 
        style={{ display: "none" }} 
        onChange={processarArquivo} 
      />

      <div>
        <label style={{ fontWeight: "bold", fontSize: "16px", color: "#111827", display: "block", marginBottom: "8px" }}>
          Objeto da Licitação: <span style={{ color: "#DC2626" }}>*</span>
        </label>
        <p style={{ color: "#6B7280", fontSize: "13px", margin: "0 0 12px 0" }}>Descreva brevemente o objeto licitado para direcionar a geração de especificações.</p>
        <input 
          type="text" 
          required
          value={objeto} 
          onChange={(e) => atualizarDados({ ...dados, objeto: e.target.value })}
          style={{ width: "100%", padding: "12px", borderRadius: "12px", border: objeto.trim() === "" ? "1px solid #DC2626" : "1px solid #D1D5DB", fontSize: "14px", boxSizing: "border-box" }}
        />
      </div>

      <div>
        <label style={{ fontWeight: "bold", fontSize: "16px", color: "#111827", display: "block", marginBottom: "8px" }}>
          Justificativa da Demanda: <span style={{ color: "#DC2626" }}>*</span>
        </label>
        <p style={{ color: "#6B7280", fontSize: "13px", margin: "0 0 12px 0" }}>Descreva brevemente a justificativa da demanda.</p>
        <textarea 
          required
          value={necessidade}
          onChange={(e) => atualizarDados({ ...dados, necessidade: e.target.value })}
          style={{ width: "100%", padding: "12px", borderRadius: "12px", border: necessidade.trim() === "" ? "1px solid #DC2626" : "1px solid #D1D5DB", fontSize: "14px", minHeight: "120px", resize: "vertical", boxSizing: "border-box" }}
        />
      </div>

      <div style={{ borderTop: "1px solid #E5E7EB", paddingTop: "24px" }}>
        <div style={{ display: "flex", gap: "12px", marginBottom: "16px", alignItems: "center" }}>
          <button onClick={handleAdd} style={{ width: "140px", height: "38px", background: "#2563EB", color: "white", border: "none", borderRadius: "12px", fontWeight: "bold", cursor: "pointer" }}>+ Novo Item</button>
          <button onClick={dispararImportacao} style={{ width: "140px", height: "38px", background: "#2563EB", color: "white", border: "none", borderRadius: "12px", fontWeight: "bold", cursor: "pointer" }}>Importar XLSX</button>
          {itens.length === 0 && <span style={{ color: "#DC2626", fontSize: "13px", fontWeight: "bold" }}>Adicione pelo menos 1 item para avançar.</span>}
        </div>

        <div style={{ background: "#4B5563", color: "white", display: "flex", padding: "12px", borderRadius: "8px", fontWeight: "bold", fontSize: "13px" }}>
          <div style={{ width: "40px" }}>#</div>
          <div style={{ flex: 1, minWidth: "150px" }}>Descrição</div>
          <div style={{ width: "60px" }}>UN</div>
          <div style={{ width: "80px" }}>Qtd</div>
          <div style={{ width: "130px" }}>Vlr Unit.</div>
          <div style={{ width: "130px" }}>Total</div>
          <div style={{ width: "100px" }}></div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "8px", marginTop: "8px", maxHeight: "300px", overflowY: "auto", paddingRight: "4px" }}>
          {itens.map((item: any, index: number) => (
            <div key={item.id} style={{ display: "flex", alignItems: "center", background: "#F3F4F6", padding: "8px 12px", borderRadius: "8px", gap: "8px" }}>
              <div style={{ width: "40px", fontWeight: "bold", color: "#374151" }}>{item.numero || index + 1}</div>
              
              <input type="text" required value={item.descricao} onChange={(e) => handleChange(item.id, "descricao", e.target.value)} style={{ flex: 1, minWidth: "150px", padding: "8px", borderRadius: "8px", border: item.descricao.trim() === "" ? "1px solid #DC2626" : "1px solid #D1D5DB", boxSizing: "border-box" }} />
              
              <input type="text" required value={item.un} onChange={(e) => handleChange(item.id, "un", e.target.value)} style={{ width: "60px", padding: "8px", borderRadius: "8px", border: item.un.trim() === "" ? "1px solid #DC2626" : "1px solid #D1D5DB", boxSizing: "border-box", textAlign: "center" }} />
              
              <input 
                type="number" 
                required 
                min="1" 
                step="1" 
                value={item.qtd} 
                onKeyDown={(e) => { if (e.key === '.' || e.key === ',') e.preventDefault(); }}
                onChange={(e) => handleChange(item.id, "qtd", parseInt(e.target.value, 10) || "")} 
                style={{ width: "80px", padding: "8px", borderRadius: "8px", border: Number(item.qtd) <= 0 ? "1px solid #DC2626" : "1px solid #D1D5DB", boxSizing: "border-box", textAlign: "right" }} 
              />
              
              <input type="text" required value={formatarMoeda(item.valor)} onChange={(e) => handleChange(item.id, "valor", parseMoeda(e.target.value))} style={{ width: "130px", padding: "8px", borderRadius: "8px", border: Number(item.valor) <= 0 ? "1px solid #DC2626" : "1px solid #D1D5DB", boxSizing: "border-box", textAlign: "right", fontFamily: "monospace" }} />
              
              <div style={{ width: "130px", fontWeight: "bold", color: "#111827", fontSize: "14px", overflow: "hidden", textOverflow: "ellipsis", textAlign: "right" }}>{formatarMoeda(Number(item.qtd) * Number(item.valor))}</div>
              
              <div style={{ width: "100px", display: "flex", gap: "4px", justifyContent: "flex-end" }}>
                <button onClick={() => handleMover(index, -1)} style={{ width: "28px", height: "28px", borderRadius: "6px", border: "1px solid #D1D5DB", background: "white", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center" }}>↑</button>
                <button onClick={() => handleMover(index, 1)} style={{ width: "28px", height: "28px", borderRadius: "6px", border: "1px solid #D1D5DB", background: "white", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center" }}>↓</button>
                <button onClick={() => handleRemove(item.id)} style={{ width: "28px", height: "28px", borderRadius: "6px", border: "none", background: "#DC2626", color: "white", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center" }}>X</button>
              </div>
            </div>
          ))}
          {itens.length === 0 && (
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