# Send actions

An `action` (or several in `actions`) tells NeoGram what to do when a handler matches.
Actions map to methods of `Api`. This page documents every action.

## How actions work

```toml
[commands.start]
action = "send_text"
text = "Hello!"
```

NeoGram looks up the action name as a method on `Api` and calls it with the message and
the handler config. If the action is missing, it falls back to `actions` (an array) and
tries each entry.

## `send_text`

Sends a text message. Uses `text` (single) or `texts` (multiple, one message each).
Text is evaluated as an f-string, so you can interpolate variables.

```toml
[commands.start]
action = "send_text"
text = "Hello, {message.from_user.first_name}!"
```

Multiple messages:

```toml
[commands.info]
action = "send_text"
texts = ["First message", "Second message"]
```

Renders the keyboard defined in `buttons` (if any).

## `send_photo`

Sends a photo from the project's `assets/` folder with an optional caption.

```toml
[commands.pic]
action = "send_photo"
photo = "preview.jpg"
text = "Here is the preview"
```

- `photo` — filename inside `assets/`.
- `text` — caption (f-string supported).

## `send_document`

Sends a document from `assets/`. Supports a single document or a list.

```toml
[commands.file]
action = "send_document"
document = { name = "report.pdf", text = "Your report" }
```

Multiple documents:

```toml
[commands.files]
action = "send_document"
documents = [ { name = "a.pdf", text = "Doc A" }, { name = "b.pdf", text = "Doc B" } ]
```

## `edit_text`

Edits an existing message (works in callback handlers, where the message to edit is the
one with the button).

```toml
[callbacks.next]
action = "edit_text"
text = "Updated text"
```

For callbacks it edits the message the button was attached to; for commands it edits the
user's latest message.

## `resend_message`

Resends whatever the user sent (text, photo, or document) back to them.

```toml
[commands.resend]
action = "resend_message"
```

Useful for echo bots.

## Action chaining with `actions`

Multiple actions run in order:

```toml
[files.photo]
name = "test"
actions = ["get_photo", "send_text"]
texts = ["Photo successfully accepted"]
```

`get_photo` stores the file, then `send_text` confirms it.

## Reference table

| Action | Params | Description |
|--------|--------|-------------|
| `send_text` | `text` / `texts` | Send text message(s). |
| `send_photo` | `photo`, `text` | Send a photo from `assets/` with caption. |
| `send_document` | `document` / `documents` | Send document(s) from `assets/`. |
| `edit_text` | `text` | Edit an existing message. |
| `resend_message` | — | Echo the user's message back. |
| `get_photo` | `name`, `owner` | Store an incoming photo. |
| `get_audio` | `name`, `owner` | Store an incoming audio. |
| `get_voice` | `name`, `owner` | Store an incoming voice. |
| `get_document` | `name`, `owner` | Store an incoming document. |
| `get_video` | `name`, `owner` | Store an incoming video. |
| `get_location` | `name`, `owner` | Store an incoming location. |
| `get_contact` | `name`, `owner` | Store an incoming contact. |

## Related

- [Configuration](configuration.md) — handler fields.
- [Files & media](files-media.md) — the `get_*` actions in detail.
- [API reference](api-reference.md) — the full method signatures.