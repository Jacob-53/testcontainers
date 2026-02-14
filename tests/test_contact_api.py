def test_inserting_contact_returns_created_data(client):
    # Given

    # When
    response = client.post(
        "/contacts/",
        json={
            "name": "Jacob",
            "phone": "010-1234-5678",
            "email": "jacob@addmore.com",
        },
    )

    # Then
    assert response.status_code == 201
    assert isinstance(response.json()["id"], int)


def test_inserted_contact_can_be_retrieved(client):
    # Given
    client.post(
        "/contacts/",
        json={
            "name": "Jacob",
            "phone": "010-1234-5678",
            "email": "jacob@addmore.com",
        },
    )

    # When
    response = client.get("/contacts/")

    # Then
    assert response.status_code == 200
    assert len(response.json()) == 1