def test_upload_accepted_file(testclient):
    with open("tests/assets/files/sleep.fit", "rb") as f:
        files = {"files": ("sleep.fit", f)}
        response = testclient.post("/files", files=files)

        assert response.status_code == 200

        json_response: dict = response.json()
        assert len(json_response["data"]) == 1

        file_info = json_response["data"][0]
        assert file_info["filename"] == "sleep.fit"
        assert file_info["accepted"]
        assert file_info["id"][:9] == "alice_49_"
        assert file_info["errors"] == []
        assert file_info["zip_filename"] is None


def test_upload_accepted_file_with_upper_extension(testclient):
    with open("tests/assets/files/sleep.FIT", "rb") as f:
        files = {"files": ("sleep.fit", f)}
        response = testclient.post("/files", files=files)

        assert response.status_code == 200

        json_response: dict = response.json()
        assert len(json_response["data"]) == 1

        file_info = json_response["data"][0]
        assert file_info["filename"] == "sleep.fit"
        assert file_info["accepted"]
        assert file_info["id"][:9] == "alice_49_"
        assert file_info["errors"] == []
        assert file_info["zip_filename"] is None


def test_upload_a_file_twice(testclient):
    with open("tests/assets/files/sleep.fit", "rb") as f:
        files = {"files": ("sleep.fit", f)}
        response = testclient.post("/files", files=files)
        response = testclient.post("/files", files=files)

        assert response.status_code == 200

        json_response: dict = response.json()
        assert len(json_response["data"]) == 1

        file_info = json_response["data"][0]
        assert file_info["filename"] == "sleep.fit"
        assert not file_info["accepted"]
        assert file_info["id"] is None
        assert file_info["errors"] == ["The document already exists"]
        assert file_info["zip_filename"] is None


def test_upload_not_extension_accepted_file(testclient):
    with open("tests/assets/files/file.txt", "rb") as f:
        files = {"files": ("file.txt", f)}
        response = testclient.post("/files", files=files)

        assert response.status_code == 200

        json_response: dict = response.json()
        assert len(json_response["data"]) == 1

        file_info = json_response["data"][0]
        assert file_info["filename"] == "file.txt"
        assert not file_info["accepted"]
        assert file_info["id"] is None
        assert file_info["errors"] == ["File extension not allowed"]
        assert file_info["zip_filename"] is None


def test_upload_zip_file(testclient):
    with open("tests/assets/files/2023-09-26.zip", "rb") as f:
        files = {"files": ("2023-09-26.zip", f)}
        response = testclient.post("/files", files=files)

        assert response.status_code == 200

        json_response: dict = response.json()
        assert len(json_response["data"]) == 13

        for fi in json_response["data"]:
            assert fi["filename"].lower().endswith(".fit")
            assert (
                (not fi["accepted"] and fi["id"] is None) or
                (fi["accepted"] and fi["id"] is not None)
            )
            assert "errors" in fi
            assert fi["zip_filename"] == "2023-09-26.zip"
