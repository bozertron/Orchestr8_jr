"""Unit tests for settlement_survey.py schema module."""

import pytest
from IP.contracts.settlement_survey import (
    SettlementSurvey,
    FiefdomData,
    BoundaryContract,
    WiringConnection,
    WiringStatus,
    parse_settlement_survey,
    EXAMPLE_SURVEY,
)


def test_parse_example_survey():
    """Test that EXAMPLE_SURVEY parses correctly."""
    survey = parse_settlement_survey(EXAMPLE_SURVEY)

    assert survey.metadata == {"project": "Orchestr8", "timestamp": "2026-02-13"}
    assert "core" in survey.fiefdoms
    assert survey.fiefdoms["core"].name == "core"
    assert survey.fiefdoms["core"].files == ["orchestr8.py"]
    assert survey.boundary_contracts == []
    assert survey.wiring_state == []


def test_missing_required_field_metadata():
    """Test that missing metadata raises ValueError."""
    data = {
        "fiefdoms": {},
        "boundary_contracts": [],
        "wiring_state": [],
    }

    with pytest.raises(ValueError, match="Missing required survey field: metadata"):
        parse_settlement_survey(data)


def test_missing_required_field_fiefdoms():
    """Test that missing fiefdoms raises ValueError."""
    data = {
        "metadata": {},
        "boundary_contracts": [],
        "wiring_state": [],
    }

    with pytest.raises(ValueError, match="Missing required survey field: fiefdoms"):
        parse_settlement_survey(data)


def test_missing_required_field_boundary_contracts():
    """Test that missing boundary_contracts raises ValueError."""
    data = {
        "metadata": {},
        "fiefdoms": {},
        "wiring_state": [],
    }

    with pytest.raises(
        ValueError, match="Missing required survey field: boundary_contracts"
    ):
        parse_settlement_survey(data)


def test_missing_required_field_wiring_state():
    """Test that missing wiring_state raises ValueError."""
    data = {
        "metadata": {},
        "fiefdoms": {},
        "boundary_contracts": [],
    }

    with pytest.raises(ValueError, match="Missing required survey field: wiring_state"):
        parse_settlement_survey(data)


def test_fiefdom_parsing():
    """Test that fiefdom data is correctly parsed into FiefdomData objects."""
    data = {
        "metadata": {},
        "fiefdoms": {
            "test_fiefdom": {
                "name": "test_fiefdom",
                "files": ["file1.py", "file2.py"],
                "entry_points": ["file1.py"],
                "exports": ["func1", "func2"],
                "internal_coupling": 0.8,
                "external_coupling": 0.2,
            }
        },
        "boundary_contracts": [],
        "wiring_state": [],
    }

    survey = parse_settlement_survey(data)

    assert "test_fiefdom" in survey.fiefdoms
    fiefdom = survey.fiefdoms["test_fiefdom"]
    assert isinstance(fiefdom, FiefdomData)
    assert fiefdom.name == "test_fiefdom"
    assert fiefdom.files == ["file1.py", "file2.py"]
    assert fiefdom.entry_points == ["file1.py"]
    assert fiefdom.exports == ["func1", "func2"]
    assert fiefdom.internal_coupling == 0.8
    assert fiefdom.external_coupling == 0.2


def test_wiring_status_enum_mapping():
    """Test that wiring status strings are correctly mapped to WiringStatus enum."""
    data = {
        "metadata": {},
        "fiefdoms": {},
        "boundary_contracts": [],
        "wiring_state": [
            {"source": "a.py", "target": "b.py", "status": "working"},
            {"source": "c.py", "target": "d.py", "status": "broken"},
            {"source": "e.py", "target": "f.py", "status": "combat"},
        ],
    }

    survey = parse_settlement_survey(data)

    assert len(survey.wiring_state) == 3
    assert survey.wiring_state[0].status == WiringStatus.WORKING
    assert survey.wiring_state[1].status == WiringStatus.BROKEN
    assert survey.wiring_state[2].status == WiringStatus.COMBAT


def test_empty_collections_are_valid():
    """Test that empty collections are valid for all list fields."""
    data = {
        "metadata": {"test": "data"},
        "fiefdoms": {},
        "boundary_contracts": [],
        "wiring_state": [],
    }

    survey = parse_settlement_survey(data)

    assert survey.metadata == {"test": "data"}
    assert survey.fiefdoms == {}
    assert survey.boundary_contracts == []
    assert survey.wiring_state == []


def test_boundary_contract_parsing():
    """Test that boundary contracts are correctly parsed."""
    data = {
        "metadata": {},
        "fiefdoms": {},
        "boundary_contracts": [
            {
                "from_fiefdom": "core",
                "to_fiefdom": "plugins",
                "allowed_types": ["function", "class"],
                "forbidden_crossings": ["private_func"],
                "contract_status": "defined",
            }
        ],
        "wiring_state": [],
    }

    survey = parse_settlement_survey(data)

    assert len(survey.boundary_contracts) == 1
    contract = survey.boundary_contracts[0]
    assert isinstance(contract, BoundaryContract)
    assert contract.from_fiefdom == "core"
    assert contract.to_fiefdom == "plugins"
    assert contract.allowed_types == ["function", "class"]
    assert contract.forbidden_crossings == ["private_func"]
    assert contract.contract_status == "defined"


def test_wiring_connection_agents_active_default():
    """Test that agents_active defaults to False in WiringConnection."""
    data = {
        "metadata": {},
        "fiefdoms": {},
        "boundary_contracts": [],
        "wiring_state": [
            {"source": "a.py", "target": "b.py", "status": "working"}
        ],
    }

    survey = parse_settlement_survey(data)

    assert survey.wiring_state[0].agents_active is False


def test_wiring_connection_agents_active_true():
    """Test that agents_active can be set to True."""
    data = {
        "metadata": {},
        "fiefdoms": {},
        "boundary_contracts": [],
        "wiring_state": [
            {
                "source": "a.py",
                "target": "b.py",
                "status": "combat",
                "agents_active": True,
            }
        ],
    }

    survey = parse_settlement_survey(data)

    assert survey.wiring_state[0].agents_active is True


def test_multiple_fiefdoms():
    """Test parsing multiple fiefdoms."""
    data = {
        "metadata": {},
        "fiefdoms": {
            "core": {
                "name": "core",
                "files": ["core.py"],
                "entry_points": ["core.py"],
                "exports": ["Core"],
                "internal_coupling": 0.9,
                "external_coupling": 0.1,
            },
            "plugins": {
                "name": "plugins",
                "files": ["plugin1.py", "plugin2.py"],
                "entry_points": ["plugin1.py"],
                "exports": ["Plugin1", "Plugin2"],
                "internal_coupling": 0.7,
                "external_coupling": 0.3,
            },
        },
        "boundary_contracts": [],
        "wiring_state": [],
    }

    survey = parse_settlement_survey(data)

    assert len(survey.fiefdoms) == 2
    assert "core" in survey.fiefdoms
    assert "plugins" in survey.fiefdoms
    assert survey.fiefdoms["core"].files == ["core.py"]
    assert survey.fiefdoms["plugins"].files == ["plugin1.py", "plugin2.py"]


def test_complex_survey():
    """Test parsing a complex survey with all fields populated."""
    data = {
        "metadata": {"project": "TestProject", "version": "1.0.0"},
        "fiefdoms": {
            "core": {
                "name": "core",
                "files": ["core.py"],
                "entry_points": ["core.py"],
                "exports": ["CoreFunc"],
                "internal_coupling": 0.9,
                "external_coupling": 0.2,
            }
        },
        "boundary_contracts": [
            {
                "from_fiefdom": "core",
                "to_fiefdom": "plugins",
                "allowed_types": ["function"],
                "forbidden_crossings": [],
                "contract_status": "defined",
            }
        ],
        "wiring_state": [
            {
                "source": "core.py",
                "target": "plugin.py",
                "status": "working",
                "agents_active": False,
            }
        ],
    }

    survey = parse_settlement_survey(data)

    assert survey.metadata["project"] == "TestProject"
    assert len(survey.fiefdoms) == 1
    assert len(survey.boundary_contracts) == 1
    assert len(survey.wiring_state) == 1
    assert isinstance(survey.wiring_state[0], WiringConnection)
