document.addEventListener('DOMContentLoaded', () => {
    let authToken = null;  // Declare authToken at the top

    // Backend API proxy via main process (bypasses CORS/sandbox)
    function backendFetch(method, path, body) {
        return window.electronAPI.backendRequest(method, path, body)
            .then(result => {
                if (!result.ok) {
                    const err = new Error(result.data?.error || result.data?.message || 'Request failed');
                    err.status = result.status;
                    throw err;
                }
                return result.data;
            });
    }

    // Function to wait for the token
    function waitForToken() {
        return new Promise((resolve, reject) => {
            if (authToken) {
                resolve(authToken);
            } else {
                window.electronAPI.onTokenReceived((token) => {
                    authToken = token;
                    resolve(authToken);
                });
            }
        });
    }
    const minBtn = document.getElementById('minimize-btn');
    if (minBtn) {
        minBtn.addEventListener('click', () => {
            window.electronAPI.minimizeApp();
        });
    }

    const closeBtn = document.getElementById('close-btn');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            window.electronAPI.closeApp();
        });
    }
    const consoleMinBtn = document.getElementById('consolemin-btn');
    if (consoleMinBtn) {
        consoleMinBtn.addEventListener('click', () => {
            window.electronAPI.send('minimize-console');
        });
    }
    const consoleCloseBtn = document.getElementById('consoleclose-btn');
    if (consoleCloseBtn) {
        consoleCloseBtn.addEventListener('click', () => {
            window.electronAPI.send('toggle-console');
        });
    }

    const loginScreen = document.getElementsByClassName('login-box');
    const updateWindow = document.getElementsByClassName('update-content');
    if (loginScreen.length > 0) {
        const responseMessage = document.getElementById('responseMessage');
        const supportBtn = document.getElementById('supportBtn');
        const submitBtn = document.getElementById('submit-button');
        const passwordInput = document.getElementById('password');
        const passwordToggle = document.getElementById('password-toggle');
        const forgotPassword = document.getElementById('forgot-pass');

        passwordToggle.addEventListener('click', function () {
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                passwordToggle.classList.add('active');
                passwordToggle.classList.replace('fa-eye', 'fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                passwordToggle.classList.remove('active');
                passwordToggle.classList.replace('fa-eye-slash', 'fa-eye');
            }
        });

        supportBtn.addEventListener('click', async (event) => {
            event.preventDefault();
            const url = ''; // Support URL
            window.electronAPI.send('open-external-link', url);
        });

        forgotPassword.addEventListener('click', async (event) => {
            event.preventDefault();
            const url = 'https://crbrs.io/login'; // The URL you want to open
            window.electronAPI.send('open-external-link', url);
        });

        document.getElementById('submit-button').addEventListener('click', async (event) => {
            event.preventDefault();
            console.log('Submit button clicked'); // Ensure this is firing

            const username = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const stayloggedinboolean = document.getElementById('stay-logged-in').checked;
            let payload;

            payload = { username, password, stayloggedin: stayloggedinboolean };

            const authOption = 'login';
            window.electronAPI.send('login-attempt', { payload, authOption });

            // Handle the response from the main process
            window.electronAPI.receive('login-response', (response) => {
                const responseMessage = document.getElementById('responseMessage');
                if (response.success) {
                    responseMessage.innerHTML = '<span class="success-icon"></span>' + response.message;
                    responseMessage.className = 'success';
                } else if (response.message.includes("Backend API")) {
                    responseMessage.innerHTML = '<span class="error-icon"></span>' + response.message;
                    responseMessage.className = 'error';
                    submitBtn.style.display = "none";
                } else {
                    responseMessage.innerHTML = '<span class="error-icon"></span>' + response.message;
                    responseMessage.className = 'error';
                }
                responseMessage.style.display = 'block';
            });
        });
    } else if (updateWindow.length > 0) {
        const versionInfoElement = document.getElementById('version-info');
        window.electronAPI.receive('version-info', (versions) => {
            console.log('Received version-info:', versions);
            const versionText = `Version ${versions.latestVersion} is available. You are currently on version ${versions.currentVersion}.`;
            versionInfoElement.innerText = versionText;
        });

        window.electronAPI.receive('download-progress', ({ progress }) => {
            document.getElementById('downloadProgress').value = progress;
        });

        document.getElementById('updateNow').addEventListener('click', () => {
            window.electronAPI.send('update-choice', 'update');
        });

        document.getElementById('remindLater').addEventListener('click', () => {
            window.electronAPI.send('update-choice', 'skip');
        });

    } else {
        waitForToken().then(() => {

            let startTime;
            let timerInterval;

            loadConfigs();
            loadBatches();
            reloadBatchOptions();
            loadSettings();
            hideLoadingModal();

            const configDropdown = document.getElementById('configDropdown');
            const loadConfigButton = document.getElementById('loadConfigButton');

            // Load selected configuration
            loadConfigButton.addEventListener('click', () => {
                const selectedConfig = configDropdown.value;
                backendFetch('GET', `/get_config?name=${selectedConfig}`)
                    .then(config => {
                        fillConfigForm(config);
                    })
                    .catch(error => {
                        console.error('Error fetching config data:', error);
                    });
            });

            function fillConfigForm(config) {
                document.getElementById('config-name').value = config.config_name;
                document.getElementById('threads-to-start').value = config.threads_to_start;
                document.getElementById('thread-start-delay').value = config.thread_start_delay || 30;
                document.getElementById('optimize-tidal-app').checked = config.optimize_tidal_app;
                document.getElementById('hide-tidal-app').checked = config.hide_tidal_app; // New
                document.getElementById('mute-tidal-app').checked = config.mute_tidal_app; // New
                document.getElementById('streaming-quality-to-low').checked = config.streaming_quality_to_low || false;
                document.getElementById('streams-to-do').value = config.streams_to_do;
                document.getElementById('album-likes-rate').value = config.album_likes_rate;
                document.getElementById('song-likes-rate').value = config.song_likes_rate;
                document.getElementById('follows-rate').value = config.follows_rate;
                document.getElementById('playtime-type').value = config.playtime_type;
                document.getElementById('playtime-seconds').value = config.playtime_seconds;
                document.getElementById('playtime-percentage').value = config.playtime_percentage;
                document.getElementById('use-proxies').checked = config.use_proxies;
                document.getElementById('proxyless-login').checked = config.proxyless_login || false;
                document.getElementById('use-dual-proxies').checked = config.use_dual_proxies || false;
                document.getElementById('links-select').value = config.links_batch_id;
                document.getElementById('proxies-select').value = config.proxies_batch_id;
                document.getElementById('streaming-proxies-select-proxyless').value = config.streaming_proxies_batch_id || '';
                document.getElementById('login-proxies-select').value = config.login_proxies_batch_id || '';
                document.getElementById('streaming-proxies-select').value = config.streaming_proxies_batch_id || '';
                document.getElementById('accounts-select').value = config.accounts_batch_id;
                document.getElementById('ppa').value = config.ppa;
                document.getElementById('stay-logged-in').checked = config.stay_logged_in;
                document.getElementById('shuffle-perc').value = config.shuffle_perc;
                document.getElementById('search-links-perc').value = config.search_links_perc;
                document.getElementById('use-webhook').checked = config.webhook.use;
                document.getElementById('webhook-name').value = config.webhook.name;
                document.getElementById('webhook-url').value = config.webhook.url;
                document.getElementById('webhook-interval').value = config.webhook.interval;

                toggleWebhook(document.getElementById('use-webhook'));
                toggleProxies(document.getElementById('use-proxies'));
                toggleProxylessLogin(document.getElementById('proxyless-login'));
                toggleDualProxies(document.getElementById('use-dual-proxies'));
                togglePlaytimeInput(document.getElementById('playtime-type'));
            }

            const playtimeTypeSelect = document.getElementById('playtime-type');
            if (playtimeTypeSelect) {
                playtimeTypeSelect.addEventListener('change', function() {
                    togglePlaytimeInput(this);
                });
            }


            const useWebhookCheckbox = document.getElementById('use-webhook');
            if (useWebhookCheckbox) {
                useWebhookCheckbox.addEventListener('change', function() {
                    toggleWebhook(this);
                });
            }

            // Attach the event listener for the proxies checkbox
            const useProxiesCheckbox = document.getElementById('use-proxies');
            if (useProxiesCheckbox) {
                useProxiesCheckbox.addEventListener('change', function() {
                    toggleProxies(this);
                });
            }

            // Attach the event listener for the proxyless login checkbox
            const proxylessLoginCheckbox = document.getElementById('proxyless-login');
            if (proxylessLoginCheckbox) {
                proxylessLoginCheckbox.addEventListener('change', function() {
                    toggleProxylessLogin(this);
                });
            }

            // Attach the event listener for the dual proxies checkbox
            const useDualProxiesCheckbox = document.getElementById('use-dual-proxies');
            if (useDualProxiesCheckbox) {
                useDualProxiesCheckbox.addEventListener('change', function() {
                    toggleDualProxies(this);
                });
            }

            // Initial call to set the correct visibility based on the initial state
            toggleWebhook(useWebhookCheckbox);
            toggleProxies(useProxiesCheckbox);
            toggleProxylessLogin(proxylessLoginCheckbox);
            toggleDualProxies(useDualProxiesCheckbox);
            togglePlaytimeInput(playtimeTypeSelect);


            document.getElementById('showConsole').addEventListener('click', () => {
                window.electronAPI.send('toggle-console');
            });

            // Listen for console toggle reply from main process
            window.electronAPI.receive('console-toggled', (message) => {
                document.getElementById('showConsole').textContent = message;
            });

            // Attach event listeners to all form inputs for auto-save in the Settings tab
            const settingsFormElements = document.querySelectorAll('#settingsForm input');

            settingsFormElements.forEach(element => {
                element.addEventListener('input', () => {
                    saveCurrentSettings();
                });
            });
            document.getElementById('startDate').addEventListener('change', updateChart);
            document.getElementById('endDate').addEventListener('change', updateChart);
            showTab('home');

            const sidebarButtons = {
                homeBtn: 'home',
                configBtn: 'config',
                manageBtn: 'manage',
                analyticsBtn: 'analytics',
                settingsBtn: 'settings'
            };

            Object.keys(sidebarButtons).forEach(buttonId => {
                const button = document.getElementById(buttonId);
                const tabName = sidebarButtons[buttonId];
                if (button) {
                    button.addEventListener('click', () => showTab(tabName));
                }
            });

            const factoryResetBtn = document.getElementById('factoryResetBtn');
            if (factoryResetBtn) {
                factoryResetBtn.addEventListener('click', () => {
                    if (confirm('¿ESTÁS SEGURO? Esto eliminará TODOS los datos (cuentas, proxies, lotes, sesiones, configs, caché) y matará todos los procesos. La app se cerrará.')) {
                        if (confirm('CONFIRMACIÓN FINAL: Esta acción no se puede deshacer. ¿Restablecer todo?')) {
                            window.electronAPI.send('factory-reset');
                        }
                    }
                });
            }

            const logoutAllBtn = document.getElementById('logoutAllBtn');
            if (logoutAllBtn) {
                logoutAllBtn.addEventListener('click', () => {
                    if (confirm('¿Cerrar sesión de TODAS las cuentas? Se eliminarán las sesiones guardadas.')) {
                        window.electronAPI.send('logout-all-accounts');
                    }
                });
            }

            const optimizerBtn = document.getElementById('optimizerBtn');
            if (optimizerBtn) {
                optimizerBtn.addEventListener('click', () => {
                    if (confirm('¿Ejecutar optimizador del sistema? Se limpiarán archivos temporales, cachés y se liberará memoria.')) {
                        window.electronAPI.send('run-optimizer');
                    }
                });
            }

            const startStopButton = document.getElementById('startStopButton');
            if (startStopButton) {
                startStopButton.addEventListener('click', () => startBot());
            }

            const saveConfigButton = document.getElementById('saveConfigButton');
            if (saveConfigButton) {
                saveConfigButton.addEventListener('click', saveConfig);
            }

            // Event listener for batch type selection
            const batchTypeSelect = document.getElementById('batch-type');
            if (batchTypeSelect) {
                batchTypeSelect.addEventListener('change', loadBatches);
            }

            // Event listener for adding new batch
            const addBatchButton = document.getElementById('addBatchButton');
            if (addBatchButton) {
                addBatchButton.addEventListener('click', showAddBatchModal);
            }

            // Event listener for saving a new batch in the modal
            const batchModalSaveButton = document.getElementById('batchModalSaveButton');
            if (batchModalSaveButton) {
                batchModalSaveButton.addEventListener('click', saveNewBatch);
            }

            // Event listener for canceling batch modal
            const batchModalCancelButton = document.getElementById('batchModalCancelButton');
            if (batchModalCancelButton) {
                batchModalCancelButton.addEventListener('click', closeAddBatchModal);
            }

            // Event listener for closing batch modal
            const batchModalCloseButton = document.getElementById('batchModalCloseButton');
            if (batchModalCloseButton) {
                batchModalCloseButton.addEventListener('click', closeAddBatchModal);
            }

            // Event listener for closing loading modal
            const loadingModalCloseButton = document.getElementById('loadingModalCloseButton');
            if (loadingModalCloseButton) {
                loadingModalCloseButton.addEventListener('click', hideLoadingModal);
            }

            function showTab(tabName) {
                // Hide all tabs
                const tabs = document.querySelectorAll('.content-tab, .content-tab-scrollable');
                tabs.forEach(tab => {
                    tab.classList.remove('active');
                });

                // Get the tab to show
                const tabToShow = document.getElementById(tabName);
                if (tabToShow) {
                    tabToShow.classList.add('active');
                } else {
                    console.error(`Tab with ID ${tabName} does not exist.`);
                }

                // Update the active button in the sidebar
                const buttons = document.querySelectorAll('#sidebar button');
                buttons.forEach(button => {
                    button.classList.remove('active');
                });

                const activeButton = document.getElementById(tabName + 'Btn');
                if (activeButton) {
                    activeButton.classList.add('active');
                } else {
                    console.error(`Button with ID ${tabName + 'Btn'} does not exist.`);
                }

                // Load settings if the settings tab is shown
                if (tabName === 'settings') {
                    loadSettings();
                }
            }

            function saveConfig() {
                const configData = {
                    config_name: document.getElementById('config-name').value,
                    threads_to_start: document.getElementById('threads-to-start').value,
                    thread_start_delay: document.getElementById('thread-start-delay').value,
                    optimize_tidal_app: document.getElementById('optimize-tidal-app').checked,
                    hide_tidal_app: document.getElementById('hide-tidal-app').checked, // New
                    mute_tidal_app: document.getElementById('mute-tidal-app').checked, // New
                    streaming_quality_to_low: document.getElementById('streaming-quality-to-low').checked,
                    streams_to_do: document.getElementById('streams-to-do').value,
                    album_likes_rate: document.getElementById('album-likes-rate').value,
                    song_likes_rate: document.getElementById('song-likes-rate').value,
                    follows_rate: document.getElementById('follows-rate').value,
                    playtime_type: document.getElementById('playtime-type').value,
                    playtime_seconds: document.getElementById('playtime-seconds').value,
                    playtime_percentage: document.getElementById('playtime-percentage').value,
                    use_proxies: document.getElementById('use-proxies').checked,
                    proxyless_login: document.getElementById('proxyless-login').checked,
                    use_dual_proxies: document.getElementById('use-dual-proxies').checked,
                    links_batch_id: document.getElementById('links-select').value,
                    proxies_batch_id: document.getElementById('proxies-select').value,
                    login_proxies_batch_id: document.getElementById('login-proxies-select').value,
                    streaming_proxies_batch_id: document.getElementById('proxyless-login').checked 
                        ? document.getElementById('streaming-proxies-select-proxyless').value 
                        : document.getElementById('streaming-proxies-select').value,
                    accounts_batch_id: document.getElementById('accounts-select').value,
                    ppa: document.getElementById('ppa').value,
                    stay_logged_in: document.getElementById('stay-logged-in').checked,
                    shuffle_perc: document.getElementById('shuffle-perc').value,
                    search_links_perc: document.getElementById('search-links-perc').value,
                    webhook: {
                        use: document.getElementById('use-webhook').checked,
                        name: document.getElementById('webhook-name').value,
                        url: document.getElementById('webhook-url').value,
                        interval: document.getElementById('webhook-interval').value
                    }
                };

                backendFetch('POST', '/save_config', configData)
                    .then(data => {
                        alert(data.message);
                        loadConfigs();
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            }

            function startBot() {
                const configName = document.getElementById('configSelect').value;

                backendFetch('POST', '/start_bot', { config_name: configName })
                    .then(data => {
                        fetchWorkerThreads();
                        setInterval(fetchWorkerThreads, 5000);
                        fetchWorkerStats();
                        setInterval(fetchWorkerStats, 5000);
                        toggleStartStopButton();
                        startTimer();
                    })
                    .catch(error => {
                        alert('Error: ' + error.message);
                    });
            }

            function loadBatchOptions(selectId, batchType) {
                backendFetch('GET', `/get_batches?type=${batchType}`)
                    .then(data => {
                        const select = document.getElementById(selectId);
                        select.innerHTML = '';
                        data.batches.forEach(batch => {
                            const option = document.createElement('option');
                            option.value = batch.id;
                            option.textContent = batch.name;
                            select.appendChild(option);
                        });
                    })
                    .catch(error => {
                        console.error('Error loading batch options:', error);
                    });
            }

            function loadConfigs() {
                backendFetch('GET', '/get_configs')
                    .then(data => {
                        const configDropdown = document.getElementById('configDropdown'); // Assuming you're using this ID
                        const configSelect = document.getElementById('configSelect'); // If you have another dropdown

                        if (configDropdown) {
                            configDropdown.innerHTML = ''; // Clear existing options

                            data.configs.forEach(config => {
                                const option = document.createElement('option');
                                option.value = config;
                                option.textContent = config; // Assuming the config name is also the file name without extension
                                configDropdown.appendChild(option);
                            });

                            if (data.configs.length > 0) {
                                configDropdown.value = data.configs[0]; // Select the first config by default
                            }
                        }

                        // If you have another dropdown to populate, ensure to do the same
                        if (configSelect) {
                            configSelect.innerHTML = ''; // Clear existing options

                            data.configs.forEach(config => {
                                const option = document.createElement('option');
                                option.value = config;
                                option.textContent = config;
                                configSelect.appendChild(option);
                            });

                            if (data.configs.length > 0) {
                                configSelect.value = data.configs[0]; // Select the first config by default
                            }
                        }

                    })
                    .catch(error => {
                        console.error('Error loading configs:', error);
                        // Consider showing a user-friendly message in the UI
                    });
            }

            function fetchWorkerThreads() {
                backendFetch('GET', '/get_worker_threads')
                    .then(data => {
                        const threadsTableBody = document.querySelector('#threadsTable tbody');
                        threadsTableBody.innerHTML = '';

                        // Sort the threads by their thread number
                        data.sort((a, b) => a.thread_number - b.thread_number);

                        data.forEach(thread => {
                            const proxy = thread.proxy;
                            const truncatedProxy = proxy.length > 20 ? proxy.substring(0, 20) + '...' : proxy;

                            const row = document.createElement('tr');
                            row.innerHTML = `
                                <td>${thread.thread_number}</td>
                                <td>${thread.status}</td>
                                <td>${truncatedProxy}</td>
                                <td>${thread.logins}</td>
                                <td>${thread.streams}</td>
                                <td>${thread.likes}</td>
                                <td>${thread.follows}</td>
                                <td>${thread.errors}</td>
                                <td>${thread.pid}</td>
                                <td>
                                    <button class="viewbtn boton-elegante">Ver</button>
                                    <button class="restartbtn boton-elegante">Reiniciar</button>
                                </td>
                            `;
                            const viewButton = row.querySelector('.viewbtn');
                            viewButton.addEventListener('click', () => {
                                viewThread(thread.pid);
                            });

                            const restartButton = row.querySelector('.restartbtn');
                            restartButton.addEventListener('click', () => {
                                restartThread(thread.thread_number, thread.port, restartButton);
                            });

                            threadsTableBody.appendChild(row);
                        });
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            }

            function viewThread(pid) {
                backendFetch('POST', '/view_thread', { pid: pid })
                    .then(data => {
                        console.log(data.message);
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            }

            function restartThread(threadNumber, port, button) {
                button.textContent = 'Cargando...';
                document.getElementById('loadingText').textContent = `Reiniciando hilo ${threadNumber}, por favor espere un momento a que reinicie.`; // Update modal text
                document.getElementById('main-content').classList.add('blurred'); // Blur background content
                document.getElementById('loadingModal').style.display = 'flex'; // Show loading modal

                backendFetch('POST', '/restart_thread', { thread_number: threadNumber, port: port })
                    .then(data => {
                        fetchWorkerThreads();
                        button.textContent = 'Reiniciar';
                        document.getElementById('main-content').classList.remove('blurred'); // Unblur background content
                        document.getElementById('loadingModal').style.display = 'none'; // Hide loading modal
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        button.textContent = 'Reiniciar';
                        document.getElementById('main-content').classList.remove('blurred'); // Unblur background content
                        document.getElementById('loadingModal').style.display = 'none'; // Hide loading modal
                    });
            }

            async function fetchWorkerStats() {
                try {
                    const stats = await backendFetch('GET', '/get_worker_stats');

                    document.getElementById('threadsRunning').innerText = stats.worker_threads_running;
                    document.getElementById('streamsDone').innerText = stats.worker_streams_done;
                    document.getElementById('successfulLogins').innerText = stats.worker_successful_logins;
                    document.getElementById('failedLogins').innerText = stats.worker_unsuccessful_logins;
                    document.getElementById('songLikesDone').innerText = stats.worker_song_likes;
                    document.getElementById('albumLikesDone').innerText = stats.worker_album_likes;
                    document.getElementById('followsDone').innerText = stats.worker_follows_done;
                    document.getElementById('proxyErrors').innerText = stats.worker_proxy_errors;
                    document.getElementById('botErrors').innerText = stats.worker_bot_errors;
                } catch (error) {
                    console.error('Error fetching worker stats:', error);
                }
            }

            function toggleStartStopButton() {
                const button = document.getElementById('startStopButton');
                if (button.textContent === 'Iniciar' || button.textContent === 'Start') {
                    button.textContent = 'Detener';
                    button.classList.remove('start-button');
                    button.classList.add('stop-button');
                } else {
                    button.textContent = 'Iniciar';
                    button.classList.remove('stop-button');
                    button.classList.add('start-button');
                }
            }

            function toggleWebhook(checkbox) {
                const webhookSection = document.getElementById('webhook-section');
                if (checkbox.checked) {
                    webhookSection.style.display = 'block';
                } else {
                    webhookSection.style.display = 'none';
                }
            }

            function toggleProxies(checkbox) {
                const proxiesSection = document.getElementById('proxies-section');
                if (checkbox.checked) {
                    proxiesSection.style.display = 'block';
                } else {
                    proxiesSection.style.display = 'none';
                }
            }

            function toggleProxylessLogin(checkbox) {
                const proxylessLoginSection = document.getElementById('proxyless-login-section');
                const dualProxiesCheckbox = document.getElementById('use-dual-proxies');
                if (checkbox && checkbox.checked) {
                    proxylessLoginSection.style.display = 'block';
                    // Disable dual proxies if proxyless login is enabled (they're mutually exclusive)
                    if (dualProxiesCheckbox) {
                        dualProxiesCheckbox.checked = false;
                        toggleDualProxies(dualProxiesCheckbox);
                    }
                } else {
                    proxylessLoginSection.style.display = 'none';
                }
            }

            function toggleDualProxies(checkbox) {
                const dualProxiesSection = document.getElementById('dual-proxies-section');
                const proxylessLoginCheckbox = document.getElementById('proxyless-login');
                if (checkbox && checkbox.checked) {
                    dualProxiesSection.style.display = 'block';
                    // Disable proxyless login if dual proxies is enabled (they're mutually exclusive)
                    if (proxylessLoginCheckbox) {
                        proxylessLoginCheckbox.checked = false;
                        toggleProxylessLogin(proxylessLoginCheckbox);
                    }
                } else {
                    dualProxiesSection.style.display = 'none';
                }
            }

            function togglePlaytimeInput(select) {
                const playtimeSecondsGroup = document.getElementById('playtime-seconds-group');
                const playtimePercentageGroup = document.getElementById('playtime-percentage-group');
                if (select.value === 'seconds') {
                    playtimeSecondsGroup.style.display = 'block';
                    playtimePercentageGroup.style.display = 'none';
                } else {
                    playtimeSecondsGroup.style.display = 'none';
                    playtimePercentageGroup.style.display = 'block';
                }
            }

            function startTimer() {
                startTime = new Date();
                timerInterval = setInterval(updateTimeRunning, 1000);
            }

            function updateTimeRunning() {
                const now = new Date();
                const elapsedTime = now - startTime;
                const seconds = Math.floor((elapsedTime / 1000) % 60);
                const minutes = Math.floor((elapsedTime / 1000 / 60) % 60);
                const hours = Math.floor((elapsedTime / 1000 / 60 / 60) % 24);
                document.getElementById('timeRunning').textContent =
                    `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
            }

            function loadBatches() {
                const batchType = document.getElementById('batch-type').value;
                const batchList = document.getElementById('batch-list');
                batchList.innerHTML = '';

                backendFetch('GET', `/get_batches?type=${batchType}`)
                    .then(data => {
                        if (!data.batches || !Array.isArray(data.batches)) {
                            throw new Error('Invalid data format: "batches" is missing or not an array');
                        }

                        data.batches.forEach(batch => {
                            const batchCard = document.createElement('div');
                            batchCard.className = 'batch-card';

                            // Create the input element
                            const inputElement = document.createElement('input');
                            inputElement.type = 'text';
                            inputElement.value = batch.name;
                            inputElement.readOnly = true;

                            // Create the button group container
                            const buttonGroup = document.createElement('div');
                            buttonGroup.className = 'button-group';

                            // Create the edit button
                            const editButton = document.createElement('button');
                            editButton.className = 'edit-button';
                            editButton.textContent = 'Editar';

                            // Add event listener for edit button
                            editButton.addEventListener('click', () => {
                                editBatch(batch.type, batch.id, batch.name, batch.content);
                            });

                            // Create the delete button
                            const deleteButton = document.createElement('button');
                            deleteButton.className = 'delete-button';
                            deleteButton.textContent = 'Eliminar';

                            // Add event listener for delete button
                            deleteButton.addEventListener('click', () => {
                                deleteBatch(batch.type, batch.id);
                            });

                            // Append buttons to the button group
                            buttonGroup.appendChild(editButton);
                            buttonGroup.appendChild(deleteButton);

                            // Append input and button group to the batch card
                            batchCard.appendChild(inputElement);
                            batchCard.appendChild(buttonGroup);

                            // Append the batch card to the batch list container
                            document.getElementById('batch-list').appendChild(batchCard);
                        });


                    })
                    .catch(error => {
                        console.error('Error loading batches:', error);
                        alert(`Error loading batches: ${error.message}`);
                    });
            }

            function deleteBatch(batchType, batchId) {
                backendFetch('POST', '/delete_batch', { type: batchType, id: batchId })
                    .then(data => {
                        if (data.message) {
                            loadBatches(); // Reload the list of batches
                        } else {
                            console.error('Failed to delete batch:', data.error);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            }

            function showAddBatchModal() {
                document.getElementById('batchModalTitle').textContent = 'Añadir Nuevo Lote';
                document.getElementById('batch-name').value = '';
                document.getElementById('batch-content').value = '';
                document.getElementById('batch-file').value = ''; // Clear file input
                document.getElementById('batchModalSaveButton').setAttribute('data-edit-mode', 'false');
                document.getElementById('batchModal').style.display = "block";
            }

            function closeAddBatchModal() {
                document.getElementById('batch-name').value = '';
                document.getElementById('batch-content').value = '';
                document.getElementById('batch-file').value = ''; // Clear file input
                document.getElementById('batchModal').style.display = "none";
            }

            function reloadBatchOptions() {
                loadBatchOptions('accounts-select', 'accounts');
                loadBatchOptions('proxies-select', 'proxies');
                loadBatchOptions('login-proxies-select', 'proxies');
                loadBatchOptions('streaming-proxies-select', 'proxies');
                loadBatchOptions('streaming-proxies-select-proxyless', 'proxies');
                loadBatchOptions('links-select', 'links');
            }

            function saveNewBatch() {
                const batchType = document.getElementById('batch-type').value;
                const batchName = document.getElementById('batch-name').value;
                let batchContent = document.getElementById('batch-content').value;

                // Remove empty lines
                batchContent = batchContent
                    .split('\n')                    // Split content into lines
                    .map(line => line.trim())        // Trim each line to remove surrounding whitespace
                    .filter(line => line.length > 0) // Filter out empty lines
                    .join('\n');                     // Join the lines back together

                const editMode = document.getElementById('batchModalSaveButton').getAttribute('data-edit-mode') === 'true';

                if (editMode) {
                    const batchId = document.getElementById('batchModalSaveButton').getAttribute('data-batch-id');
                    backendFetch('POST', '/update_batch', { type: batchType, id: batchId, name: batchName, content: batchContent })
                        .then(data => {
                            closeAddBatchModal();
                            loadBatches();
                            reloadBatchOptions();
                        })
                        .catch(error => {
                            console.error('Error updating batch:', error);
                        });
                } else {
                    backendFetch('POST', '/add_batch', { type: batchType, name: batchName, content: batchContent })
                        .then(data => {
                            closeAddBatchModal();
                            loadBatches();
                            reloadBatchOptions();
                        })
                        .catch(error => {
                            console.error('Error adding batch:', error);
                        });
                }
            }


            function editBatch(batchType, batchId, batchName, batchContent) {
                document.getElementById('batchModalTitle').textContent = 'Editar Lote';
                document.getElementById('batch-name').value = batchName;
                document.getElementById('batch-content').value = batchContent;
                document.getElementById('batchModalSaveButton').setAttribute('data-edit-mode', 'true');
                document.getElementById('batchModalSaveButton').setAttribute('data-batch-id', batchId);
                document.getElementById('batchModal').style.display = "block";
            }

            document.getElementById('batch-file').addEventListener('change', function (event) {
                const file = event.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function (e) {
                        document.getElementById('batch-content').value = e.target.result;
                    };
                    reader.readAsText(file);
                }
            });

            const ctx = document.getElementById('streamsChart').getContext('2d');
            const gradient = ctx.createLinearGradient(0, 0, 0, 400);
            gradient.addColorStop(0, 'rgba(255, 255, 255, 0.5)');
            gradient.addColorStop(1, 'rgba(0, 0, 0, 0.5)');

            const streamsChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Streams Done',
                        data: [],
                        fill: true,
                        backgroundColor: gradient,
                        borderColor: 'rgba(255, 255, 255, 1)',
                        tension: 0.1
                    }]
                },
                options: {
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'day',
                                tooltipFormat: 'DD/MM/YYYY',
                                displayFormats: {
                                    day: 'DD/MM/YYYY'
                                }
                            },
                            title: {
                                display: true,
                                text: 'Date'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Streams Done'
                            }
                        }
                    }
                }
            });

            function saveCurrentSettings() {
                const settingsData = {
                    apiKey: document.getElementById('api-key').value,
                    // Add other settings here as needed
                };

                backendFetch('POST', '/save_settings', settingsData)
                    .then(data => {
                        console.log('Settings saved automatically:', data.message);
                    })
                    .catch(error => {
                        console.error('Error auto-saving settings:', error);
                    });
            }

            // Function to load settings when the settings tab is opened
            function loadSettings() {
                backendFetch('GET', '/load_settings')
                    .then(data => {
                        document.getElementById('api-key').value = data.apiKey;
                        // Load other settings as needed
                    })
                    .catch(error => {
                        console.error('Error loading settings:', error);
                    });
            }

            function updateChart() {
                const startDate = document.getElementById('startDate').value;
                const endDate = document.getElementById('endDate').value;

                backendFetch('GET', `/get_streams_done?start_date=${startDate}&end_date=${endDate}`)
                    .then(data => {
                        if (data.error) {
                            alert(data.error);
                            return;
                        }

                        const testData = data.streams;

                        // Create a map to store the streams done per day
                        const streamsPerDay = {};

                        testData.forEach(item => {
                            const date = item.timestamp.split(' ')[0]; // Get only the date part
                            if (!streamsPerDay[date]) {
                                streamsPerDay[date] = 0;
                            }
                            streamsPerDay[date] += item.streams_done;
                        });

                        // Generate the full range of dates between startDate and endDate
                        const dateRange = [];
                        let currentDate = new Date(startDate);
                        const end = new Date(endDate);
                        while (currentDate <= end) {
                            const formattedDate = currentDate.toISOString().split('T')[0];
                            dateRange.push(formattedDate);
                            if (!streamsPerDay[formattedDate]) {
                                streamsPerDay[formattedDate] = 0; // Fill missing dates with 0 streams
                            }
                            currentDate.setDate(currentDate.getDate() + 1);
                        }

                        const labels = dateRange;
                        const streamsData = dateRange.map(date => streamsPerDay[date]);

                        streamsChart.data.labels = labels;
                        streamsChart.data.datasets[0].data = streamsData;
                        streamsChart.update();

                        const totalStreams = streamsData.reduce((acc, streams) => acc + streams, 0);
                        document.getElementById('totalStreamsText').innerText = `Total de Reproducciones Realizadas: ${totalStreams}`;
                    })
                    .catch(error => {
                        console.error('Error fetching streams data:', error);
                    });
            }

            document.getElementById('startDate').addEventListener('change', updateChart);
            document.getElementById('endDate').addEventListener('change', updateChart);

        });
    }

    function hideLoadingModal() {
        const loadingModal = document.getElementById('loadingModal');
        const mainContent = document.getElementById('main-content');

        if (loadingModal) {
            loadingModal.style.display = 'none';
        }

        if (mainContent) {
            mainContent.classList.remove('blurred');
        }
    }
});