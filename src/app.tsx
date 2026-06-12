import { useState, useContext, useEffect } from "react";
import { invoke } from "@tauri-apps/api/core";
import logo from "./assets/logo.png";
import { ThemeContext } from "./context/ThemeContext";
import Wizard from "./views/wizard";
import ConfigIA from "./components/configIA";

export default function App() {
  const [logado, setLogado] = useState(false);
  const [statusGemini, setStatusGemini] = useState<boolean | null>(null);
  const [statusOpenRouter, setStatusOpenRouter] = useState<boolean | null>(null);
  const { theme, toggleTheme } = useContext(ThemeContext);

  const isDark = theme === "dark";
  const bgBody = isDark ? "#111827" : "#F3F4F6";
  const bgCard = isDark ? "#1F2937" : "#FFFFFF";
  const textColor = isDark ? "#F9FAFB" : "#111827";
  const textMuted = isDark ? "#9CA3AF" : "#6B7280";

  useEffect(() => {
    verificarApis();
    verificarSessao();

    const timer = setInterval(() => {
      verificarApis();
    }, 60000);

    return () => clearInterval(timer);
  }, []);

  const verificarSessao = async () => {
    try {
      const config: any = await invoke("ler_config_ia");
      if (config && config.chave_api) {
        setLogado(true);
      }
    } catch (error) {}
  };

  const verificarApis = async () => {
    try {
      const resultado = await invoke<{
        gemini: boolean;
        openrouter: boolean;
      }>("verificar_status_apis");

      setStatusGemini(resultado.gemini);
      setStatusOpenRouter(resultado.openrouter);
    } catch {
      setStatusGemini(false);
      setStatusOpenRouter(false);
    }
  };

  const obterStatus = () => {
    if (statusGemini === null || statusOpenRouter === null) {
      return {
        texto: "Verificando disponibilidade das APIs...",
        cor: "#6B7280",
      };
    }

    if (statusGemini && statusOpenRouter) {
      return {
        texto: "Conectado às APIs Gemini e OpenRouter",
        cor: "#22C55E",
      };
    }

    if (statusGemini && !statusOpenRouter) {
      return {
        texto: "Conectado à API Gemini (OpenRouter indisponível - Contate o suporte)",
        cor: "#F59E0B",
      };
    }

    if (!statusGemini && statusOpenRouter) {
      return {
        texto: "Conectado à API OpenRouter (Gemini indisponível - Contate o suporte)",
        cor: "#F59E0B",
      };
    }

    return {
      texto: "Falha de conexão às APIs. Contate o suporte",
      cor: "#EF4444",
    };
  };

  const status = obterStatus();

  if (logado) {
    return <Wizard />;
  }

  return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh", backgroundColor: bgBody, transition: "background-color 0.3s", fontFamily: "sans-serif" }}>
      
      <button 
        onClick={toggleTheme} 
        style={{ position: "absolute", top: "20px", right: "20px", padding: "8px 16px", borderRadius: "8px", border: "none", cursor: "pointer", background: isDark ? "#374151" : "#E5E7EB", color: textColor }}
      >
        {isDark ? "☀️ Modo Claro" : "🌙 Modo Escuro"}
      </button>

      <div style={{ background: bgCard, padding: "40px", borderRadius: "24px", boxShadow: "0 10px 25px rgba(0,0,0,0.1)", width: "100%", maxWidth: "600px", textAlign: "center", transition: "background-color 0.3s" }}>
        
        <img src={logo} alt="Licita.AI Logo" style={{ width: "90px", marginBottom: "16px" }} />
        <h1 style={{ margin: "0 0 8px 0", fontSize: "34px", color: textColor }}>Licita.AI</h1>
        <p style={{ color: textMuted, marginBottom: "35px" }}>
          Automatize a criação de DFD, ETP e TR com Inteligência Artificial
        </p>

        <ConfigIA 
          onSuccess={() => setLogado(true)} 
          textoBotao="Acessar Sistema" 
          temaEscuro={isDark} 
        />

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginTop: "30px",
            fontSize: "12px",
            color: textMuted,
          }}
        >
          <span
            style={{
              color: status.cor,
              fontWeight: "bold",
            }}
          >
            {status.texto}
          </span>

          <span>@danih.morais</span>
        </div>
      </div>
    </div>
  );
}