from pathlib import Path
from kremover.retentions import get_client_retentions

cur_dir = Path(__file__).parent
retentions_file = cur_dir / 'retentions.json'


def test_retentions_default_100days():

    retentions = get_client_retentions(default=100, clients_file=retentions_file)
    assert 100 == retentions['some_default_client']
    assert 100 == retentions['another_random_client']


def test_retentions_default_30days():
    retentions = get_client_retentions(default=30, clients_file=retentions_file)
    assert 30 == retentions['some_default_client']
    assert 30 == retentions['another_random_client']


def test_retentions_custom_client_with_50_days_retention():
    retentions = get_client_retentions(default=30, clients_file=retentions_file)
    assert 50 == retentions["client_with_50days"]

