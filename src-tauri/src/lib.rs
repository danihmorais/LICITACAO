use serde_json::{json, Value};
use std::fs;
use std::io::Write;
use std::process::{Command, Stdio};
use tauri::{AppHandle, Manager, State};
use tauri_plugin_opener::OpenerExt;

pub struct AppState {
    pub http_client: reqwest::Client,
}

#[tauri::command]
pub fn gerar_documentos(app: AppHandle, dados_usuario: Value, dados_ia: Value) -> Result<String, String> {
    let resource_dir = app.path().resource_dir().map_err(|e| e.to_string())?;
    let main_py_path = resource_dir.join("main.py");

    if !main_py_path.exists() {
        return Err("Arquivo main.py não encontrado nos recursos da aplicação.".to_string());
    }

    let python_path = if cfg!(target_os = "windows") {
        "python"
    } else {
        "python3"
    };

    let mut child = Command::new(python_path)
        .arg(&main_py_path)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|_| "Falha ao iniciar o processo Python. Verifique se o Python está instalado e configurado no PATH do sistema.".to_string())?;

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

    if !output.status.success() {
        return Err(String::from_utf8_lossy(&output.stderr).into_owned());
    }

    Ok(String::from_utf8_lossy(&output.stdout).into_owned())
}

#[tauri::command]
pub fn salvar_config_ia(app: AppHandle, provedor: String, chave: String) -> Result<(), String> {
    let app_dir = app.path().app_data_dir().map_err(|e| e.to_string())?;
    fs::create_dir_all(&app_dir).map_err(|e| e.to_string())?;
    let settings_path = app_dir.join("settings.json");

    let mut settings = if let Ok(content) = fs::read_to_string(&settings_path) {
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
pub fn ler_config_ia(app: AppHandle) -> Result<Value, String> {
    let app_dir = app.path().app_data_dir().map_err(|e| e.to_string())?;
    let settings_path = app_dir.join("settings.json");

    if let Ok(content) = fs::read_to_string(settings_path) {
        if let Ok(settings) = serde_json::from_str::<Value>(&content) {
            return Ok(settings);
        }
    }

    Ok(json!({
        "provedor": "gemini",
        "chave_api": ""
    }))
}

#[tauri::command]
pub fn abrir_link(app: AppHandle, url: String) -> Result<(), String> {
    app.opener()
        .open_url(url, None::<&str>)
        .map_err(|e| e.to_string())?;

    Ok(())
}

#[tauri::command]
pub fn aplicar_atualizacao(_url: String) -> Result<(), String> {
    Ok(())
}

#[derive(serde::Serialize)]
pub struct StatusApis {
    pub gemini: bool,
    pub openrouter: bool,
}

#[tauri::command]
pub async fn verificar_status_apis(state: State<'_, AppState>) -> Result<StatusApis, String> {
    let gemini = state.http_client
        .get("https://generativelanguage.googleapis.com")
        .send()
        .await
        .map(|r| r.status().is_success())
        .unwrap_or(false);

    let openrouter = state.http_client
        .get("https://openrouter.ai/api/v1/models")
        .send()
        .await
        .map(|r| r.status().is_success())
        .unwrap_or(false);

    Ok(StatusApis {
        gemini,
        openrouter,
    })
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let http_client = reqwest::Client::builder()
        .timeout(std::time::Duration::from_secs(5))
        .build()
        .expect("Falha ao construir o cliente HTTP");

    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .manage(AppState { http_client })
        .invoke_handler(tauri::generate_handler![
            gerar_documentos,
            salvar_config_ia,
            ler_config_ia,
            abrir_link,
            aplicar_atualizacao,
            verificar_status_apis
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}