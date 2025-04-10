import os
from collections import defaultdict
import re

#exercicio 1 
def Grafo(amostra):
    grafo = defaultdict(lambda: defaultdict(int))

    for nome in os.listdir(amostra): # lista de pastas/pessoas
        pasta_pessoa = os.path.join(amostra, nome)
        if not os.path.isdir(pasta_pessoa):
            continue

        for raiz, _, arquivos in os.walk(pasta_pessoa):
            for arquivo in arquivos:
                caminhoArquivo = os.path.join(raiz, arquivo) #caminho do email
                if os.path.isfile(caminhoArquivo):
                    try:
                        with open(caminhoArquivo, 'r', encoding='utf-8', errors='ignore') as f: 
                            linhas = f.readlines()
                            remetente = None
                            destinatarios = []

                            for linha in linhas:
                                if linha.startswith("From:"):
                                    linhaRemetente = linha.split(":", 1)[1].strip()
                                    remetente = regexEmail(linhaRemetente)

                                elif linha.startswith("To:"):
                                    linhaDestinatario = linha.split(":", 1)[1].strip()
                                    destinatarios = [regexEmail(email) for email in linhaDestinatario.split(",")]
                                    destinatarios = [email for email in destinatarios if email]
                            if remetente and destinatarios and len(destinatarios) > 0:
                                for dest in destinatarios:
                                    grafo[remetente][dest] += 1 
                    except Exception as e:
                        print(f"Erro ao processar {caminhoArquivo}: {e}")
#se for um arquivo ele corre linha por linha e salva as linhas que começam com from e to para salvar os remetentes e destinatarios usa o regex neles e se remetent e 
# destinatario nao for nulo , e destinatario for maior q 0 ele adiciona no grafo
    return grafo

def regexEmail(texto):
    match = re.search(r'[\w\.-]+@[\w\.-]+', texto) #permite letras numeros . e - 
    return match.group(0).lower() if match else None

def salvarListaADJ(grafo, textoSaida):
    with open(textoSaida, 'w', encoding='utf-8') as f:
        for remetente in sorted(grafo.keys()):
            destinatario = grafo[remetente]
            if destinatario:
                linha = f"{remetente} -> " + ", ".join(f"{dest} ({peso})" for dest, peso in destinatario.items())
                f.write("\n" + linha + "\n")
#abre o txt e ordena todos remetentes em ordem alfabetica , dps pega os destinatarios do remetente e se existir 1 destinatario ele add na lista 



# exercicio 2


def grauVertice(grafo):
    entrada = defaultdict(int)
    saida = defaultdict(int)

    for remetente in grafo:
        saida[remetente] = sum(grafo[remetente].values())
        for destinatario in grafo[remetente]:
            entrada[destinatario] += grafo[remetente][destinatario]

    return entrada, saida
#pega todos remetentes e soma os valores(mgs) que cada um enviou (saida)
#pega todos destinatarios e soma o remetente enviou pra ele

#2a
def ordemVertice(grafo):
    remetentes = set(grafo.keys())
    for destinos in grafo.values():
        remetentes.update(destinos.keys())
    return len(remetentes)
#cria um objeto com todos os remetentes e add dps todos destinatarios sem repetir ngm , e retorna o len dos vertices

#2b
def tamanhoArestas(grafo):
    return sum(len(destinatario) for destinatario in grafo.values())
#conta o numero de destinatarios nos valores do grafo e retorna a soma

# 2c
def verticeIsolado(grafo):
    entrada, saida = grauVertice(grafo)
    todos = set(entrada.keys()) | set(saida.keys())
    return [v for v in todos if entrada.get(v, 0) == 0 and saida.get(v, 0) == 0]
#calcula entrada e saida, coloca os dois em um conjunto e retorna true se entrada e saida = 0

#2d e 2e
def top20Graus(graus):
    return sorted(graus.items(), key=lambda x: x[1], reverse=True)[:20]
#ordena os 20 maiores graus do dicionario que recebe

#exercicio 3

    #Verifica se o grafo é fortemente euleriano/conexo ( chegar de qualquer vértice a qualquer outro vértice seguindo as arestas)
def verificar_fortemente_conexo(grafo):
    if not grafo:
        return False 

    visitados = set() # conjunto para armazenar os vertices visitados
    pilha = [next(iter(grafo.keys()))] # comeca a busca a partir do primeiro vertice

    # enquanto a pilha nao estiver vazia, continua a busca em profundidade(DFS)
    while pilha:
        vertice = pilha.pop()
        if vertice not in visitados:
            visitados.add(vertice)
            for vizinho in grafo[vertice]: # adiciona os vizinhos nao visitados pilha
                if vizinho not in visitados:
                    pilha.append(vizinho)

    return len(visitados) == len(grafo) # verifica se todos os vertices foram visitados

# verifica se o grafo é euleriano, se sim, retorna true, se nao, false
def euleriano(grafo):
    if not grafo:
        return False, ["Grafo vazio"] 

    falhas = [] # lista de falhas

    if not verificar_fortemente_conexo(grafo):
        falhas.append("O grafo não é fortemente conexo") # se o grafo nao for fortemente conexo, retorna false e falha

    grau_entrada, grau_saida = grauVertice(grafo) 

    problemas_grau = [] 
    # verifica se o grau de entrada e saida sao iguais para todos os vertices

    for vertice in grafo:
        if grau_entrada.get(vertice, 0) != grau_saida.get(vertice, 0):
            problemas_grau.append(vertice)
            # se o grau de entrada for diferente do grau de saida, add na lista de problemas

    for vertice in grau_entrada:
        if vertice not in grafo and grau_entrada[vertice] != grau_saida.get(vertice, 0):
            problemas_grau.append(vertice)

    # se o vertice nao estiver no grafo e o grau de entrada for diferente do grau de saida, add na lista de problemas
    if problemas_grau:
        falhas.append(f"Vértices com grau de entrada diferente do grau de saída: {', '.join(problemas_grau[:5])}{'...' if len(problemas_grau) > 5 else ''}")

    # se houver problemas de grau, add na lista de falhas
    if not falhas:
        return True, []
    else:
        return False, falhas

            
# ===== Exercício 4 =====
def eh_email_simples(s):
    return '@' in s and '.' in s and ' ' not in s

def vertices_ate_distancia_D(grafo, origem, D):
    dist = {origem: 0}
    visitado = set()
    fila = [(origem, 0)]

    while fila:
        atual, custo_atual = fila.pop(0)
        if atual in visitado:
            continue
        visitado.add(atual)

        for vizinho, peso in grafo.get(atual, {}).items():
            novo_custo = custo_atual + peso
            if novo_custo <= D and (vizinho not in dist or novo_custo < dist[vizinho]):
                dist[vizinho] = novo_custo
                fila.append((vizinho, novo_custo))

    del dist[origem]

    return sorted([v for v in dist.keys() if eh_email_simples(v)])


# ===== Exercício 5 =====
from collections import defaultdict

def bfs(graph, start):
    visited = {}
    queue = [(start, [start])]
    paths = {}

    while queue:
        current, path = queue.pop(0)
        if current not in visited:
            visited[current] = True
            paths[current] = path
            for neighbor in graph[current]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    return paths

def grafo_diametro(graph):
    max_distance = -1
    longest_path = []

    for node in list(graph):  
        shortest_paths = bfs(graph, node)
        for target in shortest_paths:
            path = shortest_paths[target]
            if len(path) - 1 > max_distance:
                max_distance = len(path) - 1
                longest_path = path

    return max_distance, longest_path


# testes e prints
if __name__ == "__main__":
    caminho_amostra = os.path.join(os.path.dirname(__file__), 'Amostra')
    caminho_saida = os.path.join(os.path.dirname(__file__), 'grafo_emails.txt')
    
    #teste ex1
    grafo = Grafo(caminho_amostra)
    salvarListaADJ(grafo, caminho_saida)
    print(f"Grafo salvo em {caminho_saida}")


    #print do ex 2
    print("\n\nExercicio 2")
    entrada, saida = grauVertice(grafo)
    
    print(f"Número de vértices: {ordemVertice(grafo)}")
    
    print(f"Número de arestas: {tamanhoArestas(grafo)}")
    
    print(f"Número de vértices isolados: {len(verticeIsolado(grafo))}")
    
    i = 1
    print("Top 20 maiores graus de saída:")
    for email, grau in top20Graus(saida):
        print(f"{i}- {email}: {grau}")
        i +=1
    x = 1
    print("Top 20 maiores graus de entrada:")
    for email, grau in top20Graus(entrada):
        print(f"{x}- {email}: {grau}")
        x += 1
    
    
    #print ex3
    print("\n\nExercicio 3")
    euleriano, falhas = euleriano(grafo)
    if euleriano:
        print("O grafo é Euleriano!")
    else:
        print("O grafo NÃO é Euleriano. Razões:")
        for falha in falhas:
            print(f"- {falha}")

# ===== Print do Exercício 4 =====
    print("\n\nExercicio 4")
    email_origem = 'mike.carson@enron.com'
    distancia_max = 40000

    if email_origem in grafo:
        resultado = vertices_ate_distancia_D(grafo, email_origem, distancia_max)
        print(f"\nVértices até distância {distancia_max} de '{email_origem}':")
        for i, v in enumerate(resultado, 1):
            print(f"{i}- {v}")
    else:
        print(f"\nO vértice '{email_origem}' não foi encontrado no grafo.")


# ===== Print do Exercício 5 =====
    print("\n\nExercicio 5")
    diametro, caminho = grafo_diametro(grafo)
    print(f"\nDiâmetro do grafo: {diametro}")
    print("Caminho correspondente ao diâmetro:")
    for i, vertice in enumerate(caminho):
        print(f"{i+1}- {vertice}")