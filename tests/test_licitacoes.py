from fastapi.testclient import TestClient


def criar_licitacao(
    client: TestClient,
    titulo: str = "Construção de escola municipal",
    cidade: str = "Campinas",
    valor_estimado: float = 850000,
    modalidade: str = "Concorrência",
):
    return client.post(
        "/licitacoes/",
        json={
            "titulo": titulo,
            "cidade": cidade,
            "valor_estimado": valor_estimado,
            "modalidade": modalidade,
        },
    )


def test_criar_licitacao(client: TestClient):
    response = criar_licitacao(client)

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["titulo"] == "Construção de escola municipal"
    assert data["cidade"] == "Campinas"
    assert data["modalidade"] == "Concorrência"
    assert "criado_em" in data
    assert "atualizado_em" in data


def test_listar_licitacoes(client: TestClient):
    criar_licitacao(client)
    criar_licitacao(
        client,
        titulo="Reforma de unidade de saúde",
        cidade="Paulínia",
        valor_estimado=320000,
        modalidade="Pregão",
    )

    response = client.get("/licitacoes/")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert data["limit"] == 10
    assert data["offset"] == 0
    assert len(data["items"]) == 2


def test_buscar_licitacao_por_id(client: TestClient):
    criar_licitacao(client)

    response = client.get("/licitacoes/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["cidade"] == "Campinas"


def test_buscar_licitacao_inexistente(client: TestClient):
    response = client.get("/licitacoes/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Licitação não encontrada"


def test_atualizar_licitacao(client: TestClient):
    criar_licitacao(client)

    response = client.put(
        "/licitacoes/1",
        json={
            "titulo": "Construção de escola municipal - Fase 2",
            "cidade": "Campinas",
            "valor_estimado": 950000,
            "modalidade": "Concorrência",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["titulo"] == "Construção de escola municipal - Fase 2"


def test_deletar_licitacao(client: TestClient):
    criar_licitacao(client)

    response = client.delete("/licitacoes/1")

    assert response.status_code == 204

    response_busca = client.get("/licitacoes/1")

    assert response_busca.status_code == 404


def test_filtrar_licitacoes_por_cidade(client: TestClient):
    criar_licitacao(client)

    criar_licitacao(
        client,
        titulo="Reforma de unidade de saúde",
        cidade="Paulínia",
        valor_estimado=320000,
        modalidade="Pregão",
    )

    response = client.get(
        "/licitacoes/",
        params={
            "cidade": "camp",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["cidade"] == "Campinas"


def test_rejeitar_valor_estimado_invalido(client: TestClient):
    response = client.post(
        "/licitacoes/",
        json={
            "titulo": "Licitação inválida",
            "cidade": "Campinas",
            "valor_estimado": -100,
            "modalidade": "Pregão",
        },
    )

    assert response.status_code == 422

def test_filtrar_licitacoes_por_modalidade(client: TestClient):
    criar_licitacao(
        client,
        titulo="Construção de escola municipal",
        cidade="Campinas",
        valor_estimado=850000,
        modalidade="Concorrência",
    )

    criar_licitacao(
        client,
        titulo="Aquisição de equipamentos hospitalares",
        cidade="Paulínia",
        valor_estimado=420000,
        modalidade="Pregão",
    )

    response = client.get(
        "/licitacoes/",
        params={
            "modalidade": "preg",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["modalidade"] == "Pregão"


def test_paginacao_de_licitacoes(client: TestClient):
    criar_licitacao(
        client,
        titulo="Licitação número 1",
        cidade="Campinas",
    )

    criar_licitacao(
        client,
        titulo="Licitação número 2",
        cidade="Paulínia",
    )

    criar_licitacao(
        client,
        titulo="Licitação número 3",
        cidade="Sumaré",
    )

    response = client.get(
        "/licitacoes/",
        params={
            "limit": 2,
            "offset": 1,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 3
    assert data["limit"] == 2
    assert data["offset"] == 1
    assert len(data["items"]) == 2

    assert data["items"][0]["titulo"] == "Licitação número 2"
    assert data["items"][1]["titulo"] == "Licitação número 3"


def test_deletar_licitacao_inexistente(client: TestClient):
    response = client.delete("/licitacoes/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Licitação não encontrada"