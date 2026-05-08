import requests
import sys

# Variáveis globais para o Placar
total_testes = 0
testes_passaram = 0

def imprimir_resultado(nome_teste, sucesso, detalhe=""):
    global total_testes, testes_passaram
    total_testes += 1
    
    if sucesso:
        testes_passaram += 1
        print(f"✅ [PASSOU] {nome_teste} {detalhe}")
    else:
        print(f"❌ [FALHOU] {nome_teste} {detalhe}")

def iniciar_testes(base_url):
    print(f"\n🚀 Iniciando Testes Avançados na API: {base_url}\n")
    
    # 0. Resetar a API
    try:
        requests.post(f"{base_url}/reset")
        print("🔄 API Resetada para o estado inicial.\n")
    except:
        pass

    # ==========================================
    # 1. ROTA /login
    # ==========================================
    r_login_ok = requests.post(f"{base_url}/login", json={"email": "usuario@esoft.com", "password": "Abc123"})
    imprimir_resultado("LOGIN (Certo)", r_login_ok.status_code == 200, f"| Status: {r_login_ok.status_code}")

    r_login_err = requests.post(f"{base_url}/login", json={"email": "usuario@esoft.com", "password": "errada"})
    imprimir_resultado("LOGIN (Errado - Senha Incorreta)", r_login_err.status_code == 401, f"| Status recebido: {r_login_err.status_code} (Esperava 401)")

    r_login_vazio = requests.post(f"{base_url}/login", json={})
    imprimir_resultado("LOGIN (Errado - Corpo Vazio)", r_login_vazio.status_code == 401, f"| Status recebido: {r_login_vazio.status_code} (Esperava 401)")

    # ==========================================
    # 2. ROTA GET /jogos
    # ==========================================
    r_get_all = requests.get(f"{base_url}/jogos")
    imprimir_resultado("\nGET TODOS", r_get_all.status_code == 200, f"| Status: {r_get_all.status_code}")

    # ==========================================
    # 3. ROTA POST /jogos
    # ==========================================
    r_post_nom = requests.post(f"{base_url}/jogos", json={"nom": "Elden Ring", "tipo": "RPG", "nota": 9, "review": "Teste"})
    imprimir_resultado("\nPOST JOGO (Errado - Chave 'nom')", r_post_nom.status_code == 400, f"| Status: {r_post_nom.status_code} (Esperava 400)")

    r_post_branco = requests.post(f"{base_url}/jogos", json={"nome": "", "tipo": "RPG", "nota": 9, "review": "Teste"})
    imprimir_resultado("POST JOGO (Errado - Nome em branco)", r_post_branco.status_code == 400, f"| Status: {r_post_branco.status_code} (Esperava 400)")

    payload_post = {"nome": "Elden Ring", "tipo": "RPG", "nota": 9, "review": "Desafiador e impecável."}
    r_post_ok = requests.post(f"{base_url}/jogos", json=payload_post)
    imprimir_resultado("POST JOGO (Certo)", r_post_ok.status_code == 201, f"| Status: {r_post_ok.status_code}")

    id_criado = r_post_ok.json().get("id") if r_post_ok.status_code == 201 else None

    if id_criado:
        # ==========================================
        # 4. ROTA GET /jogos/{id}
        # ==========================================
        r_get_id_ok = requests.get(f"{base_url}/jogos/{id_criado}")
        imprimir_resultado(f"\nGET JOGO ID {id_criado} (Certo)", r_get_id_ok.status_code == 200, f"| Status: {r_get_id_ok.status_code}")

        r_get_id_err = requests.get(f"{base_url}/jogos/99999")
        imprimir_resultado("GET JOGO ID Inexistente (Errado)", r_get_id_err.status_code == 404, f"| Status: {r_get_id_err.status_code} (Esperava 404)")

        # ==========================================
        # 5. ROTA PUT /jogos/{id}
        # ==========================================
        r_put_err = requests.put(f"{base_url}/jogos/99999", json=payload_post)
        imprimir_resultado("\nPUT JOGO ID Inexistente (Errado)", r_put_err.status_code == 404, f"| Status: {r_put_err.status_code} (Esperava 404)")

        payload_put = {"nome": "Elden Ring - Shadow of the Erdtree", "tipo": "RPG", "nota": 10, "review": "A expansão é perfeita!"}
        r_put_ok = requests.put(f"{base_url}/jogos/{id_criado}", json=payload_put)
        imprimir_resultado("PUT JOGO (Certo)", r_put_ok.status_code == 200, f"| Status: {r_put_ok.status_code}")

        r_get_pos_put = requests.get(f"{base_url}/jogos/{id_criado}")
        nome_alterado = r_get_pos_put.json().get("nome")
        mudou_mesmo = nome_alterado == "Elden Ring - Shadow of the Erdtree"
        imprimir_resultado("VALIDAÇÃO PÓS-PUT (Verificação Real)", mudou_mesmo, f"| Nome lido do servidor: '{nome_alterado}'")

        # ==========================================
        # 6. ROTA DELETE /jogos/{id}
        # ==========================================
        r_del_ok = requests.delete(f"{base_url}/jogos/{id_criado}")
        imprimir_resultado("\nDELETE JOGO (Certo)", r_del_ok.status_code == 204, f"| Status: {r_del_ok.status_code}")

        r_del_err = requests.delete(f"{base_url}/jogos/{id_criado}")
        imprimir_resultado("DELETE DUPLICADO (Errado)", r_del_err.status_code == 404, f"| Status: {r_del_err.status_code} (Esperava 404)")

    else:
        print("\n⚠️ Testes de GET{id}, PUT e DELETE ignorados porque a criação inicial falhou.")

    # ==========================================
    # PLACAR FINAL
    # ==========================================
    print("\n" + "="*50)
    print("📊 RESUMO FINAL DOS TESTES")
    print("="*50)
    print(f"Pontuação: {testes_passaram}/{total_testes}")
    print(f"({testes_passaram} testes feitos de {total_testes} deram certo)")
    print("-" * 50)
    
    if testes_passaram == total_testes:
        print("🏆 RESULTADO: A API ESTÁ IMPECÁVEL! (Nota 10/10)")
    else:
        print("⚠️ RESULTADO: A API possui falhas e bugs que podem ser explorados.")
    print("="*50 + "\n")

if __name__ == "__main__":
    # Verifica se o usuário passou a URL. Se não passou, ensina como usar!
    if len(sys.argv) < 2:
        print("\n❌ ERRO: Faltou informar a URL da API.")
        print("\n📌 COMO USAR O TESTADOR:")
        print("--------------------------------------------------")
        print("Digite no terminal o comando python + o nome do")
        print("arquivo + a URL da API que você quer testar.")
        print("\nEXEMPLO DE USO:")
        print("python3 testador.py https://sua-api.onrender.com")
        print("--------------------------------------------------\n")
        sys.exit(1) # Sai do programa indicando erro
        
    # Pega a URL que o usuário digitou (e remove a barra "/" do final se ele colocar sem querer)
    url_digitada = sys.argv[1].rstrip('/')
    
    iniciar_testes(url_digitada)