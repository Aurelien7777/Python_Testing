

def test_show_summary_with_valid_email(client):
    response = client.post("/showSummary", data={
        "email": "admin@irontemple.com"
    })

    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_show_summary_with_unknown_email(client):
    response = client.post("/showSummary", data={
        "email": "unknown@test.com"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Sorry, that email was not found" in response.data