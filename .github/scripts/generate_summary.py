"""
Gera um summary em Markdown para o GitHub Actions a partir do JUnit XML.
Uso: python generate_summary.py <junit_xml_path> <titulo>
"""

import sys
import xml.etree.ElementTree as ET
from collections import defaultdict


def parse_junit(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    suites = root.findall(".//testsuite")
    if not suites:
        suites = [root] if root.tag == "testsuite" else []

    tests = []
    for suite in suites:
        for tc in suite.findall("testcase"):
            classname = tc.get("classname", "")
            name = tc.get("name", "")
            time_s = float(tc.get("time", "0"))

            failure = tc.find("failure")
            error = tc.find("error")
            skipped = tc.find("skipped")

            if failure is not None:
                status = "failed"
                message = failure.get("message", "")
            elif error is not None:
                status = "error"
                message = error.get("message", "")
            elif skipped is not None:
                status = "skipped"
                message = skipped.get("message", "")
            else:
                status = "passed"
                message = ""

            tests.append({
                "classname": classname,
                "name": name,
                "time": time_s,
                "status": status,
                "message": message,
            })

    return tests


def get_endpoint_from_class(classname):
    mapping = {
        "TestLoginComSucesso": "POST /login",
        "TestLoginComFalha": "POST /login",
        "TestLoginSeguranca": "POST /login",
        "TestListarUsuarios": "GET /usuarios",
        "TestBuscarUsuarioPorId": "GET /usuarios/{id}",
        "TestCadastrarUsuario": "POST /usuarios",
        "TestCadastrarUsuarioCamposObrigatorios": "POST /usuarios",
        "TestCadastrarUsuarioValidacaoEmail": "POST /usuarios",
        "TestEditarUsuario": "PUT /usuarios/{id}",
        "TestExcluirUsuario": "DELETE /usuarios/{id}",
        "TestListarProdutos": "GET /produtos",
        "TestCadastrarProduto": "POST /produtos",
        "TestEditarProduto": "PUT /produtos/{id}",
        "TestExcluirProduto": "DELETE /produtos/{id}",
        "TestListarCarrinhos": "GET /carrinhos",
        "TestBuscarCarrinhoPorId": "GET /carrinhos/{id}",
        "TestCadastrarCarrinho": "POST /carrinhos",
        "TestConcluirCompra": "DELETE /carrinhos/concluir",
        "TestCancelarCompra": "DELETE /carrinhos/cancelar",
        "TestFluxoCompraCompleto": "E2E Flows",
    }
    cls = classname.rsplit(".", 1)[-1] if "." in classname else classname
    return mapping.get(cls, classname)


def status_icon(status):
    return {"passed": "\u2705", "failed": "\u274c", "error": "\U0001f4a5", "skipped": "\u23ed\ufe0f"}.get(status, "\u2753")


def generate_markdown(tests, title):
    total = len(tests)
    passed = sum(1 for t in tests if t["status"] == "passed")
    failed = sum(1 for t in tests if t["status"] == "failed")
    errors = sum(1 for t in tests if t["status"] == "error")
    skipped = sum(1 for t in tests if t["status"] == "skipped")
    total_time = sum(t["time"] for t in tests)
    pass_rate = (passed / total * 100) if total > 0 else 0

    lines = []

    # Header
    lines.append(f"# \U0001f9ea {title}\n")

    # Summary cards
    if failed == 0 and errors == 0:
        lines.append("> \u2705 **Todos os testes passaram com sucesso!**\n")
    else:
        lines.append(f"> \u274c **{failed + errors} teste(s) falharam**\n")

    lines.append(f"| Metrica | Valor |")
    lines.append(f"|---|---|")
    lines.append(f"| \U0001f4ca Total de testes | **{total}** |")
    lines.append(f"| \u2705 Passou | **{passed}** |")
    lines.append(f"| \u274c Falhou | **{failed}** |")
    lines.append(f"| \U0001f4a5 Erro | **{errors}** |")
    lines.append(f"| \u23ed\ufe0f Ignorado | **{skipped}** |")
    lines.append(f"| \u23f1\ufe0f Tempo total | **{total_time:.1f}s** |")
    lines.append(f"| \U0001f3af Taxa de sucesso | **{pass_rate:.1f}%** |")
    lines.append("")

    # Progress bar
    bar_len = 30
    filled = int(bar_len * pass_rate / 100)
    bar = "\U0001f7e9" * filled + "\U0001f7e5" * (bar_len - filled)
    lines.append(f"### Taxa de Sucesso: {pass_rate:.1f}%")
    lines.append(f"`{bar}` {passed}/{total}\n")

    # Results by endpoint
    by_endpoint = defaultdict(list)
    for t in tests:
        ep = get_endpoint_from_class(t["classname"])
        by_endpoint[ep].append(t)

    lines.append("## \U0001f4cb Resultado por Endpoint\n")
    lines.append("| Endpoint | Testes | Passou | Falhou | Tempo |")
    lines.append("|---|---|---|---|---|")

    for ep in sorted(by_endpoint.keys()):
        ep_tests = by_endpoint[ep]
        ep_total = len(ep_tests)
        ep_passed = sum(1 for t in ep_tests if t["status"] == "passed")
        ep_failed = ep_total - ep_passed
        ep_time = sum(t["time"] for t in ep_tests)
        icon = "\u2705" if ep_failed == 0 else "\u274c"
        lines.append(f"| {icon} `{ep}` | {ep_total} | {ep_passed} | {ep_failed} | {ep_time:.1f}s |")

    lines.append("")

    # Detailed test list
    lines.append("<details>")
    lines.append("<summary><strong>\U0001f50d Detalhamento de todos os testes</strong></summary>\n")
    lines.append("| Status | Teste | Tempo |")
    lines.append("|---|---|---|")

    for t in sorted(tests, key=lambda x: (x["status"] != "failed", x["classname"], x["name"])):
        icon = status_icon(t["status"])
        cls = t["classname"].rsplit(".", 1)[-1] if "." in t["classname"] else t["classname"]
        test_name = t["name"].replace("[", "\\[").replace("]", "\\]")
        lines.append(f"| {icon} | `{cls}` > {test_name} | {t['time']:.2f}s |")

    lines.append("\n</details>\n")

    # Failures detail
    failures = [t for t in tests if t["status"] in ("failed", "error")]
    if failures:
        lines.append("## \u274c Detalhes das Falhas\n")
        for t in failures:
            lines.append(f"### `{t['name']}`")
            lines.append(f"**Classe:** `{t['classname']}`\n")
            lines.append(f"```")
            lines.append(t["message"][:500])
            lines.append(f"```\n")

    # Top 5 slowest
    slowest = sorted(tests, key=lambda x: x["time"], reverse=True)[:5]
    lines.append("## \U0001f422 Top 5 Testes Mais Lentos\n")
    lines.append("| Teste | Tempo |")
    lines.append("|---|---|")
    for t in slowest:
        lines.append(f"| `{t['name']}` | {t['time']:.2f}s |")

    lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    xml_path = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else "Test Report"

    tests = parse_junit(xml_path)
    print(generate_markdown(tests, title))
