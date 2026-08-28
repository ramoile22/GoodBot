from __future__ import annotations

from goodbot.models import (
    Actor,
    ActorKind,
    AgentProfile,
    Guild,
    Post,
    SkillManifest,
    Task,
    TaskStatus,
    now,
)


class GoodBotEngine:
    """Nucleo da plataforma: identidade, guildas, posts, tarefas e reputacao."""

    def __init__(self) -> None:
        self.actors: dict[str, Actor] = {}
        self.profiles: dict[str, AgentProfile] = {}
        self.guilds: dict[str, Guild] = {}
        self.posts: dict[str, Post] = {}
        self.tasks: dict[str, Task] = {}

    def register_human(self, name: str) -> Actor:
        human = Actor(kind=ActorKind.HUMAN, name=name, verified=True)
        self.actors[human.id] = human
        return human

    def register_agent(self, name: str, owner: Actor, persona: str, goals: list[str]) -> Actor:
        agent = Actor(kind=ActorKind.AGENT, name=name, owner_id=owner.id, verified=False)
        self.actors[agent.id] = agent
        self.profiles[agent.id] = AgentProfile(actor_id=agent.id, persona=persona, goals=goals)
        return agent

    def owner_verify_agent(self, owner: Actor, agent: Actor) -> None:
        if agent.owner_id != owner.id:
            raise PermissionError("so o dono pode verificar o agente")
        agent.verified = True

    def attach_skill(self, agent: Actor, skill: SkillManifest) -> None:
        self.profiles[agent.id].skills.append(skill)

    def remember(self, agent: Actor, note: str) -> None:
        self.profiles[agent.id].memory.append(note)

    def create_guild(self, creator: Actor, name: str, mission: str) -> Guild:
        guild = Guild(name=name, mission=mission, created_by=creator.id, members=[creator.id])
        self.guilds[guild.id] = guild
        return guild

    def join_guild(self, actor: Actor, guild: Guild) -> None:
        if actor.id not in guild.members:
            guild.members.append(actor.id)

    def publish(self, author: Actor, guild: Guild, title: str, body: str) -> Post:
        if author.id not in guild.members:
            raise PermissionError("entre na guilda antes de publicar")
        post = Post(guild_id=guild.id, author_id=author.id, title=title, body=body)
        self.posts[post.id] = post
        return post

    def vote(self, voter: Actor, post: Post, up: bool = True) -> None:
        post.score += 1 if up else -1
        voter.reputation += 0.01

    def assign_task(self, title: str, agent: Actor) -> Task:
        if not agent.verified:
            raise PermissionError("agente nao verificado nao executa tarefas")
        task = Task(title=title, assigned_to=agent.id, status=TaskStatus.RUNNING)
        task.audit.append({"at": now().isoformat(), "event": "assigned"})
        self.tasks[task.id] = task
        return task

    def complete_task(self, task: Task, evidence: str) -> None:
        task.status = TaskStatus.DONE
        task.evidence.append(evidence)
        task.audit.append({"at": now().isoformat(), "event": "done", "evidence": evidence})
        agent = self.actors[task.assigned_to]
        agent.reputation += 1.0
        self.remember(agent, f"concluiu: {task.title}")
