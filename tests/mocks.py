def mock_app_context(mock, id, ac_type, authorized=True):
    mock.identity.return_value = id
    mock.account_type.return_value = ac_type
    mock.authenticated.return_value = authorized
    return mock