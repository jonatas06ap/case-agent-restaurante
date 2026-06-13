"""Calculadora — ferramenta LOCAL e determinística para tirar a aritmética da
cabeça do LLM (Dia 6).

Motivo (ver `Context/simulacao.md`): o modelo erra conta e ordenação quando faz
no texto — ordenou um ranking de receita errado, calculou 71/129 como 53% (é
55%). A correção é não deixar o LLM calcular: toda soma/média/percentual/contagem/
ordenação passa por esta tool, que roda em Python puro (sem `eval`, sem rede) e
devolve o número exato. O LLM cita o que a tool retornou — grounding, igual ao
dado da API.

A tool é injetada na lista de tools de TODO turno (ver `planner.build_tools`),
independente do RAG, e despachada localmente pelo executor (sem confirmação, sem
`DionisioClient`). É `local: True` no `fn_map`.
"""

from __future__ import annotations

import json

# Nome exposto ao LLM (formato function-calling da OpenAI: ^[a-zA-Z0-9_-]+$).
TOOL_NAME = "calcular"

# Marcador no fn_map que diz ao executor "despache local, não chame a API".
FN_MAP_ENTRY = {"local": True, "operation_id": "calc.calcular"}

_OPS = ("soma", "media", "minimo", "maximo", "contar", "percentual", "ordenar")


def build_tool() -> dict:
    """Schema da tool `calcular` no formato function-calling da OpenAI."""
    return {
        "type": "function",
        "function": {
            "name": TOOL_NAME,
            "description": (
                "Faz contas de forma exata: soma, media, minimo, maximo, contar, "
                "percentual e ordenar (ranking). USE SEMPRE que precisar de qualquer "
                "calculo ou ordenacao — nunca calcule de cabeca. Os numeros devem vir "
                "de dados ja observados (respostas da API)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "op": {
                        "type": "string",
                        "enum": list(_OPS),
                        "description": "A operacao a fazer.",
                    },
                    "valores": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Lista de numeros (soma/media/minimo/maximo/contar).",
                    },
                    "parte": {
                        "type": "number",
                        "description": "Numerador (op=percentual): quanto de 'total'.",
                    },
                    "total": {
                        "type": "number",
                        "description": "Denominador (op=percentual): o total de referencia.",
                    },
                    "itens": {
                        "type": "array",
                        "description": "Pares rotulo/valor para op=ordenar (ranking).",
                        "items": {
                            "type": "object",
                            "properties": {
                                "rotulo": {"type": "string"},
                                "valor": {"type": "number"},
                            },
                            "required": ["rotulo", "valor"],
                        },
                    },
                    "ordem": {
                        "type": "string",
                        "enum": ["desc", "asc"],
                        "description": "Ordem do ranking (op=ordenar). Default desc (maior->menor).",
                    },
                },
                "required": ["op"],
            },
        },
    }


def execute(args: dict) -> str:
    """Roda a operação e devolve a observação (JSON) que volta ao LLM.

    Erros viram observação textual com a lista de operações — nunca levanta
    exception que derrube o turno (mesmo contrato do executor da API).
    """
    op = (args or {}).get("op")
    try:
        resultado = _compute(op, args or {})
    except (TypeError, ValueError, ZeroDivisionError) as e:
        return json.dumps(
            {"erro": f"nao consegui calcular: {e}", "operacoes_validas": list(_OPS)},
            ensure_ascii=False,
        )
    return json.dumps(resultado, ensure_ascii=False)


# ---------------------------------------------------------------------------
def _nums(args: dict) -> list[float]:
    valores = args.get("valores")
    if not isinstance(valores, list) or not valores:
        raise ValueError("forneca 'valores' (lista de numeros nao vazia)")
    return [float(v) for v in valores]


def _compute(op: str, args: dict) -> dict:
    if op == "soma":
        valores = _nums(args)
        return {"op": op, "valores": valores, "resultado": sum(valores)}

    if op == "media":
        valores = _nums(args)
        return {"op": op, "valores": valores, "resultado": round(sum(valores) / len(valores), 4)}

    if op == "minimo":
        valores = _nums(args)
        return {"op": op, "valores": valores, "resultado": min(valores)}

    if op == "maximo":
        valores = _nums(args)
        return {"op": op, "valores": valores, "resultado": max(valores)}

    if op == "contar":
        valores = _nums(args)
        return {"op": op, "resultado": len(valores)}

    if op == "percentual":
        parte = float(args.get("parte"))
        total = float(args.get("total"))
        if total == 0:
            raise ZeroDivisionError("total nao pode ser zero")
        return {
            "op": op,
            "parte": parte,
            "total": total,
            "resultado_pct": round(parte / total * 100, 1),
        }

    if op == "ordenar":
        itens = args.get("itens")
        if not isinstance(itens, list) or not itens:
            raise ValueError("forneca 'itens' (lista de {rotulo, valor})")
        desc = (args.get("ordem") or "desc") != "asc"
        ranking = sorted(
            ({"rotulo": str(it["rotulo"]), "valor": float(it["valor"])} for it in itens),
            key=lambda x: x["valor"],
            reverse=desc,
        )
        return {"op": op, "ordem": "desc" if desc else "asc", "ranking": ranking}

    raise ValueError(f"operacao desconhecida '{op}'")
