from jsonschema import validate, ValidationError


def validar_contrato(response_json: dict, schema: dict):
    """Valida o JSON de resposta contra o schema fornecido.
    Levanta AssertionError com detalhes se a validacao falhar."""
    try:
        validate(instance=response_json, schema=schema)
    except ValidationError as e:
        raise AssertionError(
            f"Falha na validacao de contrato: {e.message}\n"
            f"Campo: {'.'.join(str(p) for p in e.absolute_path)}\n"
            f"Schema esperado: {e.schema}"
        ) from e
