const { app, BrowserWindow, Menu, Tray, ipcMain, shell, dialog, session, nativeImage } = require('electron');
const { spawn, exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const axios = require('axios');
const https = require('https');
const treeKill = require('tree-kill');

const store = 'Tidal';
const currentVersion = app.getVersion();

let updateWindow;
let mainWindow;
let splashScreen;
let backendProcess;
let tray = null;
let consoleShown = false;
let consoleWindow = null;

const gotTheLock = app.requestSingleInstanceLock();
app.disableHardwareAcceleration();
app.commandLine.appendSwitch('disable-gpu');

if (!gotTheLock) {
    app.quit();
} else {
    app.on('second-instance', (event, commandLine, workingDirectory) => {
        if (mainWindow) {
            if (mainWindow.isMinimized()) mainWindow.restore();
            mainWindow.focus();
        }
    });

    const GITHUB_OWNER = 'soportemusical29-create';
    const GITHUB_REPO = 'Aoi-Tidal';
    const LOCAL_VERSION = (function() {
        try {
            const vp = path.join(__dirname, 'version.json');
            if (fs.existsSync(vp)) return JSON.parse(fs.readFileSync(vp, 'utf8')).version || '0.0.0';
        } catch (e) {}
        return '0.0.0';
    })();

    async function checkForUpdates() {
        try {
            const res = await axios.get(`https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/releases/latest`, {
                headers: { 'Accept': 'application/vnd.github.v3+json', 'User-Agent': 'Aoi-Tidal-Updater' },
                timeout: 10000
            });
            const latest = res.data.tag_name.replace(/^v/, '');
            if (compareVersions(latest, LOCAL_VERSION) > 0) {
                // Find update.zip asset
                const asset = res.data.assets.find(a => a.name === 'update.zip');
                if (!asset) {
                    console.log('No update.zip asset found in latest release');
                    return { updateAvailable: false };
                }
                return { updateAvailable: true, version: latest, zipUrl: asset.browser_download_url, notes: res.data.body || '' };
            }
        } catch (e) {
            console.log('Update check failed:', e.message);
        }
        return { updateAvailable: false };
    }

    function compareVersions(a, b) {
        const pa = a.split('.').map(Number);
        const pb = b.split('.').map(Number);
        for (let i = 0; i < 3; i++) {
            if ((pa[i]||0) > (pb[i]||0)) return 1;
            if ((pa[i]||0) < (pb[i]||0)) return -1;
        }
        return 0;
    }

    async function downloadAndInstallUpdate(zipUrl, newVersion) {
        const tmpDir = path.join(require('os').tmpdir(), 'aoi_update_' + Date.now());
        const zipPath = tmpDir + '.zip';
        const appDir = __dirname;
        const backupDir = appDir + '_backup';

        try {
            // Download
            await createUpdateWindow('Descargando actualización ' + newVersion + '...');
            const writer = fs.createWriteStream(zipPath);
            const dl = await axios({ url: zipUrl, method: 'GET', responseType: 'stream', timeout: 120000 });
            dl.data.pipe(writer);
            await new Promise((resolve, reject) => { writer.on('finish', resolve); writer.on('error', reject); });

            await createUpdateWindow('Extrayendo archivos...');
            if (fs.existsSync(tmpDir)) fs.rmSync(tmpDir, { recursive: true, force: true });
            fs.mkdirSync(tmpDir, { recursive: true });

            // Extract using PowerShell Expand-Archive
            await new Promise((resolve, reject) => {
                exec(`powershell -Command "Expand-Archive -Path '${zipPath}' -DestinationPath '${tmpDir}' -Force"`, { windowsHide: true }, (err) => {
                    if (err) reject(err); else resolve();
                });
            });

            await createUpdateWindow('Instalando actualización...');

            // Files to update (update.zip contains these directly)
            const filesToUpdate = ['api.exe', 'main.js', 'index.html', 'console.html', 'renderer.js', 'preload.js', 'version.json', 'background.jpg', 'splash.html'];
            if (fs.existsSync(backupDir)) fs.rmSync(backupDir, { recursive: true, force: true });
            fs.mkdirSync(backupDir);

            for (const file of filesToUpdate) {
                const src = path.join(tmpDir, file);
                const dst = path.join(appDir, file);
                if (fs.existsSync(src)) {
                    if (fs.existsSync(dst)) {
                        // Kill api.exe before replacing it
                        if (file === 'api.exe') {
                            if (backendProcess && !backendProcess.killed) {
                                treeKill(backendProcess.pid, 'SIGTERM', () => {});
                                await new Promise(r => setTimeout(r, 2000));
                            }
                        }
                        // Backup existing
                        try { fs.copyFileSync(dst, path.join(backupDir, file)); } catch(e) {}
                        // Replace
                        try { fs.copyFileSync(src, dst); } catch(e) { console.log('Failed to update', file, e.message); }
                    }
                }
            }

            // Cleanup
            try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch(e) {}
            try { fs.rmSync(zipPath, { force: true }); } catch(e) {}
            try { fs.rmSync(backupDir, { recursive: true, force: true }); } catch(e) {}

            await createUpdateWindow('✅ Actualización completada. Reiniciando...');
            await new Promise(r => setTimeout(r, 1500));

            // Restart
            if (updateWindow && !updateWindow.isDestroyed()) updateWindow.close();
            app.relaunch();
            app.quit();
        } catch (e) {
            console.error('Update failed:', e);
            // Restore backup
            if (fs.existsSync(backupDir)) {
                for (const file of filesToUpdate) {
                    const bak = path.join(backupDir, file);
                    const dst = path.join(appDir, file);
                    if (fs.existsSync(bak)) {
                        try { fs.copyFileSync(bak, dst); } catch(ex) {}
                    }
                }
                try { fs.rmSync(backupDir, { recursive: true, force: true }); } catch(ex) {}
            }
            try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch(ex) {}
            try { fs.rmSync(zipPath, { force: true }); } catch(ex) {}
            if (updateWindow && !updateWindow.isDestroyed()) {
                updateWindow.loadURL(`data:text/html,<html><body style="background:#000;color:#fff;display:flex;align-items:center;justify-content:center;font-family:Arial;text-align:center"><div><h2>Error al actualizar</h2><p>${e.message}</p><p>Reinicia la app manualmente</p></div></body></html>`);
                await new Promise(r => setTimeout(r, 3000));
                if (updateWindow && !updateWindow.isDestroyed()) updateWindow.close();
            }
        }
    }

    async function createUpdateWindow(message) {
        if (updateWindow && !updateWindow.isDestroyed()) {
            try { updateWindow.loadURL(`data:text/html,<html><body style="background:#000;color:#fff;display:flex;align-items:center;justify-content:center;font-family:Arial;text-align:center"><div><h2 style="color:#27ae60;">Aoi Tidal</h2><p>${message}</p></div></body></html>`); } catch(e) {}
        } else {
            updateWindow = new BrowserWindow({
                width: 400, height: 200, frame: false, resizable: false,
                alwaysOnTop: true, webPreferences: { sandbox: true }
            });
            updateWindow.loadURL(`data:text/html,<html><body style="background:#000;color:#fff;display:flex;align-items:center;justify-content:center;font-family:Arial;text-align:center"><div><h2 style="color:#27ae60;">Aoi Tidal</h2><p>${message}</p></div></body></html>`);
            updateWindow.show();
        }
    }

    function killProcessOnPort(port) {
        exec(`netstat -ano | findstr :${port}`, (err, stdout, stderr) => {
            if (err) {
                console.error(`Error finding process on port ${port}:`, stderr);
                return;
            }

            const lines = stdout.trim().split('\n');
            if (lines.length > 0) {
                const parts = lines[0].trim().split(/\s+/);
                const pid = parts[parts.length - 1];

                exec(`taskkill /PID ${pid} /F`, { windowsHide: true }, (err, stdout, stderr) => {
                    if (err) {
                        console.error(`Error killing process with PID ${pid}:`, stderr);
                    } else {
                        console.log(`Process with PID ${pid} on port ${port} was killed.`);
                    }
                });
            } else {
                console.log(`No process found on port ${port}`);
            }
        });
    }



    function createSplashScreen() {
        splashScreen = new BrowserWindow({
            width: 300,
            height: 180,
            transparent: true,
            frame: false,
            alwaysOnTop: false,
            resizable: false,
            fullscreenable: false,
            webPreferences: {
                nodeIntegration: false,
                contextIsolation: true,
                enableRemoteModule: false,
                sandbox: true,
            },
        });

        splashScreen.loadFile('splash.html');
        splashScreen.show();

        splashScreen.on('closed', () => {
            splashScreen = null;
        });
    }

    function createMainWindow(token) {
        if (splashScreen && !splashScreen.isDestroyed()) {
            splashScreen.close();
        }

        Menu.setApplicationMenu(null);
        mainWindow = new BrowserWindow({
            minWidth: 1380,
            minHeight: 770,
            width: 1380,
            height: 770,
            resizable: false,
            frame: false,
            minimizable: true,
            maximizable: false,
            webPreferences: {
                preload: path.join(__dirname, 'preload.js'),
                nodeIntegration: false,
                contextIsolation: true,
                enableRemoteModule: false,
                sandbox: true,
            },
        });

        mainWindow.loadFile('index.html').catch(err => {
            console.error('Failed to load index.html:', err);
        });

        mainWindow.webContents.on('did-finish-load', () => {
            if (mainWindow && !mainWindow.isDestroyed()) {
                mainWindow.webContents.send('token-received', token);
            }
        });

        mainWindow.on('closed', () => {
            mainWindow = null;
            cleanUpAndQuit();
        });

        // Handle window minimize/restore events
        mainWindow.on('minimize', () => {
            // Window minimized
        });

        mainWindow.on('restore', () => {
            // Window restored
        });

        if (process.env.NODE_ENV !== 'development') {
            mainWindow.webContents.on('devtools-opened', () => {
                if (mainWindow && !mainWindow.isDestroyed()) {
                    mainWindow.webContents.closeDevTools();
                }
            });
        }
    }



    function createConsoleWindow() {
        consoleWindow = new BrowserWindow({
            width: 750,
            height: 470,
            minWidth: 750,
            minHeight: 470,
            frame: false,
            show: false,
            minimizable: true,
            maximizable: false,
            webPreferences: {
                nodeIntegration: false,
                contextIsolation: true,
                enableRemoteModule: false,
                preload: path.join(__dirname, 'preload.js'),
                scrollable: false,
            },
        });

        consoleWindow.loadFile('console.html');
        consoleWindow.setMenu(null);

        // Modify 'close' event to check if quitting
        consoleWindow.on('close', (event) => {
            if (!app.isQuitting) {
                event.preventDefault();
                consoleWindow.hide();
                consoleShown = false;
                if (mainWindow && !mainWindow.isDestroyed()) {
                    mainWindow.webContents.send('console-toggled', 'Ver Consola');
                }
            } else {
                consoleWindow = null; // If app is quitting, allow window to close properly
            }
        });

        consoleWindow.on('closed', () => {
            consoleWindow = null;
        });

        // Handle console window minimize/restore events
        consoleWindow.on('minimize', () => {
            // Console window minimized
        });

        consoleWindow.on('restore', () => {
            // Console window restored
        });

        consoleWindow.on('show', () => {
            consoleShown = true;
            if (mainWindow && !mainWindow.isDestroyed()) {
                mainWindow.webContents.send('console-toggled', 'Ocultar Consola');
            }
        });

        consoleWindow.on('hide', () => {
            consoleShown = false;
            if (mainWindow && !mainWindow.isDestroyed()) {
                mainWindow.webContents.send('console-toggled', 'Ver Consola');
            }
        });
    }

    async function waitForBackendReady() {
        while (true) {
            try {
                console.log('Attempting to check backend readiness...');
                const response = await axios.post('http://127.0.0.1:8111/backend');
                if (response.data.ready) {
                    console.log('Backend is ready');
                    break;
                } else {
                    console.log(`Backend not ready yet, reason: ${response.data.message}. Retrying in 1 second...`);
                }
            } catch (error) {
                console.log(`Error checking backend readiness: ${error.message}. Retrying in 1 second...`);
            }
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
    }

    async function autoLogin() {
        try {
            const response = await axios.post('http://127.0.0.1:8111/login', { username: 'user', password: 'user', stayloggedin: false });
            if (response.data.success) {
                return { success: true, token: response.data.token };
            }
        } catch (error) {
            console.error('Auto-login error:', error);
        }
        return { success: false, token: '' };
    }

    ipcMain.on('toggle-console', (event) => {
        if (consoleWindow === null) {
            createConsoleWindow();
        }

        if (consoleWindow.isVisible()) {
            consoleWindow.hide();
        } else {
            consoleWindow.show();
        }
    });

    ipcMain.on('minimize-console', () => {
        if (consoleWindow && !consoleWindow.isDestroyed()) {
            try {
                consoleWindow.minimize();
                // Fallback: if minimize doesn't work, hide the window
                setTimeout(() => {
                    if (consoleWindow && !consoleWindow.isDestroyed() && !consoleWindow.isMinimized()) {
                        consoleWindow.hide();
                    }
                }, 100);
            } catch (error) {
                console.error('Error minimizing console window:', error);
                consoleWindow.hide();
            }
        }
    });



    app.on('window-all-closed', () => {
        if (process.platform !== 'darwin') {
            cleanUpAndQuit();
        }
    });

    app.on('before-quit', () => {
        console.log('Application is quitting. Terminating backend process...');
        app.isQuitting = true;  // Set a flag indicating app is quitting
        cleanUpAndQuit();
    });

    ipcMain.on('close-app', () => {
        const focusedWindow = BrowserWindow.getFocusedWindow();
        if (focusedWindow && !focusedWindow.isDestroyed()) {
            focusedWindow.close();
        }
    });

    ipcMain.on('kill-processes', () => {
        const { exec } = require('child_process');
        const path = require('path');
        exec('taskkill /f /im api.exe 2>nul & taskkill /f /im Aoi-Tidal.exe 2>nul & taskkill /f /im chromium.exe 2>nul', (err) => {
            const files = [
                path.join(process.env.APPDATA, 'Aoi', 'Tidal', 'Files', 'chromedriver.zip'),
                path.join(process.env.APPDATA, 'Aoi', 'Tidal', 'Files', 'chromedriver.exe')
            ];
            files.forEach(f => {
                try { require('fs').unlinkSync(f); } catch (e) {}
            });
            app.quit();
        });
    });

    ipcMain.on('factory-reset', () => {
        const { execSync } = require('child_process');
        const path = require('path');
        const fs = require('fs');

        try { execSync('taskkill /f /im api.exe 2>nul', { stdio: 'ignore' }); } catch (e) {}
        try { execSync('taskkill /f /im chromium.exe 2>nul', { stdio: 'ignore' }); } catch (e) {}

        const tidalDir = path.join(process.env.APPDATA, 'Aoi', 'Tidal');
        try {
            if (fs.existsSync(tidalDir)) {
                fs.rmSync(tidalDir, { recursive: true, force: true });
            }
        } catch (e) {}

        const tmpDir = process.env.TEMP;
        try {
            fs.readdirSync(tmpDir).forEach(item => {
                if (item.startsWith('_MEI') || item.startsWith('aoi_build')) {
                    try { fs.rmSync(path.join(tmpDir, item), { recursive: true, force: true }); } catch (e) {}
                }
            });
        } catch (e) {}

        app.quit();
    });

    ipcMain.on('minimize-window', () => {
        if (mainWindow && !mainWindow.isDestroyed()) mainWindow.minimize();
    });

    ipcMain.on('minimize-app', () => {
        if (mainWindow && !mainWindow.isDestroyed()) {
            try {
                mainWindow.minimize();
                // Fallback: if minimize doesn't work, hide the window
                setTimeout(() => {
                    if (mainWindow && !mainWindow.isDestroyed() && !mainWindow.isMinimized()) {
                        mainWindow.hide();
                    }
                }, 100);
            } catch (error) {
                console.error('Error minimizing window:', error);
                mainWindow.hide();
            }
        }
    });

    ipcMain.on('close-window', () => {
        if (mainWindow && !mainWindow.isDestroyed()) mainWindow.close();
    });

    // Token stored for IPC backend proxy
    let backendToken = '';

    // Handle backend API requests from renderer (bypasses CORS/sandbox issues)
    ipcMain.handle('backend-request', async (event, { method, path, body }) => {
        try {
            const headers = { 'Authorization': `Bearer ${backendToken}` };
            if (body) headers['Content-Type'] = 'application/json';
            const response = await axios({
                method: method.toLowerCase(),
                url: `http://127.0.0.1:8111${path}`,
                headers,
                data: body,
                timeout: 30000,
            });
            return { ok: true, data: response.data };
        } catch (error) {
            if (error.response) {
                return { ok: false, status: error.response.status, data: error.response.data };
            }
            return { ok: false, error: error.message };
        }
    });

    ipcMain.on('logout-all-accounts', async () => {
        try {
            const headers = { 'Authorization': `Bearer ${backendToken}` };
            const response = await axios.post('http://127.0.0.1:8111/logout_all_accounts', {}, { headers, timeout: 15000 });
            if (mainWindow && !mainWindow.isDestroyed()) {
                dialog.showMessageBox(mainWindow, {
                    type: 'info',
                    title: 'Cuentas cerradas',
                    message: response.data?.message || 'Todas las cuentas han sido deslogueadas correctamente.',
                });
            }
        } catch (error) {
            if (mainWindow && !mainWindow.isDestroyed()) {
                dialog.showMessageBox(mainWindow, {
                    type: 'error',
                    title: 'Error',
                    message: 'No se pudo cerrar sesión de las cuentas: ' + (error.response?.data?.error || error.message),
                });
            }
        }
    });

    ipcMain.on('run-optimizer', async () => {
        try {
            const headers = { 'Authorization': `Bearer ${backendToken}` };
            const response = await axios.post('http://127.0.0.1:8111/run_optimizer', {}, { headers, timeout: 180000 });
            if (mainWindow && !mainWindow.isDestroyed()) {
                dialog.showMessageBox(mainWindow, {
                    type: 'info',
                    title: 'Optimizador',
                    message: response.data?.message || 'Optimizacion completada',
                    detail: response.data?.output || '',
                });
            }
        } catch (error) {
            if (mainWindow && !mainWindow.isDestroyed()) {
                dialog.showMessageBox(mainWindow, {
                    type: 'error',
                    title: 'Error',
                    message: 'No se pudo ejecutar el optimizador: ' + (error.response?.data?.error || error.message),
                });
            }
        }
    });

    function createTray() {
        tray = new Tray(nativeImage.createEmpty());
        const contextMenu = Menu.buildFromTemplate([
            {
                label: 'Show',
                click: () => {
                    if (mainWindow && !mainWindow.isDestroyed()) {
                        if (mainWindow.isMinimized()) {
                            mainWindow.restore();
                        } else {
                            mainWindow.show();
                        }
                        mainWindow.focus();
                    } else {
                        createMainWindow();
                    }
                }
            },
            {
                label: 'Exit',
                click: () => {
                    cleanUpAndQuit();
                }
            }
        ]);

        tray.setToolTip(`Aoi ${store} ${currentVersion}`);
        tray.setContextMenu(contextMenu);
        
        // Add double-click handler to restore/show window
        tray.on('double-click', () => {
            if (mainWindow && !mainWindow.isDestroyed()) {
                if (mainWindow.isMinimized()) {
                    mainWindow.restore();
                } else {
                    mainWindow.show();
                }
                mainWindow.focus();
            } else {
                createMainWindow();
            }
        });
    }

    app.on('ready', async () => {
        killProcessOnPort(8111);

        // Check for updates first (before starting backend)
        const updateInfo = await checkForUpdates();
        if (updateInfo.updateAvailable) {
            await downloadAndInstallUpdate(updateInfo.zipUrl, updateInfo.version);
            // downloadAndInstallUpdate calls app.relaunch() + app.quit() if successful
            return;
        }

        const apiExePath = (function() {
            const candidates = [
                path.join(process.resourcesPath || __dirname, 'app', 'api.exe'),
                path.join(process.resourcesPath || __dirname, 'api.exe'),
                path.join(__dirname, 'api.exe'),
            ];
            for (const p of candidates) {
                if (fs.existsSync(p)) return p;
            }
            return 'api.exe';
        })();
        backendProcess = spawn(apiExePath, [], { cwd: path.dirname(apiExePath) });
        //backendProcess = null;

        createSplashScreen();

        try {
            await waitForBackendReady();
            console.log('Backend is ready, closing splash screen');

            const { success, token } = await autoLogin();
            console.log("auto-login result:", success);
            backendToken = token;
            createMainWindow(token);
        } catch (error) {
            console.error('An error occurred while setting up the application:', error);
            createMainWindow('');
        }

        createTray();
    });

    function cleanUpAndQuit() {
        console.log('Cleaning up before quitting...');
        if (backendProcess && !backendProcess.killed) {
            treeKill(backendProcess.pid, 'SIGTERM', (err) => {
                if (err) {
                    console.error('Failed to kill backend process:', err);
                } else {
                    console.log('Backend process terminated.');
                }
                app.quit();
            });
        } else {
            app.quit();
        }
    }
}
