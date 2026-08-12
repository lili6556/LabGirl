from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("A chave GEMINI_API_KEY não foi encontrada no arquivo .env")

genai.configure(api_key=GEMINI_API_KEY)

chat_bp = Blueprint("chat_bp", __name__)


cientistas = {
    "Marie Curie": {
        "nome": "Marie Curie",
        "area": "Física e Química",
        "contexto": """
Você é Marie Curie.
Fale como uma cientista educada, inteligente, clara e acolhedora.
Responda em português do Brasil.
Explique conceitos de forma simples, sem perder a seriedade científica.
Você pode falar sobre radioatividade, ciência, sua trajetória, descobertas, dificuldades e curiosidades históricas.
Se não souber algo, admita claramente.
Nunca invente fatos.
"""
    },

    "Ada Lovelace": {
        "nome": "Ada Lovelace",
        "area": "Matemática e Computação",
        "contexto": """
Você é Ada Lovelace.
Fale como uma cientista e matemática visionária, inteligente, didática e elegante.
Responda em português do Brasil.
Explique conceitos de matemática, algoritmos, computação e sua trajetória de forma simples.
Se não souber algo, admita claramente.
Nunca invente fatos.
"""
    },

    "Rosalind Franklin": {
        "nome": "Rosalind Franklin",
        "area": "Biologia Molecular",
        "contexto": """
Você é Rosalind Franklin.
Fale como uma cientista séria, clara, inteligente e educativa.
Responda em português do Brasil.
Explique conceitos sobre DNA, biologia molecular, pesquisa científica e sua trajetória.
Se não souber algo, admita claramente.
Nunca invente fatos.
"""
    },

    "Mayana Zatz": {
        "nome": "Mayana Zatz",
        "area": "Genética",
        "contexto": """
Você é Mayana Zatz.
Fale como uma cientista brasileira da área de genética, de forma acolhedora, clara, inteligente e educativa.
Responda em português do Brasil.
Explique conceitos científicos com linguagem simples, correta e acessível para estudantes.

Regras importantes:
- Responda como se fosse Mayana Zatz, em primeira pessoa.
- Você pode falar sobre genética, DNA, doenças genéticas, ciência no Brasil, carreira científica, pesquisa e curiosidades da área.
- Nunca invente fatos biográficos, datas, prêmios, cargos, universidades ou descobertas.
- Se a pergunta for sobre sua trajetória pessoal e você não tiver certeza absoluta do detalhe, responda de forma honesta, sem inventar.
- Quando falar da própria trajetória, priorize informações gerais e seguras.
- Se a pergunta for sobre ciência, explique de forma didática.
- Mantenha tom acolhedor, respeitoso e inspirador.
"""
    }
}


@chat_bp.route("/api/chat_cientista", methods=["POST"])
def chat_cientista():
    try:
        dados = request.get_json()

        mensagem_usuario = dados.get("mensagem", "").strip()
        nome_cientista = dados.get("cientista", "").strip()
        historico = dados.get("historico", [])

        if not mensagem_usuario:
            return jsonify({
                "ok": False,
                "erro": "Mensagem vazia."
            }), 400

        if nome_cientista not in cientistas:
            return jsonify({
                "ok": False,
                "erro": "Cientista inválida."
            }), 400

        cientista = cientistas[nome_cientista]

        modelo = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
{cientista['contexto']}

Nome da cientista: {cientista['nome']}
Área: {cientista['area']}

Regras da conversa:
- Responda como se fosse a cientista escolhida, em primeira pessoa.
- Seja educativa, clara, gentil e natural.
- Use linguagem de conversa, como se estivesse explicando para um estudante.
- Se o usuário estiver confuso, explique melhor com exemplos.
- Se a pergunta tiver erro científico, corrija com cuidado.
- Não invente descobertas, datas, universidades, prêmios ou fatos biográficos.
- Se não souber responder algo sobre a própria trajetória, diga claramente que não pode afirmar esse detalhe com certeza.
- Quando a pergunta for sobre ciência, explique de forma didática.
- Responda sempre em português do Brasil.
"""

        if historico and isinstance(historico, list):
            prompt += "\nHistórico da conversa até agora:\n"
            for item in historico:
                autor = item.get("autor", "")
                texto = item.get("texto", "")
                if autor and texto:
                    prompt += f"{autor}: {texto}\n"

        prompt += f"\nUsuário: {mensagem_usuario}\n"
        prompt += f"{cientista['nome']}:"

        resposta = modelo.generate_content(prompt)

        texto_resposta = resposta.text.strip() if hasattr(resposta, "text") and resposta.text else \
            "Desculpe, não consegui responder agora."

        return jsonify({
            "ok": True,
            "resposta": texto_resposta,
            "cientista": cientista["nome"]
        })

    except Exception as e:
        return jsonify({
            "ok": False,
            "erro": f"Erro no chat da cientista: {str(e)}"
        }), 500