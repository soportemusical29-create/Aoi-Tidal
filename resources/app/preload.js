const { contextBridge, ipcRenderer } = require('electron');

// Define allowed channels for send and receive to ensure security
const validSendChannels = ['toggle-console', 'toggle-always-on-top', 'minimize-app', 'minimize-console', 'close-app', 'send-token', 'update-choice', 'kill-processes', 'factory-reset', 'logout-all-accounts', 'run-optimizer'];
const validReceiveChannels = ['console-toggled', 'token-received', 'version-info', 'download-progress'];

contextBridge.exposeInMainWorld('electronAPI', {
    saveSettings: (settings) => ipcRenderer.send('save-settings', settings),
    loadSettings: () => ipcRenderer.invoke('load-settings'),
    toggleAlwaysOnTop: (isOnTop) => {
        if (validSendChannels.includes('toggle-always-on-top')) {
            ipcRenderer.send('toggle-always-on-top', isOnTop);
        }
    },
    minimizeApp: () => {
        if (validSendChannels.includes('minimize-app')) {
            ipcRenderer.send('minimize-app');
        }
    },
    closeApp: () => {
        if (validSendChannels.includes('close-app')) {
            ipcRenderer.send('close-app');
        }
    },
    sendTokenToRenderer: (token) => {
        if (validSendChannels.includes('send-token')) {
            ipcRenderer.send('send-token', token);
        }
    },
    onTokenReceived: (callback) => {
        if (validReceiveChannels.includes('token-received')) {
            ipcRenderer.on('token-received', (event, token) => callback(token));
        }
    },
    send: (channel, data) => {
        if (validSendChannels.includes(channel)) {
            ipcRenderer.send(channel, data);
        }
    },
    receive: (channel, func) => {
        if (validReceiveChannels.includes(channel)) {
            ipcRenderer.on(channel, (event, ...args) => func(...args));
        }
    },
    // Backend API proxy via main process (bypasses CORS/sandbox)
    backendRequest: (method, path, body) => ipcRenderer.invoke('backend-request', { method, path, body })
});
