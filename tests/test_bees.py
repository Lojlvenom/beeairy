JATAI = {
    "common_name": "Jataí",
    "scientific_name": "Tetragonisca angustula",
    "bee_type": "stingless",
    "native": True,
    "description": "Abelha sem ferrão, dócil.",
}

APIS = {
    "common_name": "Abelha-europeia",
    "scientific_name": "Apis mellifera",
    "bee_type": "apis",
    "native": False,
}


def test_create_and_get_bee(client):
    resp = client.post("/bees", json=JATAI)
    assert resp.status_code == 201
    body = resp.json()
    assert body["id"] > 0
    assert body["common_name"] == "Jataí"

    resp = client.get(f"/bees/{body['id']}")
    assert resp.status_code == 200
    assert resp.json()["scientific_name"] == "Tetragonisca angustula"


def test_duplicate_scientific_name_returns_409(client):
    client.post("/bees", json=JATAI)
    resp = client.post("/bees", json=JATAI)
    assert resp.status_code == 409


def test_list_and_filter_bees(client):
    client.post("/bees", json=JATAI)
    client.post("/bees", json=APIS)

    assert len(client.get("/bees").json()) == 2

    stingless = client.get("/bees", params={"bee_type": "stingless"}).json()
    assert [b["common_name"] for b in stingless] == ["Jataí"]

    search = client.get("/bees", params={"search": "mellifera"}).json()
    assert [b["scientific_name"] for b in search] == ["Apis mellifera"]


def test_update_bee(client):
    bee_id = client.post("/bees", json=JATAI).json()["id"]
    resp = client.patch(f"/bees/{bee_id}", json={"description": "Mel muito apreciado."})
    assert resp.status_code == 200
    assert resp.json()["description"] == "Mel muito apreciado."
    assert resp.json()["common_name"] == "Jataí"


def test_update_to_existing_scientific_name_returns_409(client):
    client.post("/bees", json=JATAI)
    apis_id = client.post("/bees", json=APIS).json()["id"]
    resp = client.patch(f"/bees/{apis_id}", json={"scientific_name": JATAI["scientific_name"]})
    assert resp.status_code == 409


def test_delete_bee(client):
    bee_id = client.post("/bees", json=JATAI).json()["id"]
    assert client.delete(f"/bees/{bee_id}").status_code == 204
    assert client.get(f"/bees/{bee_id}").status_code == 404


def test_not_found(client):
    assert client.get("/bees/999").status_code == 404
    assert client.patch("/bees/999", json={"native": False}).status_code == 404
    assert client.delete("/bees/999").status_code == 404


def test_invalid_payload(client):
    resp = client.post("/bees", json={"common_name": "", "bee_type": "wasp"})
    assert resp.status_code == 422
