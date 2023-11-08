import {reactive} from "vue";


class Api {
    constructor(app) {
        this.base = "/api";
        this.app = app;
    }

    async fetch({url, method = 'GET', body = null}) {
        const controller = new AbortController();
        const signal = controller.signal;
        // const id = setTimeout(() => controller.abort(), 10);

        try {
            const response = await fetch(url, {
                method: method || 'GET',
                signal: signal,
                body: body
            });

            // clearTimeout(id);

            return response;
        } catch (e) {
            console.error("Request failed/timed out", e);
        }
    }

    async listSwitches() {
        const key = "useless-switches";
        let choices = sessionStorage.getItem(key);
        if (choices === null) {
            const response = await this.fetch({url: this.base + '/'});
            choices = await response.json();
        }
        return choices;
    }

    async switchValue({name}) {
        const response = await this.fetch({url: this.base + `/${name}`});
        const data = await response.json();
        return data.state;
    }

    async switch({name, state}) {
        const response = await this.fetch({
            url: this.base + `/${name}`,
            method: 'PUT',
            body: state
        });
        const data = await response.json();
        if (response.status === 208) {
            console.warn("Action was not performed:", name, data.detail);
            return state;
        }
        return data.state;
    }

    async activitySocket({name}) {
        const socket = new WebSocket(`ws://${location.host}${this.base}/${name}`);
        return socket
        socket.addEventListener("message", handler);
    }


    async auditLog({name}) {
        const response = await this.fetch({
            url: `${this.base}/${name}/audit-log`
        });
        return await response.json();
    }
}


export default {
    install: (app) => {
        app.config.globalProperties.$api = reactive(new Api(app))
    }
}
