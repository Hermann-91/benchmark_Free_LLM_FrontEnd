import time
import requests
import json
import os

def main():
    api_key = "COLOQUE_SUA_API_KEY_AQUI"
    prompt = (
        "Atue como um Engenheiro Front-end sênior e UI/UX Designer. "
        "Crie uma Landing Page responsiva em arquivo único (HTML + CSS) para uma marca "
        "de chocolates premium chamada 'Pé da Mata', cujos chocolates de origem (Tree to Bar) "
        "são produzidos em Barro Preto, no Sul da Bahia. O design deve ter um visual moderno, "
        "usar cores terrosas, tons de cacau e verde folha, além de incluir chamadas para ação (CTAs). "
        "Escreva um código limpo, componentizado, com classes semânticas. "
        "IMPORTANTE: Retorne apenas o bloco de código fonte (html), sem introduções ou explicações adicionais."
    )
    
    models = [
        "inclusionai/ling-3.0-flash:free",
        "poolside/laguna-s-2.1:free",
        "poolside/laguna-xs-2.1:free",
        "cohere/north-mini-code:free",
        "nvidia/nemotron-3-ultra-550b-a55b:free",
        "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        "poolside/laguna-m.1:free",
        "google/gemma-4-26b-a4b-it:free",
        "google/gemma-4-31b-it:free",
        "nvidia/nemotron-3-super-120b-a12b:free",
        "nvidia/nemotron-3-nano-30b-a3b:free",
        "nvidia/nemotron-nano-9b-v2:free",
        "openai/gpt-oss-20b:free"
    ]

    results = []
    output_dir = "resultados_benchmark"
    os.makedirs(output_dir, exist_ok=True)

    for model in models:
        print(f"\\nIniciando teste com: {model}...")
        start_time = time.time()
        
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}]
                }),
                timeout=180
            )
            response.raise_for_status()
            data = response.json()
            content = data['choices'][0]['message']['content']
            
            end_time = time.time()
            elapsed = round(end_time - start_time, 2)
            
            # Salvar arquivo HTML
            safe_name = model.replace("/", "_").replace(":", "_")
            file_path = os.path.join(output_dir, f"{safe_name}.html")
            
            # Limpeza rápida
            clean_content = content.replace("```html", "").replace("```", "").strip()
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(clean_content)
                
            print(f"✓ Sucesso! Tempo: {elapsed}s")
            results.append({"model": model, "status": "success", "time_seconds": elapsed, "file": file_path})
            
        except Exception as e:
            end_time = time.time()
            elapsed = round(end_time - start_time, 2)
            print(f"✗ Falha após {elapsed}s. Erro: {str(e)}")
            results.append({"model": model, "status": "failed", "time_seconds": elapsed, "error": str(e)})

    # Salvar relatório base
    with open(os.path.join(output_dir, "relatorio.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
        
    print("\\n🚀 Benchmark Concluído! Relatório salvo.")

if __name__ == "__main__":
    main()
