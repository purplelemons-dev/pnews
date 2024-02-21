
const newsList = document.getElementById('news-list');

new EventSource('/listen').onmessage = async (event) => {
    const news = JSON.parse(event.data);
    newsList.innerHTML = '';
    let count = 0;
    for (const url of news) {
        console.log(url);
        const listItem = document.createElement('li');
        const link = document.createElement('a');
        link.href = url;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        const image = document.createElement('img');
        image.src = `/${count}.png`;
        link.appendChild(image);
        listItem.appendChild(link);
        newsList.appendChild(listItem);
        count++;
    }
};
