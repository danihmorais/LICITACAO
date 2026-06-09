import React, { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/core";
import Step1 from "./steps/step1";
import Step2 from "./steps/step2";
import Step3 from "./steps/step3";
import Step4 from "./steps/step4";
import Step5 from "./steps/step5";
import { mapearDadosWizard } from "../utils/mapearDados";
import { processarDadosIA } from "../providers/services/geradorIA";

export default function Wizard() {
  const [etapaAtual, setEtapaAtual] = useState(0);
  const [dados, setDados] = useState({
    objeto: "",
    necessidade: "",
    itens: [],
    amostra: false,
    vistoria: false,
    execucao: "",
    secretarias: [],
    contatosSecretarias: {},
    gestores: [],
    fiscais: [],
    instrumento: "CONTRATO",
    prorrogar: false,
    meepp: "SIM",
    criterio: "ITEM",
    motivoCriterio: "",
    modalidade: "PREGAO_ELETRONICO",
    motivoModalidade: "",
    pac: "SIM",
    motivoPac: "",
    vigenciaNum: 1,
    vigenciaUnidade: "Meses",
    dotacao: "",
    caminhoImagemDotacao: ""
  });
  const [carregando, setCarregando] = useState(false);
  const [statusTexto, setStatusTexto] = useState("Iniciando...");

  const atualizarDados = (novosDados: Partial<typeof dados>) => {
    setDados((prev) => ({ ...prev, ...novosDados }));
  };

  useEffect(() => {
    const temLote = dados.itens.some((item: any) => item.lote && item.lote.toString().trim() !== "");
    if (temLote && dados.criterio !== "LOTE") {
      atualizarDados({ criterio: "LOTE" });
    } else if (!temLote && dados.criterio !== "ITEM" && dados.criterio !== "GLOBAL") {
      atualizarDados({ criterio: "ITEM" });
    }
  }, [dados.itens]);

  const validarEtapa = () => {
    switch (etapaAtual) {
      case 0:
        return dados.objeto.trim() !== "" && dados.necessidade.trim() !== "" && dados.itens.length > 0;
      case 1:
        return dados.execucao.trim() !== "";
      case 2:
        return dados.secretarias.length > 0;
      case 3:
        return dados.gestores.length > 0 && dados.fiscais.length > 0;
      case 4:
        const criterioValido = (dados.criterio === "ITEM") || ((dados.criterio === "GLOBAL" || dados.criterio === "LOTE") && dados.motivoCriterio.trim() !== "");
        const modalidadeValida = dados.modalidade === "PREGAO_ELETRONICO" || dados.motivoModalidade.trim() !== "";
        const pacValido = dados.pac === "SIM" || dados.motivoPac.trim() !== "";
        const dotacaoValida = dados.dotacao.trim() !== "" || !!dados.caminhoImagemDotacao;
        
        return dados.instrumento !== "" && criterioValido && modalidadeValida && pacValido && dotacaoValida;
      default:
        return true;
    }
  };

  const avancar = () => {
    if (etapaAtual < 4) {
      setEtapaAtual(etapaAtual + 1);
    } else {
      confeccionarDocumentos();
    }
  };

  const voltar = () => {
    if (etapaAtual > 0) {
      setEtapaAtual(etapaAtual - 1);
    }
  };

  const confeccionarDocumentos = async () => {
    setCarregando(true);
    setStatusTexto("A ler configurações da IA...");
    try {
      const config: any = await invoke("ler_config_ia");
      const provedor = config.provedor || "gemini";
      const chaveApi = config.chave_api || "";

      if (!chaveApi) {
        alert("Chave de API não configurada. Por favor, volte ao início e insira a sua chave.");
        setCarregando(false);
        return;
      }

      const dadosMapeados = mapearDadosWizard(dados);
      const meeppExclusivo = dados.meepp === "SIM";

      setStatusTexto("A gerar Documento de Formalização de Demanda (DFD)...");
      const dadosIaDfd = await processarDadosIA(dadosMapeados, chaveApi, provedor, meeppExclusivo, "DFD");

      setStatusTexto("A estruturar o Estudo Técnico Preliminar (ETP)...");
      const dadosIaEtp = await processarDadosIA(dadosMapeados, chaveApi, provedor, meeppExclusivo, "ETP");

      setStatusTexto("A compor o Termo de Referência (TR)...");
      const dadosIaTr = await processarDadosIA(dadosMapeados, chaveApi, provedor, meeppExclusivo, "TR");

      const dadosIaFinais = { ...dadosIaDfd, ...dadosIaEtp, ...dadosIaTr };

      setStatusTexto("A preencher os ficheiros DOCX finais...");
      await invoke("gerar_documentos", { 
        dadosUsuario: dadosMapeados, 
        dadosIa: dadosIaFinais 
      });

      alert("Documentos gerados com sucesso!");
    } catch (erro) {
      alert("Erro na geração: " + erro);
    } finally {
      setCarregando(false);
    }
  };

  const renderizarEtapa = () => {
    switch (etapaAtual) {
      case 0: return <Step1 dados={dados} atualizarDados={atualizarDados} />;
      case 1: return <Step2 dados={dados} atualizarDados={atualizarDados} />;
      case 2: return <Step3 dados={dados} atualizarDados={atualizarDados} />;
      case 3: return <Step4 dados={dados} atualizarDados={atualizarDados} />;
      case 4: return <Step5 dados={dados} atualizarDados={atualizarDados} />;
      default: return <div style={{ padding: "2rem" }}>Próximas etapas na sequência...</div>;
    }
  };

  if (carregando) {
    return (
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "100vh", background: "#F3F4F6" }}>
        <div style={{ background: "white", padding: "40px", borderRadius: "24px", boxShadow: "0 10px 25px rgba(0,0,0,0.1)", textAlign: "center", width: "100%", maxWidth: "600px" }}>
          <h2 style={{ margin: "0 0 16px 0", color: "#111827", fontSize: "24px" }}>Gerando Artefatos com IA</h2>
          <p style={{ color: "#6B7280", margin: "0 0 24px 0" }}>{statusTexto}</p>
          <div style={{ width: "100%", height: "6px", background: "#E5E7EB", borderRadius: "4px", overflow: "hidden" }}>
            <div style={{ width: "50%", height: "100%", background: "#2563EB", transition: "width 0.3s", animation: "progress 2s infinite" }}></div>
          </div>
        </div>
      </div>
    );
  }

  const podeAvancar = validarEtapa();

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh", backgroundColor: "#F3F4F6" }}>
      <div style={{ padding: "24px 40px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
          <div>
            <h1 style={{ margin: 0, fontSize: "22px", color: "#111827" }}>
              {etapaAtual === 0 && "Etapa 1: Objeto e Justificativa"}
              {etapaAtual === 1 && "Etapa 2: Condições de Execução"}
              {etapaAtual === 2 && "Etapa 3: Unidade Demandante"}
              {etapaAtual === 3 && "Etapa 4: Equipe de Planejamento"}
              {etapaAtual === 4 && "Etapa 5: Definição do Instrumento"}
            </h1>
            <p style={{ margin: "4px 0 0 0", color: "#4B5563", fontSize: "14px" }}>
              Forneça os dados do processo com clareza para gerar os artefatos corretamente.
            </p>
          </div>
        </div>
        <span style={{ color: "#6B7280", fontWeight: "bold", fontSize: "14px" }}>Passo {etapaAtual + 1} de 5</span>
      </div>
      
      <div style={{ flex: 1, padding: "0 40px", overflow: "hidden" }}>
        <div style={{ height: "100%", background: "white", borderRadius: "24px", boxShadow: "0 4px 6px rgba(0,0,0,0.05)", border: "1px solid #E5E7EB", overflowY: "auto", padding: "32px" }}>
          {renderizarEtapa()}
        </div>
      </div>

      <div style={{ padding: "24px 40px", display: "flex", justifyContent: "space-between" }}>
        <button 
          onClick={voltar} 
          disabled={etapaAtual === 0} 
          style={{ width: "140px", height: "44px", borderRadius: "12px", border: "2px solid #D1D5DB", background: "transparent", color: "#374151", fontWeight: "bold", fontSize: "14px", cursor: etapaAtual === 0 ? "not-allowed" : "pointer", opacity: etapaAtual === 0 ? 0.5 : 1 }}
        >
          Voltar
        </button>
        <button 
          onClick={avancar}
          disabled={!podeAvancar}
          style={{ width: "140px", height: "44px", borderRadius: "12px", border: "none", background: !podeAvancar ? "#9CA3AF" : (etapaAtual === 4 ? "#22C55E" : "#2563EB"), color: "white", fontWeight: "bold", fontSize: "14px", cursor: !podeAvancar ? "not-allowed" : "pointer" }}
        >
          {etapaAtual === 4 ? "Confeccionar" : "Avançar"}
        </button>
      </div>
    </div>
  );
}