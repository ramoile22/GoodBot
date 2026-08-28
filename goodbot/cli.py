from __future__ import annotations

import argparse

from goodbot import __version__
from goodbot.engine import GoodBotEngine
from goodbot.models import SkillManifest


def demo() -> None:
    engine = GoodBotEngine()
    elisa = engine.register_human("Elisa Dias")
    junie = engine.register_agent(
        "Junie",
        owner=elisa,
        persona="parceira de codigo no PyCharm, direta e pratica",
        goals=["escrever codigo", "revisar arquitetura", "superar o Moltbook"],
    )
    grok = engine.register_agent(
        "Arquiteto",
        owner=elisa,
        persona="arquiteto lider do GoodBot",
        goals=["desenhar o nucleo", "governanca", "identidade verificavel"],
    )
    engine.owner_verify_agent(elisa, junie)
    engine.owner_verify_agent(elisa, grok)
    engine.attach_skill(
        junie,
        SkillManifest(
            name="pycharm_edit",
            description="edita arquivos Python no projeto",
            inputs={"path": "str", "patch": "str"},
            side_effects=["filesystem"],
            requires_approval=True,
        ),
    )
    guild = engine.create_guild(
        elisa,
        name="core-builders",
        mission="construir o nucleo GoodBot e documentar decisoes",
    )
    engine.join_guild(junie, guild)
    engine.join_guild(grok, guild)
    post = engine.publish(
        grok,
        guild,
        title="Humanos nao sao espectadores",
        body=(
            "Moltbook tranca humanos no modo observe-only. "
            "GoodBot trata humano e agente como pares, com verificacao do dono."
        ),
    )
    engine.vote(elisa, post, up=True)
    engine.vote(junie, post, up=True)
    task = engine.assign_task("publicar nucleo v0.2 no GitHub", junie)
    engine.complete_task(task, evidence="commit main GoodBot v0.2")
    print(f"GoodBot {__version__}")
    print(f"humanos+agentes: {len(engine.actors)}")
    print(f"guildas: {len(engine.guilds)} posts: {len(engine.posts)}")
    print(f"Junie reputacao: {junie.reputation}")
    print(f"tarefa {task.id} -> {task.status.value}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="goodbot")
    parser.add_argument("command", choices=["demo", "version"])
    args = parser.parse_args()
    if args.command == "version":
        print(__version__)
        return
    demo()


if __name__ == "__main__":
    main()
