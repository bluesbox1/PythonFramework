import pytest
import requests
import json
import yaml
from jsonschema import validate, ValidationError

# Load JSON schema
with open('./schema/contract1.json') as f:
    schema = json.load(f)

# Load test steps from YAML
with open('./config/steps/api_steps.yaml') as f:
    test_steps = yaml.safe_load(f)['tests']

@pytest.mark.parametrize("test_case", test_steps, ids=[step['name'] for step in test_steps])
def test_api(test_case):
    url = f"https://reqres.in/{test_case['endpoint']}"
    method = test_case['method']
    expected_status = test_case['expected_status']

    response = requests.request(method, url)
    assert response.status_code == expected_status, f"Expected status {expected_status}, got {response.status_code}"

    if expected_status == 200:
        try:
            validate(instance=response.json(), schema=schema)
        except ValidationError as e:
            pytest.fail(f"Response JSON does not match schema: {e.message}")