
// VCAT Evidence Repository - Client-side Search
let searchIndex = [];

// Load search index
fetch('/VCAT-Evidence-Repository/_data/search_index.json')
  .then(response => response.json())
  .then(data => {
    searchIndex = data;
    console.log('Search index loaded:', searchIndex.length, 'entries');
  })
  .catch(error => console.error('Error loading search index:', error));

function performSearch() {
  const query = document.getElementById('search-input').value.toLowerCase().trim();
  const resultsDiv = document.getElementById('search-results');
  
  if (!query) {
    resultsDiv.innerHTML = '';
    return;
  }
  
  // Simple text search
  const results = searchIndex.filter(item => {
    return item.title.toLowerCase().includes(query) ||
           item.content.toLowerCase().includes(query) ||
           (item.sender && item.sender.toLowerCase().includes(query));
  });
  
  // Display results
  if (results.length === 0) {
    resultsDiv.innerHTML = '<p>No results found for "' + query + '"</p>';
  } else {
    let html = '<h3>Search Results (' + results.length + ')</h3>';
    html += '<div class="results-list">';
    
    results.slice(0, 10).forEach(result => {
      html += '<div class="result-item">';
      html += '<h4><a href="' + result.url + '">' + result.title + '</a></h4>';
      html += '<p class="result-type">' + result.type.toUpperCase() + '</p>';
      html += '<p class="result-preview">' + result.content.substring(0, 200) + '...</p>';
      if (result.date) {
        html += '<p class="result-date">Date: ' + new Date(result.date).toLocaleDateString() + '</p>';
      }
      html += '</div>';
    });
    
    html += '</div>';
    resultsDiv.innerHTML = html;
  }
}

// Search on Enter key
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('search-input');
  if (searchInput) {
    searchInput.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        performSearch();
      }
    });
  }
});
