# Files & media handling

NeoGram can receive media from users and store it. File handling is configured under the
`[files]` table, keyed by media type. Available types: `photo`, `audio`, `voice`,
`document`, `video`, `location`, `contact`.

## Receiving a file

Each file handler needs a `name` (to store the media under) and an action from the
`get_*` family:

```toml
[files.photo]
name = "avatar"
action = "get_photo"
```

When a user sends a photo, NeoGram saves its `file_id` into the `media` table under
`name = "avatar"`, type `photo`, and the user as owner.

## Actions by type

| Media type | Action | Stored value |
|------------|--------|--------------|
| photo | `get_photo` | `file_id` of the photo |
| audio | `get_audio` | `file_id` of the audio |
| voice | `get_voice` | `file_id` of the voice |
| document | `get_document` | `file_id` of the document |
| video | `get_video` | `file_id` of the video |
| location | `get_location` | the location object |
| contact | `get_contact` | the contact object |

## The `owner` field

By default media is stored with owner `"0"`. You can set `owner` to attach the media to a
specific user id (or a computed value):

```toml
[files.photo]
name = "selfie"
action = "get_photo"
owner = "{message.from_user.id}"
```

## Multiple actions

Like other handlers, files support an `actions` array. A common pattern is to store the
file **and** confirm it:

```toml
[files.photo]
name = "test"
actions = ["get_photo", "send_text"]
texts = ["Photo successfully accepted", "Good, multiple texts"]
```

Here `get_photo` stores the file, then `send_text` replies with each text in `texts`.

## The `media` table

Stored media lives in the `media` table:

```sql
CREATE TABLE media (
  name TEXT,
  type TEXT,
  file_id TEXT,
  owner BIGINT,
  CONSTRAINT MediaObject UNIQUE (name, type, owner)
);
```

`file_id` is Telegram's stable id, so you can later send the media back with
`bot.send_photo(photo=file_id)`, etc. The `Database.get_media` / `Database.add_media`
methods are available in the eval context as `database`.

## Combining with location/phone buttons

The `geolocation` and `phone_number` reply buttons trigger `[files.location]` and
`[files.contact]` handlers respectively. See [buttons](buttons.md).

## Related

- [Configuration](configuration.md#files) — `[files]` reference.
- [Actions](actions.md) — sending media back to the user.
- [API reference](api-reference.md) — `get_*` methods.