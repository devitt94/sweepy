
export default class ApiClient {
    async getSweepstake(id) {
        const url = `/api/sweepstakes/${id}`;
        const headers = {
            'Content-Type': 'application/json',
        };
        const response = await fetch(url, {
            method: 'GET',
            headers: headers,
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;
    };

    async refreshSweepstake(id) {
        const url = `/api/sweepstakes/${id}/refresh`;
        const headers = {
            'Content-Type': 'application/json',
        };
        const response = await fetch(url, {
            method: 'POST',
            headers: headers,
        })

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;

    };

    async createSweepstake(sweepstakeData) {
        const url = '/api/sweepstakes';
        const headers = {
            'Content-Type': 'application/json',
        };
        const response = await fetch(url, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(sweepstakeData),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;
    };


    async getAllSweepstakes() {
        const url = '/api/sweepstakes';
        const headers = {
            'Content-Type': 'application/json',
        };
        const response = await fetch(url, {
            method: 'GET',
            headers: headers,
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;
    };

    async closeSweepstake(id) {
        const url = `/api/sweepstakes/${id}/close`;
        const headers = {
            'Content-Type': 'application/json',
        };
        const response = await fetch(url, {
            method: 'POST',
            headers: headers,
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;
    };

    async getEventTypes() {
        const url = '/api/event-types';
        const headers = {
            'Content-Type': 'application/json',
        };
        const response = await fetch(url, {
            method: 'GET',
            headers: headers,
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;
    };

    async getMarkets(eventType) {
        const url = `/api/markets/${eventType}`;
        const headers = {
            'Content-Type': 'application/json',
        };
        const response = await fetch(url, {
            method: 'GET',
            headers: headers,
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;
    }
}
