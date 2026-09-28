from chain_intelligence import classify_chain


def test_ethereum_chain():
    assert classify_chain("ethereum") == "ethereum"


def test_bnb_chain():
    assert classify_chain("bnb_chain") == "bnb_chain"


def test_solana_chain():
    assert classify_chain("solana") == "solana"


def test_base_chain():
    assert classify_chain("base") == "base"


def test_arbitrum_chain():
    assert classify_chain("arbitrum") == "arbitrum"


def test_unknown_chain():
    assert classify_chain("unknown_chain") == "unknown"


def test_empty_chain():
    assert classify_chain("") == "unknown"


def test_non_string_chain():
    assert classify_chain(None) == "unknown"


def test_chain_is_case_insensitive():
    assert classify_chain("ETHEREUM") == "ethereum"


def test_chain_whitespace_is_normalized():
    assert classify_chain("  solana  ") == "solana"
