## Command Reference

The plugin uses the `tc` command alias. Most commands require **admin** capabilities.

| Command | Arguments | Description |
| :--- | :--- | :--- |
| **tc enable** | None | Enables compliance logic for the current network and sets `+B`. |
| **tc disable** | None | Disables compliance logic for the current network. |
| **tc set** | `<botlist|rollcall> <text>` | Sets the response string for the mandatory triggers. |
| **tc list** | None | Lists all networks where compliance is currently enabled. |
| **!botlist** | None | Triggered by anyone. Returns the botlist string (works regardless of prefix). |
| **!rollcall** | None | Triggered by anyone. Returns the rollcall string (works regardless of prefix). |

### Example Setup
```irc
<YourNick> !tc enable
<bot> Tilde.chat compliance enabled for tilde. UserModes updated to include +B.
<YourNick> !tc set botlist Maintainer: YourNick <youremail@domain.tld>
<bot> The operation succeeded.
<YourNick> !tc set rollcall Maintainer: YourNick <youremail@domain.tld>