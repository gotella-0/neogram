# Buttons & keyboards

Keyboards are defined declaratively in the `buttons` field of any handler. NeoGram
supports **inline** keyboards (buttons attached to the message) and **reply** keyboards
(buttons shown in the input bar).

## Structure

`buttons` is a list of **rows**. Each row is a list of buttons.

```toml
buttons = [ [button1, button2], [button3] ]
```

- Outer list → rows (each row is rendered on its own line).
- Inner list → the buttons in that row.

## Inline buttons

An inline button has `type = "inline"`, a `text`, and `data` (the `callback_data` sent
when pressed):

```toml
[commands.menu]
action = "send_text"
text = "Choose:"
buttons = [ [{text = "Profile", type = "inline", data = "profile"}, {text = "Help", type = "inline", data = "help"}] ]
```

Pressing a button with `data = "help"` fires the callback handler keyed `"help"`:

```toml
[callbacks.help]
action = "send_text"
text = "This is the help section"
```

> `data` matches the key of a `[callbacks.<data>]` handler. See
> [configuration](configuration.md#callbacks).

## Reply buttons

A reply button has `type = "text"` (or no type — text is the default). You can also
request the user's **geolocation** or **phone number**.

```toml
[commands.start]
action = "send_text"
text = "Use the buttons below"
buttons = [ [{text = "Profile", type = "text"}, {text = "Help"}] ]
```

The reply button text is matched against `[messages.<text>]` handlers:

```toml
[messages.Profile]
action = "send_text"
text = "Your profile"
```

### Location and phone request buttons

```toml
[commands.start]
action = "send_text"
text = "Send your location or phone:"
buttons = [ [{text = "Send location", type = "geolocation"}, {text = "Send phone", type = "phone_number"}] ]
```

- `geolocation` → requests the user's location (handled by `[files.location]`).
- `phone_number` → requests the user's contact (handled by `[files.contact]`).

See [files & media](files-media.md).

## Per-state buttons

Because buttons live inside a handler, you can define different keyboards per state using
the `state.<name>` variants:

```toml
[commands.menu]
action = "send_text"
text = "Main menu"
buttons = [ [{text = "Profile", type = "text"}, {text = "Help", type = "text"}] ]

[commands.menu.state.menuProfile]
action = "send_text"
text = "Profile menu"
buttons = [ [{text = "Back", type = "text"}] ]
```

## Mixed row note

Each row uses a single keyboard type (inline or reply), determined by the first button of
the row. Keep the buttons in a row of the same kind for predictable results.

## Related

- [Actions](actions.md) — `send_text`, `send_photo`, etc. render `markup`.
- [States](states.md) — combine buttons with state variants for menus.