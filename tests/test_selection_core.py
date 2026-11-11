"""Example tests (happy path only). They import only selection_core: the lesson 4 test rule."""
import copy

import pytest

import selection_core

from baseline.tasks import first_missing


@pytest.mark.req("REQ-SEL-01")
def test_valid_selection_is_returned(sample_event):
    selection = selection_core.submit_selection(sample_event, "cli_100", ["med_1"], ["add_to_album"])
    assert selection["media_ids"] == ["med_1"]
    assert selection["service_codes"] == ["add_to_album"]


@pytest.mark.req("REQ-SEL-01")
def test_valid_selection_is_recorded_on_the_event(sample_event):
    selection_core.submit_selection(sample_event, "cli_100", ["med_1", "med_2"], ["add_to_album"])
    assert len(sample_event["selections"]) == 1


@pytest.mark.req("REQ-SEL-03")
def test_available_services_lists_enabled_services_only(sample_event):
    assert selection_core.available_services(sample_event) == ["add_to_album"]


@pytest.mark.req("REQ-SEL-02")
def test_media_from_another_event_is_rejected(sample_event):
    with pytest.raises(selection_core.SelectionError) as err:
        selection_core.submit_selection(
            sample_event, "cli_100", ["med_9"], ["add_to_album"])
    assert err.value.code == "MEDIA_NOT_IN_EVENT"


@pytest.mark.req("REQ-SEL-05")
def test_duplicate_media_is_rejected(sample_event):
    with pytest.raises(selection_core.SelectionError) as err:
        selection_core.submit_selection(
            sample_event, "cli_100", ["med_1", "med_1"], ["add_to_album"])
    assert err.value.code == "DUPLICATE_MEDIA"


@pytest.mark.req("REQ-SEL-04")
def test_rejected_selection_does_not_change_the_event(sample_event):
    before = copy.deepcopy(sample_event)
    with pytest.raises(selection_core.SelectionError):
        selection_core.submit_selection(sample_event, "cli_100", ["med_1"], ["print_10x15"])
    assert sample_event == before


@pytest.mark.req("REQ-SEL-06")
def test_only_the_events_client_may_select(sample_event):
    with pytest.raises(selection_core.SelectionError) as err:
        selection_core.submit_selection(sample_event, "cli_200", ["med_1"], ["add_to_album"])
    assert err.value.code == "FORBIDDEN"    

@pytest.mark.req("BASELINE-04")
def test_first_missing_returns_first_required_item_not_present():
    assert first_missing(["a", "b", "c"], ["a", "c"]) == "b"
    assert first_missing(["a", "b", "c"], ["c"]) == "a"
    assert first_missing(["a", "b"], ["a", "b"]) is None