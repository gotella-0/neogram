# States & multi-step dialogs

States let you build multi-step conversations. A state is a string stored per user in the
`states` database table. When a handler matches, NeoGram looks up the current user state
and picks the matching variant of the handler.

## How state selection works

Every handler in `logic_commands` is transformed by `_check_state` into:

```python
{
    "any":  <the handler itself>,
    "<state1>": <handler variant for state1>,
    "<state2>": <handler variant for state2>,
    ...
}
```

When a message/command/callback arrives, NeoGram:

1. Gets the user's current state (`get_state` from the DB).
2. If a variant for that state exists, uses it.
3. Otherwise falls back to `"any"`.

## Setting a state: `set_state`

After a handler runs, you can switch the user to a new state with `set_state`:

```toml
[commands.start]
text = "Welcome! Choose an option:"
action = "send_text"
set_state = "menu"
```

Now this user is in the `"menu"` state.

## Per-state variants: `state.<name>`

You can define a different behavior of the **same** handler depending on the user's state.
The syntax is `[commands.<name>.state.<state_name>]`:

```toml
[commands.start]
text = "You are in the default state"
action = "send_text"

[commands.start.state.pressed]
text = "You already pressed start!"
action = "send_text"
```

Here, a user in state `"pressed"` who types `/start` gets the second text instead of the
first.

## A complete two-step dialog

```toml
[commands.start]
text = "What is your name?"
action = "send_text"
set_state = "await_name"

[messages.await_name.state.await_name]
action = "send_text"
text = "Nice to meet you!"
set_state = "done"

[messages.done.state.done]
action = "send_text"
text = "We already know your name :)"
```

Let's trace it:

1. User sends `/start` → NeoGram replies "What is your name?" and sets state
   `"await_name"`.
2. User types any message → the `[messages.await_name]` handler only exists for state
   `"await_name"`, so it matches only while the user is in that state. It replies and sets
   state `"done"`.
3. User sends another message → the `[messages.done]` handler (state `"done"`) matches and
   replies.

> Tip: Because the state variants are matched by state, a handler defined only under a
> specific `state.<name>` simply does nothing in other states — no need to check anything
> manually.

## State storage

States are stored in the `states` table:

```sql
CREATE TABLE states (user_id BIGINT PRIMARY KEY, state TEXT);
```

The `Database.get_state` / `Database.update_state` / `Database.delete_state` methods are
exposed in the eval context as `database`, so custom modules can read and write states
directly.

## Related

- [Buttons](buttons.md) — combine states with keyboards for menus.
- [Configuration](configuration.md) — handler fields reference.
- [API reference](api-reference.md) — `set_state`, `_check_state`.