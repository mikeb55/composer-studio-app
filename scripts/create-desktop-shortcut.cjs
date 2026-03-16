#!/usr/bin/env node
/**
 * Create a native Windows desktop shortcut for Composer Studio.
 * Points to the packaged Tauri executable. No .bat, no Python scripts.
 */
const path = require('path');
const { execSync } = require('child_process');
const fs = require('fs');
const os = require('os');

const projectRoot = path.resolve(__dirname, '..');
const exePath = path.join(projectRoot, 'src-tauri', 'target', 'release', 'Composer Studio.exe');
const desktopPath = path.join(process.env.USERPROFILE || process.env.HOME, 'Desktop');
const shortcutPath = path.join(desktopPath, 'Composer Studio.lnk');
const workingDir = path.dirname(exePath);

// Build PowerShell script with proper escaping
const psScript = [
  '$WshShell = New-Object -ComObject WScript.Shell',
  `$Shortcut = $WshShell.CreateShortcut('${shortcutPath.replace(/'/g, "''")}')`,
  `$Shortcut.TargetPath = '${exePath.replace(/'/g, "''")}'`,
  `$Shortcut.WorkingDirectory = '${workingDir.replace(/'/g, "''")}'`,
  `$Shortcut.IconLocation = '${(exePath + ',0').replace(/'/g, "''")}'`,
  "$Shortcut.Description = 'Composer Studio - Creative composition app'",
  '$Shortcut.Save()',
  '[System.Runtime.Interopservices.Marshal]::ReleaseComObject($WshShell)',
].join('; ');

try {
  const tmpFile = path.join(os.tmpdir(), 'cs-shortcut.ps1');
  fs.writeFileSync(tmpFile, psScript, 'utf8');
  execSync(`powershell -NoProfile -ExecutionPolicy Bypass -File "${tmpFile}"`, {
    stdio: 'inherit',
    windowsHide: true,
  });
  fs.unlinkSync(tmpFile);
  console.log('Desktop shortcut created:', shortcutPath);
  console.log('Target:', exePath);
  if (!fs.existsSync(exePath)) {
    console.log('Note: Executable not yet built. Run "npm run tauri:build" (requires Rust) to build.');
  }
} catch (err) {
  console.error('Failed to create shortcut:', err.message);
  process.exit(1);
}
