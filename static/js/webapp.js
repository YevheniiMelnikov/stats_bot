// Пример JavaScript кода для WebApp
async function fetchAndDisplayStats() {
    try {
        // Первый запрос для получения данных
        const statsResponse = await fetch('/get_stats', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: Telegram.WebApp.initDataUnsafe.user.id,
                // bot_id: someBotsId  // если нужна статистика конкретного бота
            })
        });

        const statsData = await statsResponse.json();
        if (statsData.error) {
            console.error('Error fetching stats:', statsData.error);
            return;
        }

        // Показываем какой-то базовый UI с данными
        displayBasicStats(statsData);

        // Второй запрос для получения графиков
        const graphsResponse = await fetch('/generate_graphs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                stats: statsData.raw_data
            })
        });

        const graphsData = await graphsResponse.json();
        if (graphsData.error) {
            console.error('Error generating graphs:', graphsData.error);
            return;
        }

        // Вставляем HTML с графиками в DOM
        document.getElementById('graphs-container').innerHTML = graphsData.graph_html;

    } catch (error) {
        console.error('Error:', error);
    }
}