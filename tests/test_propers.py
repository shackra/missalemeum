from datetime import date
from exceptions import InvalidInput, ProperNotFound

import pytest

from constants import common as c
from kalendar.models import Observance
from propers.models import ProperConfig
from propers.parser import ProperParser
from tests.conftest import get_missal

language = 'Polski'


def test_parse_proper_no_refs():
    proper_vernacular, proper_latin = ProperParser.parse(c.SANCTI_01_06, language)

    assert 'Objawienie' in proper_vernacular.title
    assert 1 == proper_vernacular.rank
    assert '«Obchodzimy dzień święty' in proper_vernacular.description
    assert 'Stacja u Św. Piotra' in proper_vernacular.additional_info
    assert 'Szaty białe' in proper_vernacular.additional_info
    assert 'Ml 3:1' in proper_vernacular.get_section('Introitus').body[0]
    assert 'Boże, w dniu dzisiejszym' in proper_vernacular.get_section('Oratio').body[0]
    assert '*Iz 60:1-6*' in proper_vernacular.get_section('Lectio').body[1]
    assert 'Iz 60:6; 60:1' in proper_vernacular.get_section('Graduale').body[0]
    assert '*Mt 2:1-12*' in proper_vernacular.get_section('Evangelium').body[1]
    assert 'Ps 71:10-11' in proper_vernacular.get_section('Offertorium').body[0]
    assert 'Wejrzyj miłościwie' in proper_vernacular.get_section('Secreta').body[0]
    assert 'Mt 2:2' in proper_vernacular.get_section('Communio').body[0]
    assert 'Spraw, prosimy,' in proper_vernacular.get_section('Postcommunio').body[0]
    assert 'Prefacja o Objawieniu' in proper_vernacular.get_section('Prefatio').body[0]

    assert 'Malach 3:1' in proper_latin.get_section('Introitus').body[0]
    assert 'Deus, qui hodiérna die' in proper_latin.get_section('Oratio').body[0]
    assert '*Is 60:1-6*' in proper_latin.get_section('Lectio').body[1]
    assert '*Isa 60:6; 60:1*' in proper_latin.get_section('Graduale').body[0]
    assert '*Matt 2:1-12*' in proper_latin.get_section('Evangelium').body[1]
    assert '*Ps 71:10-11*' in proper_latin.get_section('Offertorium').body[0]
    assert 'Ecclésiæ tuæ, quǽsumus' in proper_latin.get_section('Secreta').body[0]
    assert '*Matt 2:2*' in proper_latin.get_section('Communio').body[0]
    assert 'Præsta, quǽsumus, omnípotens' in proper_latin.get_section('Postcommunio').body[0]
    assert '*de Epiphania Domini*' in proper_latin.get_section('Prefatio').body[0]


def test_parse_proper_refs_inside_sections_and_in_vide():
    proper_vernacular, proper_latin = ProperParser.parse(c.SANCTI_01_22, language)

    assert 'Śś. Wincentego' in proper_vernacular.title
    assert '*Ps 78:11-12; 78:10*' in proper_vernacular.get_section('Introitus').body[0]
    assert 'Przychyl się, Panie,' in proper_vernacular.get_section('Oratio').body[0]
    assert '*Mdr 3:1-8*' in proper_vernacular.get_section('Lectio').body[1]
    assert '*Wj 15:11*' in proper_vernacular.get_section('Graduale').body[0]
    assert '*Wj 15:11*' in proper_vernacular.get_section('Tractus').body[0]
    assert '*Łk 21:9-19*' in proper_vernacular.get_section('Evangelium').body[1]
    assert '*Ps 67:36*' in proper_vernacular.get_section('Offertorium').body[0]
    assert 'Ofiarujemy Ci, Panie, te dary' in proper_vernacular.get_section('Secreta').body[0]
    assert '*Mdr 3:4-6*' in proper_vernacular.get_section('Communio').body[0]
    assert 'Prosimy Cię, wszechmogący' in proper_vernacular.get_section('Postcommunio').body[0]
    assert 'Prefacja zwykła' in proper_vernacular.get_section('Prefatio').body[0]

    assert '*Ps 78:11-12; 78:10*' in proper_latin.get_section('Introitus').body[0]
    assert 'Adésto, Dómine, supplicatiónibus' in proper_latin.get_section('Oratio').body[0]
    assert '*Sap 3:1-8*' in proper_latin.get_section('Lectio').body[1]
    assert '*Exod 15:11*' in proper_latin.get_section('Graduale').body[0]
    assert '*Exod 15:11*' in proper_latin.get_section('Tractus').body[0]
    assert '*Luc 21:9-19*' in proper_latin.get_section('Evangelium').body[1]
    assert '*Ps 67:36*' in proper_latin.get_section('Offertorium').body[0]
    assert 'Múnera tibi, Dómine,' in proper_latin.get_section('Secreta').body[0]
    assert '*Sap 3:4-6*' in proper_latin.get_section('Communio').body[0]
    assert 'Quǽsumus, omnípotens Deus:' in proper_latin.get_section('Postcommunio').body[0]
    assert '*Communis*' in proper_latin.get_section('Prefatio').body[0]


def test_parse_proper_ref_outside_sections():
    proper_vernacular, proper_latin = ProperParser.parse(c.SANCTI_10_DUr, language)
    assert 'Chrystusa Króla' in proper_vernacular.title
    assert '*Ap 5:12; 1:6*' in proper_vernacular.get_section('Introitus').body[0]
    assert '*Apoc 5:12; 1:6*' in proper_latin.get_section('Introitus').body[0]


def test_invalid_proper_id():
    with pytest.raises(InvalidInput):
        ProperParser.parse('bla', language)


def test_proper_not_found():
    with pytest.raises(ProperNotFound):
        ProperParser.parse('tempora:bla', language)


def test_get_proper_from_observance():
    proper_vernacular, proper_latin = Observance(c.SANCTI_01_06, date(2018, 1, 6), language).get_proper()
    assert 'Objawienie' in proper_vernacular.title
    assert 'Ml 3:1' in proper_vernacular.get_section('Introitus').body[0]
    assert 'Malach 3:1' in proper_latin.get_section('Introitus').body[0]
    assert 'Deus, qui hodiérna die' in proper_latin.get_section('Oratio').body[0]


def test_get_proper_from_day():
    missal = get_missal(2018, language)
    proper_vernacular, proper_latin = missal.get_day(date(2018, 1, 6)).get_proper()[0]
    assert 'Objawienie' in proper_vernacular.title
    assert 'Ml 3:1' in proper_vernacular.get_section('Introitus').body[0]
    assert 'Malach 3:1' in proper_latin.get_section('Introitus').body[0]
    assert 'Deus, qui hodiérna die' in proper_latin.get_section('Oratio').body[0]


@pytest.mark.parametrize("date_,proper", [
    ((2018, 1, 4), 'In Circumcisione Domini'),
    ((2018, 1, 12), 'Dominica infra Octavam Epiphaniae'),  # Feast of the Holy Family
    ((2018, 2, 13), 'Dominica in Quinquagesima'),
    ((2018, 7, 4), 'Dominica VI Post Pentecosten'),
    ((2018, 7, 9), 'Dominica VII Post Pentecosten'),  # Feast of the Most Precious Blood
    ((2018, 10, 31), 'Dominica XXIII Post Pentecosten'),  # Feast of Christ the King
])
def test_get_proper_for_day_without_own_proper(date_, proper):
    # For days without their own propers we show the proper from the last Sunday
    missal = get_missal(date_[0], language)
    _, proper_latin = missal.get_day(date(*date_)).get_proper()[0]
    assert proper in proper_latin.get_section('Rank').body[0]


def test_get_repr():
    missal = get_missal(2018, language)
    container = missal.get_day(date(2018, 1, 13))
    assert 'Sobota po 1 Niedzieli po Objawieniu' in container.get_tempora_name()
    assert 'Wspomnienie Chrztu Pańskiego' in container.get_celebration_name()
    assert str(container) == '[<tempora:Epi1-6:4>][<sancti:01-13:2>][]'


@pytest.mark.parametrize("date_,sections", [
    ((2018, 12, 11), ['Commemoratio Oratio', 'Commemoratio Secreta', 'Commemoratio Postcommunio']),
    ((2018, 12, 7), ['Commemoratio Oratio', 'Commemoratio Secreta', 'Commemoratio Postcommunio']),
    ((2018, 12, 6), ['Rank1570']),
    ((2019, 3, 25), ['Graduale'])
])
def test_ignored_sections(date_, sections):
    missal = get_missal(date_[0], language)
    _, proper_latin = missal.get_day(date(*date_)).get_proper()[0]
    for section in sections:
        assert proper_latin.get_section(section) is None


@pytest.mark.parametrize("date_,preface_body", [
    ((2018, 10, 28), '*de D.N. Jesu Christi Rege*'),  # Christ the King
    ((2018, 12, 16), '*de sanctissima Trinitate*'),  # 3rd Sunday of Advent - should be Trinity
    ((2018, 12, 17), '*Communis*'),  # Monday after 3rd Sunday of Advent - should be Communis
    ((2019, 6, 24), '*Communis*'),  # Nativity of John Baptist - should be Communis, but in source files it's st. John
    ((2019, 4, 27), '*Paschalis*'),
    ((2019, 4, 30), '*Paschalis*'),
    ((2019, 5, 1), '*de S. Joseph*'),
    ((2019, 1, 25), '*de Apostolis*'),  # Conversion of st. Paul the Apostle
    ((2019, 7, 25), '*de Apostolis*'),  # st. James, the Apostle
    ((2019, 12, 21), '*de Apostolis*'),  # st. Thomas, the Apostle
])
def test_correct_preface_calculated_by_date(date_, preface_body):
    missal = get_missal(date_[0], language)
    _, proper = missal.get_day(date(*date_)).get_proper()[0]
    assert preface_body == proper.get_section('Prefatio').get_body()[0]


@pytest.mark.parametrize("proper_id,preface_name,preface_body", [
    ('tempora:Adv2-0', 'Communis', '*Communis*'),
    ('tempora:Adv2-0', 'Trinitate', '*de sanctissima Trinitate*'),
])
def test_correct_preface_calculated_by_proper_id(proper_id, preface_name, preface_body):
    _, proper = ProperParser.parse(proper_id, language, ProperConfig(preface=preface_name))
    assert preface_body == proper.get_section('Prefatio').get_body()[0]
