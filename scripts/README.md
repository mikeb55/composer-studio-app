# Composer Studio Scripts

## create-desktop-shortcut.cjs

Creates a native Windows desktop shortcut for Composer Studio. Points to the packaged Tauri executable. No .bat files or Python scripts.

**Usage:**
```bash
npm run create-shortcut
```

**Requirements:**
- App built via `npm run tauri:build` (requires Rust)
- Shortcut target: `src-tauri/target/release/Composer Studio.exe`

**Full build + shortcut:**
```bash
npm run tauri:build:full
```
