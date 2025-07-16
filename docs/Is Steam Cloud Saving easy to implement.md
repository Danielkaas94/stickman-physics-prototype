## 🎮 Is Steam Cloud Saving easy to implement?

**Yes** — *relatively* easy, **if** you're using a supported engine like **Unity** or **Godot** with Steamworks integration.

### 🔧 What’s required?

1. **Integrate Steamworks SDK**

   * In Unity: Use [Facepunch.Steamworks](https://github.com/Facepunch/Facepunch.Steamworks) or [Steamworks.NET](https://steamworks.github.io/)
   * In Godot: Use the [GodotSteam plugin](https://github.com/CoaguCo-Industries/GodotSteam)

2. **Use Steam Cloud APIs or default config**

   * You can **let Steam handle it** automatically if you:

     * Define save file locations in your app’s `steam_appid.vdf` or `Steamworks backend`
     * Store your game data in those files (e.g. `user/wormData.json`)
     * Steam will sync it for you between devices.
   * For **manual control**, you'd call functions like:

     * `SteamRemoteStorage.FileWrite()`
     * `SteamRemoteStorage.FileRead()`

So overall: **if you're already integrating with Steam**, it’s relatively painless. The most work is upfront (getting Steam integration running and deciding where/what to save).