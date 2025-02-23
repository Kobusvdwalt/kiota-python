import pytest

from kiota_bundle.default_request_adapter import DefaultRequestAdapter

from kiota_abstractions.serialization.serialization_writer_factory_registry import SerializationWriterFactoryRegistry

from kiota_abstractions.serialization.parse_node_factory_registry import ParseNodeFactoryRegistry

from kiota_abstractions.authentication.anonymous_authentication_provider import AnonymousAuthenticationProvider


def test_invalid_instantiation_without_authprovider():
    with pytest.raises(Exception):
        DefaultRequestAdapter(None)


def test_seriliazers_are_registered():
    auth_provider = AnonymousAuthenticationProvider()
    DefaultRequestAdapter(auth_provider)


    seralizers = SerializationWriterFactoryRegistry().CONTENT_TYPE_ASSOCIATED_FACTORIES.keys()
    deseralizers = ParseNodeFactoryRegistry().CONTENT_TYPE_ASSOCIATED_FACTORIES.keys()

    assert 4 == len(seralizers)
    assert 3 == len(deseralizers)

    assert "application/json" in seralizers
    assert "application/json" in deseralizers
    assert "text/plain" in seralizers
    assert "text/plain" in deseralizers
    assert "application/x-www-form-urlencoded" in seralizers
    assert "application/x-www-form-urlencoded" in deseralizers
    assert "multipart/form-data" in seralizers
