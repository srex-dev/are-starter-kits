# Nigel 15-Minute ARE Live Lab Script

This is a tight live-lab script for showing ARE Foundation first, then pointing
to the full ARE platform.

Core line:

```text
Pick one action. Prove who can do it. Check policy. Return proof. Execute nothing.
```

## Before The Room

Terminal 1:

```powershell
cd C:\Users\jonat\are-starter-kits
python scripts\live_lab.py reset
python scripts\live_lab.py serve --port 8765
```

Browser:

```powershell
start http://127.0.0.1:8765/demo/live-lab.html
```

Terminal 2:

```powershell
cd C:\Users\jonat\are-starter-kits
python scripts\live_lab.py doctor
```

## 0:00-1:15 - Cold Open

Say:

> I want to introduce Nigel. Nigel is not malicious. Nigel is helpful.

> Nigel has attended one AI webinar and is now ready to modernize the operating
> model.

> He does not want to break production. He merely has access to the button that
> might.

Point:

- AI governance is not only about malicious actors.
- It is about helpful actors, tools, agents, and workflows moving faster than
  the organization can reason about.

Run:

```powershell
python scripts\live_lab.py intro
```

## 1:15-3:00 - Translate Nigel Into An Agent Problem

Say:

> A local agent with tools is Nigel with an API key and no lunch break.

> The question is not "do we trust Nigel?" The question is "what can Nigel do,
> under which authority, against which policy, with what proof?"

Point at browser:

- Actor
- Authority
- Scope
- Policy
- Proof before action

## 3:00-5:00 - Register Actor And Issue Passport

Say:

> First, we make the actor attributable. ARE gives the actor a scoped passport.
> Not blind trust. Not a vibes-based permission slip. Scoped authority.

Run:

```powershell
python scripts\live_lab.py actor
```

Emphasize:

- Actor is registered.
- Passport is issued.
- Scope is explicit.
- Nothing executed.

Joke:

> Nigel now has paperwork. This is where British management traditionally
> becomes comfortable.

## 5:00-6:45 - Allowed Governed Check

Say:

> Now Nigel asks for a model promotion check. ARE checks authority and policy
> before any customer action happens.

Run:

```powershell
python scripts\live_lab.py allow
```

Say:

> This is the happy path: the actor has authority, the resource fits policy,
> and the system can explain why.

Point:

- Scope result
- Policy result
- `executed=false`

## 6:45-8:15 - Denied Governed Check

Say:

> Now Nigel sees an experimental model. Nigel thinks "experimental" means
> visionary. Policy hears "maybe do not ship that to production over tea."

Run:

```powershell
python scripts\live_lab.py deny
```

Say:

> The important part is not that the system said no. The important part is that
> it said no before action, with a reason, and with an audit-friendly trail.

## 8:15-10:15 - MCP Tool Calls

Say:

> MCP is the beachhead because tool calls are where agent intent turns into
> system action.

> Here the same ARE pattern wraps tool calls. Safe read is allowed. Unsafe
> delete is denied before the tool executes.

Run:

```powershell
python scripts\live_lab.py mcp
```

Say:

> That is the developer wedge: govern your MCP tool calls in roughly twenty
> lines, then grow from local governance into enterprise governance.

## 10:15-11:15 - Public Proof Summary

Run:

```powershell
python scripts\live_lab.py summary
```

Say:

> The output is intentionally boring in the best possible way: who acted, what
> authority existed, what policy said, what was denied, and whether anything
> executed.

> In this lab: executed equals false.

## 11:15-13:30 - Full ARE Preview

Say:

> The OSS foundation is the first gate: identity, passports, scope, policy, and
> proof basics.

> Full ARE extends that into BYOPolicy, HITL approval, ledger and evidence
> replay, observability, live pulse, workflow maps, recovery, and
> governance-strata for higher-risk transitions.

Optional show:

- ARE client demo site
- Command Center
- BYOPolicy page
- Live Pulse or governed map

Keep it short. Do not tour everything.

## 13:30-15:00 - Close

Say:

> The point is not to make Nigel smarter. The point is to make sure Nigel cannot
> accidentally become infrastructure.

> ARE starts with one governed workflow. If that works, you expand. If it does
> not, you know exactly which authority, policy, source, or proof gap failed.

Close with:

> Helpful people and helpful agents will keep trying to do useful things. ARE
> gives the organization a way to say: yes, no, escalate, and here is the proof.

## Commands In One Block

Use this for rehearsal:

```powershell
python scripts\live_lab.py reset
python scripts\live_lab.py intro
python scripts\live_lab.py actor
python scripts\live_lab.py allow
python scripts\live_lab.py deny
python scripts\live_lab.py mcp
python scripts\live_lab.py summary
```
