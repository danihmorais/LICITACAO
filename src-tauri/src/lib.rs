use serde_json::{json, Value};
use std::env;
use std::fs;
use std::io::Write;
use std::process::{Command, Stdio};
use tauri_plugin_opener::OpenerExt;

#[tauri::command]
async fn gerar_documentos(dados_usuario: Value, dados_ia: Value) -> Result<String, String> {
    let exe_dir = env::current_exe().unwrap_or_default();
    let base_dir = exe_dir.parent().unwrap_or(std::path::Path::new(""));
    let python_path = if cfg!(target_os = "windows") {
        "python"
    } else {
        "python3"
    };
    let main_py_path = base_dir.join("main.py");

    let mut child = Command::new(python_path)
        .arg(main_py_path)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .map_err(|e| e.to_string())?;

    if let Some(mut stdin) = child.stdin.take() {
        let payload = json!({
            "acao": "salvar_documentos",
            "dados_ia": dados_ia,
            "dados_usuario": dados_usuario,
            "preenchimentos_manuais": {},
            "pasta_saida": "Documentos_Gerados",
            "pasta_modelos": "modelos",
            "arquivos_base": [
                "DFD - BASE.docx",
                "ETP - BASE.docx",
                "TR - BASE.docx"
            ]
        });
        stdin
            .write_all(payload.to_string().as_bytes())
            .map_err(|e| e.to_string())?;
    }

    let output = child.wait_with_output().map_err(|e| e.to_string())?;
    Ok(String::from_utf8_lossy(&output.stdout).to_string())
}

#[tauri::command]
fn salvar_config_ia(provedor: String, chave: String) -> Result<(), String> {
    let settings_path = "settings.json";
    let mut settings = if let Ok(content) = fs::read_to_string(settings_path) {
        serde_json::from_str::<Value>(&content).unwrap_or(json!({}))
    } else {
        json!({})
    };

    settings["provedor"] = json!(provedor);
    settings["chave_api"] = json!(chave);

    fs::write(
        settings_path,
        serde_json::to_string_pretty(&settings).unwrap_or_default(),
    )
    .map_err(|e| e.to_string())?;
    Ok(())
}

#[tauri::command]
fn ler_config_ia() -> Result<Value, String> {
    let settings_path = "settings.json";
    if let Ok(content) = fs::read_to_string(settings_path) {
        if let Ok(settings) = serde_json::from_str::<Value>(&content) {
            return Ok(settings);
        }
    }
    Ok(json!({ "provedor": "gemini", "chave_api": "" }))
}

#[tauri::command]
fn abrir_link(app: tauri::AppHandle, url: String) -> Result<(), String> {
    app.opener()
        .open_url(url, None::<&str>)
        .map_err(|e| e.to_string())?;
    Ok(())
}

#[tauri::command]
fn aplicar_atualizacao(_url: String) -> Result<(), String> {
    Ok(())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![
            gerar_documentos,
            salvar_config_ia,
            ler_config_ia,
            abrir_link,
            aplicar_atualizacao
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}