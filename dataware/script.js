let articlesData = [];
let currentPage = 1;
const articlesPerPage = 10;

// Ladataan JSON-data ja luodaan artikkelit
fetch('data.json')
  .then(response => {
    if (!response.ok) {
      throw new Error("JSON-tiedostoa ei voitu ladata");
    }
    return response.json();
  })
  .then(data => {
    articlesData = data;
    renderArticles();
    renderPagination();
  })
  .catch(error => {
    console.error("Virhe ladattaessa artikkeleita:", error);
  });

// Renderöi artikkelit ja näytä vain ne, jotka kuuluvat nykyiselle sivulle
function renderArticles() {
  const articlesContainer = document.getElementById('articles');
  articlesContainer.innerHTML = '';

  const startIndex = (currentPage - 1) * articlesPerPage;
  const endIndex = startIndex + articlesPerPage;
  const currentArticles = articlesData.slice(startIndex, endIndex);

  currentArticles.forEach(article => {
    const articleDiv = document.createElement('div');
    articleDiv.className = 'article';

    const title = document.createElement('h2');
    title.textContent = article.title;

    const content = document.createElement('p');
    content.textContent = article.content;

    const author = document.createElement('p');
    author.className = 'author';
    author.textContent = `Kirjoittaja: ${article.author}`;

    const date = document.createElement('p');
    date.className = 'date';
    date.textContent = `Julkaisupäivä: ${article.date}`;

    const readMore = document.createElement('a');
    readMore.href = `data.html?id=${article.id}`;
    readMore.className = 'read-more';
    readMore.textContent = 'Lue lisää';

    articleDiv.appendChild(title);
    articleDiv.appendChild(content);
    articleDiv.appendChild(author);
    articleDiv.appendChild(date);
    articleDiv.appendChild(readMore);

    articlesContainer.appendChild(articleDiv);
  });
}

// Renderöi sivutusnavigointi
function renderPagination() {
  const paginationContainer = document.getElementById('pagination');
  paginationContainer.innerHTML = '';

  const totalPages = Math.ceil(articlesData.length / articlesPerPage);

  // "Edellinen"-nappi
  if (currentPage > 1) {
    const prevButton = document.createElement('button');
    prevButton.textContent = 'Edellinen';
    prevButton.onclick = () => changePage(currentPage - 1);
    paginationContainer.appendChild(prevButton);
  }

  // Sivunumerot
  for (let i = 1; i <= totalPages; i++) {
    const pageButton = document.createElement('button');
    pageButton.textContent = i;
    pageButton.onclick = () => changePage(i);
    if (i === currentPage) {
      pageButton.style.fontWeight = 'bold';
    }
    paginationContainer.appendChild(pageButton);
  }

  // "Seuraava"-nappi
  if (currentPage < totalPages) {
    const nextButton = document.createElement('button');
    nextButton.textContent = 'Seuraava';
    nextButton.onclick = () => changePage(currentPage + 1);
    paginationContainer.appendChild(nextButton);
  }
}

// Vaihda sivua
function changePage(page) {
  currentPage = page;
  renderArticles();
  renderPagination();
}

// Hakuartikkelit
function searchArticles() {
  const searchQuery = document.getElementById('search-box').value.toLowerCase();

  const filteredArticles = articlesData.filter(article => {
    return article.title.toLowerCase().includes(searchQuery) || article.content.toLowerCase().includes(searchQuery);
  });

  articlesData = filteredArticles;
  currentPage = 1; // Nollataan sivu hakemisen jälkeen
  renderArticles();
  renderPagination();
}
