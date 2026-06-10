import { useState, useContext, useEffect } from "react";
import { invoke } from "@tauri-apps/api/core";
import logo from "./assets/logo.png";
import { ThemeContext } from "./context/ThemeContext";

export default function App() {
  const [provedor, setProvedor] = useState("gemini");
  const [chaveApi, setChaveApi] = useState("");
  const [carregando, setCarregando] = useState(false);
  const [statusGemini, setStatusGemini] = useState<boolean | null>(null);
  const [statusOpenRouter, setStatusOpenRouter] = useState<boolean | null>(null);
  const { theme, toggleTheme } = useContext(ThemeContext);

  const isDark = theme === "dark";
  const bgBody = isDark ? "#111827" : "#F3F4F6";
  const bgCard = isDark ? "#1F2937" : "#FFFFFF";
  const textColor = isDark ? "#F9FAFB" : "#111827";
  const textMuted = isDark ? "#9CA3AF" : "#6B7280";
  const inputBg = isDark ? "#374151" : "#FFFFFF";
  const inputBorder = isDark ? "#4B5563" : "#D1D5DB";

  useEffect(() => {
  verificarApis();

  const timer = setInterval(() => {
    verificarApis();
  }, 60000);

  return () => clearInterval(timer);
}, []);

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

  const fazerLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setCarregando(true);
    
    try {
      await invoke("salvar_config_ia", { provedor, chave: chaveApi });
    } catch (error) {
      alert("Erro ao validar a chave de API.");
    } finally {
      setCarregando(false);
    }
  };

  const abrirAjuda = () => {
    const url = provedor === "openrouter" 
      ? "https://openrouter.ai/settings/keys" 
      : "https://aistudio.google.com/app/apikey";
    invoke("abrir_link", { url }); 
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

        <h3 style={{ fontSize: "16px", color: textColor, marginBottom: "16px" }}>Selecione o motor de Inteligência Artificial</h3>
        <div style={{ display: "flex", justifyContent: "center", gap: "24px", marginBottom: "35px", color: textColor }}>
          <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer" }}>
            <input type="radio" value="gemini" checked={provedor === "gemini"} onChange={(e) => setProvedor(e.target.value)} style={{accentColor: "#2563EB", outline: "none", boxShadow: "none"}} />
            Google Gemini
          </label>
          <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer" }}>
            <input type="radio" value="openrouter" checked={provedor === "openrouter"} onChange={(e) => setProvedor(e.target.value)} style={{accentColor: "#2563EB", outline: "none", boxShadow: "none"}} />
            OpenRouter
          </label>
        </div>

        <form onSubmit={fazerLogin} style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
          <div style={{ textAlign: "left" }}>
            <label style={{ fontWeight: "bold", fontSize: "14px", color: textColor, display: "block", marginBottom: "8px" }}>Chave de API</label>
            <input 
              type="password" 
              placeholder="Cole sua chave de API aqui" 
              value={chaveApi}
              onChange={(e) => setChaveApi(e.target.value)}
              required
              style={{ width: "100%", padding: "14px", borderRadius: "14px", border: `1px solid ${inputBorder}`, backgroundColor: inputBg, color: textColor, fontSize: "14px", boxSizing: "border-box" }}
            />
          </div>
          
          <button type="button" onClick={abrirAjuda} style={{ background: "none", border: "none", color: "#3B82F6", cursor: "pointer", fontSize: "13px", textAlign: "left", padding: 0 }}>
            Não tem uma chave? Saiba como obter gratuitamente.
          </button>

          <button type="submit" disabled={carregando} style={{ marginTop: "24px", padding: "16px", backgroundColor: "#2563EB", color: "white", border: "none", borderRadius: "14px", fontSize: "16px", fontWeight: "bold", cursor: carregando ? "not-allowed" : "pointer" }}>
            {carregando ? "Conectando..." : "Acessar Sistema"}
          </button>
        </form>

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