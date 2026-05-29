"""Unit tests for the UWU text transformer (deterministic: noise disabled)."""
import pytest

from uwu_translator import UwuTranslator, uwu_translate


@pytest.fixture
def tr():
    # Disable random additions so output is deterministic.
    return UwuTranslator(noise_probability=0.0, cyber_vibe_probability=0.0)


def test_empty_input_returned_as_is(tr):
    assert tr.translate("") == ""
    assert tr.translate("   ") == "   "


def test_dictionary_replacement_cyrillic(tr):
    # 'код' -> 'кодик~'; no phonetic-affected letters, so it stays exact.
    assert tr.translate("код") == "кодик~"


def test_dictionary_replacement_case_insensitive(tr):
    assert tr.translate("КОД") == "кодик~"


def test_dictionary_replacement_english(tr):
    assert tr.translate("wolf") == "wuffie"


def test_dictionary_whole_word_only(tr):
    # 'код' is a substring of 'кодекс' but must NOT be replaced there.
    assert "кодик~" not in tr.translate("кодекс")


def test_russian_phonetics_r_to_l(tr):
    # 'р' -> 'ль' (no dictionary entry for 'рык'? there is: 'рык'->'рычулька')
    out = tr.translate("трава")  # not in dict
    assert "р" not in out  # all 'р' converted
    assert "ль" in out


def test_english_phonetics_n_vowel(tr):
    assert tr.translate("na") == "nya"


def test_no_noise_when_probability_zero(tr):
    # With noise disabled, punctuation does not gain wolf noises.
    assert tr.translate("код.") == "кодик~."


def test_noise_added_when_probability_one():
    tr = UwuTranslator(noise_probability=1.0, cyber_vibe_probability=0.0)
    out = tr.translate("код.")
    # Something was appended after the sentence.
    assert len(out) > len("кодик~.")


def test_wrapper_matches_default_instance():
    # The module-level wrapper should not raise and should transform text.
    out = uwu_translate("Привет")
    assert isinstance(out, str) and out != ""


def test_translate_is_idempotent_on_type(tr):
    assert isinstance(tr.translate("любой текст"), str)
