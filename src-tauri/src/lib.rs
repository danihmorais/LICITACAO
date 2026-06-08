use serde_json::Value;
use std::process::{Command, Stdio};
use std::io::Write;

#[tauri::command]
fn gerar_documentos(dados: Value) -> Result<String, String> {
    let mut child = Command::new("python")
        .arg("main.py")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .map_err(|e| e.to_string())?;

    if let Some(mut stdin) = child.stdin.take() {
        let payload = serde_json::json!({
            "acao": "salvar_documentos",
            "dados_usuario": dados
        });
        stdin.write_all(payload.to_string().as_bytes()).map_err(|e| e.to_string())?;
    }

    let output = child.wait_with_output().map_err(|e| e.to_string())?;
    Ok(String::from_utf8_lossy(&output.stdout).to_string())
}

#[tauri::command]
fn salvar_config_ia(_chave: String) -> Result<(), String> {
    Ok(())
}

#[tauri::command]
fn abrir_link(_url: String) -> Result<(), String> {
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
            abrir_link,
            aplicar_atualizacao
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}